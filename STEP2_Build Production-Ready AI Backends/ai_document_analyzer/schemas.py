from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any

################ AUTHENTICATION ################
class UserCreate(BaseModel):
    """Schema for user registration"""
    username:str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

class Token(BaseModel):
    """Schema for user information response"""
    id: str
    username: str
    email: str
    created_at: datetime

class UserReponse(BaseModel):
    """Schema for user information response"""
    id: str
    username: str
    email: str
    created_at: datetime

################ DOCUMENT #################
class DocumentUpload(BaseModel):
    """Schema for document upload metadata"""
    filename: str
    file_type: str

class DocumentResponse(BaseModel):
    """Schema for document information"""
    id: str
    filename: str
    file_type: str
    status: str
    created_at: datetime
    user_id: str

class ProcessingStatus(BaseModel):
    """Schema for task processing status"""
    task_id: str
    status: str
    progress: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class AnalysisResult(BaseModel):
    """Schema for document analysis results"""
    document_id: str
    summary: str
    key_points: List[str]
    world_count: int
    sentiment: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any]
    created_at: datetime

