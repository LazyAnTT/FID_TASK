from datetime import date, timedelta
from pathlib import Path
import random
import xml.etree.ElementTree as ET

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "documents.xml"

DOCUMENT_NAMES = [
    "Informācijas drošības politika",
    "Darbinieku rokasgrāmata",
    "Gada pārskats",
    "Risku pārvaldības vadlīnijas",
    "Klientu apkalpošanas kārtība",
]

UNITS = [
    "IT nodaļa",
    "Finanšu nodaļa",
    "Personāla nodaļa",
    "Juridiskā nodaļa",
    "Klientu apkalpošanas nodaļa",
]

DESCRIPTIONS = [
    "Dokuments nosaka darba organizācijas principus un atbildību.",
    "Dokumentā apkopotas prasības un ieteikumi ikdienas darbam.",
    "Dokuments apraksta procedūras un to piemērošanas kārtību.",
]

FILE_TYPES = ["pdf", "docx", "xlsx"]
IMPORTANCE_LEVELS = ["zems", "vidējs", "augsts", "kritisks"]
CATEGORIES = [
    "publisks",
    "iekšējs",
    "ierobežotas pieejamības",
    "konfidenciāls",
]


def generate_xml(count=25, seed=42):
    rng = random.Random(seed)
    root = ET.Element("documents")
    reference_date = date(2026, 9, 30)

    for number in range(1, count + 1):
        document_id = f"doc-{number:03d}"
        name = rng.choice(DOCUMENT_NAMES)
        file_type = rng.choice(FILE_TYPES)
        created_at = reference_date - timedelta(days=rng.randint(0, 365))

        document = ET.SubElement(root, "document", id=document_id)

        fields = {
            "name": f"{name} {number}",
            "description": rng.choice(DESCRIPTIONS),
            "responsibleUnit": rng.choice(UNITS),
            "createdAt": created_at.isoformat(),
            "url": f"https://example.com/documents/{document_id}.{file_type}",
            "fileType": file_type,
            "readingTimeMinutes": str(rng.randint(2, 45)),
            "importance": rng.choice(IMPORTANCE_LEVELS),
            "category": rng.choice(CATEGORIES),
            "active": rng.choice(["jā", "nē"]),
        }

        for field_name, value in fields.items():
            ET.SubElement(document, field_name).text = value

    return ET.ElementTree(root)


if __name__ == "__main__":
    tree = generate_xml()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(tree, space="    ")
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

    print(f"Created {len(tree.getroot())} documents: {OUTPUT_FILE}")
