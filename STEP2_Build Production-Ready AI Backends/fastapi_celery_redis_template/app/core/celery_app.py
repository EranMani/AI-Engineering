"""Celery application initialization and configuration

This module creates and configures the Celery application instance. Celery is a
distributed task queue that executes tasks asynchronously using worker processes.
Redis serves as both the message broker (queues tasks) and result backend (stores results).

Key Components:
- Broker: Redis queue where tasks are stored before execution
- Backend: Redis storage where task results are saved
- Workers: Separate processes that execute tasks from the queue
"""
from celery import Celery
from app.config import settings

# Initialize Celery application instance
# broker: Where tasks are queued (Redis)
# backend: Where results are stored (Redis)
celery_app = Celery(
    "fastapi_celery_redis_template",  # Application name
    broker=settings.get_celery_broker_url(),      # Message broker URL
    backend=settings.get_celery_backend_url()      # Result backend URL
)

# Configure Celery settings
celery_app.conf.update(
    # Serialization: Use JSON for task and result serialization
    # JSON is human-readable, language-agnostic, and works well with Redis
    task_serializer='json',
    accept_content=['json'],  # Only accept JSON messages (security)
    result_serializer='json',
    
    # Timezone: Use UTC for consistent scheduling across timezones
    timezone='UTC',
    enable_utc=True,
    
    # Task tracking: Track when tasks start (not just PENDING/SUCCESS)
    # Enables STARTED state for better monitoring
    task_track_started=True,
    
    # Time limits: Prevent tasks from running indefinitely
    # Hard limit: Worker killed if exceeded
    # Soft limit: Raises exception, allows cleanup before hard limit
    task_time_limit=settings.TASK_TIME_LIMIT,      # Hard limit (default: 30 min)
    task_soft_time_limit=settings.TASK_SOFT_TIME_LIMIT,  # Soft limit (default: 25 min)
    
    # Worker configuration: Control worker behavior
    # Prefetch: How many tasks worker grabs at once (1 = fair distribution)
    # Max tasks per child: Restart worker after N tasks (prevents memory leaks)
    worker_prefetch_multiplier=settings.WORKER_PREFETCH_MULTIPLIER,  # Default: 1
    worker_max_tasks_per_child=settings.WORKER_MAX_TASKS_PER_CHILD,  # Default: 1000
    
    # Result backend: Configure result storage
    # Results expire after 1 hour to prevent Redis memory bloat
    result_expires=3600,  # Results expire after 1 hour
    
    # Task routing: Route specific tasks to specific queues (empty = default queue)
    # Example: {'app.tasks.priority_task': {'queue': 'high_priority'}}
    task_routes={},
    
    # Task discovery: Explicitly include task modules
    # Ensures tasks are registered even if autodiscover fails
    include=[
        'app.tasks.email_tasks',
        'app.tasks.progress_tasks',
        'app.tasks.websocket_tasks',
        'app.tasks.queue_tasks',
    ]
)

# Auto-discover tasks from app.tasks package
# Automatically finds and registers all @celery_app.task decorated functions
celery_app.autodiscover_tasks(['app.tasks'])
