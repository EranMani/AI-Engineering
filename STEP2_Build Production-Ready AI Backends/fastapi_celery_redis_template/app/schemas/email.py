"""Email service schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class EmailRequest(BaseModel):
    """Request schema for sending email"""
    to: EmailStr
    subject: str
    body: str


class EmailResponse(BaseModel):
    """Response schema after triggering email task"""
    task_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    """Response schema for task status check"""
    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
