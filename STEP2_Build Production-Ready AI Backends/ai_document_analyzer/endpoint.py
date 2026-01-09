import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from celery.result import AsyncResult
from schemas import(
    DocumentResponse,
    ProcessingStatus,
    AnalysisResult
)
from auth import get_current_user
from worker import process_document, celery_app
from utils import save_uploaded_file, get_file_type, validate_file, load_analysis_result
from config import get_max_file_size

document_router = APIRouter()

document_db: Dict[str, Dict] = {}

@document_router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), current_user: Dict =Depends(get_current_user)):
    """Upload a document for processing. Protected route - requires authentication"""
    # Validate file
    if not validate_file(file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Supported: PDF, image, text files"
        )

    # Check file size (read first chunk)
    content = await file.read()
    if len(content) > get_max_file_size():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {get_max_file_size()} bytes"
        )

    # reset file pointer
    await file.seek(0)

    # Generate document ID
    document_id = str(uuid.uuid4())

    # Save file
    file_path = await save_uploaded_file(file, current_user["id"])

    # Get file type
    file_type = get_file_type(file.filename)

    # Create document record
    document = {
        "id": document_id,
        "filename": file.filename,
        "file_type": file_type,
        "file_path": str(file_path),
        "status": "PENDING",
        "user_id": current_user["id"],
        "created_at": datetime.utcnow()
    }

    document_db[document_id] = document
    
    # Queue celery task
    task = process_document.delay()