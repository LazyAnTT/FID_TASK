from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.app.database import PROJECT_ROOT
from backend.app.routers.documents import router as documents_router
from backend.app.routers.imports import router as imports_router

app = FastAPI(title="Document Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(imports_router)


@app.get("/source/documents.xml", tags=["source"])
def get_xml_source():
    source_file = PROJECT_ROOT / "data" / "documents.xml"

    if not source_file.is_file():
        raise HTTPException(
            status_code=404,
            detail="Generate data/documents.xml first.",
        )

    return FileResponse(
        source_file,
        media_type="application/xml",
    )
