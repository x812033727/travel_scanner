import hashlib
import hmac
import ipaddress
import logging
from collections.abc import Awaitable, Mapping
from datetime import UTC, datetime
from functools import lru_cache
from typing import Any, cast
from uuid import UUID

from fastapi import Request
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import get_settings
from app.problems import AppError

logger = logging.getLogger(__name__)


@lru_cache
def get_redis() -> Redis:
    return cast(Redis, Redis.from_url(get_settings().redis_url, decode_responses=True))


PROXY_TOKEN_HEADER = "X-Travel-Proxy-Token"


def _from_our_proxy(headers: Mapping[str, str]) -> bool:
    """Whether this request carries our BFF's shared token.

    Only meaningful once a token is configured. Until then every caller passes, which
    is the behaviour this replaced: a token present on the API but missing from the web
    container would stop every forwarded address being believed at once, collapsing all
    visitors into the web container's single bucket.
    """
    expected = get_settings().internal_proxy_token
    if not expected:
        return True
    presented = headers.get(PROXY_TOKEN_HEADER) or ""
    if hmac.compare_digest(presented, expected):
        return True
    # Loud, because the same silence covers "someone forged a header" and "the token was
    # rolled on one side only", and the second is the one that quietly degrades metering.
    logger.warning("a forwarded address arrived without our proxy token; ignoring it")
    return False


def forwarded_client_ip(headers: Mapping[str, str]) -> str | None:
    """The caller's address as the BFF reported it, or ``None``.

    ``None`` covers four things on purpose: we are not configured to believe the header,
    it did not come from our own proxy, nobody set it, or what arrived was not an
    address. All four mean the same thing to a caller -- there is no address worth
    keying on.
    """
    if not get_settings().trust_proxy_client_ip:
        return None
    forwarded = headers.get("X-Travel-Client-IP")
    if not forwarded:
        return None
    if not _from_our_proxy(headers):
        return None
    try:
        return str(ipaddress.ip_address(forwarded.strip()))
    except ValueError:
        return None


def client_ip(request: Request) -> str:
    return forwarded_client_ip(request.headers) or (
        request.client.host if request.client else "unknown"
    )


def _rate_key(namespace: str, identifier: str) -> str:
    digest = hashlib.sha256(identifier.encode("utf-8")).hexdigest()
    return f"rate:{namespace}:{digest}"


_WINDOW_SCRIPT = (
    "local n=redis.call('INCR',KEYS[1]); "
    "if n==1 then redis.call('EXPIRE',KEYS[1],ARGV[1]) end; return n"
)


async def _incr_window(namespace: str, identifier: str, *, window_seconds: int) -> int | None:
    """Count one hit in this window, or ``None`` when Redis could not be reached.

    What an unreachable Redis means is the caller's decision, and the two callers
    disagree: guarding a login it has to be a refusal, guarding a public page it
    has to be a shrug. Returning the ambiguity keeps that choice where it belongs.
    """
    try:
        count = await cast(
            Awaitable[Any],
            get_redis().eval(
                _WINDOW_SCRIPT, 1, _rate_key(namespace, identifier), str(window_seconds)
            ),
        )
    except RedisError:
        logger.warning("rate limit window %s could not be counted", namespace, exc_info=True)
        return None
    return int(count)


async def enforce_named_rate_limit(
    namespace: str,
    identifier: str,
    *,
    limit: int,
    window_seconds: int,
) -> None:
    count = await _incr_window(namespace, identifier, window_seconds=window_seconds)
    if count is None:
        raise AppError(503, "rate_limit_unavailable", "安全驗證服務暫時無法使用")
    if count > limit:
        raise AppError(429, "rate_limit_exceeded", "請求過於頻繁，請稍後再試")


async def over_named_rate_limit(
    namespace: str,
    identifier: str,
    *,
    limit: int,
    window_seconds: int,
) -> bool:
    """Whether this caller has spent the window, failing **open**.

    The counterpart to :func:`enforce_named_rate_limit` for traffic where being
    wrong in the strict direction is the worse outcome. A public catalogue page
    that goes dark because Redis blinked is a worse failure than a scrape that
    went uncounted for the length of the blink.
    """
    count = await _incr_window(namespace, identifier, window_seconds=window_seconds)
    return count is not None and count > limit


async def record_rate_limit_hit(namespace: str, identifier: str) -> None:
    """Keep a week of daily counts per source, so a threshold can be judged before it bites.

    The source is stored hashed, like the counter keys themselves: knowing that one
    address accounts for most of a day's hits is the whole question, and the address
    itself is not needed to answer it.
    """
    digest = hashlib.sha256(identifier.encode("utf-8")).hexdigest()[:16]
    key = f"abuse:{namespace}:{datetime.now(UTC).date().isoformat()}"
    try:
        redis = get_redis()
        await cast(Awaitable[Any], redis.hincrby(key, digest, 1))
        await cast(Awaitable[Any], redis.expire(key, 7 * 86_400))
    except RedisError:
        logger.warning("could not record a %s hit", namespace, exc_info=True)


async def refund_named_rate_limit(namespace: str, identifier: str) -> None:
    """Give back the one slot a call counted but could not use.

    For a request the server itself could not serve — every planner provider
    down, say — so an outage does not also cost the caller an hour of the
    budget that other features draw on. Never goes below zero.
    """
    script = (
        "local n=redis.call('GET',KEYS[1]); "
        "if n and tonumber(n)>0 then return redis.call('DECR',KEYS[1]) end; return 0"
    )
    try:
        await cast(Awaitable[Any], get_redis().eval(script, 1, _rate_key(namespace, identifier)))
    except RedisError:
        return


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
