"""Queue management Celery tasks"""
from app.core.celery_app import celery_app


@celery_app.task
def process_queue_task(task_data: dict) -> dict:
    """
    Process a task from a queue
    
    This is a simple example task that can be used with queue management.
    In production, you would have more specific task handlers.
    
    Args:
        task_data: Task data dictionary
        
    Returns:
        Processing result
    """
    print(f"[Queue Task] Processing task: {task_data.get('id', 'unknown')}")
    return {
        "status": "processed",
        "task_data": task_data,
        "processed_at": "now"
    }
