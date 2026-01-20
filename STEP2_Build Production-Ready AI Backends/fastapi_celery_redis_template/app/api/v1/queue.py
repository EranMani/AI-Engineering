"""Queue management API endpoints

This module provides direct Redis queue management operations. Unlike Celery
tasks which are managed automatically, these endpoints allow manual control
over Redis queues for advanced use cases like custom task routing, queue
inspection, and direct queue manipulation.

Key Difference: These are raw Redis list operations, not Celery tasks.
Useful for custom queue management, monitoring, and debugging.
"""
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

# Initialize queue manager instance (singleton pattern)
queue_manager = RedisQueueManager()


@router.post("/push", response_model=QueueTaskResponse)
async def push_task(request: QueueTaskRequest):
    """
    Push a task directly to a Redis queue
    
    Manually adds a task to a Redis list (queue). This bypasses Celery and
    allows direct queue manipulation. Tasks are stored as JSON in Redis lists.
    
    Args:
        request: Queue name and task data dictionary
        
    Returns:
        QueueTaskResponse with task_id and confirmation message
        
    Example:
        POST /api/v1/queue/push
        {
            "queue_name": "my_queue",
            "task_data": {"action": "process", "data": "example"}
        }
    """
    try:
        # Push task to Redis list (FIFO queue)
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
    
    Inspects a Redis queue without modifying it. Returns queue length and
    optionally a preview of tasks (without removing them).
    
    Args:
        queue_name: Name of the queue to inspect
        limit: Maximum number of tasks to return in preview (default: 10)
        
    Returns:
        QueueInfoResponse with queue length and task preview
        
    Example:
        GET /api/v1/queue/info/my_queue?limit=5
        
        Response:
        {
            "queue_name": "my_queue",
            "length": 15,
            "tasks": [{"id": "task1", ...}, {"id": "task2", ...}]
        }
    """
    try:
        # Get queue length (number of tasks waiting)
        length = queue_manager.get_queue_length(queue_name)
        # Peek at tasks without removing them
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
    
    Removes all tasks from the specified queue. Useful for cleanup, resetting
    queues, or clearing stuck tasks. This operation is irreversible.
    
    Args:
        queue_name: Name of the queue to clear
        
    Returns:
        Dictionary with removal confirmation and count
        
    Example:
        DELETE /api/v1/queue/clear/my_queue
        
        Response:
        {
            "message": "Cleared 5 tasks from queue my_queue",
            "queue_name": "my_queue",
            "removed_count": 5
        }
        
    Warning:
        This permanently deletes all tasks in the queue!
    """
    try:
        # Delete entire queue (removes all tasks)
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
    
    Transfers a task from the source queue to the destination queue. Useful
    for task routing, priority changes, or moving failed tasks to retry queues.
    
    Args:
        request: Source and destination queue names
        
    Returns:
        Dictionary with move confirmation and moved task data
        
    Example:
        POST /api/v1/queue/move
        {
            "from_queue": "failed_tasks",
            "to_queue": "retry_queue"
        }
        
        Response:
        {
            "message": "Task moved from failed_tasks to retry_queue",
            "task": {"id": "task123", "action": "process", ...}
        }
        
    Raises:
        404: If source queue is empty
    """
    try:
        # Pop from source queue and push to destination
        task = queue_manager.move_task(request.from_queue, request.to_queue)
        if task:
            return {
                "message": f"Task moved from {request.from_queue} to {request.to_queue}",
                "task": task
            }
        else:
            # Source queue was empty
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
    List all queues in Redis
    
    Discovers and returns all queue names currently in Redis. Useful for
    monitoring, debugging, and queue management dashboards.
    
    Returns:
        QueueListResponse with list of queue names and total count
        
    Example:
        GET /api/v1/queue/list
        
        Response:
        {
            "queues": ["my_queue", "priority_queue", "failed_queue"],
            "total": 3
        }
        
    Note:
        Returns all Redis keys - may include non-queue keys depending on
        Redis configuration. In production, consider using queue naming
        conventions or separate tracking.
    """
    try:
        # Get all queue names (Redis keys)
        queues = queue_manager.get_all_queues()
        return QueueListResponse(
            queues=queues,
            total=len(queues)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
