import xml.etree.ElementTree as ET

from scripts.generate_xml import generate_xml


def test_generator_creates_complete_records():
    root = generate_xml(count=25).getroot()

    assert root.tag == "documents"

    documents = root.findall("document")
    assert len(documents) == 25

    ids = [document.get("id") for document in documents]
    assert all(ids)
    assert len(set(ids)) == 25

    required_fields = {
        "name",
        "description",
        "responsibleUnit",
        "createdAt",
        "url",
        "fileType",
        "readingTimeMinutes",
        "importance",
        "category",
        "active",
    }

    for document in documents:
        assert len(document) == len(required_fields)
        assert {field.tag for field in document} == required_fields
        assert all(field.text and field.text.strip() for field in document)

        assert int(document.findtext("readingTimeMinutes")) > 0

        assert document.findtext("importance") in {
            "zems",
            "vidējs",
            "augsts",
            "kritisks",
        }

        assert document.findtext("category") in {
            "publisks",
            "iekšējs",
            "ierobežotas pieejamības",
            "konfidenciāls",
        }

        assert document.findtext("active") in {"jā", "nē"}


def test_same_seed_produces_same_xml():
    first = generate_xml(seed=42)
    second = generate_xml(seed=42)

    first_xml = ET.tostring(first.getroot(), encoding="utf-8")
    second_xml = ET.tostring(second.getroot(), encoding="utf-8")

    assert first_xml == second_xml
