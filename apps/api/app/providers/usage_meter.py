from __future__ import annotations

from calendar import monthrange
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast

from redis.asyncio import Redis
from redis.exceptions import RedisError

GOOGLE_MAPS_PROVIDER = "google_maps"
GOOGLE_MAPS_OPERATIONS = (
    "places_autocomplete",
    "place_details",
    "places_text_search",
    "places_photo",
    "routes",
)


@dataclass(frozen=True)
class ProviderUsageSnapshot:
    period: str
    period_start: date
    period_end: date
    used: int | None
    monthly_limit: int
    remaining: int | None
    percentage: float | None
    breakdown: dict[str, int]
    tracking_started_at: datetime | None
    observed_at: datetime
    available: bool


def _month_window(now: datetime) -> tuple[date, date]:
    start = date(now.year, now.month, 1)
    end = date(now.year, now.month, monthrange(now.year, now.month)[1])
    return start, end


def _usage_key(now: datetime) -> str:
    return f"provider-usage:{GOOGLE_MAPS_PROVIDER}:{now:%Y-%m}"


def _text(value: object) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


async def record_google_maps_request(
    redis: Redis,
    operation: str,
    *,
    now: datetime | None = None,
) -> None:
    """Record one outbound request without making provider availability depend on telemetry."""
    if operation not in GOOGLE_MAPS_OPERATIONS:
        raise ValueError(f"unsupported Google Maps usage operation: {operation}")
    observed_at = now or datetime.now(UTC)
    _, period_end = _month_window(observed_at)
    expires_at = datetime.combine(period_end, datetime.min.time(), tzinfo=UTC) + timedelta(
        days=93
    )
    try:
        pipeline = redis.pipeline(transaction=True)
        pipeline.hincrby(_usage_key(observed_at), "total", 1)
        pipeline.hincrby(_usage_key(observed_at), f"operation:{operation}", 1)
        pipeline.hsetnx(
            _usage_key(observed_at), "tracking_started_at", observed_at.isoformat()
        )
        pipeline.expireat(_usage_key(observed_at), expires_at)
        await pipeline.execute()
    except RedisError:
        # Usage telemetry must never turn a successful provider request into an application error.
        return


async def google_maps_usage_snapshot(
    redis: Redis,
    monthly_limit: int,
    *,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    observed_at = now or datetime.now(UTC)
    period_start, period_end = _month_window(observed_at)
    try:
        raw = await cast(
            Awaitable[dict[Any, Any]], redis.hgetall(_usage_key(observed_at))
        )
    except RedisError:
        return ProviderUsageSnapshot(
            period=f"{observed_at:%Y-%m}",
            period_start=period_start,
            period_end=period_end,
            used=None,
            monthly_limit=monthly_limit,
            remaining=None,
            percentage=None,
            breakdown={},
            tracking_started_at=None,
            observed_at=observed_at,
            available=False,
        )

    values = {_text(key): _text(value) for key, value in raw.items()}
    used = int(values.get("total", 0))
    started = values.get("tracking_started_at")
    breakdown = {
        operation: int(values.get(f"operation:{operation}", 0))
        for operation in GOOGLE_MAPS_OPERATIONS
    }
    return ProviderUsageSnapshot(
        period=f"{observed_at:%Y-%m}",
        period_start=period_start,
        period_end=period_end,
        used=used,
        monthly_limit=monthly_limit,
        remaining=max(0, monthly_limit - used),
        percentage=round(used / monthly_limit * 100, 1),
        breakdown=breakdown,
        tracking_started_at=datetime.fromisoformat(started) if started else None,
        observed_at=observed_at,
        available=True,
    )
