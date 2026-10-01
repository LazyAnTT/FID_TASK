from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_FILE = PROJECT_ROOT / "data" / "documents.db"
DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{DATABASE_FILE}",
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
