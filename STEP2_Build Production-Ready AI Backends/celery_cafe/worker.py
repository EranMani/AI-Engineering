import time
import random
from celery import Celery, current_task
from config import get_redis_url

REDIS_URL = get_redis_url()

# 1. Setup Celery (The kitchen)
celery_app = Celery(
    "cafe_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Configure Celery to track task states
celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# 2. Define the menu (Task Logic)
# bind=True allows us to access 'self' to update the state
@celery_app.task(bind=True)
def make_coffee(self, order_id: str, coffee_type: str, customer_name: str):
    try:
        print(f"☕ BARISTA: Starting order for {customer_name} ({coffee_type})")

        # Step 1: Grinding Beans
        self.update_state(state="GRINDING", meta={"progress": "30%"})
        time.sleep(random.uniform(2, 4)) # simulate work

        # Step 2: Brewing
        self.update_state(state="BREWING", meta={"progress": "60%"})
        time.sleep(random.uniform(3, 6)) # Brewing takes longer!

        # Step 3: Pouring Milk
        self.update_state(state="POURING", meta={"progress": "90%"})
        time.sleep(random.uniform(1, 2))

        print(f"✅ BARISTA: Order {order_id} is ready!")
        return f"{coffee_type} for {customer_name} is served!"
    except Exception as e:
        print(f"❌ BARISTA ERROR: {str(e)}")
        raise  # Re-raise to mark task as FAILURE