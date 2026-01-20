"""Application configuration management module.

This module implements a singleton-like pattern for application settings.
It loads configuration from environment variables and provides a single
global instance that can be imported throughout the application.

Usage:
    from app.config import settings
    redis_url = settings.get_redis_url()
    app_name = settings.APP_NAME

The Settings class contains all configuration values (ports, URLs, behavior
settings, metadata) loaded from environment variables with sensible defaults.
A global 'settings' instance is created at module level for convenient access.
"""

from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # ----------------- PORTS AND URLS ----------------- #
    ######################################################
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

    # Flower Configuration
    FLOWER_PORT: int = int(os.getenv("FLOWER_PORT", "5555"))
    FLOWER_BASIC_AUTH: Optional[str] = os.getenv("FLOWER_BASIC_AUTH", None)


    # --------------- BEHAVIOR SETTINGS --------------- #
    #####################################################
    # Task Configuration
    TASK_TIME_LIMIT: int = int(os.getenv("TASK_TIME_LIMIT", "1800"))  # 30 minutes
    TASK_SOFT_TIME_LIMIT: int = int(os.getenv("TASK_SOFT_TIME_LIMIT", "1500"))  # 25 minutes
    WORKER_MAX_TASKS_PER_CHILD: int = int(os.getenv("WORKER_MAX_TASKS_PER_CHILD", "1000"))
    WORKER_PREFETCH_MULTIPLIER: int = int(os.getenv("WORKER_PREFETCH_MULTIPLIER", "1"))


    # -------------------- METADATA ------------------- #
    #####################################################
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Celery Redis Template")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    
    # Class methods provide abstraction for future extensibility (validation, logging) 
    # and work with both class and instance access patterns.
    # NOTE: @classmethod automatically passes the class as the first argument
    # NOTE: cls refers to the class (Settings), not an instance
    # NOTE: used like this since the variables are class attributes, defined at class level (not in __init__)
    @classmethod
    def get_redis_url(cls) -> str:
        """Get Redis URL for connections"""
        return cls.REDIS_URL
    
    @classmethod
    def get_celery_broker_url(cls) -> str:
        """Get Celery broker URL"""
        return cls.CELERY_BROKER_URL
    
    @classmethod
    def get_celery_backend_url(cls) -> str:
        """Get Celery result backend URL"""
        return cls.CELERY_RESULT_BACKEND


# Singleton-like instance: create once here so other modules can import and use directly.
# This ensures a single source of truth for configuration across the entire application.
# Usage: from app.config import settings
settings = Settings()
