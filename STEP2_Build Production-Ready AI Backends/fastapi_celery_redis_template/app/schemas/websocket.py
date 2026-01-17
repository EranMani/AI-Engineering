"""WebSocket schemas"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class GenerateReportRequest(BaseModel):
    """Request schema for report generation"""
    report_type: str
    parameters: Optional[Dict[str, Any]] = None


class GenerateReportResponse(BaseModel):
    """Response schema after triggering report generation"""
    job_id: str
    status: str
    websocket_url: str


class WebSocketMessage(BaseModel):
    """WebSocket message schema"""
    status: str
    job_id: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
