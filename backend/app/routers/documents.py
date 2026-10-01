from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import Document
from backend.app.schemas import DocumentResponse

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=list[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    statement = select(Document).order_by(
        Document.created_at.desc(),
        Document.id.desc(),
    )

    return db.scalars(statement).all()
