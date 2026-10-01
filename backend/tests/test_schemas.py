from datetime import date

import pytest
from pydantic import ValidationError

from backend.app.schemas import DocumentInput

VALID_DOCUMENT = {
    "external_id": "doc-001",
    "title": "Informācijas drošības politika",
    "description": "Organizācijas informācijas drošības prasības.",
    "responsible_unit": "IT nodaļa",
    "created_at": "2026-09-15",
    "url": "https://example.com/documents/doc-001.pdf",
    "file_type": "pdf",
    "reading_time_minutes": 12,
    "importance": "high",
    "category": "internal",
    "active": True,
}


def test_valid_document():
    document = DocumentInput(**VALID_DOCUMENT)

    assert document.title == "Informācijas drošības politika"
    assert document.created_at == date(2026, 9, 15)
    assert document.active is True


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("title", "   "),
        ("created_at", "2026-02-30"),
        ("url", "not-a-url"),
        ("reading_time_minutes", 0),
        ("importance", "urgent"),
        ("category", "secret"),
        ("active", "jā"),
    ],
)
def test_invalid_document(field, invalid_value):
    data = {**VALID_DOCUMENT, field: invalid_value}

    with pytest.raises(ValidationError):
        DocumentInput(**data)
