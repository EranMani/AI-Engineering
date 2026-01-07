# ☕ Celery Cafe Project - Complete Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Why This Architecture?](#why-this-architecture)
3. [Project Structure](#project-structure)
4. [Key Concepts Explained](#key-concepts-explained)
5. [Complete Flow Walkthrough](#complete-flow-walkthrough)
6. [File-by-File Breakdown](#file-by-file-breakdown)
7. [How to Run the Project](#how-to-run-the-project)
8. [When to Use This Pattern](#when-to-use-this-pattern)
9. [Common Patterns and Extensions](#common-patterns-and-extensions)

---

## Project Overview

### What is This Project?

This project is a **production-ready demonstration** of how to build a **non-blocking, asynchronous web application** using **FastAPI** (web framework) and **Celery** (task queue system). 

Think of it as a **coffee shop simulation**:
- **Customers** (clients) place orders
- **Cashier** (FastAPI) takes orders instantly and gives customers a ticket
- **Kitchen** (Celery Worker) makes the coffee in the background
- **Customers** can check their order status using their ticket number

### The Core Problem It Solves

**Without this architecture:**
- If making coffee takes 10 seconds, the cashier is blocked for 10 seconds
- Other customers must wait in line
- The system can't handle multiple orders efficiently
- Server resources are wasted waiting

**With this architecture:**
- Cashier takes order in milliseconds and immediately helps the next customer
- Coffee is made in the background by dedicated workers
- Multiple orders can be processed simultaneously
- System scales horizontally (add more workers = handle more orders)

---

## Why This Architecture?

### The Blocking Problem

Imagine you're building a web application that needs to:
- Process large files
- Call slow external APIs
- Run machine learning models
- Generate reports
- Send emails

If you do these tasks **directly in your web request handler**, your server will:
- ❌ Block other requests while waiting
- ❌ Timeout (most web servers have 30-60 second limits)
- ❌ Crash under load
- ❌ Provide poor user experience (users see loading spinners forever)

### The Solution: Task Queue Pattern

This project demonstrates the **Task Queue Pattern**:
1. **Web server** (FastAPI) receives requests instantly
2. **Tasks** are queued in Redis (message broker)
3. **Workers** (Celery) process tasks in the background
4. **Results** are stored and can be retrieved later

**Benefits:**
- ✅ Fast response times (milliseconds instead of seconds)
- ✅ Horizontal scaling (add more workers)
- ✅ Fault tolerance (tasks survive server restarts)
- ✅ Progress tracking (can show "30% complete")
- ✅ Retry mechanisms (failed tasks can be retried)

---

## Project Structure

```
celery_cafe/
├── main.py          # FastAPI application entry point
├── router.py        # Master router that organizes all routes
├── endpoint.py      # API endpoints (order placement, status checking)
├── worker.py        # Celery tasks (the actual coffee-making logic)
├── schemas.py       # Data validation models (Pydantic)
├── config.py        # Configuration management (Redis URL, logging)
├── client.py        # Test client (simulates multiple customers)
└── PROJECT_GUIDE.md # This file!
```

### Architecture Diagram

```
┌─────────────┐
│   Client    │  (Browser, Mobile App, or client.py)
│  (Customer) │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────────────────────────────────────┐
│           FastAPI Application                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ main.py  │→ │router.py │→ │endpoint.py│    │
│  └──────────┘  └──────────┘  └─────┬────┘     │
│                                    │           │
│                                    │ .delay()  │
└────────────────────────────────────┼───────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  Redis Broker   │
                            │  (Message Queue)│
                            └────────┬────────┘
                                     │
                                     │ Task picked up
                                     ▼
                            ┌─────────────────┐
                            │ Celery Worker   │
                            │  (worker.py)    │
                            │  make_coffee()  │
                            └────────┬────────┘
                                     │
                                     │ Result stored
                                     ▼
                            ┌─────────────────┐
                            │ Redis Backend   │
                            │  (Result Store) │
                            └─────────────────┘
```

---

## Key Concepts Explained

### 1. FastAPI - The Web Framework

**What it is:** A modern Python web framework for building APIs.

**Why we use it:**
- Fast (built on Starlette and Pydantic)
- Automatic API documentation (Swagger UI)
- Type validation with Pydantic
- Async support (can handle many concurrent requests)

**In this project:**
- `main.py` creates the FastAPI app
- `endpoint.py` defines the API routes
- Handles HTTP requests and returns JSON responses

### 2. Celery - The Task Queue System

**What it is:** A distributed task queue that allows you to run tasks asynchronously in the background.

**Key Components:**

#### a) Celery App (`celery_app`)
- The main Celery application instance
- Configured with broker (Redis) and backend (Redis)
- Defines how tasks are serialized and processed

#### b) Tasks (`@celery_app.task`)
- Functions decorated with `@celery_app.task` become background tasks
- Can be called with `.delay()` to run asynchronously
- Run in separate worker processes

#### c) Broker (Redis)
- Message queue that holds tasks waiting to be processed
- Ensures tasks aren't lost if worker is busy
- First-In-First-Out (FIFO) queue

#### d) Backend (Redis)
- Stores task results
- Since workers run in separate processes, they can't return values directly
- Results are stored here and retrieved by task_id

#### e) Worker
- Separate process that watches the broker
- Picks up tasks and executes them
- Can run on the same machine or different machines

### 3. Task States

Celery tasks have different states:

- **PENDING** - Task is waiting to be picked up by a worker
- **STARTED** - Worker has started processing the task
- **SUCCESS** - Task completed successfully
- **FAILURE** - Task failed with an exception
- **RETRY** - Task is being retried after failure
- **REVOKED** - Task was cancelled

**Custom States** (in this project):
- **GRINDING** - Custom state we defined (30% progress)
- **BREWING** - Custom state we defined (60% progress)
- **POURING** - Custom state we defined (90% progress)

### 4. `bind=True` - Accessing Task Context

When you use `@celery_app.task(bind=True)`:
- The task function receives `self` as the first parameter
- `self` gives you access to the task's context
- You can call `self.update_state()` to update progress
- You can call `self.retry()` to retry on failure

**Example:**
```python
@celery_app.task(bind=True)
def my_task(self, data):
    # self is the task instance
    self.update_state(state="PROCESSING", meta={"progress": 50})
    # ... do work ...
    return result
```

### 5. AsyncResult - Checking Task Status

`AsyncResult` is a Celery class that represents a task result:
- Created with a `task_id`
- Can check if task is ready: `result.ready()`
- Can get the result: `result.result`
- Can get the status: `result.status`
- Can get error info: `result.info` (if failed)

### 6. Pydantic Schemas - Data Validation

**What it is:** A library for data validation using Python type annotations.

**Why we use it:**
- Automatic validation of incoming data
- Type checking
- Clear error messages
- Automatic API documentation

**In this project:**
- `OrderSchema` - Validates incoming order data
- `OrderResponse` - Defines the structure of API responses

---

## Complete Flow Walkthrough

Let's trace a complete order from start to finish:

### Step 1: Customer Places Order

**File:** `client.py`
```python
response = requests.post(f"{BASE_URL}/order", json={
    "customer_name": "Alice",
    "coffee_type": "Latte"
})
```

**What happens:**
1. Client sends HTTP POST request to `/api/v1/cafe/order`
2. Request includes JSON with customer name and coffee type

### Step 2: FastAPI Receives Request

**File:** `endpoint.py` → `place_order()`
```python
@cafe_router.post("/order")
async def place_order(order: OrderSchema):
    order_id = str(uuid.uuid4())
    task = make_coffee.delay(order_id, order.coffee_type, order.customer_name)
    return OrderResponse(...)
```

**What happens:**
1. FastAPI receives the request
2. Pydantic validates the data against `OrderSchema`
3. Generates a unique `order_id` (UUID)
4. Calls `make_coffee.delay()` - **This returns IMMEDIATELY!**
5. Returns response with `task_id` to the client

**Key Point:** The function returns in **milliseconds**, not waiting for coffee to be made!

### Step 3: Task is Queued

**What happens:**
1. `.delay()` sends the task to Redis (broker)
2. Task is added to the queue
3. Task gets a unique `task_id`
4. Task status is **PENDING**

### Step 4: Worker Picks Up Task

**File:** `worker.py` → `make_coffee()`

**What happens:**
1. Celery worker (running in separate process) sees the task
2. Worker picks up the task from Redis
3. Task status changes to **STARTED**
4. Worker begins executing `make_coffee()` function

### Step 5: Coffee Making Process

**File:** `worker.py`
```python
# Step 1: Grinding Beans
self.update_state(state="GRINDING", meta={"progress": "30%"})
time.sleep(random.uniform(2, 4))

# Step 2: Brewing
self.update_state(state="BREWING", meta={"progress": "60%"})
time.sleep(random.uniform(3, 6))

# Step 3: Pouring Milk
self.update_state(state="POURING", meta={"progress": "90%"})
time.sleep(random.uniform(1, 2))

return f"{coffee_type} for {customer_name} is served!"
```

**What happens:**
1. Worker updates state to **GRINDING** (30% progress)
2. Simulates work with `time.sleep()`
3. Updates state to **BREWING** (60% progress)
4. More simulated work
5. Updates state to **POURING** (90% progress)
6. Final simulated work
7. Returns the result string

**Key Point:** Each `update_state()` call:
- Updates the task status in Redis
- Stores metadata (like progress percentage)
- Can be retrieved by the client checking status

### Step 6: Result is Stored

**What happens:**
1. Worker finishes executing
2. Return value is stored in Redis (backend)
3. Task status changes to **SUCCESS**
4. Result is available for retrieval

### Step 7: Client Checks Status

**File:** `client.py`
```python
while status not in ["SUCCESS", "FAILURE"]:
    time.sleep(random.uniform(1.5, 3))
    r = requests.get(f"{BASE_URL}/status/{task_id}")
    status = r.json()["status"]
```

**What happens:**
1. Client polls the status endpoint every 1.5-3 seconds
2. Sends GET request to `/api/v1/cafe/status/{task_id}`

### Step 8: FastAPI Returns Status

**File:** `endpoint.py` → `get_status()`
```python
@cafe_router.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    # ... check status and return ...
```

**What happens:**
1. FastAPI receives the status request
2. Creates `AsyncResult` object with the `task_id`
3. Checks the task status from Redis
4. Returns current status and progress (if in progress)
5. Returns result (if completed)

### Step 9: Client Receives Final Result

**What happens:**
1. When status is **SUCCESS**, client receives the result
2. Displays: `"[Alice] 😋 RECEIVED: Latte for Alice is served!"`
3. Loop exits

---

## File-by-File Breakdown

### `main.py` - Application Entry Point

**Purpose:** Creates and configures the FastAPI application.

**Key Components:**
- `FastAPI()` - Creates the main app instance
- `app.include_router()` - Connects routers to the app
- Health check endpoint (`/`) - Simple endpoint to verify server is running

**Why it exists:**
- Central place to configure the application
- Entry point for running the server (`uvicorn main:app`)
- Can add middleware, exception handlers, etc. here

### `router.py` - Master Router

**Purpose:** Organizes and groups related routes.

**Key Components:**
- `APIRouter()` - Creates a router instance
- `include_router()` - Includes sub-routers with prefixes and tags

**Why it exists:**
- **Modularity:** Keeps routes organized
- **Scalability:** Easy to add new feature routers
- **API Versioning:** Can have `/api/v1/`, `/api/v2/`, etc.
- **Documentation:** Tags group endpoints in Swagger UI

**Structure:**
```
api_router (master)
  └── cafe_router (feature router)
      ├── /order (POST)
      └── /status/{task_id} (GET)
```

### `endpoint.py` - API Endpoints

**Purpose:** Defines the HTTP endpoints that clients interact with.

**Endpoints:**

#### 1. `POST /order`
- **Input:** `OrderSchema` (customer_name, coffee_type)
- **Action:** Creates a Celery task
- **Output:** `OrderResponse` (order_id, task_id, message, status_url)
- **Key:** Returns immediately, doesn't wait for coffee

#### 2. `GET /status/{task_id}`
- **Input:** `task_id` (from URL path)
- **Action:** Queries Celery for task status
- **Output:** Status, result (if ready), progress (if in progress)
- **Key:** Can be called repeatedly to poll for updates

**Why separate file:**
- Keeps business logic separate from routing
- Easy to test endpoints independently
- Clear separation of concerns

### `worker.py` - Celery Tasks

**Purpose:** Defines the actual work that happens in the background.

**Key Components:**

#### 1. Celery App Configuration
```python
celery_app = Celery(
    "cafe_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)
```
- **Name:** "cafe_worker" (identifies this Celery app)
- **Broker:** Where tasks are queued (Redis)
- **Backend:** Where results are stored (Redis)

#### 2. Celery Configuration
```python
celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    # ...
)
```
- **task_track_started:** Track when task starts (not just PENDING)
- **Serializers:** How to encode/decode task data (JSON)

#### 3. Task Definition
```python
@celery_app.task(bind=True)
def make_coffee(self, order_id, coffee_type, customer_name):
    # Task logic here
```

**Why `bind=True`:**
- Gives access to `self` (task instance)
- Can call `self.update_state()` to update progress
- Can call `self.retry()` to retry on failure

**Task Flow:**
1. Update state to GRINDING (30%)
2. Simulate grinding (2-4 seconds)
3. Update state to BREWING (60%)
4. Simulate brewing (3-6 seconds)
5. Update state to POURING (90%)
6. Simulate pouring (1-2 seconds)
7. Return result

**Error Handling:**
- Wrapped in try/except
- Logs errors
- Re-raises exception to mark task as FAILURE

### `schemas.py` - Data Models

**Purpose:** Defines the structure and validation for data.

**Schemas:**

#### 1. `OrderSchema`
```python
class OrderSchema(BaseModel):
    customer_name: str
    coffee_type: str
```
- **Purpose:** Validates incoming order data
- **Used in:** `POST /order` endpoint
- **Benefits:** 
  - Automatic validation
  - Type checking
  - Clear error messages if invalid

#### 2. `OrderResponse`
```python
class OrderResponse(BaseModel):
    order_id: str
    task_id: str
    message: str
    status_url: str
```
- **Purpose:** Defines the structure of API responses
- **Used in:** `POST /order` endpoint response
- **Benefits:**
  - Consistent response format
  - Automatic API documentation
  - Type safety

**Why Pydantic:**
- Runtime validation (catches errors early)
- Automatic conversion (e.g., string to int if needed)
- Great error messages
- Works seamlessly with FastAPI

### `config.py` - Configuration Management

**Purpose:** Centralizes configuration and utility functions.

**Functions:**

#### 1. `get_redis_url()`
```python
def get_redis_url() -> str:
    url = os.getenv("REDIS_URL")
    if not url:
        raise ValueError("REDIS_URL not found!")
    return url
```
- **Purpose:** Gets Redis URL from environment variables
- **Why:** 
  - Security (don't hardcode credentials)
  - Flexibility (different URLs for dev/prod)
  - Best practice (12-factor app methodology)

#### 2. `setup_logger()`
```python
def setup_logger(name: str, log_file: str = "logs/app.log"):
    # Sets up logging with console and file handlers
```
- **Purpose:** Configures logging for the application
- **Features:**
  - Console output (INFO level)
  - File output (DEBUG level)
  - Different formats for each
  - Creates log directory if needed

**Why separate file:**
- Single source of truth for configuration
- Easy to change settings
- Reusable across modules

### `client.py` - Test Client

**Purpose:** Simulates multiple customers placing orders simultaneously.

**Key Components:**

#### 1. `simulate_customer()`
- Places an order via HTTP POST
- Polls status endpoint until complete
- Displays progress updates
- Shows final result

#### 2. `ThreadPoolExecutor`
```python
with ThreadPoolExecutor(max_workers=5) as executor:
    for name, coffee in customers:
        executor.submit(simulate_customer, name, coffee)
```
- **Purpose:** Runs multiple customers concurrently
- **Why:** Tests that the system can handle multiple simultaneous requests
- **Result:** All 5 customers place orders at roughly the same time

**Why it exists:**
- Demonstrates the async nature of the system
- Tests the application
- Shows real-world usage pattern (polling for status)

---

## How to Run the Project

### Prerequisites

1. **Python 3.8+** installed
2. **Redis** running (message broker and result backend)
3. **Dependencies** installed (celery, fastapi, redis, etc.)

### Step-by-Step Setup

#### 1. Install Dependencies

```bash
# Using pip
pip install celery fastapi uvicorn redis python-dotenv pydantic requests

# Or using uv (if you have a pyproject.toml)
uv sync
```

#### 2. Start Redis

**Option A: Docker (Recommended)**
```bash
docker run -d -p 6379:6379 redis:latest
```

**Option B: Local Installation**
```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Windows (using WSL or Docker)
# Use Docker option above
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

#### 3. Set Environment Variables

Create a `.env` file in the project directory:
```env
REDIS_URL=redis://localhost:6379/0
```

Or export it:
```bash
# Linux/macOS
export REDIS_URL=redis://localhost:6379/0

# Windows PowerShell
$env:REDIS_URL="redis://localhost:6379/0"
```

#### 4. Start the Celery Worker

**Open Terminal 1:**
```bash
cd "STEP2_Build Production-Ready AI Backends/celery_cafe"
celery -A worker worker --loglevel=info
```

**Expected output:**
```
[tasks]
  . worker.make_coffee

[INFO/MainProcess] Connected to redis://localhost:6379/0
[INFO/MainProcess] celery@your-machine ready.
```

**Keep this terminal open!** The worker must be running to process tasks.

#### 5. Start the FastAPI Server

**Open Terminal 2:**
```bash
cd "STEP2_Build Production-Ready AI Backends/celery_cafe"
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### 6. Run the Client

**Open Terminal 3:**
```bash
cd "STEP2_Build Production-Ready AI Backends/celery_cafe"
python client.py
```

**Expected output:**
```
[Alice] 🚶 Entering cafe...
[Bob] 🚶 Entering cafe...
[Alice] 🎫 Order placed! Ticket: abc12...
[Bob] 🎫 Order placed! Ticket: def34...
[Alice] 🗣️  Status: GRINDING 30%
[Bob] 🗣️  Status: PENDING
[Alice] 🗣️  Status: BREWING 60%
[Bob] 🗣️  Status: GRINDING 30%
...
[Alice] 😋 RECEIVED: Latte for Alice is served!
[Bob] 😋 RECEIVED: Espresso for Bob is served!
```

### Troubleshooting

#### Problem: "Connection refused to Redis"
**Solution:** Make sure Redis is running. Check with `redis-cli ping`

#### Problem: "No module named 'worker'"
**Solution:** Make sure you're in the `celery_cafe` directory when running Celery

#### Problem: Tasks are queued but not executing
**Solution:** 
- Check that the Celery worker is running
- Check worker logs for errors
- Verify task name matches: `celery -A worker inspect registered`

#### Problem: "REDIS_URL not found!"
**Solution:** Set the `REDIS_URL` environment variable or create a `.env` file

---

## When to Use This Pattern

### ✅ Use This Pattern When:

1. **Tasks take longer than 500ms**
   - Image processing
   - File uploads/downloads
   - Database migrations
   - Report generation

2. **Tasks are resource-intensive**
   - Machine learning model inference
   - Video encoding
   - Large data processing
   - Complex calculations

3. **Tasks are unreliable**
   - External API calls (might fail)
   - Network operations
   - File system operations
   - Database operations that might timeout

4. **You need progress tracking**
   - Long-running operations
   - Multi-step processes
   - User-facing progress bars

5. **You need to scale horizontally**
   - Add more workers to handle more load
   - Distribute work across multiple machines
   - Handle traffic spikes

6. **You need task scheduling**
   - Periodic tasks (cron jobs)
   - Delayed execution
   - Task dependencies

### ❌ Don't Use This Pattern When:

1. **Tasks are very fast (< 100ms)**
   - Simple database queries
   - Basic calculations
   - Simple data transformations

2. **You need immediate results**
   - Real-time chat
   - Live updates
   - Synchronous operations

3. **Simple CRUD operations**
   - Creating a user
   - Updating a record
   - Simple API calls

4. **Low traffic applications**
   - Personal projects
   - Prototypes
   - Internal tools with few users

### Real-World Examples

| Use Case | Time | Why Use Celery? |
|----------|------|-----------------|
| Generating images with AI | 5-30s | Too slow for web request |
| Sending email notifications | 1-3s | External API, can fail |
| Processing uploaded videos | Minutes | Resource-intensive |
| Batch processing 10,000 records | Variable | Parallel processing needed |
| PDF generation and OCR | 5-15s | CPU-intensive |
| RAG (Retrieval-Augmented Generation) | 10-30s | Multiple API calls, vector search |
| Data analysis and reporting | Minutes | Long-running process |

---

## Common Patterns and Extensions

### Pattern 1: Task Retries

Add automatic retries for unreliable tasks:

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def make_coffee(self, order_id, coffee_type, customer_name):
    try:
        # ... coffee making logic ...
    except ExternalAPIError as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
```

### Pattern 2: Task Timeouts

Set time limits for tasks:

```python
@celery_app.task(bind=True, time_limit=300)  # 5 minutes
def make_coffee(self, order_id, coffee_type, customer_name):
    # ... task logic ...
```

### Pattern 3: Task Priorities

Use different queues for different priorities:

```python
# High priority
@celery_app.task(queue='high_priority')
def urgent_task(data):
    pass

# Low priority
@celery_app.task(queue='low_priority')
def background_task(data):
    pass

# Start workers for specific queues
# celery -A worker worker -Q high_priority,low_priority
```

### Pattern 4: Scheduled Tasks (Cron Jobs)

Run tasks on a schedule:

```python
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'daily-report': {
        'task': 'worker.generate_daily_report',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9 AM
    },
}

# Start the beat scheduler
# celery -A worker beat --loglevel=info
```

### Pattern 5: Task Chaining

Chain tasks together (Task A → Task B → Task C):

```python
from celery import chain

workflow = chain(
    step1.s(data),
    step2.s(),
    step3.s()
)
result = workflow.apply_async()
```

### Pattern 6: Task Groups

Process multiple items in parallel:

```python
from celery import group

job = group(
    process_item.s(item) for item in items
)
result = job.apply_async()
results = result.get()  # Wait for all to complete
```

### Pattern 7: Webhooks Instead of Polling

Instead of polling, use webhooks to notify when done:

```python
@celery_app.task(bind=True)
def make_coffee(self, order_id, coffee_type, customer_name, webhook_url):
    # ... make coffee ...
    result = f"{coffee_type} for {customer_name} is served!"
    
    # Notify via webhook
    requests.post(webhook_url, json={
        "status": "completed",
        "result": result
    })
    
    return result
```

### Pattern 8: Result Expiration

Don't store results forever:

```python
task = make_coffee.apply_async(
    args=[order_id, coffee_type, customer_name],
    expires=3600  # Result expires after 1 hour
)
```

---

## Summary

This project demonstrates a **production-ready pattern** for building scalable, non-blocking web applications:

### Key Takeaways:

1. **Separation of Concerns:**
   - Web server handles requests quickly
   - Workers handle heavy processing
   - Message queue connects them

2. **Scalability:**
   - Add more workers to handle more load
   - Workers can run on different machines
   - System handles traffic spikes gracefully

3. **User Experience:**
   - Fast response times
   - Progress tracking
   - Non-blocking operations

4. **Reliability:**
   - Tasks survive server restarts
   - Retry mechanisms
   - Error handling

5. **Flexibility:**
   - Task scheduling
   - Task prioritization
   - Task chaining

### Next Steps:

1. **Add monitoring:** Use Flower (`pip install flower`) to monitor workers
2. **Add authentication:** Secure your endpoints
3. **Add rate limiting:** Prevent abuse
4. **Add logging:** Better error tracking
5. **Add tests:** Unit tests and integration tests
6. **Deploy:** Use Docker, Kubernetes, or cloud services

---

## Additional Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Happy Coding! ☕🚀**

