# 🥦 The AI Engineer's Guide to Celery
## From "The Spinning Wheel of Death" to "Background Magic"

---

## Table of Contents
1. [The Core Problem: "The Blocking Waiter"](#the-core-problem-the-blocking-waiter)
2. [The Solution: Celery Architecture](#the-solution-celery-architecture)
3. [When Should You Use Celery?](#when-should-you-use-celery)
4. [Setting Up Celery: Step-by-Step](#setting-up-celery-step-by-step)
5. [Understanding the Code Flow](#understanding-the-code-flow)
6. [Production Best Practices](#production-best-practices)
7. [Common Patterns and Examples](#common-patterns-and-examples)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## The Core Problem: "The Blocking Waiter"

### The Coffee Shop Analogy

Imagine you run a coffee shop (your Web App).

**Without Celery:** A customer orders a fancy latte that takes 5 minutes to make. The cashier (FastAPI) stops taking orders, walks to the machine, makes the coffee, and hands it over. Meanwhile, a line of 50 angry customers forms. The shop effectively freezes.

**With Celery:** The cashier takes the order, writes it on a ticket, sticks it on a rail, and immediately asks the next customer, "Can I help you?" A separate Barista (Celery Worker) grabs the ticket and makes the coffee in the background.

### The Technical Reality

Web servers (like Uvicorn/FastAPI) are designed to handle requests in **milliseconds**. AI models take **seconds or minutes**. If you run AI logic inside the web server, you block the "cashier," causing:

- ⚠️ **Timeouts**: Requests exceed the 30-60 second limit
- ⚠️ **Crashes**: Server runs out of memory or connections
- ⚠️ **Poor User Experience**: Users see loading spinners forever
- ⚠️ **Scalability Issues**: Can't handle multiple requests simultaneously

### Real-World Example

```python
# ❌ BAD: This blocks the entire server for 10 seconds
@app.post("/process")
async def process_data(data: dict):
    result = heavy_ai_model.generate(data)  # Takes 10 seconds!
    return {"result": result}

# ✅ GOOD: This returns immediately, work happens in background
@app.post("/process")
async def process_data(data: dict):
    task = heavy_ai_task.delay(data)  # Returns in milliseconds!
    return {"task_id": task.id, "status": "processing"}
```

---

## The Solution: Celery Architecture

Celery is a **Task Queue** system. It allows your application to offload work to be done "later" or "somewhere else."

### The Four Main Characters

#### 1. **The Producer** (FastAPI/Your Web App)
- **Role**: Creates tasks and sends them to the queue
- **Location**: Your FastAPI endpoints (`endpoint.py`)
- **Action**: Calls `my_task.delay(data)` - returns immediately!

#### 2. **The Broker** (Redis/RabbitMQ)
- **Role**: The "Ticket Rail" - message transport layer
- **Function**: Holds tasks in a queue (First-In-First-Out)
- **Benefit**: Ensures no task is lost even if the worker is busy
- **Common Choice**: Redis (simple, fast, widely used)

#### 3. **The Worker** (Celery Process)
- **Role**: The "Barista" - executes the actual work
- **Location**: Separate terminal/process running `celery -A worker worker --loglevel=info`
- **Action**: Watches the broker, grabs tasks, executes Python code
- **Benefit**: Can run on different machines (horizontal scaling)

#### 4. **The Result Backend** (Redis/Database)
- **Role**: The "Pickup Counter" - stores task results
- **Function**: Since the Worker runs in a different process, it can't return a value directly
- **Solution**: Writes the result to Redis/Database where the Producer can look it up using `task_id`

### Visual Flow Diagram

```
┌─────────────┐         ┌──────────┐         ┌──────────┐         ┌──────────────┐
│   Client    │         │ FastAPI  │         │  Redis   │         │   Celery     │
│  (Browser)  │────────▶│ Producer │────────▶│  Broker  │────────▶│   Worker     │
└─────────────┘         └──────────┘         └──────────┘         └──────────────┘
                              │                    │                       │
                              │                    │                       │
                              │                    │                       ▼
                              │                    │              ┌─────────────────┐
                              │                    │              │  Execute Task   │
                              │                    │              │  (10 seconds)   │
                              │                    │              └─────────────────┘
                              │                    │                       │
                              │                    │                       │
                              │                    ▼                       │
                              │              ┌──────────┐                 │
                              │              │  Result  │◀────────────────┘
                              │              │ Backend  │
                              │              └──────────┘
                              │                    │
                              │                    │
                              ▼                    ▼
                        ┌─────────────┐    ┌─────────────┐
                        │ Return      │    │ Poll for    │
                        │ task_id     │    │ result      │
                        └─────────────┘    └─────────────┘
```

---

## When Should You Use Celery?

Use this checklist. If you answer **YES** to any of these, you need Celery:

- ✅ Is the task slower than **500ms**? (e.g., Image resizing, sending an email)
- ✅ Is the task **resource-heavy**? (e.g., Loading a 4GB PyTorch model into RAM)
- ✅ Is the task **unreliable**? (e.g., Connecting to a 3rd party API that might fail and need retries)
- ✅ Do you need to **schedule it**? (e.g., "Run this report every Monday at 9 AM")
- ✅ Do you need **parallel processing**? (e.g., Process 1000 images simultaneously)

### Common AI Use Cases

| Use Case | Time | Why Celery? |
|----------|------|-------------|
| Generating images with Stable Diffusion | 5-10s | Too slow for web request |
| RAG (Retrieval-Augmented Generation) | 10-30s | Multiple API calls, vector search |
| Fine-tuning a small model | Minutes/Hours | Long-running process |
| Batch processing 10,000 comments | Variable | Parallel processing needed |
| Sending email notifications | 1-3s | External API, can fail |
| PDF processing and OCR | 5-15s | CPU-intensive |

---

## Setting Up Celery: Step-by-Step

### Prerequisites

1. **Install Redis** (the broker)
   ```bash
   # Windows (using WSL or Docker)
   docker run -d -p 6379:6379 redis:latest
   
   # macOS
   brew install redis
   brew services start redis
   
   # Linux
   sudo apt-get install redis-server
   sudo systemctl start redis
   ```

2. **Install Celery** (Python package)
   ```bash
   pip install celery redis
   # or with uv
   uv add celery redis
   ```

### Step 1: Create the Celery App (`worker.py`)

This file defines your Celery application and tasks.

```python
from celery import Celery
import time

# Setup Celery
# "tasks" is the name of our module
# broker = tells Celery where Redis is (localhost port 6379)
# backend = tells Celery where to store results
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Define a Task
# The @celery_app.task decorator turns a normal function into a background job
@celery_app.task
def simulate_heavy_ai_task(event_id: str, data: dict):
    """Simulates a slow AI process (like generating an image or summarizing text)"""
    print(f"Worker: Starting process for {event_id}...")
    time.sleep(10)  # Simulates 10 seconds of work
    
    result = f"AI Analysis completed for {event_id}. Logic: {data.get('event_type')}"
    print(f"Worker: Finished {event_id}")
    return result
```

**Key Points:**
- `broker`: Where tasks are queued (Redis URL)
- `backend`: Where results are stored (usually same Redis instance)
- `@celery_app.task`: Decorator that makes a function a Celery task
- The function runs in a **separate process**, not in your web server

### Step 2: Create the FastAPI Endpoint (`endpoint.py`)

This file creates endpoints that trigger Celery tasks.

```python
from fastapi import APIRouter
from pydantic import BaseModel
from worker import simulate_heavy_ai_task

# Setup a specific router for this logic
events_router = APIRouter()

# Define the schema (the contract)
class EventSchema(BaseModel):
    event_id: str
    event_type: str
    data: dict

# The endpoint
@events_router.post("/event-handler")
async def handle_event(event: EventSchema):
    # 1. Send the task to Celery
    # We use .delay() to send it to the background.
    # This returns IMMEDIATELY. It does not wait for the 10s sleep.
    task = simulate_heavy_ai_task.delay(event.event_id, event.data)
    
    # 2. Return the Task ID to the user
    # The user can use this ID later to check if the job is done.
    return {
        "status": "processing", 
        "task_id": task.id,
        "message": "Your request is queued. Check back later."
    }
```

**Key Points:**
- `.delay()`: The magic method that sends the task to the queue
- Returns **immediately** - doesn't wait for the task to complete
- Returns a `task_id` that can be used to check status later

### Step 3: Start the Celery Worker

**Important:** You need to run the Celery worker in a **separate terminal**!

```bash
# Navigate to your project directory
cd STEP2_Build\ Production-Ready\ AI\ Backends/ai_backend_basic

# Start the worker
celery -A worker worker --loglevel=info
```

You should see:
```
[tasks]
  . worker.simulate_heavy_ai_task

[INFO/MainProcess] Connected to redis://localhost:6379/0
[INFO/MainProcess] celery@your-machine ready.
```

**Keep this terminal open!** The worker must be running to process tasks.

### Step 4: Start Your FastAPI Server

In a **different terminal**:

```bash
# Start FastAPI
uvicorn main:app --reload
```

### Step 5: Test It!

Use the client script or send a POST request:

```bash
python client.py
```

Or use curl:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/event-handler" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_1055",
    "event_type": "user_prompt",
    "data": {"prompt": "Hello world"}
  }'
```

You should get an immediate response:
```json
{
  "status": "processing",
  "task_id": "c64f-4d8a-9b2e-1f3a",
  "message": "Your request is queued. Check back later."
}
```

Watch the Celery worker terminal - you'll see it processing the task!

---

## Understanding the Code Flow

Here is the complete lifecycle of a Celery task from start to finish:

### 1. **Definition** (`worker.py`)
```python
@celery_app.task
def simulate_heavy_ai_task(event_id: str, data: dict):
    # This function belongs to the Worker
    return result
```

### 2. **Trigger** (`endpoint.py`)
```python
task = simulate_heavy_ai_task.delay(event_id, data)
# .delay() returns instantly - doesn't run the code!
# Returns an AsyncResult object with a unique task_id
```

### 3. **Queueing** (Redis)
- The message sits in Redis waiting for a free worker
- Multiple tasks can queue up
- Redis ensures no task is lost

### 4. **Execution** (Celery Worker)
- A Worker picks up the task
- Executes the code (blocking only itself, not the web server)
- Can run on a different machine!

### 5. **Completion** (Result Backend)
- Worker saves the return value to Redis
- Updates status to `SUCCESS`

### 6. **Retrieval** (Check Status Endpoint)
```python
from celery.result import AsyncResult

result = AsyncResult(task_id, app=celery_app)
if result.ready():
    return {"status": "completed", "result": result.get()}
else:
    return {"status": "processing"}
```

---

## Production Best Practices

### 1. **Environment Variables for Configuration**

Never hardcode Redis URLs! Use environment variables:

```python
import os
from celery import Celery

celery_app = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)
```

### 2. **Task Timeouts and Retries**

Configure automatic retries for unreliable tasks:

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def unreliable_api_call(self, data):
    try:
        response = external_api.call(data)
        return response
    except Exception as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc)
```

### 3. **Task Status Endpoint**

Create an endpoint to check task status:

```python
from celery.result import AsyncResult
from worker import celery_app

@events_router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    
    if result.ready():
        if result.successful():
            return {
                "status": "completed",
                "result": result.get()
            }
        else:
            return {
                "status": "failed",
                "error": str(result.info)
            }
    else:
        return {
            "status": "processing",
            "task_id": task_id
        }
```

### 4. **Error Handling**

Always handle errors gracefully:

```python
@celery_app.task
def process_data(data: dict):
    try:
        result = ai_model.process(data)
        return {"success": True, "result": result}
    except Exception as e:
        # Log the error
        print(f"Error processing {data}: {e}")
        return {"success": False, "error": str(e)}
```

### 5. **Task Prioritization**

Use different queues for different priorities:

```python
# High priority task
@celery_app.task(queue='high_priority')
def urgent_task(data):
    pass

# Low priority task
@celery_app.task(queue='low_priority')
def background_task(data):
    pass

# Start workers for specific queues
# celery -A worker worker -Q high_priority,low_priority
```

### 6. **Monitoring and Logging**

Use proper logging:

```python
import logging

logger = logging.getLogger(__name__)

@celery_app.task
def process_data(data: dict):
    logger.info(f"Starting task for {data.get('id')}")
    try:
        result = process(data)
        logger.info(f"Task completed successfully")
        return result
    except Exception as e:
        logger.error(f"Task failed: {e}", exc_info=True)
        raise
```

### 7. **Result Expiration**

Don't store results forever - set expiration:

```python
@celery_app.task
def process_data(data: dict):
    result = process(data)
    return result

# When calling the task
task = process_data.apply_async(
    args=[data],
    expires=3600  # Result expires after 1 hour
)
```

---

## Common Patterns and Examples

### Pattern 1: Simple Background Task

```python
@celery_app.task
def send_email(to: str, subject: str, body: str):
    # Send email logic
    email_service.send(to, subject, body)
    return "Email sent"

# In your endpoint
@router.post("/send-email")
async def send_email_endpoint(email_data: EmailSchema):
    task = send_email.delay(
        email_data.to,
        email_data.subject,
        email_data.body
    )
    return {"task_id": task.id}
```

### Pattern 2: Task with Progress Updates

```python
from celery import current_task

@celery_app.task(bind=True)
def long_running_task(self, data: dict):
    total_steps = 100
    for i in range(total_steps):
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': total_steps}
        )
        # Do work
        process_step(i)
    return {'current': total_steps, 'total': total_steps, 'status': 'Done'}
```

### Pattern 3: Chained Tasks (Task A → Task B → Task C)

```python
from celery import chain

# Define tasks
@celery_app.task
def step1(data):
    return process_step1(data)

@celery_app.task
def step2(result):
    return process_step2(result)

@celery_app.task
def step3(result):
    return process_step3(result)

# Chain them
workflow = chain(step1.s(data), step2.s(), step3.s())
result = workflow.apply_async()
```

### Pattern 4: Scheduled Tasks (Cron Jobs)

```python
from celery.schedules import crontab

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'daily-report': {
        'task': 'worker.generate_daily_report',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9 AM
    },
    'weekly-cleanup': {
        'task': 'worker.cleanup_old_data',
        'schedule': crontab(hour=0, minute=0, day_of_week=1),  # Every Monday
    },
}

# Start the beat scheduler
# celery -A worker beat --loglevel=info
```

### Pattern 5: Batch Processing

```python
@celery_app.task
def process_single_item(item: dict):
    return process(item)

# Process many items in parallel
@router.post("/process-batch")
async def process_batch(items: list):
    tasks = [process_single_item.delay(item) for item in items]
    return {"task_ids": [task.id for task in tasks]}

# Wait for all to complete
from celery import group

job = group(process_single_item.s(item) for item in items)
result = job.apply_async()
results = result.get()  # Wait for all
```

---

## Troubleshooting Guide

### Problem 1: "No module named 'worker'"

**Solution:** Make sure you're running Celery from the correct directory:
```bash
cd ai_backend_basic
celery -A worker worker --loglevel=info
```

### Problem 2: "Connection refused to Redis"

**Solution:** 
1. Check if Redis is running: `redis-cli ping` (should return `PONG`)
2. Start Redis: `docker run -d -p 6379:6379 redis:latest`
3. Check the Redis URL in `worker.py`

### Problem 3: Tasks are queued but not executing

**Solution:**
1. Make sure the Celery worker is running in a separate terminal
2. Check worker logs for errors
3. Verify the task name matches: `celery -A worker inspect registered`

### Problem 4: "Task result backend is not configured"

**Solution:** Make sure both `broker` and `backend` are set:
```python
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"  # Don't forget this!
)
```

### Problem 5: Tasks are slow or timing out

**Solution:**
1. Check worker resources (CPU, memory)
2. Add more workers: `celery -A worker worker --concurrency=4`
3. Use task timeouts: `@celery_app.task(time_limit=300)`  # 5 minutes

### Problem 6: Results are not being retrieved

**Solution:**
1. Make sure `backend` is configured
2. Check if result has expired (set longer expiration)
3. Use the same Celery app instance: `AsyncResult(task_id, app=celery_app)`

---

## Quick Reference Cheat Sheet

### Basic Setup
```python
from celery import Celery
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def my_task(data):
    return process(data)
```

### Calling Tasks
```python
# Async (returns immediately)
task = my_task.delay(data)

# Sync (waits for result - don't use in production!)
result = my_task(data)
```

### Checking Status
```python
from celery.result import AsyncResult
result = AsyncResult(task_id, app=celery_app)

if result.ready():
    if result.successful():
        print(result.get())
    else:
        print(result.info)  # Error info
```

### Starting Workers
```bash
# Basic worker
celery -A worker worker --loglevel=info

# Multiple workers (4 processes)
celery -A worker worker --concurrency=4

# Specific queue
celery -A worker worker -Q high_priority

# Beat scheduler (for periodic tasks)
celery -A worker beat --loglevel=info
```

---

## Next Steps

1. **Add monitoring**: Use Flower (`pip install flower`) to monitor your Celery workers
2. **Add retries**: Configure automatic retries for unreliable tasks
3. **Add task status endpoint**: Let users check their task status
4. **Scale horizontally**: Run workers on multiple machines
5. **Add error notifications**: Send alerts when tasks fail

---

## Summary

Celery solves the fundamental problem of **blocking operations** in web applications:

- ✅ **Fast responses**: Web server returns immediately
- ✅ **Scalability**: Process tasks in parallel across multiple workers
- ✅ **Reliability**: Tasks are queued and won't be lost
- ✅ **Flexibility**: Run workers on different machines
- ✅ **Monitoring**: Track task status and results

Remember: **If it takes longer than 500ms, use Celery!**

---

## Additional Resources

- [Official Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [FastAPI + Celery Tutorial](https://testdriven.io/blog/fastapi-and-celery/)
- [Celery Best Practices](https://docs.celeryq.dev/en/stable/userguide/tasks.html#best-practices)

---

**Happy Coding! 🚀**

