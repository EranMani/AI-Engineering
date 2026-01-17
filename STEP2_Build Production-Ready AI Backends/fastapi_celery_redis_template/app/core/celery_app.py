"""Celery application initialization and configuration"""
from celery import Celery
from app.config import settings

# Initialize Celery app
celery_app = Celery(
    "fastapi_celery_redis_template",
    broker=settings.get_celery_broker_url(),
    backend=settings.get_celery_backend_url()
)

# Configure Celery
celery_app.conf.update(
    # Serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='UTC',
    enable_utc=True,
    
    # Task tracking
    task_track_started=True,
    
    # Time limits
    task_time_limit=settings.TASK_TIME_LIMIT,
    task_soft_time_limit=settings.TASK_SOFT_TIME_LIMIT,
    
    # Worker configuration
    worker_prefetch_multiplier=settings.WORKER_PREFETCH_MULTIPLIER,
    worker_max_tasks_per_child=settings.WORKER_MAX_TASKS_PER_CHILD,
    
    # Result backend configuration
    result_expires=3600,  # Results expire after 1 hour
    
    # Task routing (can be extended)
    task_routes={},
    
    # Task discovery
    include=[
        'app.tasks.email_tasks',
        'app.tasks.progress_tasks',
        'app.tasks.websocket_tasks',
        'app.tasks.queue_tasks',
    ]
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['app.tasks'])
