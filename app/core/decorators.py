from functools import wraps
from typing import Optional, Callable, Any
from .cache import cache

def cached(
    key_prefix: str,
    ttl: Optional[int] = None,
    invalidate_patterns: Optional[list[str]] = None
):
    """
    Decorator to cache function results in Redis.
    
    Args:
        key_prefix: Prefix for the cache key
        ttl: Optional TTL in seconds
        invalidate_patterns: Optional list of patterns to clear when setting new value
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Generate cache key from function args
            cache_key = f"{key_prefix}:"
            
            # Add args to key (skip self)
            if len(args) > 1:  # First arg is self
                cache_key += ":".join(str(arg) for arg in args[1:])
            
            # Add kwargs to key
            if kwargs:
                cache_key += ":" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            
            # Try to get from cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function if not in cache
            result = await func(*args, **kwargs)
            
            # Cache the result
            if result is not None:
                await cache.set(cache_key, result, ttl)
                
                # Clear invalidation patterns if specified
                if invalidate_patterns:
                    for pattern in invalidate_patterns:
                        await cache.clear_pattern(pattern)
            
            return result
        return wrapper
    return decorator 