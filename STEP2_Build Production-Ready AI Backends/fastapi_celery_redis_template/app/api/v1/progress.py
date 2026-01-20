"""Progress tracking API endpoints

This module demonstrates how to track progress of long-running tasks using
custom Celery task states. Unlike simple tasks that only show PENDING/SUCCESS,
progress tasks can report intermediate states (PROGRESS) with metadata like
percentage complete, current step, etc.

Key Feature: Custom task states via update_state() allow real-time progress
tracking for long-running operations like file processing, data imports, etc.
"""
from fastapi import APIRouter
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.tasks.progress_tasks import process_large_file
from app.schemas.progress import ProcessFileRequest, ProcessFileResponse, ProgressResponse

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.post("/process-file", response_model=ProcessFileResponse)
async def trigger_file_processing(request: ProcessFileRequest):
    """
    Start file processing task with progress tracking
    
    Queues a long-running task that will report progress updates. The task
    uses custom PROGRESS states to report completion percentage, current step,
    and other metadata during execution.
    
    Args:
        request: File path and optional size (determines number of steps)
        
    Returns:
        ProcessFileResponse with task_id for tracking progress
        
    Example:
        POST /api/v1/progress/process-file
        {"file_path": "/data/file.txt", "file_size": 20}
        
        Response: {"task_id": "abc-123", "status": "PENDING", ...}
    """
    # Queue task - worker will process and update progress state
    task = process_large_file.delay(
        request.file_path,
        request.file_size or 100
    )
    
    return ProcessFileResponse(
        task_id=task.id,
        status="PENDING",
        message=f"File processing started for {request.file_path}"
    )


@router.get("/status/{task_id}", response_model=ProgressResponse)
async def get_progress_status(task_id: str):
    """
    Get current progress status of a task
    
    Returns task state and progress metadata. When status is 'PROGRESS',
    includes metadata like current step, total steps, and percentage complete.
    
    Task States:
    - PENDING: Queued, not started
    - PROGRESS: Running (includes progress metadata)
    - SUCCESS: Completed (includes result)
    - FAILURE: Failed (includes error)
    
    Args:
        task_id: Task identifier from POST /process-file response
        
    Returns:
        ProgressResponse with status and progress/result/error based on state
        
    Example Response (PROGRESS state):
        {
            "task_id": "abc-123",
            "status": "PROGRESS",
            "progress": {
                "current": 5,
                "total": 20,
                "percent": 25,
                "status": "Processing step 5/20"
            }
        }
    """
    result = AsyncResult(task_id, app=celery_app)
    
    response = ProgressResponse(
        task_id=task_id,
        status=result.state
    )
    
    if result.state == 'PROGRESS':
        # Custom progress state - return metadata (percent, current step, etc.)
        response.progress = result.info
    elif result.ready():
        # Task completed - return result or error
        if result.successful():
            response.result = result.get()
        else:
            response.error = str(result.info)
    
    return response
