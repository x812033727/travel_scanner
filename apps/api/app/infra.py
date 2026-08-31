import hashlib
import ipaddress
from collections.abc import Awaitable
from functools import lru_cache
from typing import Any, cast
from uuid import UUID

from fastapi import Request
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import get_settings
from app.problems import AppError


@lru_cache
def get_redis() -> Redis:
    return cast(Redis, Redis.from_url(get_settings().redis_url, decode_responses=True))


def client_ip(request: Request) -> str:
    settings = get_settings()
    if settings.trust_proxy_client_ip:
        forwarded = request.headers.get("X-Travel-Client-IP")
        if forwarded:
            try:
                return str(ipaddress.ip_address(forwarded.strip()))
            except ValueError:
                pass
    return request.client.host if request.client else "unknown"


def _rate_key(namespace: str, identifier: str) -> str:
    digest = hashlib.sha256(identifier.encode("utf-8")).hexdigest()
    return f"rate:{namespace}:{digest}"


async def enforce_named_rate_limit(
    namespace: str,
    identifier: str,
    *,
    limit: int,
    window_seconds: int,
) -> None:
    redis = get_redis()
    script = (
        "local n=redis.call('INCR',KEYS[1]); "
        "if n==1 then redis.call('EXPIRE',KEYS[1],ARGV[1]) end; return n"
    )
    try:
        count = await cast(
            Awaitable[Any],
            redis.eval(script, 1, _rate_key(namespace, identifier), str(window_seconds)),
        )
    except RedisError as exc:
        raise AppError(503, "rate_limit_unavailable", "安全驗證服務暫時無法使用") from exc
    if int(count) > limit:
        raise AppError(429, "rate_limit_exceeded", "請求過於頻繁，請稍後再試")


async def clear_named_rate_limit(namespace: str, identifier: str) -> None:
    try:
        await get_redis().delete(_rate_key(namespace, identifier))
    except RedisError:
        return


async def enforce_rate_limit(user_id: UUID) -> None:
    await enforce_named_rate_limit(
        "user",
        str(user_id),
        limit=get_settings().rate_limit_per_minute,
        window_seconds=60,
    )
