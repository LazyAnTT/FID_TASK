from backend.app.database import Base, DATABASE_FILE, engine
from backend.app.models import Document

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(f"Database ready: {DATABASE_FILE}")
