"""Redis client utilities for sync and async operations"""
import redis
import redis.asyncio as aioredis
from typing import Optional
from app.config import settings


# Synchronous Redis client (for Celery tasks)
def get_redis_client() -> redis.Redis:
    """Get synchronous Redis client for Celery tasks"""
    return redis.Redis.from_url(
        settings.get_redis_url(),
        decode_responses=False,  # Keep as bytes for Celery compatibility
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
    )


# Async Redis client instance (for FastAPI/WebSocket)
_async_redis_client: Optional[aioredis.Redis] = None


async def get_async_redis_client() -> aioredis.Redis:
    """Get async Redis client for FastAPI/WebSocket operations"""
    global _async_redis_client
    if _async_redis_client is None:
        _async_redis_client = aioredis.from_url(
            settings.get_redis_url(),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
    return _async_redis_client


async def close_async_redis_client():
    """Close async Redis client connection"""
    global _async_redis_client
    if _async_redis_client:
        await _async_redis_client.close()
        _async_redis_client = None
