import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.xml_importer import import_from_source

router = APIRouter(prefix="/api", tags=["imports"])


@router.post("/import")
def import_xml(db: Session = Depends(get_db)):
    try:
        return import_from_source(db)

    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail="Could not download the XML source.",
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error
