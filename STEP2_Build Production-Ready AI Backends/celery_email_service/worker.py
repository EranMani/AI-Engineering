from celery import Celery
from config import get_redis_url
import time
import random

celery_app = Celery(
    "Email Service",
    broker=get_redis_url(),
    backend=get_redis_url()
)

celery_app.conf.update(
    task_always_eager=False,
    worker_pool='threads',  # Thread-based pool for Windows
    worker_threads=4,  # Number of threads
)

"""
NOTE: you can call a task by using simple .delay()
you can call a task with more options such as delays, expiration, priorities by using .apply_async()
"""
@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_email(self, to: str, subject: str, body: str) -> str:
    try:
        print(f"Got email task data. Sending email to: {to} with subject: {subject} and with the content: {body}")

        error_chance = random.random()
        print(f"error chance: {error_chance}")

        if error_chance < 0.1: # 10% chance
            raise ConnectionError("SMTP server connection failed")
        elif error_chance < 0.15: 
            raise TimeoutError("Request timed out")
        elif error_chance < 0.18:
            raise Exception("SMTP server returned 503: service temporarily unavailable")

        time.sleep(2)
        print(f"Email sent successfully to {to}")
        return f"Email sent to {to} with subject: {subject}"
        
    except (ConnectionError, TimeoutError) as exc:
        print(f"Network error (attempt {self.request.retries + 1}/{self.max_retries}): {exc}")
        raise self.retry(exc=exc, countdown=5)
        
    except Exception as exc:
        # Log error but allow worker to continue
        print(f"Permanent error - task failed: {exc}")
        # This will mark task as FAILURE but worker continues
        raise