from backend.app.database import PROJECT_ROOT, SessionLocal
from backend.app.services.xml_importer import import_documents

if __name__ == "__main__":
    source_file = PROJECT_ROOT / "data" / "documents.xml"
    xml_text = source_file.read_text(encoding="utf-8")

    with SessionLocal() as db:
        result = import_documents(xml_text, db)

    print(result)
