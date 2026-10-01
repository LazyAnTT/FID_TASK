import xml.etree.ElementTree as ET

from backend.app.schemas import DocumentInput

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
