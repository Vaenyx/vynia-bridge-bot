import functools
import hashlib
import json
import os
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from redis import Redis
from redis.exceptions import RedisError

P = ParamSpec("P")
T = TypeVar("T")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


def _make_cache_key(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    raw_key = json.dumps(
        {
            "module": func.__module__,
            "function": func.__name__,
            "args": args,
            "kwargs": kwargs,
        },
        sort_keys=True,
        default=str,
    )

    hashed = hashlib.sha256(raw_key.encode()).hexdigest()
    return f"cache:{func.__module__}.{func.__name__}:{hashed}"


def redis_cache(ttl: int = 60) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = _make_cache_key(func, args, kwargs)

            try:
                cached = redis.get(cache_key)
                if cached is not None:
                    print(f"Redis cache HIT: {func.__name__}")
                    return json.loads(cached)
            except (RedisError, json.JSONDecodeError) as e:
                print(f"Redis cache read failed for {func.__name__}: {e}")

            print(f"Redis cache MISS: {func.__name__}")
            result = func(*args, **kwargs)

            try:
                redis.set(
                    cache_key,
                    json.dumps(result, default=str),
                    ex=ttl,
                )
            except (RedisError, TypeError) as e:
                print(f"Redis cache write failed for {func.__name__}: {e}")

            return result

        return wrapper

    return decorator
