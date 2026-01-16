# FastAPI, Celery & Redis: Complete Guide to Background Task Systems

## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts & Definitions](#core-concepts--definitions)
3. [Common Use Cases](#common-use-cases)
4. [Architecture Overview](#architecture-overview)
5. [Component Deep Dive](#component-deep-dive)
6. [Implementation Guide](#implementation-guide)
7. [Monitoring & Infrastructure](#monitoring--infrastructure)
8. [Complete Code Examples](#complete-code-examples)
9. [Best Practices](#best-practices)

---

## Introduction

Building high-performance applications requires efficient handling of time-consuming operations. Background task systems allow you to offload heavy work from your main application, ensuring fast response times and better user experience. This guide provides an in-depth exploration of using **FastAPI**, **Celery**, and **Redis** together to build robust, scalable background task systems.

---

## Core Concepts & Definitions

### Background Task
A **background task** is any process that is offloaded from the main request-response cycle to improve application performance. Instead of making users wait for long-running operations (like sending emails, generating reports, or processing data), these tasks are executed asynchronously in the background.

**Key Benefits:**
- **Non-blocking**: Main application remains responsive
- **Scalable**: Can handle multiple tasks concurrently
- **Resilient**: Tasks can be retried on failure
- **Distributed**: Can run across multiple machines

### Celery
**Celery** is a "batteries-included," distributed task queue that allows for the asynchronous execution of work. It's written in Python and is designed to handle large volumes of messages while maintaining simplicity.

**Core Features:**
- Asynchronous task execution
- Distributed architecture (multiple workers)
- Task scheduling (via Celery Beat)
- Result tracking and storage
- Retry mechanisms
- Rate limiting
- Task prioritization

### Redis (Remote Dictionary Server)
**Redis** is a high-speed, in-memory database often used as a message broker or result backend in Celery setups. It acts as the communication layer between your application and workers.

**Why Redis for Celery?**
- **Sub-millisecond latency**: In-memory storage provides extremely fast read/write operations
- **Pub/Sub support**: Enables real-time messaging patterns
- **Data structures**: Supports lists, sets, hashes, and streams
- **Persistence**: Can be configured for durability (RDB snapshots, AOF)
- **High availability**: Supports clustering and replication

### Producer
The **producer** is the client code (typically your FastAPI application) that defines and triggers tasks. When a user makes a request, the producer creates a task and sends it to the message broker (Redis).

### Consumer/Worker
A **consumer** (also called a **worker**) is a separate process that pulls tasks from the queue and executes them. Workers run independently of your main application and can be scaled horizontally across multiple machines.

### Message Broker
The **message broker** (Redis in our case) acts as the transport medium, holding tasks in a queue until a worker is ready to process them. It decouples the producer from the consumer.

### Result Backend
The **result backend** (also Redis in our setup) stores task statuses (PENDING, SUCCESS, FAILURE) and return values for later retrieval. This allows you to check task status and retrieve results.

---

## Common Use Cases

Background tasks are ideal for operations that would otherwise block the user experience:

### 1. **Sending Emails**
- Email verification during registration
- Password reset emails
- Notification emails
- Marketing campaigns
- Transactional emails (receipts, confirmations)

**Why Background?** Email delivery can take 1-5 seconds. Users shouldn't wait for this.

### 2. **Report Generation**
- Creating large CSV files
- Generating PDF reports
- Data aggregation and analysis
- Exporting database records

**Why Background?** Large reports can take minutes to generate.

### 3. **Data Processing**
- Image/video processing
- File uploads and transformations
- Batch data imports
- Machine learning inference
- Data validation and cleaning

**Why Background?** Heavy computations can take significant time.

### 4. **Scheduling**
- Running maintenance tasks at specific intervals (using Celery Beat)
- Periodic data synchronization
- Cleanup jobs
- Health checks
- Automated backups

### 5. **API Integrations**
- Calling external APIs with rate limits
- Webhook processing
- Third-party service synchronization
- Payment processing

---

## Architecture Overview

The system follows a **Producer-Broker-Consumer** model:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   FastAPI   │────────▶│    Redis    │────────▶│   Celery    │
│  (Producer) │  Task   │  (Broker)   │  Task   │   Worker    │
│             │  Queue  │             │  Pull   │ (Consumer)  │
└─────────────┘         └─────────────┘         └─────────────┘
      │                        │                        │
      │                        │                        │
      │                        │                        │
      │                        │                        │
      │                        ▼                        │
      │              ┌─────────────┐                   │
      │              │    Redis    │                   │
      │              │   (Result   │                   │
      │              │   Backend)  │                   │
      │              └─────────────┘                   │
      │                        │                        │
      │                        │                        │
      └────────────────────────┼────────────────────────┘
                               │
                               │ Status & Results
                               │
                               ▼
                        ┌─────────────┐
                        │   Client    │
                        │  (Browser)  │
                        └─────────────┘
```

### Flow Breakdown:

1. **FastAPI (Producer)**: Receives a request and pushes a task to the broker
   - User makes HTTP request to FastAPI endpoint
   - FastAPI creates a Celery task using `.delay()` or `.apply_async()`
   - Task is serialized and sent to Redis
   - FastAPI immediately returns a response with `task_id`

2. **Redis (Broker)**: Acts as the transport medium
   - Stores tasks in queues (lists)
   - Workers poll Redis for new tasks
   - Ensures tasks are delivered even if workers are temporarily unavailable

3. **Celery Worker (Consumer)**: Picks up and executes tasks
   - Continuously polls Redis for new tasks
   - Executes the task function
   - Updates task state (STARTED, PROGRESS, SUCCESS, FAILURE)
   - Stores results in the result backend

4. **Result Backend (Redis)**: Stores task statuses and results
   - Tracks task state (PENDING → STARTED → SUCCESS/FAILURE)
   - Stores return values
   - Enables status checking via `AsyncResult`

5. **Client**: Retrieves results
   - Polls status endpoint (traditional approach)
   - Connects via WebSocket for real-time updates (advanced approach)

---

## Component Deep Dive

### Redis: Features & Capabilities

#### Sub-millisecond Latency
As an in-memory store, Redis provides significantly faster performance than disk-based databases. Typical operations complete in under 1 millisecond.

#### Durability Options
Redis offers two persistence mechanisms:

1. **RDB (Redis Database Backup)**
   - Point-in-time snapshots
   - Configurable intervals (e.g., save every 5 minutes if 10+ keys changed)
   - Compact file format
   - Good for disaster recovery

2. **AOF (Append Only File)**
   - Logs every write operation
   - More durable but larger files
   - Can be configured to fsync on every write (safest but slowest)

#### Multi-Modal Data Structures
Redis supports various data types:
- **Strings**: Simple key-value pairs
- **Lists**: Ordered collections (used for queues)
- **Sets**: Unordered unique collections
- **Hashes**: Field-value maps
- **Sorted Sets**: Ordered sets with scores
- **Streams**: Log-like data structure (great for event sourcing)

#### High Availability
- **Clustering**: Distributes data across multiple nodes
- **Sharding**: Splits data for horizontal scaling
- **Replication**: Master-slave and active-active configurations
- **Sentinel**: Automatic failover for high availability

### Celery: Architecture & Features

#### Asynchronous Execution
Celery offloads work so the main app returns a response in milliseconds while the task runs elsewhere. This is achieved through:

- **Task Decorators**: `@celery_app.task` marks functions as tasks
- **Task Invocation**: `.delay()` or `.apply_async()` triggers execution
- **Non-blocking**: Main thread continues immediately

#### Distributed Nature
Workers can run on multiple machines to distribute load:
- **Horizontal Scaling**: Add more workers to handle more tasks
- **Load Distribution**: Tasks are distributed across available workers
- **Fault Tolerance**: If one worker fails, others continue processing

#### Task Management
Celery provides powerful task management features:

- **Task States**: PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED
- **Task Routing**: Send specific tasks to specific queues
- **Task Priorities**: Prioritize important tasks
- **Task Expiration**: Set time-to-live for tasks
- **Task Retries**: Automatic retry on failure with exponential backoff

#### Synchronous Conversion
For async code (like FastAPI's async functions), tools like `asgiref` are used to run it within Celery's synchronous workers:

```python
from asgiref.sync import async_to_sync

@celery_app.task
def send_async_email(email_data):
    # Convert async function to sync for Celery
    async_to_sync(send_email_async)(email_data)
```

---

## Implementation Guide

### Step 1: Setup Redis

#### Installation
```bash
# Using Docker (Recommended)
docker run -d -p 6379:6379 --name redis redis:latest

# Or install locally
# Windows: Download from https://redis.io/download
# Linux: sudo apt-get install redis-server
# macOS: brew install redis
```

#### Configuration
Create a `.env` file:
```env
REDIS_URL=redis://localhost:6379/0
```

#### Verify Redis is Running
```bash
redis-cli ping
# Should return: PONG
```

### Step 2: Install Dependencies

```bash
pip install fastapi uvicorn celery redis python-dotenv
```

Or using `pyproject.toml`:
```toml
[tool.poetry.dependencies]
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
celery = "^5.3.0"
redis = "^5.0.0"
python-dotenv = "^1.0.0"
```

### Step 3: Create Celery Configuration

**`config.py`**:
```python
from dotenv import load_dotenv
import os

load_dotenv()

def get_redis_url() -> str:
    """Get Redis URL from environment variables"""
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    if not url:
        raise ValueError("REDIS_URL environment variable is required!")
    return url
```

### Step 4: Define Celery App and Tasks

**`worker.py`**:
```python
from celery import Celery
from config import get_redis_url

# Initialize Celery app
celery_app = Celery(
    "my_app",  # App name
    broker=get_redis_url(),      # Message broker (where tasks are queued)
    backend=get_redis_url()      # Result backend (where results are stored)
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',           # Serialize tasks as JSON
    accept_content=['json'],           # Only accept JSON content
    result_serializer='json',         # Serialize results as JSON
    timezone='UTC',                    # Timezone for scheduled tasks
    enable_utc=True,                   # Use UTC
    task_track_started=True,          # Track when tasks start
    task_time_limit=30 * 60,          # Hard time limit (30 minutes)
    task_soft_time_limit=25 * 60,     # Soft time limit (25 minutes)
    worker_prefetch_multiplier=1,     # Prefetch only one task at a time
    worker_max_tasks_per_child=1000,  # Restart worker after N tasks (memory management)
)

# Define a simple task
@celery_app.task(bind=True, max_retries=3)
def process_data(self, data: dict) -> dict:
    """
    Example task that processes data
    
    Args:
        self: Task instance (needed when bind=True)
        data: Input data dictionary
        
    Returns:
        Processed data dictionary
    """
    try:
        # Simulate processing
        result = {"processed": True, "data": data}
        return result
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60)  # Retry after 60 seconds
```

### Step 5: Create FastAPI Application

**`main.py`**:
```python
from fastapi import FastAPI
from worker import celery_app, process_data
from celery.result import AsyncResult
import uvicorn

app = FastAPI(title="Background Tasks API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Background Tasks API"}

@app.post("/process")
async def trigger_processing(data: dict):
    """
    Trigger a background task and return immediately
    """
    # Send task to Celery
    task = process_data.delay(data)
    
    return {
        "task_id": task.id,
        "status": "PENDING",
        "message": "Task queued successfully"
    }

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Check the status of a task
    """
    result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": result.status,
        "result": None
    }
    
    if result.ready():
        if result.successful():
            response["result"] = result.get()
        else:
            response["error"] = str(result.info)
    
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

### Step 6: Run the System

**Terminal 1 - Start Redis (if not using Docker)**:
```bash
redis-server
```

**Terminal 2 - Start Celery Worker**:
```bash
celery -A worker worker --loglevel=info
```

**Terminal 3 - Start FastAPI**:
```bash
python main.py
# Or: uvicorn main:app --reload
```

---

## Monitoring & Infrastructure

### Flower: Real-Time Monitoring

**Flower** is a web-based GUI for real-time monitoring of your Celery tasks.

#### Installation
```bash
pip install flower
```

#### Running Flower
```bash
celery -A worker flower --port=5555
```

Access at: `http://localhost:5555`

#### Features
- **Task Monitoring**: View active, succeeded, and failed tasks
- **Worker Status**: Monitor worker health and performance
- **Task Details**: Execution time, arguments, results, and tracebacks
- **Broker Information**: Queue lengths and message rates
- **Real-time Updates**: Live dashboard with auto-refresh

### Docker Infrastructure

Modern setups use Docker to run each component in a dedicated container:

#### `docker-compose.yml`:
```yaml
version: '3.8'

services:
  # Redis Broker & Backend
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # FastAPI Application
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # Celery Worker
  worker:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - .:/app
    command: celery -A worker worker --loglevel=info

  # Flower Monitoring
  flower:
    build: .
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - .:/app
    command: celery -A worker flower --port=5555

volumes:
  redis_data:
```

#### `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Complete Code Examples

### Example 1: Basic Email Service

This example shows a complete email service with task triggering and status checking.

#### `worker.py`:
```python
from celery import Celery
from config import get_redis_url
import time
import random

celery_app = Celery(
    "email_service",
    broker=get_redis_url(),
    backend=get_redis_url()
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_email(self, to: str, subject: str, body: str) -> str:
    """
    Send an email (simulated)
    
    Args:
        self: Task instance
        to: Recipient email address
        subject: Email subject
        body: Email body
        
    Returns:
        Success message
    """
    try:
        print(f"Sending email to: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        
        # Simulate network delay
        time.sleep(2)
        
        # Simulate occasional failures (for retry demonstration)
        if random.random() < 0.1:  # 10% failure rate
            raise ConnectionError("SMTP server connection failed")
        
        return f"Email sent successfully to {to}"
        
    except (ConnectionError, TimeoutError) as exc:
        print(f"Network error (attempt {self.request.retries + 1}/{self.max_retries}): {exc}")
        raise self.retry(exc=exc, countdown=5)
        
    except Exception as exc:
        print(f"Permanent error: {exc}")
        raise
```

#### `main.py`:
```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from worker import celery_app, send_email
from celery.result import AsyncResult
import uvicorn

app = FastAPI(title="Email Service", version="1.0.0")

# Request/Response Models
class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str

class EmailResponse(BaseModel):
    task_id: str
    status: str
    message: str

class StatusResponse(BaseModel):
    task_id: str
    status: str
    result: str | None = None
    error: str | None = None

@app.post("/send_email", response_model=EmailResponse)
async def handle_send_email(email: EmailRequest):
    """
    Trigger email sending task
    """
    # Send task to Celery queue
    task = send_email.delay(email.to, email.subject, email.body)
    
    return EmailResponse(
        task_id=task.id,
        status="PENDING",
        message="Email queued for sending"
    )

@app.get("/status/{task_id}", response_model=StatusResponse)
async def check_email_status(task_id: str):
    """
    Check the status of an email task
    """
    result = AsyncResult(task_id, app=celery_app)
    
    if result.ready():
        if result.successful():
            return StatusResponse(
                task_id=task_id,
                status="SUCCESS",
                result=result.get()
            )
        else:
            return StatusResponse(
                task_id=task_id,
                status="FAILURE",
                error=str(result.info)
            )
    else:
        return StatusResponse(
            task_id=task_id,
            status=result.state,
            result="Task is still processing"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

#### Usage:
```bash
# Start worker
celery -A worker worker --loglevel=info

# Start FastAPI
python main.py

# Send email
curl -X POST "http://localhost:8000/send_email" \
  -H "Content-Type: application/json" \
  -d '{"to": "user@example.com", "subject": "Hello", "body": "Test email"}'

# Check status
curl "http://localhost:8000/status/{task_id}"
```

### Example 2: Task with Progress Updates

This example shows how to update task progress during execution.

#### `worker.py`:
```python
from celery import Celery
from config import get_redis_url
import time

celery_app = Celery(
    "progress_tracker",
    broker=get_redis_url(),
    backend=get_redis_url()
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

@celery_app.task(bind=True)
def process_large_file(self, file_path: str) -> dict:
    """
    Process a large file with progress updates
    """
    total_steps = 10
    
    for step in range(1, total_steps + 1):
        # Update task state with progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': step,
                'total': total_steps,
                'percent': int((step / total_steps) * 100),
                'status': f'Processing step {step}/{total_steps}'
            }
        )
        
        # Simulate work
        time.sleep(1)
        print(f"Step {step}/{total_steps} completed")
    
    return {
        'file_path': file_path,
        'status': 'completed',
        'total_steps': total_steps
    }
```

#### `main.py`:
```python
from fastapi import FastAPI
from worker import celery_app, process_large_file
from celery.result import AsyncResult

app = FastAPI()

@app.post("/process_file")
async def trigger_file_processing(file_path: str):
    task = process_large_file.delay(file_path)
    return {"task_id": task.id, "status": "PENDING"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    
    if result.state == 'PROGRESS':
        return {
            "task_id": task_id,
            "status": result.state,
            "progress": result.info
        }
    elif result.ready():
        return {
            "task_id": task_id,
            "status": result.state,
            "result": result.get()
        }
    else:
        return {
            "task_id": task_id,
            "status": result.state
        }
```

### Example 3: WebSocket Real-Time Updates

This example shows how to use WebSockets to automatically receive task results without polling.

#### Architecture:
1. FastAPI receives request and triggers Celery task
2. FastAPI returns `task_id` to client
3. Client connects to WebSocket endpoint with `task_id`
4. Celery worker publishes result to Redis channel when done
5. FastAPI WebSocket subscribes to Redis channel and forwards to client

#### `worker.py`:
```python
from celery import Celery
import redis
import json
import time
from config import get_redis_url

celery_app = Celery(
    "websocket_example",
    broker=get_redis_url(),
    backend=get_redis_url()
)

# Redis client for pub/sub
redis_client = redis.Redis.from_url(get_redis_url())

@celery_app.task
def generate_report(job_id: str, report_type: str) -> dict:
    """
    Generate a report and publish result via Redis pub/sub
    """
    print(f"Starting report generation: {job_id}")
    
    # Simulate report generation
    time.sleep(5)
    
    result = {
        "job_id": job_id,
        "report_type": report_type,
        "status": "completed",
        "download_url": f"https://example.com/reports/{job_id}.pdf",
        "generated_at": time.time()
    }
    
    # Publish result to Redis channel (channel name = job_id)
    redis_client.publish(job_id, json.dumps(result))
    
    print(f"Published result to channel: {job_id}")
    return result
```

#### `main.py`:
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
import json
import uuid
from worker import generate_report

app = FastAPI()

# Redis async client for WebSocket
redis_client = redis.Redis.from_url("redis://localhost:6379/0")

@app.post("/generate_report")
async def trigger_report_generation(report_type: str):
    """
    Trigger report generation and return job_id
    """
    job_id = str(uuid.uuid4())
    
    # Send task to Celery
    generate_report.delay(job_id, report_type)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "websocket_url": f"/ws/{job_id}"
    }

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time task updates
    """
    # Accept WebSocket connection
    await websocket.accept()
    
    # Create Redis pub/sub client
    pubsub = redis_client.pubsub()
    
    try:
        # Subscribe to Redis channel (channel name = job_id)
        await pubsub.subscribe(job_id)
        
        # Send initial connection message
        await websocket.send_json({
            "status": "connected",
            "job_id": job_id,
            "message": "Waiting for task completion..."
        })
        
        # Listen for messages from Redis
        while True:
            # Get message from Redis pub/sub
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0
            )
            
            if message:
                # Decode message data
                data = json.loads(message["data"].decode("utf-8"))
                
                # Forward to WebSocket client
                await websocket.send_json(data)
                
                # If task completed, close connection
                if data.get("status") == "completed":
                    break
                    
    except WebSocketDisconnect:
        print(f"Client disconnected: {job_id}")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_json({
            "status": "error",
            "message": str(e)
        })
    finally:
        # Cleanup
        await pubsub.unsubscribe(job_id)
        await pubsub.close()
        await redis_client.close()
```

#### `client.html` (Example Frontend):
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Task Monitor</title>
</head>
<body>
    <h1>Report Generator</h1>
    <button onclick="generateReport()">Generate Report</button>
    <div id="status"></div>
    <div id="result"></div>

    <script>
        let ws = null;

        async function generateReport() {
            // Trigger task
            const response = await fetch('http://localhost:8000/generate_report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({report_type: 'monthly'})
            });
            
            const data = await response.json();
            const jobId = data.job_id;
            
            // Connect to WebSocket
            ws = new WebSocket(`ws://localhost:8000/ws/${jobId}`);
            
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                document.getElementById('status').innerHTML = 
                    `<p>Status: ${message.status}</p>`;
                
                if (message.status === 'completed') {
                    document.getElementById('result').innerHTML = 
                        `<p>Download: <a href="${message.download_url}">${message.download_url}</a></p>`;
                    ws.close();
                }
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }
    </script>
</body>
</html>
```

### Example 4: Redis Queue Management

This example shows how to directly interact with Redis queues for advanced use cases.

#### `queue_manager.py`:
```python
import redis
import json
from typing import List, Dict, Optional

class RedisQueueManager:
    """Manage Redis queues directly"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_client = redis.Redis.from_url(redis_url)
    
    def push_task(self, queue_name: str, task_data: dict) -> str:
        """
        Push a task to a Redis queue
        
        Args:
            queue_name: Name of the queue
            task_data: Task data dictionary
            
        Returns:
            Task ID
        """
        task_id = task_data.get("id", f"task_{int(time.time())}")
        task_data["id"] = task_id
        
        # Push to list (left push for queue behavior)
        self.redis_client.lpush(queue_name, json.dumps(task_data))
        
        return task_id
    
    def pop_task(self, queue_name: str, timeout: int = 0) -> Optional[dict]:
        """
        Pop a task from a Redis queue
        
        Args:
            queue_name: Name of the queue
            timeout: Blocking timeout in seconds (0 = non-blocking)
            
        Returns:
            Task data dictionary or None
        """
        if timeout > 0:
            # Blocking pop (waits for task)
            result = self.redis_client.brpop(queue_name, timeout=timeout)
            if result:
                _, data = result
                return json.loads(data.decode("utf-8"))
        else:
            # Non-blocking pop
            data = self.redis_client.rpop(queue_name)
            if data:
                return json.loads(data.decode("utf-8"))
        
        return None
    
    def get_queue_length(self, queue_name: str) -> int:
        """Get the number of tasks in queue"""
        return self.redis_client.llen(queue_name)
    
    def get_queue_tasks(self, queue_name: str, limit: int = 10) -> List[dict]:
        """Get tasks from queue without removing them"""
        tasks = self.redis_client.lrange(queue_name, 0, limit - 1)
        return [json.loads(task.decode("utf-8")) for task in tasks]
    
    def clear_queue(self, queue_name: str) -> int:
        """Clear all tasks from queue"""
        return self.redis_client.delete(queue_name)
    
    def move_task(self, from_queue: str, to_queue: str) -> Optional[dict]:
        """Move a task from one queue to another"""
        task = self.pop_task(from_queue)
        if task:
            self.push_task(to_queue, task)
        return task

# Usage example
if __name__ == "__main__":
    import time
    
    manager = RedisQueueManager()
    
    # Push tasks
    task1 = manager.push_task("my_queue", {"action": "process", "data": "test1"})
    task2 = manager.push_task("my_queue", {"action": "process", "data": "test2"})
    
    print(f"Queue length: {manager.get_queue_length('my_queue')}")
    
    # Pop task
    task = manager.pop_task("my_queue")
    print(f"Popped task: {task}")
    
    print(f"Queue length: {manager.get_queue_length('my_queue')}")
```

### Example 5: Complete Integration Example

This is a complete example showing all concepts together.

#### Project Structure:
```
project/
├── config.py          # Configuration
├── worker.py          # Celery tasks
├── main.py            # FastAPI app
├── queue_manager.py   # Redis queue utilities
├── .env               # Environment variables
└── requirements.txt   # Dependencies
```

#### `config.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

def get_redis_url() -> str:
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")
```

#### `worker.py`:
```python
from celery import Celery
from config import get_redis_url
import redis
import json
import time

REDIS_URL = get_redis_url()

celery_app = Celery(
    "complete_example",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Redis client for pub/sub
redis_pubsub = redis.Redis.from_url(REDIS_URL)

@celery_app.task(bind=True)
def process_order(self, order_id: str, items: list) -> dict:
    """Process an order with progress updates"""
    total_items = len(items)
    
    # Update progress
    for i, item in enumerate(items, 1):
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i,
                'total': total_items,
                'percent': int((i / total_items) * 100),
                'item': item
            }
        )
        time.sleep(1)  # Simulate processing
    
    result = {
        "order_id": order_id,
        "status": "completed",
        "items_processed": total_items
    }
    
    # Publish to Redis for WebSocket
    redis_pubsub.publish(f"order_{order_id}", json.dumps(result))
    
    return result
```

#### `main.py`:
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from worker import celery_app, process_order
from celery.result import AsyncResult
import redis.asyncio as redis
import json
import uuid
import uvicorn

app = FastAPI(title="Complete Example")

redis_client = redis.Redis.from_url("redis://localhost:6379/0")

class OrderRequest(BaseModel):
    items: list[str]

@app.post("/order")
async def create_order(order: OrderRequest):
    """Create an order and process it in background"""
    order_id = str(uuid.uuid4())
    
    # Trigger Celery task
    task = process_order.delay(order_id, order.items)
    
    return {
        "order_id": order_id,
        "task_id": task.id,
        "status": "queued",
        "websocket_url": f"/ws/order_{order_id}"
    }

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """Check task status (polling method)"""
    result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": result.state
    }
    
    if result.state == 'PROGRESS':
        response["progress"] = result.info
    elif result.ready():
        if result.successful():
            response["result"] = result.get()
        else:
            response["error"] = str(result.info)
    
    return response

@app.websocket("/ws/{channel}")
async def websocket_updates(websocket: WebSocket, channel: str):
    """WebSocket for real-time updates"""
    await websocket.accept()
    
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    
    try:
        await websocket.send_json({"status": "connected", "channel": channel})
        
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True,
                timeout=1.0
            )
            
            if message:
                data = json.loads(message["data"].decode("utf-8"))
                await websocket.send_json(data)
                
                if data.get("status") == "completed":
                    break
                    
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

## How Everything Works Together

### Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                          │
│  POST /api/process                                              │
│  { "data": "example" }                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI (PRODUCER)                         │
│  1. Receives HTTP request                                       │
│  2. Creates Celery task: task.delay(data)                      │
│  3. Task serialized to JSON                                     │
│  4. Returns response with task_id immediately                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Task JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REDIS (MESSAGE BROKER)                       │
│  Queue: celery (default queue)                                  │
│  [Task1, Task2, Task3, ...]                                    │
│                                                                 │
│  Structure:                                                     │
│  - Lists: Used for queues                                       │
│  - Hashes: Store task metadata                                  │
│  - Strings: Store task results                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Worker polls for tasks
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CELERY WORKER (CONSUMER)                      │
│  1. Polls Redis for new tasks                                   │
│  2. Deserializes task JSON                                      │
│  3. Executes task function                                      │
│  4. Updates state: PENDING → STARTED → SUCCESS                  │
│  5. Stores result in Redis (result backend)                     │
│  6. Publishes to Redis channel (for WebSocket)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Result stored
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              REDIS (RESULT BACKEND)                              │
│  Key: celery-task-meta-{task_id}                               │
│  Value: {                                                       │
│    "status": "SUCCESS",                                         │
│    "result": {...},                                             │
│    "traceback": null                                            │
│  }                                                              │
│                                                                 │
│  Pub/Sub Channel: {task_id}                                     │
│  Message: {"status": "completed", "result": {...}}             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Status check / WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT                                  │
│  Method 1: Polling                                              │
│    GET /api/status/{task_id}                                    │
│    → Returns current status and result                          │
│                                                                 │
│  Method 2: WebSocket (Real-time)                                │
│    WS /ws/{task_id}                                             │
│    → Subscribes to Redis channel                                │
│    → Receives updates automatically                             │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Execution Flow

#### 1. **Task Submission**
```python
# Client sends request
POST /api/process
{"data": "example"}

# FastAPI receives request
@app.post("/api/process")
async def process(data: dict):
    # Create and send task
    task = process_data.delay(data)
    # Returns immediately with task_id
    return {"task_id": task.id, "status": "PENDING"}
```

#### 2. **Task Queuing in Redis**
```python
# Internally, Celery does:
# 1. Serialize task to JSON
task_json = {
    "id": "abc-123-def",
    "task": "worker.process_data",
    "args": [{"data": "example"}],
    "kwargs": {}
}

# 2. Push to Redis list (queue)
redis_client.lpush("celery", json.dumps(task_json))
```

#### 3. **Worker Processing**
```python
# Worker continuously polls Redis
while True:
    # Blocking pop from queue
    task_data = redis_client.brpop("celery", timeout=1)
    
    if task_data:
        # Deserialize and execute
        task = json.loads(task_data[1])
        result = execute_task(task)
        
        # Store result
        redis_client.set(
            f"celery-task-meta-{task['id']}",
            json.dumps({
                "status": "SUCCESS",
                "result": result
            })
        )
```

#### 4. **Status Retrieval (Polling)**
```python
# Client polls for status
GET /api/status/abc-123-def

# FastAPI checks Redis
result = AsyncResult("abc-123-def", app=celery_app)
# AsyncResult internally reads from Redis:
# redis_client.get("celery-task-meta-abc-123-def")

return {
    "status": result.status,  # "SUCCESS"
    "result": result.get()     # Actual result
}
```

#### 5. **Real-Time Updates (WebSocket)**
```python
# Client connects
WS /ws/abc-123-def

# FastAPI subscribes to Redis channel
pubsub = redis_client.pubsub()
pubsub.subscribe("abc-123-def")

# Worker publishes when done
redis_client.publish("abc-123-def", json.dumps(result))

# FastAPI receives and forwards to client
message = pubsub.get_message()
await websocket.send_json(message)
```

---

## Best Practices

### 1. **Error Handling**
- Always use `bind=True` for tasks that need retry logic
- Set appropriate `max_retries` and `default_retry_delay`
- Handle different exception types differently
- Log errors for debugging

```python
@celery_app.task(bind=True, max_retries=3)
def my_task(self, data):
    try:
        # Task logic
        pass
    except RetryableError as exc:
        raise self.retry(exc=exc, countdown=60)
    except PermanentError as exc:
        # Don't retry, just log
        logger.error(f"Permanent error: {exc}")
        raise
```

### 2. **Task Idempotency**
- Design tasks to be idempotent (safe to run multiple times)
- Use unique identifiers to prevent duplicate processing
- Check if work was already done before processing

```python
@celery_app.task
def process_payment(payment_id: str):
    # Check if already processed
    if is_payment_processed(payment_id):
        return {"status": "already_processed"}
    
    # Process payment
    result = charge_card(payment_id)
    mark_as_processed(payment_id)
    return result
```

### 3. **Resource Management**
- Set appropriate time limits for tasks
- Use `worker_max_tasks_per_child` to prevent memory leaks
- Monitor worker memory usage
- Clean up resources in finally blocks

```python
celery_app.conf.update(
    task_time_limit=30 * 60,      # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_max_tasks_per_child=1000,  # Restart after 1000 tasks
)
```

### 4. **Queue Management**
- Use separate queues for different task types
- Set priorities for important tasks
- Monitor queue lengths
- Set up alerts for queue backlogs

```python
# Route tasks to specific queues
@celery_app.task(queue='high_priority')
def important_task():
    pass

@celery_app.task(queue='low_priority')
def background_task():
    pass
```

### 5. **Monitoring**
- Use Flower for real-time monitoring
- Set up logging for all tasks
- Monitor Redis memory usage
- Track task success/failure rates
- Set up alerts for failures

### 6. **Security**
- Validate all task inputs
- Use environment variables for sensitive data
- Implement rate limiting
- Use secure Redis connections (TLS)
- Sanitize data before logging

### 7. **Testing**
- Test tasks in isolation
- Mock external dependencies
- Test retry logic
- Test error handling
- Use Celery's `task_always_eager=True` for testing

```python
# In test configuration
celery_app.conf.task_always_eager = True
# Tasks run synchronously in tests
```

### 8. **Performance Optimization**
- Use connection pooling for Redis
- Batch similar operations
- Use `worker_prefetch_multiplier=1` for fair distribution
- Monitor and optimize slow tasks
- Use result expiration for old results

```python
celery_app.conf.update(
    worker_prefetch_multiplier=1,  # Fair task distribution
    result_expires=3600,  # Results expire after 1 hour
)
```

---

## Troubleshooting

### Common Issues

#### 1. **Tasks Not Executing**
- Check if worker is running: `celery -A worker inspect active`
- Verify Redis connection
- Check task serialization format
- Look for errors in worker logs

#### 2. **Tasks Stuck in PENDING**
- Worker may not be running
- Task may be in wrong queue
- Check Redis connection
- Verify task name matches worker registration

#### 3. **Memory Issues**
- Reduce `worker_prefetch_multiplier`
- Set `worker_max_tasks_per_child`
- Clear old results from Redis
- Monitor Redis memory usage

#### 4. **Slow Performance**
- Add more workers
- Optimize task code
- Use faster Redis instance
- Check network latency
- Monitor queue lengths

---

## Conclusion

FastAPI, Celery, and Redis form a powerful combination for building high-performance applications with background task processing. This guide covered:

- **Core concepts**: Understanding the producer-broker-consumer model
- **Implementation**: Step-by-step setup and configuration
- **Advanced features**: Progress tracking, WebSocket updates, queue management
- **Best practices**: Error handling, monitoring, security, and performance

By following these patterns and practices, you can build scalable, resilient applications that handle heavy workloads efficiently while maintaining excellent user experience.

---

## Additional Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flower Documentation](https://flower.readthedocs.io/)

---

## Quick Reference

### Starting Services
```bash
# Redis
docker run -d -p 6379:6379 redis:latest

# Celery Worker
celery -A worker worker --loglevel=info

# FastAPI
uvicorn main:app --reload

# Flower
celery -A worker flower --port=5555
```

### Common Commands
```bash
# Check active tasks
celery -A worker inspect active

# Check registered tasks
celery -A worker inspect registered

# Purge all tasks
celery -A worker purge

# Check worker stats
celery -A worker inspect stats
```

---

*Last Updated: 2024*
