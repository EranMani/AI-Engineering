"""Redis queue management utilities"""
import redis
import json
import time
from typing import List, Dict, Optional
from app.core.redis_client import get_redis_client


class RedisQueueManager:
    """Manage Redis queues directly for advanced use cases"""
    
    def __init__(self, redis_url: str = None):
        """
        Initialize Redis queue manager
        
        Args:
            redis_url: Optional Redis URL (uses default from config if not provided)
        """
        if redis_url:
            self.redis_client = redis.Redis.from_url(redis_url, decode_responses=False)
        else:
            self.redis_client = get_redis_client()
    
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
        
        # Push to list (left push for queue behavior - FIFO)
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
        """
        Get the number of tasks in queue
        
        Args:
            queue_name: Name of the queue
            
        Returns:
            Number of tasks in queue
        """
        return self.redis_client.llen(queue_name)
    
    def get_queue_tasks(self, queue_name: str, limit: int = 10) -> List[dict]:
        """
        Get tasks from queue without removing them
        
        Args:
            queue_name: Name of the queue
            limit: Maximum number of tasks to return
            
        Returns:
            List of task dictionaries
        """
        tasks = self.redis_client.lrange(queue_name, 0, limit - 1)
        return [json.loads(task.decode("utf-8")) for task in tasks]
    
    def clear_queue(self, queue_name: str) -> int:
        """
        Clear all tasks from queue
        
        Args:
            queue_name: Name of the queue
            
        Returns:
            Number of tasks removed
        """
        return self.redis_client.delete(queue_name)
    
    def move_task(self, from_queue: str, to_queue: str) -> Optional[dict]:
        """
        Move a task from one queue to another
        
        Args:
            from_queue: Source queue name
            to_queue: Destination queue name
            
        Returns:
            Moved task dictionary or None
        """
        task = self.pop_task(from_queue)
        if task:
            self.push_task(to_queue, task)
        return task
    
    def get_all_queues(self) -> List[str]:
        """
        Get list of all queue names (keys matching queue pattern)
        
        Returns:
            List of queue names
        """
        # This is a simple implementation - in production you might want
        # to track queue names separately or use a naming convention
        keys = self.redis_client.keys("*")
        return [key.decode("utf-8") if isinstance(key, bytes) else key for key in keys]
