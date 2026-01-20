"""Redis client utilities for sync and async operations

This module provides Redis client factories for both synchronous (Celery tasks)
and asynchronous (FastAPI/WebSocket) operations. Different clients are needed
because Celery tasks run in sync workers while FastAPI endpoints are async.

Key Differences:
- Sync client: Used in Celery tasks, returns bytes (decode_responses=False)
- Async client: Used in FastAPI/WebSocket, returns strings (decode_responses=True)
- Async client uses singleton pattern to reuse connection across requests
"""
import redis
import redis.asyncio as aioredis
from typing import Optional
from app.config import settings


def get_redis_client() -> redis.Redis:
    """
    Get synchronous Redis client for Celery tasks
    
    Creates a new Redis client instance each time. Used in Celery tasks which
    run in synchronous worker processes. Returns bytes (not decoded strings)
    for compatibility with Celery's serialization.
    
    Returns:
        Synchronous Redis client instance
        
    Note:
        decode_responses=False keeps data as bytes, which Celery expects
    """
    return redis.Redis.from_url(
        settings.get_redis_url(),
        decode_responses=False,  # Keep as bytes for Celery compatibility
        socket_connect_timeout=5,  # Connection timeout (seconds)
        socket_timeout=5,  # Operation timeout (seconds)
        retry_on_timeout=True,  # Retry on timeout errors
    )


# Global async Redis client instance (singleton pattern)
# Reused across all FastAPI requests/WebSocket connections for efficiency
_async_redis_client: Optional[aioredis.Redis] = None


async def get_async_redis_client() -> aioredis.Redis:
    """
    Get async Redis client for FastAPI/WebSocket operations
    
    Uses singleton pattern - creates client once and reuses it. This is more
    efficient than creating a new connection for each request. The client
    automatically handles connection pooling.
    
    Returns:
        Async Redis client instance (shared across requests)
        
    Note:
        decode_responses=True returns strings (not bytes) for easier handling
        in async code. Client is created lazily on first call.
    """
    global _async_redis_client
    if _async_redis_client is None:
        # Create client on first call (lazy initialization)
        _async_redis_client = aioredis.from_url(
            settings.get_redis_url(),
            decode_responses=True,  # Return strings (not bytes)
            socket_connect_timeout=5,  # Connection timeout
            socket_timeout=5,  # Operation timeout
        )
    return _async_redis_client


async def close_async_redis_client():
    """
    Close async Redis client connection
    
    Called during application shutdown to properly close Redis connections.
    Prevents connection leaks and ensures clean shutdown. Used in FastAPI's
    lifespan shutdown event.
    
    Note:
        Should be called in application shutdown handler (see main.py)
    """
    global _async_redis_client
    if _async_redis_client:
        await _async_redis_client.close()
        _async_redis_client = None
