"""Shared dependencies for API endpoints

This module contains FastAPI dependency injection functions that are shared across
all API versions (v1, v2, etc.). Dependencies handle resource management, 
authentication, and shared logic that multiple endpoints need.

WHY USE FASTAPI DEPENDENCIES?
=============================

FastAPI's dependency injection system provides several key benefits:

1. **Resource Management & Cleanup**
   - Automatic lifecycle management (setup before request, cleanup after)
   - Ensures resources (DB connections, Redis clients, HTTP clients) are properly closed
   - Prevents resource leaks and connection pool exhaustion
   - Example: Database session automatically closes after request completes

2. **Code Reusability**
   - Write once, use in multiple endpoints
   - Consistent behavior across all endpoints
   - Single source of truth for shared logic
   - Example: Authentication logic defined once, used everywhere

3. **Testability**
   - Easy to mock dependencies in tests
   - Override dependencies for testing scenarios
   - Isolate endpoint logic from external dependencies
   - Example: Mock Redis client for unit tests

4. **Cleaner Endpoint Code**
   - Endpoints focus on business logic, not setup/teardown
   - Less boilerplate code in each endpoint
   - Clear separation of concerns
   - Example: Endpoint doesn't need to manage Redis connection lifecycle

5. **Type Safety & Validation**
   - FastAPI validates dependency return types
   - IDE autocomplete and type checking
   - Runtime validation of dependencies
   - Example: Type hints ensure correct Redis client usage

WHY IN api/ ROOT FOLDER AND NOT IN VERSIONS (v1, v2)?
======================================================

The dependencies are placed in `app/api/deps.py` (root of api folder) rather than
in version-specific folders like `app/api/v1/deps.py` for these reasons:

1. **Shared Across All API Versions**
   - Dependencies like Redis clients, database sessions, and authentication
     are typically the same across all API versions
   - Avoids code duplication between v1, v2, v3, etc.
   - Single source of truth for shared resources

2. **Version-Independent Resources**
   - Infrastructure dependencies (Redis, DB, HTTP clients) don't change
     between API versions
   - Business logic changes, but resource management stays the same
   - Example: Redis client works the same in v1 and v2

3. **Easier Maintenance**
   - Update dependency logic once, affects all versions
   - Consistent behavior across API versions
   - Easier to refactor and maintain

4. **Import Clarity**
   - Clear import path: `from app.api.deps import get_redis`
   - Works from any version folder: `from app.api.deps import ...`
   - No confusion about which version's dependencies to use

5. **Future-Proof**
   - When adding v2, v3, etc., dependencies are already available
   - No need to copy or duplicate dependency code
   - New versions can immediately use existing dependencies

Example Structure:
    app/
    ├── api/
    │   ├── deps.py          ← Shared dependencies (here!)
    │   └── v1/
    │       ├── email.py      ← Uses: from app.api.deps import get_redis
    │       └── progress.py  ← Uses: from app.api.deps import get_redis
    │   └── v2/
    │       └── email.py      ← Also uses: from app.api.deps import get_redis

WHEN TO USE DEPENDENCIES?
=========================

Use dependencies for:
- Resource management: Database connections, Redis clients, HTTP clients
- Authentication: User validation, token checking, permission verification
- Shared logic: Pagination, filtering, common data transformations
- Multiple endpoints: Same resource/logic needed in many places
- Cleanup needed: Connections or resources that need proper closing

Don't use dependencies for:
- Simple values: One-time parameters (just use function parameters)
- Static configuration: Import directly (from app.config import settings)
- Complex business logic: Better as service classes or utility functions
- Single endpoint only: Unless you need automatic cleanup/management
"""
from typing import Generator
from app.core.redis_client import get_async_redis_client
import redis.asyncio as aioredis


async def get_redis() -> Generator[aioredis.Redis, None, None]:
    """
    Dependency for getting async Redis client
    This is a FastAPI dependency injection function
    API layer only
    
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
