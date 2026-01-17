"""Queue management API endpoints"""
from fastapi import APIRouter, HTTPException
from app.utils.queue_manager import RedisQueueManager
from app.schemas.queue import (
    QueueTaskRequest,
    QueueTaskResponse,
    QueueInfoResponse,
    QueueListResponse,
    MoveTaskRequest
)

router = APIRouter(prefix="/queue", tags=["Queue Management"])

# Initialize queue manager
queue_manager = RedisQueueManager()


@router.post("/push", response_model=QueueTaskResponse)
async def push_task(request: QueueTaskRequest):
    """
    Push a task to a Redis queue
    
    This endpoint demonstrates:
    - Direct Redis queue operations
    - Manual task queuing
    """
    try:
        task_id = queue_manager.push_task(request.queue_name, request.task_data)
        return QueueTaskResponse(
            task_id=task_id,
            queue_name=request.queue_name,
            message=f"Task {task_id} pushed to queue {request.queue_name}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info/{queue_name}", response_model=QueueInfoResponse)
async def get_queue_info(queue_name: str, limit: int = 10):
    """
    Get information about a queue
    
    This endpoint demonstrates:
    - Queue inspection
    - Getting queue length
    - Viewing tasks without removing them
    """
    try:
        length = queue_manager.get_queue_length(queue_name)
        tasks = queue_manager.get_queue_tasks(queue_name, limit=limit)
        
        return QueueInfoResponse(
            queue_name=queue_name,
            length=length,
            tasks=tasks if tasks else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear/{queue_name}")
async def clear_queue(queue_name: str):
    """
    Clear all tasks from a queue
    
    This endpoint demonstrates:
    - Queue cleanup operations
    """
    try:
        removed = queue_manager.clear_queue(queue_name)
        return {
            "message": f"Cleared {removed} tasks from queue {queue_name}",
            "queue_name": queue_name,
            "removed_count": removed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/move")
async def move_task(request: MoveTaskRequest):
    """
    Move a task from one queue to another
    
    This endpoint demonstrates:
    - Task routing
    - Queue manipulation
    """
    try:
        task = queue_manager.move_task(request.from_queue, request.to_queue)
        if task:
            return {
                "message": f"Task moved from {request.from_queue} to {request.to_queue}",
                "task": task
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No task found in queue {request.from_queue}"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=QueueListResponse)
async def list_queues():
    """
    List all queues
    
    This endpoint demonstrates:
    - Queue discovery
    """
    try:
        queues = queue_manager.get_all_queues()
        return QueueListResponse(
            queues=queues,
            total=len(queues)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
