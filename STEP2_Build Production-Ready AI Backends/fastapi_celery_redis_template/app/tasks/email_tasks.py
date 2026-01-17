"""Email-related Celery tasks"""
import time
import random
from app.core.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_email(self, to: str, subject: str, body: str) -> str:
    """
    Send an email (simulated)
    
    This task demonstrates:
    - Basic task execution
    - Error handling and retries
    - Task state tracking
    
    Args:
        self: Task instance (needed when bind=True)
        to: Recipient email address
        subject: Email subject
        body: Email body
        
    Returns:
        Success message string
    """
    try:
        print(f"[Email Task] Sending email to: {to}")
        print(f"[Email Task] Subject: {subject}")
        print(f"[Email Task] Body: {body}")
        
        # Simulate network delay
        time.sleep(2)
        
        # Simulate occasional failures (for retry demonstration)
        # In production, this would be actual SMTP operations
        if random.random() < 0.1:  # 10% failure rate
            raise ConnectionError("SMTP server connection failed")
        
        print(f"[Email Task] Email sent successfully to {to}")
        return f"Email sent successfully to {to}"
        
    except (ConnectionError, TimeoutError) as exc:
        # Retry on network errors
        retry_count = self.request.retries + 1
        print(f"[Email Task] Network error (attempt {retry_count}/{self.max_retries}): {exc}")
        raise self.retry(exc=exc, countdown=5)
        
    except Exception as exc:
        # Don't retry on other errors
        print(f"[Email Task] Permanent error: {exc}")
        raise
