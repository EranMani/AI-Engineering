"""Shared dependencies for API endpoints"""
from typing import Generator
from app.core.redis_client import get_async_redis_client
import redis.asyncio as aioredis


async def get_redis() -> Generator[aioredis.Redis, None, None]:
    """
    Dependency for getting async Redis client
    
    Usage:
        @router.get("/endpoint")
        async def endpoint(redis: aioredis.Redis = Depends(get_redis)):
            # Use redis client
    """
    redis_client = await get_async_redis_client()
    try:
        yield redis_client
    finally:
        # Connection cleanup handled by global client
        pass
