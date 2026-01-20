# 🚀 Professional Backend Setup Guide: FastAPI + Celery + Redis + Docker

**A Senior Developer's Guide for Building Production-Ready Asynchronous Systems**

---

## 📋 Table of Contents

1. [The Big Picture](#the-big-picture)
2. [Core Concepts](#core-concepts)
3. [Architecture Overview](#architecture-overview)
4. [Project Structure](#project-structure)
5. [Step-by-Step Setup](#step-by-step-setup)
6. [How Everything Connects](#how-everything-connects)
7. [Queue Routing & Task Management](#queue-routing--task-management)
8. [Key Patterns & Best Practices](#key-patterns--best-practices)
9. [Common Pitfalls & Solutions](#common-pitfalls--solutions)
10. [Quick Reference](#quick-reference)

---

## 🎯 The Big Picture

### Why This Architecture?

In a professional system, we **separate talking from doing**:

- **FastAPI (The API)**: Talks to users. Must stay fast and responsive.
- **Celery (The Workers)**: Does heavy lifting (emails, processing, reports).
- **Redis (The Broker)**: Carries messages between them.

**The Problem We Solve:**
- User sends request → API must respond in <200ms
- But email sending takes 2-5 seconds
- Solution: Queue the work, return immediately, process in background

### The Mental Model

Think of a restaurant:
- **FastAPI** = Waiter (takes orders, serves food)
- **Celery Worker** = Chef (cooks in kitchen)
- **Redis** = Order board (where orders are posted)
- **Task ID** = Order number (customer tracks their order)

---

## 🧠 Core Concepts

### 1. **Background Tasks**

Any operation that takes >500ms should be a background task:
- ✅ Sending emails
- ✅ Processing files
- ✅ Generating reports
- ✅ Image/video processing
- ✅ API calls to external services

**Rule of Thumb:** If user would notice the delay, make it async.

### 2. **Message Broker (Redis)**

Redis acts as the "post office":
- Stores tasks in queues (lists)
- Workers poll Redis for new tasks
- Results stored in Redis for retrieval
- Pub/Sub for real-time notifications

**Why Redis?**
- Sub-millisecond latency (in-memory)
- Supports lists (queues), pub/sub, and persistence
- Simple to set up and scale

### 3. **Task Queue (Celery)**

Celery manages task execution:
- **Producer**: FastAPI creates tasks
- **Broker**: Redis holds tasks
- **Worker**: Separate process executes tasks
- **Backend**: Redis stores results

**Key States:**
- `PENDING`: Task queued, not started
- `STARTED`: Task running
- `SUCCESS`: Task completed
- `FAILURE`: Task failed
- `PROGRESS`: Custom state with metadata

### 4. **Docker & Containerization**

Each service runs in its own container:
- **Redis**: Message broker + result storage
- **FastAPI**: API server
- **Celery Worker**: Task executor
- **Flower**: Monitoring dashboard

**Benefits:**
- Isolated environments
- Easy scaling (add more workers)
- Consistent across dev/staging/prod

---

## 🏗️ Architecture Overview

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT REQUEST                            │
│              POST /api/v1/email/send                        │
│              {"to": "user@example.com", ...}                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI (Producer/Waiter)                      │
│  1. Validates request (Pydantic schemas)                    │
│  2. Creates Celery task: task.delay(...)                  │
│  3. Returns immediately: {"task_id": "abc-123"}           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Task JSON
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              REDIS (Message Broker)                          │
│  Queue: celery (default)                                    │
│  [Task1, Task2, Task3, ...]                                │
│                                                              │
│  Structure:                                                  │
│  - Lists: Task queues                                       │
│  - Hashes: Task metadata                                    │
│  - Strings: Task results                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Worker polls
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          CELERY WORKER (Consumer/Chef)                     │
│  1. Polls Redis for tasks                                   │
│  2. Executes task function                                  │
│  3. Updates state: PENDING → STARTED → SUCCESS              │
│  4. Stores result in Redis                                  │
│  5. (Optional) Publishes to Redis pub/sub                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Result stored
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         REDIS (Result Backend)                               │
│  Key: celery-task-meta-{task_id}                           │
│  Value: {"status": "SUCCESS", "result": {...}}             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Status check / WebSocket
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT                                   │
│  Method 1: Polling                                          │
│    GET /api/v1/email/status/{task_id}                      │
│                                                              │
│  Method 2: WebSocket (Real-time)                            │
│    WS /api/v1/websocket/ws/{task_id}                       │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Role | What It Does |
|-----------|------|--------------|
| **FastAPI** | API Server | Receives HTTP requests, validates data, queues tasks, returns responses |
| **Celery** | Task Queue | Manages task execution, retries, scheduling |
| **Redis** | Broker + Backend | Stores tasks, results, enables pub/sub |
| **Worker** | Task Executor | Runs tasks in background processes |
| **Flower** | Monitor | Web UI for monitoring tasks and workers |

---

## 📁 Project Structure

### Standard Layout (Why Each Folder Exists)

```
fastapi_celery_redis_template/
├── app/
│   ├── __init__.py              # Makes 'app' a Python package
│   ├── main.py                   # FastAPI app entry point
│   ├── config.py                 # Configuration (singleton pattern)
│   │
│   ├── core/                     # Core infrastructure
│   │   ├── celery_app.py         # Celery initialization & config
│   │   └── redis_client.py       # Redis clients (sync + async)
│   │
│   ├── api/                      # API layer
│   │   ├── deps.py               # Shared dependencies (FastAPI DI)
│   │   └── v1/                   # API version 1
│   │       ├── router.py         # Main router (includes all features)
│   │       ├── email.py          # Email endpoints
│   │       ├── progress.py       # Progress tracking endpoints
│   │       ├── websocket.py      # WebSocket endpoints
│   │       └── queue.py          # Queue management endpoints
│   │
│   ├── tasks/                    # Background tasks (Celery)
│   │   ├── email_tasks.py        # Email sending tasks
│   │   ├── progress_tasks.py     # Long-running tasks with progress
│   │   ├── websocket_tasks.py    # Tasks that publish to Redis
│   │   └── queue_tasks.py        # Queue processing tasks
│   │
│   ├── schemas/                  # Pydantic models (validation)
│   │   ├── email.py              # Email request/response schemas
│   │   ├── progress.py           # Progress schemas
│   │   ├── websocket.py          # WebSocket schemas
│   │   └── queue.py              # Queue schemas
│   │
│   └── utils/                    # Utility functions
│       └── queue_manager.py      # Direct Redis queue operations
│
├── worker.py                     # Celery worker entry point
├── docker-compose.yml            # Multi-container orchestration
├── Dockerfile                    # Application container definition
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project metadata
└── .env.example                  # Environment variables template
```

### Folder Roles Explained

| Folder | Purpose | Analogy |
|--------|---------|---------|
| `app/core/` | Infrastructure setup | Engine room - powers everything |
| `app/api/` | HTTP endpoints | Restaurant floor - where customers interact |
| `app/tasks/` | Background work | Kitchen - where heavy work happens |
| `app/schemas/` | Data validation | Contracts - ensures data is correct |
| `app/utils/` | Helper functions | Tools - reusable utilities |

---

## 🛠️ Step-by-Step Setup

### Step 1: Project Initialization

```bash
# Create project directory
mkdir my_backend_project
cd my_backend_project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn celery redis python-dotenv flower pydantic
```

**Why:** Virtual environment isolates dependencies. Each project has its own packages.

### Step 2: Create Project Structure

```bash
# Create folder structure
mkdir -p app/{core,api/v1,tasks,schemas,utils}
touch app/__init__.py
touch app/core/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/tasks/__init__.py
touch app/schemas/__init__.py
touch app/utils/__init__.py
```

**Why:** `__init__.py` files make directories into Python packages, enabling imports.

### Step 3: Configuration (`app/config.py`)

```python
"""Centralized configuration management"""
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
    
    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "My Backend")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    @classmethod
    def get_redis_url(cls) -> str:
        return cls.REDIS_URL

# Singleton instance - import this everywhere
settings = Settings()
```

**Key Points:**
- Environment variables for different environments (dev/staging/prod)
- Sensible defaults for local development
- Singleton pattern: one instance shared across app
- Class methods for abstraction (can add validation later)

### Step 4: Redis Client (`app/core/redis_client.py`)

```python
"""Redis clients for sync and async operations"""
import redis
import redis.asyncio as aioredis
from app.config import settings

# Sync client (for Celery tasks)
def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(
        settings.get_redis_url(),
        decode_responses=False  # Bytes for Celery
    )

# Async client (for FastAPI/WebSocket) - singleton pattern
_async_redis_client = None

async def get_async_redis_client() -> aioredis.Redis:
    global _async_redis_client
    if _async_redis_client is None:
        _async_redis_client = aioredis.from_url(
            settings.get_redis_url(),
            decode_responses=True  # Strings for async
        )
    return _async_redis_client
```

**Why Two Clients?**
- **Sync**: Celery workers run synchronously → need sync Redis client
- **Async**: FastAPI/WebSocket are async → need async Redis client
- **Different encoding**: Celery expects bytes, FastAPI prefers strings

### Step 5: Celery App (`app/core/celery_app.py`)

```python
"""Celery application initialization"""
from celery import Celery
from app.config import settings

# Initialize Celery
celery_app = Celery(
    "my_app",
    broker=settings.get_celery_broker_url(),      # Where tasks are queued
    backend=settings.get_celery_backend_url()    # Where results are stored
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',           # Serialize tasks as JSON
    accept_content=['json'],          # Security: only accept JSON
    result_serializer='json',         # Serialize results as JSON
    timezone='UTC',
    task_track_started=True,         # Track STARTED state
    task_time_limit=1800,            # Hard limit: 30 minutes
    task_soft_time_limit=1500,       # Soft limit: 25 minutes
    worker_prefetch_multiplier=1,    # Fair distribution
    worker_max_tasks_per_child=1000, # Prevent memory leaks
    result_expires=3600,             # Results expire after 1 hour
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['app.tasks'])
```

**Key Settings Explained:**
- `task_serializer='json'`: Human-readable, language-agnostic
- `task_track_started=True`: Enables STARTED state (better monitoring)
- `worker_prefetch_multiplier=1`: Each worker takes one task (fair distribution)
- `worker_max_tasks_per_child=1000`: Restart worker after 1000 tasks (prevents memory leaks)

### Step 6: Create Your First Task (`app/tasks/email_tasks.py`)

```python
"""Email tasks"""
from app.core.celery_app import celery_app
import time

@celery_app.task(bind=True, max_retries=3)
def send_email(self, to: str, subject: str, body: str) -> str:
    """
    Send email task
    
    Args:
        self: Task instance (needed when bind=True)
        to: Recipient email
        subject: Email subject
        body: Email body
        
    Returns:
        Success message
    """
    try:
        # Simulate email sending
        time.sleep(2)
        print(f"Email sent to {to}")
        return f"Email sent successfully to {to}"
        
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60)
```

**Key Points:**
- `@celery_app.task`: Decorator makes function a Celery task
- `bind=True`: Allows access to `self` for retries and state updates
- `max_retries=3`: Automatically retry up to 3 times on failure
- `self.retry()`: Retry the task with exponential backoff

### Step 7: Create API Endpoint (`app/api/v1/email.py`)

```python
"""Email API endpoints"""
from fastapi import APIRouter
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.tasks.email_tasks import send_email
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/email", tags=["Email"])

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str

class EmailResponse(BaseModel):
    task_id: str
    status: str
    message: str

@router.post("/send", response_model=EmailResponse)
async def trigger_send_email(email: EmailRequest):
    """Trigger email sending task"""
    # Queue task - returns immediately
    task = send_email.delay(email.to, email.subject, email.body)
    
    return EmailResponse(
        task_id=task.id,
        status="PENDING",
        message="Email queued for sending"
    )

@router.get("/status/{task_id}")
async def check_status(task_id: str):
    """Check task status"""
    result = AsyncResult(task_id, app=celery_app)
    
    if result.ready():
        if result.successful():
            return {"status": "SUCCESS", "result": result.get()}
        else:
            return {"status": "FAILURE", "error": str(result.info)}
    else:
        return {"status": result.state, "message": "Processing..."}
```

**Key Points:**
- `.delay()`: Queues task, returns immediately (non-blocking)
- `AsyncResult`: Checks task status without executing it
- `result.ready()`: True if task completed (success or failure)
- `result.get()`: Returns task result (only if successful)

### Step 8: FastAPI App (`app/main.py`)

```python
"""FastAPI application"""
from fastapi import FastAPI
from app.api.v1.router import router
from app.core.redis_client import close_async_redis_client
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("Starting application...")
    yield
    # Shutdown
    print("Shutting down...")
    await close_async_redis_client()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Key Points:**
- `lifespan`: Handles startup/shutdown (cleanup connections)
- `include_router`: Adds all API endpoints
- Health check for monitoring

### Step 9: Worker Entry Point (`worker.py`)

```python
"""Celery worker entry point"""
from app.core.celery_app import celery_app

# Usage: celery -A worker worker --loglevel=info
```

**Why:** Simple entry point for running workers. Celery needs to know which app to use.

### Step 10: Docker Setup

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  worker:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    command: celery -A worker worker --loglevel=info

  flower:
    build: .
    ports:
      - "5555:5555"
    command: celery -A worker flower --port=5555
    depends_on:
      - redis
      - worker

volumes:
  redis_data:
```

**Key Points:**
- Each service in its own container
- `depends_on`: Ensures Redis starts first
- Shared network: Containers communicate via service names
- Volumes: Persist Redis data

---

## 🔗 How Everything Connects

### Connection Flow

1. **FastAPI → Celery**
   ```python
   # In endpoint
   task = send_email.delay(...)  # Creates task
   # Internally: Serializes task → Sends to Redis broker
   ```

2. **Redis → Worker**
   ```python
   # Worker continuously polls Redis
   # When task found: Deserializes → Executes function
   ```

3. **Worker → Redis**
   ```python
   # After execution
   # Stores result in Redis backend
   # Updates state: PENDING → STARTED → SUCCESS
   ```

4. **FastAPI ← Redis**
   ```python
   # Status check
   result = AsyncResult(task_id, app=celery_app)
   # Reads from Redis backend
   ```

### Import Chain

```
main.py
  └── imports router from app.api.v1.router
      └── router imports email, progress, websocket, queue
          └── email.py imports celery_app and tasks
              └── celery_app imports settings
                  └── settings loads from .env
```

### Data Flow Example

**Scenario: Send Email**

```
1. Client → POST /api/v1/email/send
   {"to": "user@example.com", "subject": "Hello", "body": "Test"}

2. FastAPI validates → EmailRequest schema

3. FastAPI creates task:
   task = send_email.delay("user@example.com", "Hello", "Test")
   
4. Celery serializes task → JSON:
   {
     "id": "abc-123",
     "task": "app.tasks.email_tasks.send_email",
     "args": ["user@example.com", "Hello", "Test"]
   }

5. Redis stores task in queue (list):
   LPUSH celery <task_json>

6. FastAPI returns immediately:
   {"task_id": "abc-123", "status": "PENDING"}

7. Worker polls Redis:
   BRPOP celery → Gets task_json

8. Worker executes:
   send_email("user@example.com", "Hello", "Test")

9. Worker stores result in Redis:
   SET celery-task-meta-abc-123 {"status": "SUCCESS", "result": "..."}

10. Client checks status:
    GET /api/v1/email/status/abc-123
    
11. FastAPI reads from Redis:
    AsyncResult("abc-123") → Returns result
```

---

## 🎯 Queue Routing & Task Management

### Why Use Multiple Queues?

In production, you need to prioritize tasks and separate them by type:

- **High Priority**: Payment processing, critical notifications
- **Low Priority**: Analytics, logging, reports
- **Fast Tasks**: Quick operations (<1 second)
- **Slow Tasks**: Heavy processing (minutes/hours)

**The Problem:** Without queues, a slow task can block fast tasks.

**The Solution:** Separate queues + dedicated workers for each queue.

### Default Queue vs Custom Queues

**Default Queue (`celery`):**
- All tasks go here if no queue specified
- Simple setup, works for small projects
- Problem: Everything competes for same workers

**Custom Queues:**
- Separate queues for different task types
- Dedicated workers per queue
- Better resource management and prioritization

### Setting Up Queues

There are three ways to assign tasks to queues:

#### Method 1: Task Decorator (Simplest)

**Assign queue directly in task definition:**

```python
# app/tasks/email_tasks.py
from app.core.celery_app import celery_app

@celery_app.task(queue='emails')
def send_email(to: str, subject: str, body: str):
    # Task automatically goes to 'emails' queue
    pass

@celery_app.task(queue='high_priority', bind=True)
def process_payment(self, payment_id: str):
    # Task automatically goes to 'high_priority' queue
    pass
```

**Usage:**
```python
# Task goes to 'emails' queue automatically
task = send_email.delay("user@example.com", "Hello", "Body")
```

**Pros:** Simple, clear, task-level control
**Cons:** Queue hardcoded in task definition

#### Method 2: Configure Task Routes (Centralized Routing)

**In `app/core/celery_app.py`:**

```python
celery_app.conf.update(
    # ... other config ...
    
    # Task routing: Automatically route tasks to queues
    task_routes={
        'app.tasks.email_tasks.send_email': {'queue': 'emails'},
        'app.tasks.progress_tasks.process_file': {'queue': 'processing'},
        'app.tasks.websocket_tasks.generate_report': {'queue': 'reports'},
    },
    
    # Default queue for tasks without route
    task_default_queue='default',
)
```

**How It Works:**
- When you call `send_email.delay(...)`, Celery automatically routes it to `emails` queue
- No need to specify queue in code
- Centralized configuration

**Example:**
```python
# Task automatically goes to 'emails' queue
task = send_email.delay("user@example.com", "Hello", "Body")
```

#### Method 3: Manual Queue Assignment (apply_async)

**Using `apply_async()` for explicit queue control:**

```python
# Basic usage - same as .delay()
task = send_email.apply_async(args=["user@example.com", "Hello", "Body"])

# Specify queue explicitly
task = send_email.apply_async(
    args=["user@example.com", "Hello", "Body"],
    queue='high_priority'  # Send to specific queue
)

# Advanced options
task = send_email.apply_async(
    args=["user@example.com", "Hello", "Body"],
    queue='emails',                    # Queue name
    priority=9,                         # Higher priority (0-9)
    countdown=60,                      # Execute after 60 seconds
    eta=datetime.now() + timedelta(minutes=5),  # Execute at specific time
    expires=3600,                      # Task expires after 1 hour
    retry=True,                        # Enable retries
    max_retries=3,                     # Max retry attempts
)
```

**When to Use `apply_async()`:**
- Need to specify queue dynamically (based on user input, etc.)
- Need advanced options (priority, ETA, expiration)
- Want to override default routing

**When to Use `.delay()`:**
- Simple task execution
- Default queue is fine
- No special requirements

### Starting Workers for Specific Queues

**Single Queue Worker:**
```bash
# Worker only processes 'emails' queue
celery -A worker worker --loglevel=info --queues=emails

# Worker only processes 'high_priority' queue
celery -A worker worker --loglevel=info --queues=high_priority
```

**Multiple Queue Worker:**
```bash
# Worker processes multiple queues (in order of priority)
celery -A worker worker --loglevel=info --queues=high_priority,emails,default
```

**All Queues Worker:**
```bash
# Worker processes all queues (default behavior)
celery -A worker worker --loglevel=info
```

**Docker Compose Example:**
```yaml
services:
  worker_high_priority:
    build: .
    command: celery -A worker worker --queues=high_priority --concurrency=2
    environment:
      - REDIS_URL=redis://redis:6379/0
  
  worker_emails:
    build: .
    command: celery -A worker worker --queues=emails --concurrency=4
    environment:
      - REDIS_URL=redis://redis:6379/0
  
  worker_default:
    build: .
    command: celery -A worker worker --queues=default --concurrency=8
    environment:
      - REDIS_URL=redis://redis:6379/0
```

### Complete Queue Setup Example

**Step 1: Define Tasks with Queue Assignment**

You can use any of the three methods:

```python
# Method 1: Decorator (recommended for most cases)
# app/tasks/email_tasks.py
@celery_app.task(queue='emails')
def send_email(to: str, subject: str, body: str):
    pass

# Method 2: Task routes (in celery_app.py)
# No queue in decorator - routing handles it

# Method 3: apply_async (in endpoint)
# Override queue dynamically
```

**Step 2: Configure Celery**

```python
# app/core/celery_app.py
celery_app.conf.update(
    # ... other config ...
    
    # Task routing (optional - can also use @celery_app.task(queue='...'))
    task_routes={
        'app.tasks.payment_tasks.*': {'queue': 'high_priority'},
    },
    
    # Default queue
    task_default_queue='default',
    
    # Queue priorities (higher number = higher priority)
    task_default_priority=5,
)
```

**Step 3: Start Workers**

```bash
# Terminal 1: High priority worker (2 processes)
celery -A worker worker --queues=high_priority --concurrency=2

# Terminal 2: Email worker (4 processes)
celery -A worker worker --queues=emails --concurrency=4

# Terminal 3: Report worker (1 process - slow tasks)
celery -A worker worker --queues=reports --concurrency=1

# Terminal 4: Default queue worker
celery -A worker worker --queues=default --concurrency=4
```

**Step 4: Use in Endpoints**

```python
# app/api/v1/payments.py
@router.post("/process-payment")
async def process_payment(payment: PaymentRequest):
    # Goes to 'high_priority' queue automatically (from task decorator)
    task = process_payment_task.delay(payment.id)
    return {"task_id": task.id}

# app/api/v1/emails.py
@router.post("/send-email")
async def send_email(email: EmailRequest):
    # Option 1: Use default routing (from task decorator)
    task = send_email_task.delay(email.to, email.subject, email.body)
    
    # Option 2: Override queue dynamically
    if email.priority == "high":
        task = send_email_task.apply_async(
            args=[email.to, email.subject, email.body],
            queue='high_priority'
        )
    else:
        task = send_email_task.delay(email.to, email.subject, email.body)
    
    return {"task_id": task.id}
```

### Queue Priority System

**Priority Levels (0-9):**
- `0`: Lowest priority
- `5`: Default priority
- `9`: Highest priority

**How It Works:**
- Tasks with higher priority are processed first
- Within same priority, FIFO (first in, first out)
- Workers process highest priority tasks first

**Example:**
```python
# High priority task
task = process_payment.apply_async(
    args=[payment_id],
    queue='payments',
    priority=9
)

# Low priority task
task = send_newsletter.apply_async(
    args=[user_id],
    queue='emails',
    priority=1
)
```

### Monitoring Queues

**Check Queue Lengths:**
```bash
# Using Redis CLI
redis-cli LLEN celery:emails
redis-cli LLEN celery:high_priority

# Using Celery
celery -A worker inspect active_queues
```

**Using Flower:**
- Access Flower dashboard: http://localhost:5555
- View queue lengths and task distribution
- Monitor worker activity per queue

### Best Practices for Queue Management

1. **Separate by Priority**
   - Critical tasks → `high_priority` queue
   - Normal tasks → `default` queue
   - Background tasks → `low_priority` queue

2. **Separate by Duration**
   - Fast tasks (<1s) → `fast` queue
   - Slow tasks (>1min) → `slow` queue
   - Dedicated workers for each

3. **Separate by Resource Usage**
   - CPU-intensive → `cpu_intensive` queue
   - I/O-intensive → `io_intensive` queue
   - Memory-intensive → `memory_intensive` queue

4. **Use Appropriate Concurrency**
   ```bash
   # Fast tasks: More concurrency
   celery -A worker worker --queues=fast --concurrency=8
   
   # Slow tasks: Less concurrency
   celery -A worker worker --queues=slow --concurrency=2
   ```

5. **Monitor and Scale**
   - Watch queue lengths in Flower
   - Add more workers if queues are backing up
   - Remove workers if queues are empty

### Summary: .delay() vs apply_async()

| Feature | `.delay()` | `apply_async()` |
|---------|------------|-----------------|
| **Simplicity** | ✅ Simple | ⚠️ More verbose |
| **Queue Control** | ❌ Uses default/routing | ✅ Explicit queue |
| **Priority** | ❌ Default priority | ✅ Custom priority |
| **Scheduling** | ❌ Immediate | ✅ ETA/countdown |
| **Expiration** | ❌ No expiration | ✅ Can set expiration |
| **Use Case** | Simple tasks | Advanced control |

**Recommendation:**
- Use `.delay()` for 90% of cases (simple, clean)
- Use `apply_async()` when you need queue control, priority, or scheduling

---

## 🎓 Key Patterns & Best Practices

### Pattern 1: Non-Blocking Tasks

**❌ Bad (Blocking):**
```python
@router.post("/send-email")
async def send_email(email: EmailRequest):
    # This blocks for 2-5 seconds!
    send_email_smtp(email.to, email.subject, email.body)
    return {"status": "sent"}
```

**✅ Good (Non-Blocking):**
```python
@router.post("/send-email")
async def send_email(email: EmailRequest):
    # Returns immediately!
    task = send_email_task.delay(email.to, email.subject, email.body)
    return {"task_id": task.id, "status": "PENDING"}
```

### Pattern 2: Progress Tracking

**For Long-Running Tasks:**
```python
@celery_app.task(bind=True)
def process_file(self, file_path: str):
    total_steps = 10
    
    for step in range(1, total_steps + 1):
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': step,
                'total': total_steps,
                'percent': int((step / total_steps) * 100)
            }
        )
        # Do work
        process_chunk(file_path, step)
    
    return {"status": "completed"}
```

**Client polls for progress:**
```python
result = AsyncResult(task_id, app=celery_app)
if result.state == 'PROGRESS':
    progress = result.info  # {'current': 5, 'total': 10, 'percent': 50}
```

### Pattern 3: Real-Time Updates (WebSocket)

**Task publishes to Redis:**
```python
@celery_app.task
def generate_report(job_id: str):
    # Do work
    result = create_report()
    
    # Publish to Redis channel
    redis_client.publish(job_id, json.dumps(result))
    return result
```

**WebSocket subscribes:**
```python
@router.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(job_id)
    
    while True:
        message = await pubsub.get_message()
        if message:
            await websocket.send_json(json.loads(message["data"]))
```

### Pattern 4: Error Handling & Retries

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, to: str, subject: str, body: str):
    try:
        # Attempt to send
        smtp_send(to, subject, body)
        return "Email sent"
        
    except ConnectionError as exc:
        # Retry on network errors
        raise self.retry(exc=exc, countdown=60)
        
    except ValueError as exc:
        # Don't retry on validation errors
        raise  # Task fails permanently
```

**Key Points:**
- `bind=True`: Access to `self` for retries
- `max_retries=3`: Maximum retry attempts
- `self.retry()`: Retry with exponential backoff
- Different exceptions handled differently

### Pattern 5: Configuration Management

**Always use environment variables:**
```python
# config.py
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

**Create .env file:**
```env
REDIS_URL=redis://localhost:6379/0
DEBUG=True
APP_NAME=My Backend
```

**Why:** Different values for dev/staging/production without code changes.

---

## ⚠️ Common Pitfalls & Solutions

### Pitfall 1: Tasks Not Executing

**Symptoms:**
- Task stays in PENDING state
- No worker logs

**Solutions:**
```bash
# Check if worker is running
celery -A worker inspect active

# Check registered tasks
celery -A worker inspect registered

# Start worker
celery -A worker worker --loglevel=info
```

### Pitfall 2: Import Errors

**Problem:**
```python
# In tasks/email_tasks.py
from app.core.celery_app import celery_app  # ❌ ImportError
```

**Solution:**
- Ensure `__init__.py` files exist in all directories
- Use absolute imports: `from app.core.celery_app import celery_app`
- Check PYTHONPATH includes project root

### Pitfall 3: Redis Connection Issues

**Problem:**
```
ConnectionError: Error connecting to Redis
```

**Solutions:**
```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Check URL in config
echo $REDIS_URL

# Test connection
python -c "import redis; r=redis.Redis.from_url('redis://localhost:6379/0'); print(r.ping())"
```

### Pitfall 4: Tasks Stuck in PENDING

**Causes:**
- Worker not running
- Wrong queue name
- Task name mismatch

**Debug:**
```python
# Check task state
result = AsyncResult(task_id, app=celery_app)
print(result.state)  # Should be STARTED or SUCCESS

# Check worker logs
# Look for: "Received task: app.tasks.email_tasks.send_email"
```

### Pitfall 5: Memory Leaks

**Problem:**
Workers consume more memory over time

**Solution:**
```python
# In celery_app.py
celery_app.conf.update(
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks
)
```

---

## 📚 Quick Reference

### Starting Services

```bash
# Local Development
redis-server                    # Start Redis
celery -A worker worker         # Start worker
uvicorn app.main:app --reload   # Start FastAPI

# Docker
docker-compose up --build       # Start all services
docker-compose logs -f worker   # View worker logs
docker-compose down             # Stop all services
```

### Common Commands

```bash
# Celery Worker
celery -A worker worker --loglevel=info
celery -A worker worker --concurrency=4        # 4 worker processes
celery -A worker worker --queues=high_priority # Specific queue

# Celery Inspection
celery -A worker inspect active                # Active tasks
celery -A worker inspect registered            # Registered tasks
celery -A worker inspect stats                 # Worker statistics

# Flower (Monitoring)
celery -A worker flower --port=5555

# Redis
redis-cli ping                                  # Test connection
redis-cli LLEN celery                          # Queue length
redis-cli LRANGE celery 0 -1                   # View queue
```

### Code Patterns

**Create Task:**
```python
# Simple - uses default queue
task = my_task.delay(arg1, arg2)

# Advanced - explicit queue and options
task = my_task.apply_async(
    args=[arg1, arg2],
    queue='high_priority',      # Specific queue
    priority=9,                 # High priority
    countdown=60                # Execute after 60 seconds
)
```

**Check Status:**
```python
result = AsyncResult(task_id, app=celery_app)
if result.ready():
    if result.successful():
        data = result.get()
    else:
        error = result.info
```

**Update Progress:**
```python
self.update_state(state='PROGRESS', meta={'percent': 50})
```

**Retry Task:**
```python
raise self.retry(exc=exc, countdown=60)
```

---

## ✅ Junior-to-Senior Checklist

Before deploying, ask yourself:

1. **Is this task heavy?**
   - ✅ Takes >500ms → Background task
   - ✅ User shouldn't wait → Background task
   - ✅ Can fail independently → Background task

2. **What if it fails?**
   - ✅ Have try/except blocks
   - ✅ Retry logic for transient errors
   - ✅ Log errors for debugging
   - ✅ Don't retry permanent errors

3. **How will user know?**
   - ✅ Return task_id immediately
   - ✅ Provide status endpoint
   - ✅ Use WebSocket for real-time (if needed)
   - ✅ Update progress for long tasks

4. **Is it production-ready?**
   - ✅ Environment variables for config
   - ✅ Error handling
   - ✅ Logging
   - ✅ Health checks
   - ✅ Docker setup
   - ✅ Monitoring (Flower)

---

## 🎯 Summary

**The Golden Rules:**

1. **FastAPI responds fast** → Queue heavy work
2. **Celery does the work** → Separate processes
3. **Redis connects them** → Message broker + results
4. **Docker orchestrates** → Easy deployment

**Remember:**
- User experience > Code simplicity
- Background tasks for anything >500ms
- Always return task_id for tracking
- Monitor with Flower
- Use environment variables
- Handle errors gracefully

**Next Steps:**
1. Copy the template structure
2. Customize for your use case
3. Add your tasks
4. Test locally
5. Deploy with Docker

---

**Happy Coding! 🚀**

*This guide is based on the `fastapi_celery_redis_template` project. Use it as your starting point for professional backend systems.*
