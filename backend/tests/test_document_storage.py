import xml.etree.ElementTree as ET
import pytest

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from backend.app.database import Base
from backend.app.models import Document
from backend.app.services.xml_importer import import_documents
from scripts.generate_xml import generate_xml


@pytest.fixture
def db(tmp_path):
    database_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{database_file}")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    engine.dispose()


@pytest.fixture
def xml_text():
    tree = generate_xml(count=2)
    return ET.tostring(tree.getroot(), encoding="unicode")


def test_import_creates_records(db, xml_text):
    result = import_documents(xml_text, db)

    assert result == {"created": 2, "updated": 0, "total": 2}

    count = db.scalar(select(func.count()).select_from(Document))
    assert count == 2


def test_repeat_import_updates_without_duplicates(db, xml_text):
    import_documents(xml_text, db)

    root = ET.fromstring(xml_text)
    root.find("document/name").text = "Atjaunināta politika"
    changed_xml = ET.tostring(root, encoding="unicode")

    result = import_documents(changed_xml, db)

    assert result == {"created": 0, "updated": 2, "total": 2}

    count = db.scalar(select(func.count()).select_from(Document))
    assert count == 2

    document = db.scalar(select(Document).where(Document.external_id == "doc-001"))
    assert document.title == "Atjaunināta politika"
