from typing import Optional, Any
import json
from redis.asyncio import Redis
from .config import settings

class CacheService:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self.ttl = settings.REDIS_CACHE_TTL

    async def connect(self):
        """Connect to Redis if not already connected."""
        if not self.redis:
            self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def disconnect(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
            self.redis = None

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        await self.connect()
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in cache with optional TTL."""
        await self.connect()
        try:
            await self.redis.set(
                key,
                json.dumps(value),
                ex=ttl if ttl is not None else self.ttl
            )
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        await self.connect()
        return bool(await self.redis.delete(key))

    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching a pattern."""
        await self.connect()
        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0

# Create a global cache instance
cache = CacheService() 