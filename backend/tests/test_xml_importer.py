from datetime import date

import pytest
from pydantic import ValidationError

from backend.app.services.xml_importer import parse_documents

VALID_XML = """
<documents>
    <document id="doc-001">
        <name>Informācijas drošības politika</name>
        <description>Organizācijas drošības prasības.</description>
        <responsibleUnit>IT nodaļa</responsibleUnit>
        <createdAt>2026-09-15</createdAt>
        <url>https://example.com/documents/doc-001.pdf</url>
        <fileType>pdf</fileType>
        <readingTimeMinutes>12</readingTimeMinutes>
        <importance>augsts</importance>
        <category>iekšējs</category>
        <active>nē</active>
    </document>
</documents>
"""


def test_parse_valid_xml():
    documents = parse_documents(VALID_XML)

    assert len(documents) == 1

    document = documents[0]

    assert document.external_id == "doc-001"
    assert document.title == "Informācijas drošības politika"
    assert document.created_at == date(2026, 9, 15)
    assert document.reading_time_minutes == 12
    assert document.importance == "high"
    assert document.category == "internal"
    assert document.active is False


@pytest.mark.parametrize(
    "original, replacement",
    [
        ("<importance>augsts</importance>", "<importance>nezināms</importance>"),
        ("<category>iekšējs</category>", "<category>nezināma</category>"),
    ],
)
def test_parse_invalid_values(original, replacement):
    invalid_xml = VALID_XML.replace(original, replacement)

    with pytest.raises(ValidationError):
        parse_documents(invalid_xml)


def test_parse_malformed_xml():
    with pytest.raises(ValueError, match="Invalid XML format"):
        parse_documents("<documents>")
