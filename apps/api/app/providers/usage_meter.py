from __future__ import annotations

from calendar import monthrange
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Any, cast
from zoneinfo import ZoneInfo

from redis.asyncio import Redis
from redis.exceptions import RedisError

GOOGLE_MAPS_PROVIDER = "google_maps"
GOOGLE_BILLING_TIMEZONE = ZoneInfo("America/Los_Angeles")
GOOGLE_USAGE_HISTORY_MONTHS = 6
GOOGLE_USAGE_RETENTION_DAYS = 400
GOOGLE_MAPS_OPERATIONS = (
    "places_autocomplete",
    "place_details",
    "places_text_search",
    "places_photo",
    "routes",
    "weather_current",
    "weather_daily_forecast",
)


@dataclass(frozen=True)
class GoogleSkuDefinition:
    sku: str
    label: str
    category: str
    operations: tuple[str, ...]


GOOGLE_SKUS = (
    GoogleSkuDefinition(
        "autocomplete_requests",
        "Autocomplete Requests",
        "essentials",
        ("places_autocomplete",),
    ),
    GoogleSkuDefinition(
        "place_details_enterprise",
        "Place Details Enterprise",
        "enterprise",
        ("place_details",),
    ),
    GoogleSkuDefinition(
        "text_search_enterprise",
        "Text Search Enterprise",
        "enterprise",
        ("places_text_search",),
    ),
    GoogleSkuDefinition(
        "place_details_photos",
        "Place Details Photos",
        "enterprise",
        ("places_photo",),
    ),
    GoogleSkuDefinition(
        "compute_routes_essentials",
        "Compute Routes Essentials",
        "essentials",
        ("routes",),
    ),
    GoogleSkuDefinition(
        "weather_usage",
        "Weather Usage",
        "essentials",
        ("weather_current", "weather_daily_forecast"),
    ),
)


@dataclass(frozen=True)
class ProviderSkuUsageSnapshot:
    sku: str
    label: str
    category: str
    operations: tuple[str, ...]
    used: int
    free_limit: int
    free_usage: int
    free_remaining: int
    billable_overage: int
    percentage: float


@dataclass(frozen=True)
class ProviderMonthlyUsageSnapshot:
    period: str
    period_start: date
    period_end: date
    used: int
    free_limit: int
    free_usage: int
    free_remaining: int
    billable_overage: int
    breakdown: dict[str, int]
    sku_usage: tuple[ProviderSkuUsageSnapshot, ...]
    tracking_started_at: datetime | None


@dataclass(frozen=True)
class ProviderUsageSnapshot:
    period: str
    period_start: date
    period_end: date
    used: int | None
    monthly_limit: int
    remaining: int | None
    percentage: float | None
    free_limit: int
    free_usage: int | None
    free_remaining: int | None
    billable_overage: int | None
    breakdown: dict[str, int]
    sku_usage: tuple[ProviderSkuUsageSnapshot, ...]
    monthly_history: tuple[ProviderMonthlyUsageSnapshot, ...]
    tracking_started_at: datetime | None
    observed_at: datetime
    available: bool
    billing_timezone: str = "America/Los_Angeles"
    pricing_region: str = "global"


def _billing_now(now: datetime) -> datetime:
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    return now.astimezone(GOOGLE_BILLING_TIMEZONE)


def _month_window(now: datetime) -> tuple[date, date]:
    start = date(now.year, now.month, 1)
    end = date(now.year, now.month, monthrange(now.year, now.month)[1])
    return start, end


def _month_at(now: datetime, offset: int) -> datetime:
    month_index = now.year * 12 + now.month - 1 + offset
    year, zero_based_month = divmod(month_index, 12)
    return now.replace(
        year=year,
        month=zero_based_month + 1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def _usage_key(now: datetime) -> str:
    return f"provider-usage:{GOOGLE_MAPS_PROVIDER}:{now:%Y-%m}"


def _text(value: object) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


def _sku_snapshots(
    breakdown: dict[str, int],
    *,
    essentials_free_limit: int,
    pro_free_limit: int,
    enterprise_free_limit: int,
) -> tuple[ProviderSkuUsageSnapshot, ...]:
    limits = {
        "essentials": essentials_free_limit,
        "pro": pro_free_limit,
        "enterprise": enterprise_free_limit,
    }
    snapshots: list[ProviderSkuUsageSnapshot] = []
    for definition in GOOGLE_SKUS:
        used = sum(breakdown[operation] for operation in definition.operations)
        free_limit = limits[definition.category]
        snapshots.append(
            ProviderSkuUsageSnapshot(
                sku=definition.sku,
                label=definition.label,
                category=definition.category,
                operations=definition.operations,
                used=used,
                free_limit=free_limit,
                free_usage=min(used, free_limit),
                free_remaining=max(0, free_limit - used),
                billable_overage=max(0, used - free_limit),
                percentage=round(used / free_limit * 100, 1),
            )
        )
    return tuple(snapshots)


def _monthly_snapshot(
    month: datetime,
    values: dict[str, str],
    *,
    essentials_free_limit: int,
    pro_free_limit: int,
    enterprise_free_limit: int,
) -> ProviderMonthlyUsageSnapshot:
    period_start, period_end = _month_window(month)
    breakdown = {
        operation: int(values.get(f"operation:{operation}", 0))
        for operation in GOOGLE_MAPS_OPERATIONS
    }
    sku_usage = _sku_snapshots(
        breakdown,
        essentials_free_limit=essentials_free_limit,
        pro_free_limit=pro_free_limit,
        enterprise_free_limit=enterprise_free_limit,
    )
    started = values.get("tracking_started_at")
    return ProviderMonthlyUsageSnapshot(
        period=f"{month:%Y-%m}",
        period_start=period_start,
        period_end=period_end,
        used=int(values.get("total", 0)),
        free_limit=sum(item.free_limit for item in sku_usage),
        free_usage=sum(item.free_usage for item in sku_usage),
        free_remaining=sum(item.free_remaining for item in sku_usage),
        billable_overage=sum(item.billable_overage for item in sku_usage),
        breakdown=breakdown,
        sku_usage=sku_usage,
        tracking_started_at=datetime.fromisoformat(started) if started else None,
    )


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
    billing_month = _billing_now(observed_at)
    _, period_end = _month_window(billing_month)
    expires_at = datetime.combine(
        period_end + timedelta(days=1),
        time.min,
        tzinfo=GOOGLE_BILLING_TIMEZONE,
    ) + timedelta(days=GOOGLE_USAGE_RETENTION_DAYS)
    key = _usage_key(billing_month)
    try:
        pipeline = redis.pipeline(transaction=True)
        pipeline.hincrby(key, "total", 1)
        pipeline.hincrby(key, f"operation:{operation}", 1)
        pipeline.hsetnx(key, "tracking_started_at", observed_at.isoformat())
        pipeline.expireat(key, expires_at)
        await pipeline.execute()
    except RedisError:
        # Usage telemetry must never turn a successful provider request into an application error.
        return


async def google_maps_usage_snapshot(
    redis: Redis,
    monthly_limit: int | None = None,
    *,
    essentials_free_limit: int = 10_000,
    pro_free_limit: int = 5_000,
    enterprise_free_limit: int = 1_000,
    history_months: int = GOOGLE_USAGE_HISTORY_MONTHS,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    """Return app-observed requests against global per-SKU monthly free thresholds.

    ``monthly_limit`` remains accepted for backwards compatibility but is not used: Google
    applies free usage independently to every SKU.
    """
    del monthly_limit
    observed_at = now or datetime.now(UTC)
    billing_now = _billing_now(observed_at)
    period_start, period_end = _month_window(billing_now)
    months = tuple(_month_at(billing_now, -offset) for offset in range(max(1, history_months)))
    try:
        raw_months = [
            await cast(Awaitable[dict[Any, Any]], redis.hgetall(_usage_key(month)))
            for month in months
        ]
    except RedisError:
        return ProviderUsageSnapshot(
            period=f"{billing_now:%Y-%m}",
            period_start=period_start,
            period_end=period_end,
            used=None,
            monthly_limit=0,
            remaining=None,
            percentage=None,
            free_limit=0,
            free_usage=None,
            free_remaining=None,
            billable_overage=None,
            breakdown={},
            sku_usage=(),
            monthly_history=(),
            tracking_started_at=None,
            observed_at=observed_at,
            available=False,
        )

    history = tuple(
        _monthly_snapshot(
            month,
            {_text(key): _text(value) for key, value in raw.items()},
            essentials_free_limit=essentials_free_limit,
            pro_free_limit=pro_free_limit,
            enterprise_free_limit=enterprise_free_limit,
        )
        for month, raw in zip(months, raw_months, strict=True)
    )
    current = history[0]
    percentage = (
        round(current.free_usage / current.free_limit * 100, 1)
        if current.free_limit
        else 0.0
    )
    return ProviderUsageSnapshot(
        period=current.period,
        period_start=current.period_start,
        period_end=current.period_end,
        used=current.used,
        monthly_limit=current.free_limit,
        remaining=current.free_remaining,
        percentage=percentage,
        free_limit=current.free_limit,
        free_usage=current.free_usage,
        free_remaining=current.free_remaining,
        billable_overage=current.billable_overage,
        breakdown=current.breakdown,
        sku_usage=current.sku_usage,
        monthly_history=history,
        tracking_started_at=current.tracking_started_at,
        observed_at=observed_at,
        available=True,
    )
