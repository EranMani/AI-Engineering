"""Progress tracking schemas"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class ProcessFileRequest(BaseModel):
    """Request schema for file processing"""
    file_path: str
    file_size: Optional[int] = None


class ProcessFileResponse(BaseModel):
    """Response schema after triggering file processing"""
    task_id: str
    status: str
    message: str


class ProgressResponse(BaseModel):
    """Response schema for progress status"""
    task_id: str
    status: str
    progress: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
