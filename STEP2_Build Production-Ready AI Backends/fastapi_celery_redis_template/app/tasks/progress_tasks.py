"""Progress tracking Celery tasks"""
import time
from app.core.celery_app import celery_app


@celery_app.task(bind=True)
def process_large_file(self, file_path: str, file_size: int = 100) -> dict:
    """
    Process a large file with progress updates
    
    This task demonstrates:
    - Custom task states (PROGRESS)
    - Updating task state during execution
    - Progress metadata
    - Long-running task simulation
    
    Args:
        self: Task instance (needed when bind=True)
        file_path: Path to the file to process
        file_size: Size of file (used to calculate steps)
        
    Returns:
        Dictionary with processing results
    """
    total_steps = max(10, file_size // 10)  # At least 10 steps
    
    print(f"[Progress Task] Starting to process file: {file_path}")
    print(f"[Progress Task] Total steps: {total_steps}")
    
    for step in range(1, total_steps + 1):
        # Update task state with progress information
        self.update_state(
            state='PROGRESS',
            meta={
                'current': step,
                'total': total_steps,
                'percent': int((step / total_steps) * 100),
                'status': f'Processing step {step}/{total_steps}',
                'file_path': file_path
            }
        )
        
        # Simulate work (processing a chunk of the file)
        time.sleep(1)
        print(f"[Progress Task] Step {step}/{total_steps} completed ({int((step / total_steps) * 100)}%)")
    
    result = {
        'file_path': file_path,
        'status': 'completed',
        'total_steps': total_steps,
        'processed_at': time.time()
    }
    
    print(f"[Progress Task] File processing completed: {file_path}")
    return result
