"""WebSocket notification Celery tasks"""
import time
import json
from app.core.celery_app import celery_app
from app.core.redis_client import get_redis_client


@celery_app.task
def generate_report(job_id: str, report_type: str, parameters: dict = None) -> dict:
    """
    Generate a report and publish result via Redis pub/sub
    
    This task demonstrates:
    - Publishing to Redis channels
    - Real-time notifications
    - WebSocket integration pattern
    
    Args:
        job_id: Unique job identifier (used as Redis channel name)
        report_type: Type of report to generate
        parameters: Optional parameters for report generation
        
    Returns:
        Dictionary with report generation results
    """
    print(f"[WebSocket Task] Starting report generation: {job_id}")
    print(f"[WebSocket Task] Report type: {report_type}")
    
    # Simulate report generation (heavy work)
    time.sleep(5)
    
    # Generate result
    result = {
        "job_id": job_id,
        "report_type": report_type,
        "status": "completed",
        "download_url": f"https://example.com/reports/{job_id}.pdf",
        "generated_at": time.time(),
        "parameters": parameters or {}
    }
    
    # Publish result to Redis channel (channel name = job_id)
    # This allows WebSocket endpoints to receive the result in real-time
    redis_client = get_redis_client()
    redis_client.publish(job_id, json.dumps(result))
    
    print(f"[WebSocket Task] Published result to channel: {job_id}")
    return result
