from __future__ import annotations

from calendar import monthrange
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Any, Literal, cast
from zoneinfo import ZoneInfo

from redis.asyncio import Redis
from redis.exceptions import RedisError, WatchError

GOOGLE_MAPS_PROVIDER = "google_maps"
YOUTUBE_GUIDES_PROVIDER = "youtube_guides"
GOOGLE_BILLING_TIMEZONE = ZoneInfo("America/Los_Angeles")
GOOGLE_USAGE_HISTORY_MONTHS = 6
GOOGLE_USAGE_RETENTION_DAYS = 400
GOOGLE_MAPS_OPERATIONS = (
    "places_autocomplete",
    "place_details",
    "place_id_refresh",
    "places_text_search_ids_only",
    "places_text_search",
    "places_text_search_locate",
    "places_aggregate_restaurants",
    "places_nearby_restaurants",
    "place_details_restaurant",
    "places_photo",
    "routes",
    "weather_current",
    "weather_daily_forecast",
)
NAVER_MAPS_PROVIDER = "naver_maps"
NAVER_BILLING_TIMEZONE = ZoneInfo("Asia/Seoul")
NAVER_MAPS_OPERATIONS = ("local_search", "geocode", "directions")
NAVITIME_PROVIDER = "navitime"
NAVITIME_BILLING_TIMEZONE = ZoneInfo("Asia/Tokyo")
NAVITIME_OPERATIONS = ("route_transit",)
EKISPERT_PROVIDER = "ekispert"
EKISPERT_BILLING_TIMEZONE = ZoneInfo("Asia/Tokyo")
EKISPERT_OPERATIONS = ("search_course",)
ODSAY_PROVIDER = "odsay"
ODSAY_BILLING_TIMEZONE = ZoneInfo("Asia/Seoul")
ODSAY_OPERATIONS = ("search_pub_trans_path",)
YOUTUBE_OPERATIONS = ("search_list", "videos_list")


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
        ("place_details", "place_details_restaurant"),
    ),
    GoogleSkuDefinition(
        "text_search_enterprise",
        "Text Search Enterprise",
        "enterprise",
        ("places_text_search",),
    ),
    GoogleSkuDefinition(
        "text_search_pro",
        "Text Search Pro",
        "pro",
        ("places_text_search_locate",),
    ),
    GoogleSkuDefinition(
        "places_aggregate",
        "Places Aggregate API",
        "pro",
        ("places_aggregate_restaurants",),
    ),
    GoogleSkuDefinition(
        "nearby_search_enterprise",
        "Nearby Search Enterprise",
        "enterprise",
        ("places_nearby_restaurants",),
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
    period_kind: Literal["month", "day"] = "month"
    billing_timezone: str = "America/Los_Angeles"
    pricing_region: str = "global"


def _billing_now(now: datetime) -> datetime:
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    return now.astimezone(GOOGLE_BILLING_TIMEZONE)


def google_billing_date(now: datetime | None = None) -> date:
    """The day Google is currently counting against, for anything that mirrors its quota.

    Google resets daily quotas at midnight Pacific. A counter keyed on the local date
    hands out a second full allowance seven to eight hours before Google's day ends,
    so two of its windows land inside one of Google's.
    """

    return _billing_now(now or datetime.now(UTC)).date()


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


def _youtube_usage_key(now: datetime) -> str:
    return f"provider-usage:{YOUTUBE_GUIDES_PROVIDER}:{now:%Y-%m-%d}"


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


async def reserve_google_maps_request(
    redis: Redis,
    operation: str,
    monthly_budget: int,
    *,
    shared_operations: tuple[str, ...] = (),
    shared_monthly_budget: int | None = None,
    now: datetime | None = None,
) -> bool:
    """Atomically reserve and meter a budget-controlled Google request.

    Restaurant discovery fails closed when Redis cannot verify the configured
    safety limit, avoiding an unmetered paid request. The reservation remains
    counted when Google rejects the outbound call because it still represents
    an attempted provider request.
    """
    if operation not in GOOGLE_MAPS_OPERATIONS:
        raise ValueError(f"unsupported Google Maps usage operation: {operation}")
    if any(item not in GOOGLE_MAPS_OPERATIONS for item in shared_operations):
        raise ValueError("unsupported Google Maps shared usage operation")
    if shared_monthly_budget is not None and not shared_operations:
        raise ValueError("shared_operations are required with shared_monthly_budget")
    observed_at = now or datetime.now(UTC)
    billing_month = _billing_now(observed_at)
    _, period_end = _month_window(billing_month)
    expires_at = datetime.combine(
        period_end + timedelta(days=1),
        time.min,
        tzinfo=GOOGLE_BILLING_TIMEZONE,
    ) + timedelta(days=GOOGLE_USAGE_RETENTION_DAYS)
    key = _usage_key(billing_month)
    operation_field = f"operation:{operation}"
    try:
        async with redis.pipeline(transaction=True) as pipeline:
            while True:
                try:
                    await pipeline.watch(key)
                    current_value = await cast(Awaitable[Any], pipeline.hget(key, operation_field))
                    current = int(current_value or 0)
                    if current >= monthly_budget:
                        return False
                    if shared_monthly_budget is not None:
                        shared_values = await cast(
                            Awaitable[Any],
                            pipeline.hmget(
                                key,
                                [f"operation:{item}" for item in shared_operations],
                            ),
                        )
                        shared_used = sum(int(item or 0) for item in shared_values)
                        if shared_used >= shared_monthly_budget:
                            return False
                    pipeline.multi()  # type: ignore[no-untyped-call]
                    pipeline.hincrby(key, "total", 1)
                    pipeline.hincrby(key, operation_field, 1)
                    pipeline.hsetnx(key, "tracking_started_at", observed_at.isoformat())
                    pipeline.expireat(key, expires_at)
                    await pipeline.execute()
                    return True
                except WatchError:
                    continue
    except RedisError:
        return False


async def record_youtube_request(
    redis: Redis,
    operation: str,
    *,
    now: datetime | None = None,
) -> None:
    """Record a YouTube Data API request in the current Pacific Time quota day."""
    if operation not in YOUTUBE_OPERATIONS:
        raise ValueError(f"unsupported YouTube usage operation: {operation}")
    observed_at = now or datetime.now(UTC)
    billing_day = _billing_now(observed_at)
    expires_at = datetime.combine(
        billing_day.date() + timedelta(days=GOOGLE_USAGE_RETENTION_DAYS),
        time.min,
        tzinfo=GOOGLE_BILLING_TIMEZONE,
    )
    key = _youtube_usage_key(billing_day)
    try:
        pipeline = redis.pipeline(transaction=True)
        pipeline.hincrby(key, "total", 1)
        pipeline.hincrby(key, f"operation:{operation}", 1)
        pipeline.hsetnx(key, "tracking_started_at", observed_at.isoformat())
        pipeline.expireat(key, expires_at)
        await pipeline.execute()
    except RedisError:
        return


async def youtube_usage_snapshot(
    redis: Redis,
    *,
    search_daily_free_limit: int = 100,
    core_daily_free_limit: int = 10_000,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    """Return app-observed YouTube calls against the two daily quota buckets."""
    observed_at = now or datetime.now(UTC)
    billing_now = _billing_now(observed_at)
    period = f"{billing_now:%Y-%m-%d}"
    try:
        raw = await cast(Awaitable[dict[Any, Any]], redis.hgetall(_youtube_usage_key(billing_now)))
    except RedisError:
        return ProviderUsageSnapshot(
            period=period,
            period_start=billing_now.date(),
            period_end=billing_now.date(),
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
            period_kind="day",
        )

    values = {_text(key): _text(value) for key, value in raw.items()}
    breakdown = {
        operation: int(values.get(f"operation:{operation}", 0)) for operation in YOUTUBE_OPERATIONS
    }
    definitions = (
        (
            "search_queries",
            "Search Queries (search.list)",
            "search",
            ("search_list",),
            search_daily_free_limit,
        ),
        (
            "core_api_units",
            "Core API units (videos.list)",
            "core",
            ("videos_list",),
            core_daily_free_limit,
        ),
    )
    sku_usage = tuple(
        ProviderSkuUsageSnapshot(
            sku=sku,
            label=label,
            category=category,
            operations=operations,
            used=(used := sum(breakdown[operation] for operation in operations)),
            free_limit=free_limit,
            free_usage=min(used, free_limit),
            free_remaining=max(0, free_limit - used),
            billable_overage=max(0, used - free_limit),
            percentage=round(used / free_limit * 100, 1),
        )
        for sku, label, category, operations, free_limit in definitions
    )
    free_limit = sum(item.free_limit for item in sku_usage)
    free_usage = sum(item.free_usage for item in sku_usage)
    free_remaining = sum(item.free_remaining for item in sku_usage)
    billable_overage = sum(item.billable_overage for item in sku_usage)
    started = values.get("tracking_started_at")
    return ProviderUsageSnapshot(
        period=period,
        period_start=billing_now.date(),
        period_end=billing_now.date(),
        used=sum(breakdown.values()),
        monthly_limit=free_limit,
        remaining=free_remaining,
        percentage=round(free_usage / free_limit * 100, 1),
        free_limit=free_limit,
        free_usage=free_usage,
        free_remaining=free_remaining,
        billable_overage=billable_overage,
        breakdown=breakdown,
        sku_usage=sku_usage,
        monthly_history=(),
        tracking_started_at=datetime.fromisoformat(started) if started else None,
        observed_at=observed_at,
        available=True,
        period_kind="day",
    )


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
        round(current.free_usage / current.free_limit * 100, 1) if current.free_limit else 0.0
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


def _naver_usage_key(now: datetime) -> str:
    return f"provider-usage:{NAVER_MAPS_PROVIDER}:{now:%Y-%m}"


async def record_naver_maps_request(
    redis: Redis,
    operation: str,
    *,
    now: datetime | None = None,
) -> None:
    """Record server-observed NAVER API calls without affecting provider availability."""
    if operation not in NAVER_MAPS_OPERATIONS:
        raise ValueError(f"unsupported NAVER Maps usage operation: {operation}")
    observed_at = now or datetime.now(UTC)
    billing_month = observed_at.astimezone(NAVER_BILLING_TIMEZONE)
    _, period_end = _month_window(billing_month)
    expires_at = datetime.combine(
        period_end + timedelta(days=1),
        time.min,
        tzinfo=NAVER_BILLING_TIMEZONE,
    ) + timedelta(days=GOOGLE_USAGE_RETENTION_DAYS)
    key = _naver_usage_key(billing_month)
    try:
        pipeline = redis.pipeline(transaction=True)
        pipeline.hincrby(key, "total", 1)
        pipeline.hincrby(key, f"operation:{operation}", 1)
        pipeline.hsetnx(key, "tracking_started_at", observed_at.isoformat())
        pipeline.expireat(key, expires_at)
        await pipeline.execute()
    except RedisError:
        return


async def _monthly_request_snapshot(
    redis: Redis,
    *,
    key_for: Callable[[datetime], str],
    operations: tuple[str, ...],
    billing_timezone: ZoneInfo,
    billing_timezone_name: str,
    pricing_region: str,
    monthly_limit: int,
    history_months: int,
    now: datetime | None,
) -> ProviderUsageSnapshot:
    """Summarise a per-month request counter kept in one Redis hash per billing month."""
    observed_at = now or datetime.now(UTC)
    billing_now = observed_at.astimezone(billing_timezone)
    period_start, period_end = _month_window(billing_now)
    months = tuple(_month_at(billing_now, -offset) for offset in range(max(1, history_months)))
    try:
        raw_months = [
            await cast(Awaitable[dict[Any, Any]], redis.hgetall(key_for(month))) for month in months
        ]
    except RedisError:
        return ProviderUsageSnapshot(
            period=f"{billing_now:%Y-%m}",
            period_start=period_start,
            period_end=period_end,
            used=None,
            monthly_limit=monthly_limit,
            remaining=None,
            percentage=None,
            free_limit=monthly_limit,
            free_usage=None,
            free_remaining=None,
            billable_overage=None,
            breakdown={},
            sku_usage=(),
            monthly_history=(),
            tracking_started_at=None,
            observed_at=observed_at,
            available=False,
            billing_timezone=billing_timezone_name,
            pricing_region=pricing_region,
        )

    history: list[ProviderMonthlyUsageSnapshot] = []
    for month, raw in zip(months, raw_months, strict=True):
        values = {_text(key): _text(value) for key, value in raw.items()}
        used = int(values.get("total", 0))
        breakdown = {
            operation: int(values.get(f"operation:{operation}", 0)) for operation in operations
        }
        month_start, month_end = _month_window(month)
        started = values.get("tracking_started_at")
        history.append(
            ProviderMonthlyUsageSnapshot(
                period=f"{month:%Y-%m}",
                period_start=month_start,
                period_end=month_end,
                used=used,
                free_limit=monthly_limit,
                free_usage=min(used, monthly_limit) if monthly_limit else 0,
                free_remaining=max(0, monthly_limit - used) if monthly_limit else 0,
                billable_overage=max(0, used - monthly_limit) if monthly_limit else 0,
                breakdown=breakdown,
                sku_usage=(),
                tracking_started_at=datetime.fromisoformat(started) if started else None,
            )
        )
    current = history[0]
    return ProviderUsageSnapshot(
        period=current.period,
        period_start=current.period_start,
        period_end=current.period_end,
        used=current.used,
        monthly_limit=monthly_limit,
        remaining=max(0, monthly_limit - current.used) if monthly_limit else None,
        percentage=round(current.used / monthly_limit * 100, 1) if monthly_limit else None,
        free_limit=monthly_limit,
        free_usage=min(current.used, monthly_limit) if monthly_limit else None,
        free_remaining=max(0, monthly_limit - current.used) if monthly_limit else None,
        billable_overage=max(0, current.used - monthly_limit) if monthly_limit else None,
        breakdown=current.breakdown,
        sku_usage=(),
        monthly_history=tuple(history),
        tracking_started_at=current.tracking_started_at,
        observed_at=observed_at,
        available=True,
        billing_timezone=billing_timezone_name,
        pricing_region=pricing_region,
    )


async def naver_maps_usage_snapshot(
    redis: Redis,
    monthly_limit: int = 0,
    *,
    history_months: int = GOOGLE_USAGE_HISTORY_MONTHS,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    """Return app-observed NAVER server requests.

    The optional limit is administrator supplied and is not presented as NAVER billing data.
    Browser Dynamic Map loads are intentionally outside this meter.
    """
    return await _monthly_request_snapshot(
        redis,
        key_for=_naver_usage_key,
        operations=NAVER_MAPS_OPERATIONS,
        billing_timezone=NAVER_BILLING_TIMEZONE,
        billing_timezone_name="Asia/Seoul",
        pricing_region="kr",
        monthly_limit=monthly_limit,
        history_months=history_months,
        now=now,
    )


def _navitime_usage_key(now: datetime) -> str:
    return f"provider-usage:{NAVITIME_PROVIDER}:{now:%Y-%m}"


async def reserve_navitime_request(
    redis: Redis,
    monthly_budget: int,
    *,
    operation: str = "route_transit",
    now: datetime | None = None,
) -> bool:
    """Atomically reserve one NAVITIME request against the calendar-month budget.

    RapidAPI enforces its own hard monthly quota, so this guard exists to stop paid
    overage plans and abusive bursts before they reach the gateway. A budget of zero
    keeps counting without blocking; Redis failures fail closed.
    """
    if operation not in NAVITIME_OPERATIONS:
        raise ValueError(f"unsupported NAVITIME usage operation: {operation}")
    observed_at = now or datetime.now(UTC)
    billing_month = observed_at.astimezone(NAVITIME_BILLING_TIMEZONE)
    _, period_end = _month_window(billing_month)
    expires_at = datetime.combine(
        period_end + timedelta(days=1),
        time.min,
        tzinfo=NAVITIME_BILLING_TIMEZONE,
    ) + timedelta(days=GOOGLE_USAGE_RETENTION_DAYS)
    key = _navitime_usage_key(billing_month)
    try:
        async with redis.pipeline(transaction=True) as pipeline:
            while True:
                try:
                    await pipeline.watch(key)
                    current_value = await cast(Awaitable[Any], pipeline.hget(key, "total"))
                    if monthly_budget > 0 and int(current_value or 0) >= monthly_budget:
                        return False
                    pipeline.multi()  # type: ignore[no-untyped-call]
                    pipeline.hincrby(key, "total", 1)
                    pipeline.hincrby(key, f"operation:{operation}", 1)
                    pipeline.hsetnx(key, "tracking_started_at", observed_at.isoformat())
                    pipeline.expireat(key, expires_at)
                    await pipeline.execute()
                    return True
                except WatchError:
                    continue
    except RedisError:
        return False


async def navitime_usage_snapshot(
    redis: Redis,
    monthly_limit: int = 0,
    *,
    history_months: int = GOOGLE_USAGE_HISTORY_MONTHS,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    """Return app-observed NAVITIME route requests against the configured monthly cap.

    ``reserve_navitime_request`` enforces the cap per calendar month in Japan time, whereas
    RapidAPI resets its own quota on the subscription anniversary.
    """
    return await _monthly_request_snapshot(
        redis,
        key_for=_navitime_usage_key,
        operations=NAVITIME_OPERATIONS,
        billing_timezone=NAVITIME_BILLING_TIMEZONE,
        billing_timezone_name="Asia/Tokyo",
        pricing_region="jp",
        monthly_limit=monthly_limit,
        history_months=history_months,
        now=now,
    )


def _ekispert_usage_key(now: datetime) -> str:
    return f"provider-usage:{EKISPERT_PROVIDER}:{now:%Y-%m}"


async def reserve_ekispert_request(
    redis: Redis,
    monthly_budget: int,
    *,
    operation: str = "search_course",
    now: datetime | None = None,
) -> bool:
    """Atomically reserve one Ekispert request against the configured monthly cap."""
    return await _reserve_hash_request(
        redis,
        key=_ekispert_usage_key,
        operations=EKISPERT_OPERATIONS,
        operation=operation,
        limit=monthly_budget,
        billing_timezone=EKISPERT_BILLING_TIMEZONE,
        period="month",
        now=now,
    )


async def ekispert_usage_snapshot(
    redis: Redis,
    monthly_limit: int = 0,
    *,
    history_months: int = GOOGLE_USAGE_HISTORY_MONTHS,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    """Return app-observed Ekispert route searches against the monthly hard cap."""
    return await _monthly_request_snapshot(
        redis,
        key_for=_ekispert_usage_key,
        operations=EKISPERT_OPERATIONS,
        billing_timezone=EKISPERT_BILLING_TIMEZONE,
        billing_timezone_name="Asia/Tokyo",
        pricing_region="jp",
        monthly_limit=monthly_limit,
        history_months=history_months,
        now=now,
    )


def _odsay_usage_key(now: datetime) -> str:
    return f"provider-usage:{ODSAY_PROVIDER}:{now:%Y-%m-%d}"


async def _reserve_hash_request(
    redis: Redis,
    *,
    key: Callable[[datetime], str],
    operations: tuple[str, ...],
    operation: str,
    limit: int,
    billing_timezone: ZoneInfo,
    period: Literal["month", "day"],
    now: datetime | None,
) -> bool:
    """Reserve a provider request in Redis and fail closed if the counter is unavailable."""
    if operation not in operations:
        raise ValueError(f"unsupported provider usage operation: {operation}")
    observed_at = now or datetime.now(UTC)
    billing_now = observed_at.astimezone(billing_timezone)
    if period == "month":
        _, period_end = _month_window(billing_now)
        reset_at = datetime.combine(
            period_end + timedelta(days=1), time.min, tzinfo=billing_timezone
        )
    else:
        reset_at = datetime.combine(
            billing_now.date() + timedelta(days=1), time.min, tzinfo=billing_timezone
        )
    expires_at = reset_at + timedelta(days=GOOGLE_USAGE_RETENTION_DAYS)
    usage_key = key(billing_now)
    try:
        async with redis.pipeline(transaction=True) as pipeline:
            while True:
                try:
                    await pipeline.watch(usage_key)
                    current_value = await cast(Awaitable[Any], pipeline.hget(usage_key, "total"))
                    if limit > 0 and int(current_value or 0) >= limit:
                        return False
                    pipeline.multi()  # type: ignore[no-untyped-call]
                    pipeline.hincrby(usage_key, "total", 1)
                    pipeline.hincrby(usage_key, f"operation:{operation}", 1)
                    pipeline.hsetnx(usage_key, "tracking_started_at", observed_at.isoformat())
                    pipeline.expireat(usage_key, expires_at)
                    await pipeline.execute()
                    return True
                except WatchError:
                    continue
    except RedisError:
        return False


async def reserve_odsay_request(
    redis: Redis,
    daily_budget: int,
    *,
    operation: str = "search_pub_trans_path",
    now: datetime | None = None,
) -> bool:
    """Reserve one ODsay request against the Korea-calendar-day hard cap."""
    return await _reserve_hash_request(
        redis,
        key=_odsay_usage_key,
        operations=ODSAY_OPERATIONS,
        operation=operation,
        limit=daily_budget,
        billing_timezone=ODSAY_BILLING_TIMEZONE,
        period="day",
        now=now,
    )


async def odsay_usage_snapshot(
    redis: Redis,
    daily_limit: int = 0,
    *,
    now: datetime | None = None,
) -> ProviderUsageSnapshot:
    """Return app-observed ODsay calls for the current Korean quota day."""
    observed_at = now or datetime.now(UTC)
    billing_now = observed_at.astimezone(ODSAY_BILLING_TIMEZONE)
    try:
        raw = await cast(Awaitable[dict[Any, Any]], redis.hgetall(_odsay_usage_key(billing_now)))
    except RedisError:
        return ProviderUsageSnapshot(
            period=f"{billing_now:%Y-%m-%d}",
            period_start=billing_now.date(),
            period_end=billing_now.date(),
            used=None,
            monthly_limit=daily_limit,
            remaining=None,
            percentage=None,
            free_limit=daily_limit,
            free_usage=None,
            free_remaining=None,
            billable_overage=None,
            breakdown={},
            sku_usage=(),
            monthly_history=(),
            tracking_started_at=None,
            observed_at=observed_at,
            available=False,
            period_kind="day",
            billing_timezone="Asia/Seoul",
            pricing_region="kr",
        )
    values = {_text(item_key): _text(value) for item_key, value in raw.items()}
    breakdown = {
        operation: int(values.get(f"operation:{operation}", 0)) for operation in ODSAY_OPERATIONS
    }
    used = int(values.get("total", 0))
    started = values.get("tracking_started_at")
    return ProviderUsageSnapshot(
        period=f"{billing_now:%Y-%m-%d}",
        period_start=billing_now.date(),
        period_end=billing_now.date(),
        used=used,
        monthly_limit=daily_limit,
        remaining=max(0, daily_limit - used) if daily_limit else None,
        percentage=round(used / daily_limit * 100, 1) if daily_limit else None,
        free_limit=daily_limit,
        free_usage=min(used, daily_limit) if daily_limit else None,
        free_remaining=max(0, daily_limit - used) if daily_limit else None,
        billable_overage=max(0, used - daily_limit) if daily_limit else None,
        breakdown=breakdown,
        sku_usage=(),
        monthly_history=(),
        tracking_started_at=datetime.fromisoformat(started) if started else None,
        observed_at=observed_at,
        available=True,
        period_kind="day",
        billing_timezone="Asia/Seoul",
        pricing_region="kr",
    )
