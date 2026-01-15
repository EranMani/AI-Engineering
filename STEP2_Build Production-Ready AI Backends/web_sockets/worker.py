from celery import Celery
import redis
import time
import json

# setup celery
celery_app = Celery('worker', broker='redis://localhost:6379/0')

# setup redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@celery_app.task
def generate_image_task(job_id: str, prompt: str):
    print(f"🎨 Starting job {job_id}: {prompt}")

    # simulate heavy AI work
    time.sleep(10)

    result_url = f"https://fake-ai-images.com/{job_id}.png"

    # create the message to send back
    message = {
        "status": "completed",
        "url": result_url
    }

    # THE CRITICAL STEP: Send the notification
    redis_client.publish(job_id, json.dumps(message))

    print(f"✅ Published result to channel: {job_id}")