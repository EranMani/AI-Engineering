from celery import Celery
import time

# setup celery
# "tasks" is the name of our module
# broker = "tells celery where redis is living (localhost port 6379)"
# backend = "tells celery where to store results so we can check them later"
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# define a Task
# the @celery_app.task decorator turns a normal function into a background job
@celery_app.task
def simulate_heavy_ai_task(event_id: str, data: dict):
    """Simulates a slow AI process (like generating an image or summarizing text)"""
    print(f"Worker: Starting process for {event_id}...")
    time.sleep(10)

    result = f"AI Analysis completed for {event_id}. Logic: {data.get("event_type")}"
    print(f"Worker: Finished {event_id}")
    return result