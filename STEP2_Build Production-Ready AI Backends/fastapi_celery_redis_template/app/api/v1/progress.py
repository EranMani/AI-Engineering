"""Progress tracking API endpoints"""
from fastapi import APIRouter
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.tasks.progress_tasks import process_large_file
from app.schemas.progress import ProcessFileRequest, ProcessFileResponse, ProgressResponse

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.post("/process-file", response_model=ProcessFileResponse)
async def trigger_file_processing(request: ProcessFileRequest):
    """
    Trigger file processing task with progress tracking
    
    This endpoint demonstrates:
    - Starting a long-running task
    - Getting task_id for progress tracking
    """
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
    Get progress status of a task
    
    This endpoint demonstrates:
    - Checking custom task states (PROGRESS)
    - Retrieving progress metadata
    - Handling different task states
    """
    result = AsyncResult(task_id, app=celery_app)
    
    response = ProgressResponse(
        task_id=task_id,
        status=result.state
    )
    
    if result.state == 'PROGRESS':
        # Task is in progress, return progress metadata
        response.progress = result.info
    elif result.ready():
        if result.successful():
            response.result = result.get()
        else:
            response.error = str(result.info)
    
    return response
