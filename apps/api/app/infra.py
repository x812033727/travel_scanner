from collections.abc import Awaitable
from functools import lru_cache
from typing import Any, cast
from uuid import UUID

from redis.asyncio import Redis

from app.config import get_settings
from app.problems import AppError


@lru_cache
def get_redis() -> Redis:
    return cast(Redis, Redis.from_url(get_settings().redis_url, decode_responses=True))


async def enforce_rate_limit(user_id: UUID) -> None:
    redis, limit = get_redis(), get_settings().rate_limit_per_minute
    script = (
        "local n=redis.call('INCR',KEYS[1]); "
        "if n==1 then redis.call('EXPIRE',KEYS[1],60) end; return n"
    )
    count = await cast(Awaitable[Any], redis.eval(script, 1, f"rate:{user_id}"))
    if int(count) > limit:
        raise AppError(429, "rate_limit_exceeded", "Too many requests; try again shortly")
