"""Application configuration management"""
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Celery Redis Template")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
    
    # Flower Configuration
    FLOWER_PORT: int = int(os.getenv("FLOWER_PORT", "5555"))
    FLOWER_BASIC_AUTH: Optional[str] = os.getenv("FLOWER_BASIC_AUTH", None)
    
    # Task Configuration
    TASK_TIME_LIMIT: int = int(os.getenv("TASK_TIME_LIMIT", "1800"))  # 30 minutes
    TASK_SOFT_TIME_LIMIT: int = int(os.getenv("TASK_SOFT_TIME_LIMIT", "1500"))  # 25 minutes
    WORKER_MAX_TASKS_PER_CHILD: int = int(os.getenv("WORKER_MAX_TASKS_PER_CHILD", "1000"))
    WORKER_PREFETCH_MULTIPLIER: int = int(os.getenv("WORKER_PREFETCH_MULTIPLIER", "1"))
    
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


# Global settings instance
settings = Settings()
