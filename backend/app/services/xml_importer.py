import os
import httpx
import xml.etree.ElementTree as ET

from backend.app.schemas import DocumentInput
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models import Document

XML_SOURCE_URL = os.getenv(
    "XML_SOURCE_URL",
    "http://127.0.0.1:8000/source/documents.xml",
)

IMPORTANCE_VALUES = {
    "zems": "low",
    "vidējs": "medium",
    "augsts": "high",
    "kritisks": "critical",
}

CATEGORY_VALUES = {
    "publisks": "public",
    "iekšējs": "internal",
    "ierobežotas pieejamības": "restricted",
    "konfidenciāls": "confidential",
}

ACTIVE_VALUES = {
    "jā": True,
    "nē": False,
}


def get_text(element, field_name):
    return element.findtext(field_name, default="").strip()


def parse_documents(xml_text: str) -> list[DocumentInput]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as error:
        raise ValueError("Invalid XML format.") from error

    if root.tag != "documents":
        raise ValueError("Expected a <documents> root element.")

    elements = root.findall("document")

    if not elements:
        raise ValueError("The XML contains no documents.")

    documents = []

    for element in elements:
        document = DocumentInput(
            external_id=element.get("id", ""),
            title=get_text(element, "name"),
            description=get_text(element, "description"),
            responsible_unit=get_text(element, "responsibleUnit"),
            created_at=get_text(element, "createdAt"),
            url=get_text(element, "url"),
            file_type=get_text(element, "fileType"),
            reading_time_minutes=get_text(element, "readingTimeMinutes"),
            importance=IMPORTANCE_VALUES.get(get_text(element, "importance")),
            category=CATEGORY_VALUES.get(get_text(element, "category")),
            active=ACTIVE_VALUES.get(get_text(element, "active")),
        )

        documents.append(document)

    return documents


def import_documents(xml_text: str, db: Session) -> dict:
    documents = parse_documents(xml_text)

    created = 0
    updated = 0

    try:
        for document in documents:
            existing = db.scalar(
                select(Document).where(Document.external_id == document.external_id)
            )

            values = document.model_dump()
            values["url"] = str(document.url)

            if existing is None:
                db.add(Document(**values))
                created += 1
            else:
                for field, value in values.items():
                    setattr(existing, field, value)

                updated += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "created": created,
        "updated": updated,
        "total": len(documents),
    }


def import_from_source(db: Session) -> dict:
    response = httpx.get(XML_SOURCE_URL, timeout=10.0)
    response.raise_for_status()

    return import_documents(response.text, db)
