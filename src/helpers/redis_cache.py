import functools
import hashlib
import inspect
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar, cast

from redis.asyncio import Redis
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


async def init_redis() -> None:
    try:
        await redis.ping()
        print("Redis > Connected.")
    except RedisError as e:
        print(f"Redis > Connection failed, cache will be skipped: {e}")


async def close_redis() -> None:
    try:
        await redis.aclose()
        print("Redis > Connection closed.")
    except RedisError as e:
        print(f"Redis > Failed to close connection: {e}")


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


def redis_cache(
    ttl: int = 60,
) -> Callable[[Callable[P, T] | Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    def decorator(
        func: Callable[P, T] | Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = _make_cache_key(func, args, kwargs)

            try:
                cached = await redis.get(cache_key)

                if cached is not None:
                    print(f"Redis cache HIT: {func.__name__}")
                    return cast(T, json.loads(cached))

            except (RedisError, json.JSONDecodeError) as e:
                print(f"Redis cache read failed for {func.__name__}: {e}")

            print(f"Redis cache MISS: {func.__name__}")

            result = func(*args, **kwargs)

            if inspect.isawaitable(result):
                result = await result

            try:
                await redis.set(
                    cache_key,
                    json.dumps(result, default=str),
                    ex=ttl,
                )

            except (RedisError, TypeError) as e:
                print(f"Redis cache write failed for {func.__name__}: {e}")

            return cast(T, result)

        return wrapper

    return decorator
