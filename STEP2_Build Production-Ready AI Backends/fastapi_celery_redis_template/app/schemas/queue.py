"""Queue management schemas"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class QueueTaskRequest(BaseModel):
    """Request schema for pushing a task to queue"""
    queue_name: str
    task_data: Dict[str, Any]


class QueueTaskResponse(BaseModel):
    """Response schema after pushing task"""
    task_id: str
    queue_name: str
    message: str


class QueueInfoResponse(BaseModel):
    """Response schema for queue information"""
    queue_name: str
    length: int
    tasks: Optional[List[Dict[str, Any]]] = None


class QueueListResponse(BaseModel):
    """Response schema for listing queues"""
    queues: List[str]
    total: int


class MoveTaskRequest(BaseModel):
    """Request schema for moving a task"""
    from_queue: str
    to_queue: str
