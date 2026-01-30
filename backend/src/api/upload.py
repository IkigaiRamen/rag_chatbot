from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import uuid

from src.ingestion.ingest import ingest_file

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 Ingest immediately
    ingest_file(file_path)

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_added": "ok"
    }
