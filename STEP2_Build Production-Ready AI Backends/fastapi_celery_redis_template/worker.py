"""Celery worker entry point"""
from app.core.celery_app import celery_app

# This is the entry point for running Celery workers
# Usage: celery -A worker worker --loglevel=info

if __name__ == "__main__":
    celery_app.start()
