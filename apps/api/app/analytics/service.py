from __future__ import annotations

import hashlib
import hmac
import logging
import re
from collections import Counter, defaultdict
from collections.abc import Mapping
from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from urllib.parse import urlparse
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from fastapi import Request
from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.analytics.context import analytics_context
from app.analytics.schemas import (
    AnalyticsConfigResponse,
    AnalyticsEventBatch,
    AnalyticsIngestResponse,
    AnalyticsRange,
)
from app.config import Settings, get_settings
from app.i18n import active_locale
from app.infra import client_ip, enforce_named_rate_limit
from app.models import (
    AffiliateClick,
    AnalyticsDailyRollup,
    AnalyticsEvent,
    SearchRequest,
    TripPlan,
    User,
)

logger = logging.getLogger(__name__)

TAIPEI = ZoneInfo("Asia/Taipei")
LOCALES = {"en", "ja", "ko", "zh-TW", "zh-CN"}
# The whole vocabulary, and its only definition — the database no longer carries a
# CHECK (0055_analytics_event_names). `page_view` stays first because it is the only
# name that is a page rather than an action; everything else is counted per session in
# COUNTED_EVENT_NAMES below.
EVENT_NAMES = (
    "page_view",
    "registration_completed",
    "search_completed",
    "trip_created",
    "outbound_click",
    "discover_requested",
    "search_started",
    "place_added_to_trip",
    "ai_applied",
    "optimize_applied",
    "offer_attached",
    "alert_created",
    "share_created",
    "share_forked",
    "usage_charged",
    "usage_insufficient",
    "login_resumed",
)
COUNTED_EVENT_NAMES = tuple(name for name in EVENT_NAMES if name != "page_view")
# What the admin funnel walks. Every step after the first is counted as the sessions
# that reached it, so the steps have to be things one session can do in this order:
# ask for a recommendation, save the trip it produced, put a real quote on that trip,
# then leave for a provider. `sessions` is the baseline, not an event.
FUNNEL_STEPS = ("discover_requested", "trip_created", "offer_attached", "outbound_click")
# Names the server is the only truth for. A browser can still send `trip_created` —
# older bundles do — and ingest drops it rather than double-counting the trip.
SERVER_OWNED_EVENTS = frozenset({"trip_created"})
_UUID_OR_TOKEN = re.compile(r"(?i)(?:[0-9a-f]{8}-[0-9a-f-]{27,}|[A-Za-z0-9_-]{20,})")
_SAFE_UTM = re.compile(r"[^A-Za-z0-9._+\-/ ]")
_BOT = re.compile(r"bot|crawler|spider|slurp|headless|preview|monitor", re.I)


def normalize_path(raw: str) -> str | None:
    try:
        path = urlparse(raw).path or "/"
    except ValueError:
        return None
    path = re.sub(r"/{2,}", "/", path)
    parts = [part for part in path.split("/") if part]
    if parts and parts[0] in LOCALES:
        parts = parts[1:]
    if parts and parts[0].lower() in {"admin", "api", "health", "ready"}:
        return None
    safe = [":id" if _UUID_OR_TOKEN.fullmatch(part) else part[:48] for part in parts]
    normalized = "/" + "/".join(safe)
    return normalized[:128] or "/"


def _digest(secret: str, purpose: str, value: str) -> str:
    return hmac.new(secret.encode(), f"{purpose}:{value}".encode(), hashlib.sha256).hexdigest()


def _utm(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = _SAFE_UTM.sub("", value.strip())[:100]
    return cleaned or None


def _client_details(user_agent: str) -> tuple[str, str, str, bool]:
    ua = user_agent[:512]
    bot = bool(_BOT.search(ua))
    device = (
        "tablet"
        if re.search(r"iPad|Tablet", ua, re.I)
        else "mobile"
        if re.search(r"Mobile|Android|iPhone", ua, re.I)
        else "desktop"
        if ua
        else "unknown"
    )
    browser = (
        "edge"
        if "Edg/" in ua
        else "chrome"
        if "Chrome/" in ua
        else "safari"
        if "Safari/" in ua
        else "firefox"
        if "Firefox/" in ua
        else "other"
    )
    os_name = (
        "ios"
        if re.search(r"iPhone|iPad", ua)
        else "android"
        if "Android" in ua
        else "windows"
        if "Windows" in ua
        else "macos"
        if "Mac OS" in ua
        else "linux"
        if "Linux" in ua
        else "other"
    )
    return device, browser, os_name, bot


def _referrer(value: str | None, site_url: str) -> tuple[str, str | None]:
    if not value:
        return "direct", None
    try:
        host = (urlparse(value).hostname or "").lower()[:255]
        site_host = (urlparse(site_url).hostname or "").lower()
    except ValueError:
        return "direct", None
    if not host:
        return "direct", None
    if host == site_host or host.endswith(f".{site_host}"):
        return "internal", None
    if any(name in host for name in ("google.", "bing.", "yahoo.", "duckduckgo.")):
        return "search", host
    if any(
        name in host
        for name in ("facebook.", "instagram.", "youtube.", "tiktok.", "x.com", "twitter.")
    ):
        return "social", host
    return "referral", host


async def public_config(session: AsyncSession) -> AnalyticsConfigResponse:
    settings = await load_runtime_settings(session)
    candidate = (settings.ga4_measurement_id or "").strip().upper()
    measurement_id = (
        candidate if settings.ga4_enabled and re.fullmatch(r"G-[A-Z0-9]{4,16}", candidate) else None
    )
    return AnalyticsConfigResponse(
        first_party_enabled=settings.analytics_enabled,
        ga4_enabled=bool(settings.ga4_enabled and measurement_id),
        ga4_measurement_id=measurement_id,
    )


async def ingest_events(
    session: AsyncSession,
    request: Request,
    payload: AnalyticsEventBatch,
) -> AnalyticsIngestResponse:
    settings = await load_runtime_settings(session)
    if (
        not settings.analytics_enabled
        or request.headers.get("Sec-GPC") == "1"
        or request.headers.get("DNT") == "1"
    ):
        return AnalyticsIngestResponse(accepted=0, enabled=False)

    ip = client_ip(request)
    await enforce_named_rate_limit(
        "analytics-ip", ip, limit=settings.analytics_event_ip_limit, window_seconds=60
    )
    await enforce_named_rate_limit(
        "analytics-session",
        str(payload.session_id),
        limit=settings.analytics_event_session_limit,
        window_seconds=60,
    )
    now = datetime.now(UTC)
    ua = request.headers.get("X-Travel-User-Agent", "")
    device, browser, os_name, is_bot = _client_details(ua)
    country: str | None = None
    if settings.analytics_trust_country_header:
        raw_country = request.headers.get("X-Travel-Country", "").upper()
        if re.fullmatch(r"[A-Z]{2}", raw_country) and raw_country not in {"XX", "T1"}:
            country = raw_country
    today = now.astimezone(TAIPEI).date().isoformat()
    session_hash = _digest(settings.app_secret_key, "analytics-session", str(payload.session_id))
    visitor_hash = _digest(settings.app_secret_key, "analytics-day", f"{today}|{ip}|{ua}")
    values: list[dict[str, Any]] = []
    for item in payload.events:
        if item.name in SERVER_OWNED_EVENTS:
            continue
        path = normalize_path(item.path)
        if path is None:
            continue
        occurred_at = item.occurred_at.astimezone(UTC)
        if occurred_at > now + timedelta(minutes=5) or occurred_at < now - timedelta(hours=24):
            occurred_at = now
        referrer_type, referrer_host = _referrer(item.referrer, settings.next_public_site_url)
        values.append(
            {
                "event_id": item.event_id,
                "event_name": item.name,
                "occurred_at": occurred_at,
                "normalized_path": path,
                "locale": item.locale,
                "session_hash": session_hash,
                "visitor_day_hash": visitor_hash,
                "country_code": country,
                "device_type": device,
                "browser_family": browser,
                "os_family": os_name,
                "referrer_type": referrer_type,
                "referrer_host": referrer_host,
                "utm_source": _utm(item.utm_source),
                "utm_medium": _utm(item.utm_medium),
                "utm_campaign": _utm(item.utm_campaign),
                # The BFF forwards the session as a cookie (not a bearer header) so the
                # sliding renewal runs; count either presentation as signed in.
                "is_authenticated": bool(
                    request.headers.get("Authorization") or request.cookies.get("travel_access")
                ),
                "is_bot": is_bot,
                "environment": _environment(settings),
                "properties_json": {},
            }
        )
    accepted = 0
    if values:
        inserted = await session.scalars(
            postgres_insert(AnalyticsEvent)
            .values(values)
            .on_conflict_do_nothing(index_elements=[AnalyticsEvent.event_id])
            .returning(AnalyticsEvent.event_id)
        )
        accepted = len(inserted.all())
    await session.commit()
    return AnalyticsIngestResponse(
        accepted=accepted, duplicates=len(values) - accepted, enabled=True
    )


PROPERTY_KEYS = 6
# Deliberately narrower than "a short string": no hyphens, no dots, no capitals, so a
# UUID, an email, a hostname and a name someone typed all fail it. Every value the call
# sites pass is an enum the code chose, and those are all `[a-z][a-z0-9_]*`.
_PROPERTY_VALUE = re.compile(r"[a-z][a-z0-9_]{0,31}")


def _properties(raw: Mapping[str, Any] | None) -> dict[str, Any]:
    """Keep event properties to things that describe the action, never the actor.

    Rows here are read by administrators and survive far longer than a request, so the
    only values accepted are the shapes an aggregate can be built from: a short
    lower-case enum, a number, a flag. Anything else — an id, an email, a trip name a
    member typed — is dropped rather than truncated, because a truncated identifier is
    still an identifier, and a UUID is only "a short string" until you notice it names
    someone. Callers pass literals, so a dropped value is a bug in the call site, and
    ``test_analytics_events`` pins the shapes that are allowed through.
    """
    if not raw:
        return {}
    clean: dict[str, Any] = {}
    for key, value in list(raw.items())[:PROPERTY_KEYS]:
        if isinstance(value, bool) or isinstance(value, int):
            clean[key[:32]] = value
        elif isinstance(value, str) and _PROPERTY_VALUE.fullmatch(value):
            clean[key[:32]] = value
    return clean


async def record_event(
    session: AsyncSession,
    name: str,
    *,
    path: str,
    user_id: UUID | None = None,
    properties: Mapping[str, Any] | None = None,
) -> bool:
    """Record one event the server is the truth for, and never break the caller.

    The visitor ingest endpoint is the wrong door for these: it rate-limits by IP and
    session because anyone can post to it, and the server posting to itself would be
    throttled by its own busiest members. This writes the row directly instead, and
    takes the visitor identity from the request context so the funnel can count a
    server step and a browser step as the same session.

    ``path`` is the product surface the action belongs to (``/trips``, ``/search``),
    not the API route: ``normalize_path`` drops anything under ``/api``, and a funnel
    broken down by ``/api/v1/trips`` would tell nobody anything anyway.

    Analytics is never the reason a member's request fails, and the hard part of that is
    not the exception handling — it is never *flushing* the caller. Callers arrive with
    their own rows added and not yet committed. Anything here that flushes that pending
    work sends the caller's INSERT to the database early, so it fails *inside* this
    function's ``try`` — written to swallow analytics failures — leaving the session
    needing a rollback. The caller's own ``except IntegrityError`` then never runs,
    because what reaches it is a ``PendingRollbackError``: two members racing to create
    the same alert got a 500 instead of the 409 that endpoint has always returned.

    So there are two rules here, and #324 shipped a version that broke both:

    - Every query runs under ``no_autoflush``. A ``SELECT`` (the settings read, above
      all) otherwise flushes the caller's pending rows on its way out.
    - No ``begin_nested()``. A savepoint looks like protection and was put here as
      protection, but entering one flushes first, which is exactly the harm it was
      supposed to prevent.

    What is left is an insert that rides along in the caller's transaction and commits
    with it. That is deliberate: an event for a trip whose creation then rolled back
    would be a count of something that never happened. The residual risk is that a
    failing analytics insert poisons the caller's transaction — narrow, because the row
    is validated here (``EVENT_NAMES``, ``_properties``) and written with
    ``ON CONFLICT DO NOTHING`` to a table nothing else contends on, and honest to state
    rather than to paper over with a savepoint that causes worse.
    """
    if name not in EVENT_NAMES:
        logger.warning("analytics.unknown_event", extra={"event_name": name})
        return False
    context = analytics_context()
    if context.opted_out:
        return False
    try:
        with session.no_autoflush:
            settings = await load_runtime_settings(session)
            if not settings.analytics_enabled:
                return False
            now = datetime.now(UTC)
            normalized = normalize_path(path)
            if normalized is None:
                logger.warning("analytics.unusable_path", extra={"event_path": path})
                return False
            user_agent = context.user_agent or ""
            device, browser, os_name, is_bot = _client_details(user_agent)
            today = now.astimezone(TAIPEI).date().isoformat()
            # A browser that told us its analytics session gets hashed exactly the way
            # ingest hashes it, so both halves of a funnel step land on one hash. Without
            # one (a worker, a CLI, a caller that predates the header) the member is the
            # next best stable identity; anonymous and session-less is its own bucket
            # rather than a shared empty string.
            identity = (
                ("analytics-session", context.session_id)
                if context.session_id
                else ("analytics-server-user", str(user_id))
                if user_id
                else ("analytics-server-ip", f"{today}|{context.client_ip or 'unknown'}")
            )
            session_hash = _digest(settings.app_secret_key, identity[0], identity[1])
            visitor_hash = _digest(
                settings.app_secret_key,
                "analytics-day",
                f"{today}|{context.client_ip or 'unknown'}|{user_agent}",
            )
            await session.execute(
                postgres_insert(AnalyticsEvent)
                .values(
                    {
                        "event_id": uuid4(),
                        "event_name": name,
                        "occurred_at": now,
                        "normalized_path": normalized,
                        "locale": active_locale(),
                        "session_hash": session_hash,
                        "visitor_day_hash": visitor_hash,
                        "country_code": context.country_code
                        if settings.analytics_trust_country_header
                        else None,
                        "device_type": device,
                        "browser_family": browser,
                        "os_family": os_name,
                        "referrer_type": "internal",
                        "referrer_host": None,
                        "utm_source": None,
                        "utm_medium": None,
                        "utm_campaign": None,
                        "is_authenticated": user_id is not None,
                        "is_bot": is_bot,
                        "environment": _environment(settings),
                        "properties_json": _properties(properties),
                    }
                )
                .on_conflict_do_nothing(index_elements=[AnalyticsEvent.event_id])
            )
    except Exception:  # noqa: BLE001 - measurement must never fail the thing measured
        logger.exception("analytics.record_failed", extra={"event_name": name})
        return False
    return True


def _environment(settings: Settings) -> str:
    value = settings.app_env.lower()
    return (
        "production"
        if value in {"prod", "production"}
        else "staging"
        if value in {"stage", "staging"}
        else "development"
    )


def _range_bounds(value: AnalyticsRange, now: datetime) -> tuple[datetime, datetime, str]:
    durations = {
        "24h": timedelta(hours=24),
        "7d": timedelta(days=7),
        "30d": timedelta(days=30),
        "90d": timedelta(days=90),
        "12m": timedelta(days=365),
    }
    start = now - durations[value]
    bucket = "hour" if value == "24h" else "month" if value == "12m" else "day"
    return start, now, bucket


def _summary(events: list[AnalyticsEvent], now: datetime) -> dict[str, float | int]:
    names = Counter(event.event_name for event in events)
    sessions = len({event.session_hash for event in events})
    visitors_by_day = defaultdict(set)
    for event in events:
        visitors_by_day[event.occurred_at.astimezone(TAIPEI).date()].add(event.visitor_day_hash)
    days = max(1, len(visitors_by_day))
    page_views = names["page_view"]
    return {
        "live_sessions_30m": len(
            {
                event.session_hash
                for event in events
                if event.occurred_at >= now - timedelta(minutes=30)
            }
        ),
        "page_views": page_views,
        "avg_daily_visitors": round(sum(map(len, visitors_by_day.values())) / days, 1),
        "sessions": sessions,
        "pages_per_session": round(page_views / sessions, 2) if sessions else 0,
        **{name: names[name] for name in COUNTED_EVENT_NAMES},
    }


def _series(events: list[AnalyticsEvent], bucket: str) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for event in events:
        local = event.occurred_at.astimezone(TAIPEI)
        key = (
            local.strftime("%Y-%m-%dT%H:00:00+08:00")
            if bucket == "hour"
            else local.strftime("%Y-%m")
            if bucket == "month"
            else local.date().isoformat()
        )
        row = rows.setdefault(key, {"bucket": key, **{name: 0 for name in EVENT_NAMES}})
        row[event.event_name] += 1
    return [rows[key] for key in sorted(rows)]


def _ranking(
    events: list[AnalyticsEvent], attribute: str, *, page_only: bool = False, limit: int = 10
) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for event in events:
        if page_only and event.event_name != "page_view":
            continue
        value = getattr(event, attribute) or "unknown"
        counter[str(value)] += 1
    return [{"key": key, "value": value} for key, value in counter.most_common(limit)]


def _funnel(events: list[AnalyticsEvent]) -> list[dict[str, Any]]:
    steps: list[tuple[str, str | None]] = [("sessions", None)]
    steps += [(name, name) for name in FUNNEL_STEPS]
    all_sessions = {event.session_hash for event in events}
    baseline = len(all_sessions)
    result = []
    for label, event_name in steps:
        count = (
            baseline
            if event_name is None
            else len({event.session_hash for event in events if event.event_name == event_name})
        )
        result.append(
            {
                "step": label,
                "sessions": count,
                "conversion_rate": round(count * 100 / baseline, 1) if baseline else 0,
            }
        )
    return result


def _rollup_value(
    rows: list[AnalyticsDailyRollup], metric: str, dimension: str, value: str | None = None
) -> int:
    return sum(
        row.value
        for row in rows
        if row.metric == metric
        and row.dimension == dimension
        and (value is None or row.dimension_value == value)
    )


def _rollup_summary(rows: list[AnalyticsDailyRollup]) -> dict[str, float | int]:
    pages = _rollup_value(rows, "event_count", "event", "page_view")
    sessions = _rollup_value(rows, "unique_sessions", "all", "all")
    visitors_by_day: Counter[date] = Counter()
    for row in rows:
        if row.metric == "daily_visitors" and row.dimension == "all":
            visitors_by_day[row.day] += row.value
    return {
        "live_sessions_30m": 0,
        "page_views": pages,
        "avg_daily_visitors": round(sum(visitors_by_day.values()) / len(visitors_by_day), 1)
        if visitors_by_day
        else 0,
        "sessions": sessions,
        "pages_per_session": round(pages / sessions, 2) if sessions else 0,
        **{name: _rollup_value(rows, "event_count", "event", name) for name in COUNTED_EVENT_NAMES},
    }


def _rollup_ranking(
    rows: list[AnalyticsDailyRollup], dimension: str, limit: int = 10
) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for row in rows:
        if row.metric == "page_view" and row.dimension == dimension:
            counter[row.dimension_value] += row.value
    return [{"key": key, "value": value} for key, value in counter.most_common(limit)]


def _rollup_series(rows: list[AnalyticsDailyRollup]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.metric != "event_count" or row.dimension != "event":
            continue
        key = row.day.strftime("%Y-%m")
        bucket = grouped.setdefault(key, {"bucket": key, **{name: 0 for name in EVENT_NAMES}})
        bucket[row.dimension_value] = int(bucket.get(row.dimension_value, 0)) + row.value
    return [grouped[key] for key in sorted(grouped)]


def _rollup_funnel(rows: list[AnalyticsDailyRollup]) -> list[dict[str, Any]]:
    baseline = _rollup_value(rows, "unique_sessions", "all", "all")
    result = [{"step": "sessions", "sessions": baseline, "conversion_rate": 100 if baseline else 0}]
    for name in FUNNEL_STEPS:
        count = _rollup_value(rows, "funnel_sessions", "step", name)
        result.append(
            {
                "step": name,
                "sessions": count,
                "conversion_rate": round(count * 100 / baseline, 1) if baseline else 0,
            }
        )
    return result


def _tracking_start(first_event: datetime | None, first_rollup: date | None) -> datetime | None:
    if first_rollup and (
        first_event is None or first_rollup < first_event.astimezone(TAIPEI).date()
    ):
        return datetime.combine(first_rollup, time.min, TAIPEI)
    return first_event


async def dashboard(
    session: AsyncSession,
    value: AnalyticsRange,
    compare: bool,
    include_bots: bool,
) -> dict[str, Any]:
    settings = await load_runtime_settings(session)
    now = datetime.now(UTC)
    start, end, bucket = _range_bounds(value, now)
    environment = _environment(settings)
    if value == "12m":
        start_day = start.astimezone(TAIPEI).date()
        end_day = end.astimezone(TAIPEI).date()
        rollup_query = select(AnalyticsDailyRollup).where(
            AnalyticsDailyRollup.environment == environment,
            AnalyticsDailyRollup.day >= start_day,
            AnalyticsDailyRollup.day <= end_day,
        )
        if not include_bots:
            rollup_query = rollup_query.where(AnalyticsDailyRollup.is_bot.is_(False))
        rows = list((await session.scalars(rollup_query)).all())
        summary = _rollup_summary(rows)
        rollup_previous: dict[str, Any] | None = None
        rollup_changes: dict[str, float | None] = {}
        if compare:
            duration_days = (end_day - start_day).days
            previous_rollup_query = select(AnalyticsDailyRollup).where(
                AnalyticsDailyRollup.environment == environment,
                AnalyticsDailyRollup.day >= start_day - timedelta(days=duration_days),
                AnalyticsDailyRollup.day < start_day,
            )
            if not include_bots:
                previous_rollup_query = previous_rollup_query.where(
                    AnalyticsDailyRollup.is_bot.is_(False)
                )
            rollup_previous = _rollup_summary(
                list((await session.scalars(previous_rollup_query)).all())
            )
            for key, current in summary.items():
                old = float(rollup_previous.get(key, 0))
                rollup_changes[key] = round((float(current) - old) * 100 / old, 1) if old else None
        first_event = await session.scalar(select(func.min(AnalyticsEvent.occurred_at)))
        first_rollup = await session.scalar(select(func.min(AnalyticsDailyRollup.day)))
        last_event = await session.scalar(select(func.max(AnalyticsEvent.occurred_at)))
        last_rollup = await session.scalar(select(func.max(AnalyticsDailyRollup.day)))
        country_total = _rollup_value(rows, "page_view", "country")
        country_unknown = _rollup_value(rows, "page_view", "country", "unknown")
        authoritative = {
            "registrations": await session.scalar(
                select(func.count(User.id)).where(User.created_at >= start)
            ),
            "completed_searches": await session.scalar(
                select(func.count(SearchRequest.id)).where(
                    SearchRequest.created_at >= start, SearchRequest.status == "completed"
                )
            ),
            "trips_created": await session.scalar(
                select(func.count(TripPlan.id)).where(TripPlan.created_at >= start)
            ),
            "affiliate_clicks": await session.scalar(
                select(func.count(AffiliateClick.id)).where(AffiliateClick.created_at >= start)
            ),
        }
        return {
            "range": value,
            "timezone": "Asia/Taipei",
            "source": "daily_rollup",
            "summary": {
                **summary,
                "previous": rollup_previous,
                "changes": rollup_changes,
            },
            "timeseries": _rollup_series(rows),
            "funnel": _rollup_funnel(rows),
            "top_pages": _rollup_ranking(rows, "route"),
            "referrers": _rollup_ranking(rows, "referrer"),
            "utm_sources": _rollup_ranking(rows, "utm_source"),
            "devices": _rollup_ranking(rows, "device"),
            "locales": _rollup_ranking(rows, "locale"),
            "countries": _rollup_ranking(rows, "country"),
            "heatmap": [],
            "authoritative": {key: int(number or 0) for key, number in authoritative.items()},
            "data_quality": {
                "tracking_started_at": _tracking_start(first_event, first_rollup),
                "last_event_at": last_event,
                "last_rollup_day": last_rollup,
                "country_coverage_percent": round(
                    (country_total - country_unknown) * 100 / country_total, 1
                )
                if country_total
                else 0,
                "ga4_enabled": settings.ga4_enabled,
                "ga4_configured": bool(settings.ga4_measurement_id),
                "bots_excluded": not include_bots,
                "raw_retention_days": settings.analytics_retention_days,
                "rollup_retention_months": settings.analytics_rollup_retention_months,
            },
        }
    query = select(AnalyticsEvent).where(
        AnalyticsEvent.environment == environment,
        AnalyticsEvent.occurred_at >= start,
        AnalyticsEvent.occurred_at < end,
    )
    if not include_bots:
        query = query.where(AnalyticsEvent.is_bot.is_(False))
    events = list((await session.scalars(query)).all())
    summary = _summary(events, now)
    previous: dict[str, Any] | None = None
    changes: dict[str, float | None] = {}
    if compare:
        duration = end - start
        previous_query = select(AnalyticsEvent).where(
            AnalyticsEvent.environment == environment,
            AnalyticsEvent.occurred_at >= start - duration,
            AnalyticsEvent.occurred_at < start,
        )
        if not include_bots:
            previous_query = previous_query.where(AnalyticsEvent.is_bot.is_(False))
        previous_events = list((await session.scalars(previous_query)).all())
        previous = _summary(previous_events, start)
        for key, current in summary.items():
            old = float(previous.get(key, 0))
            changes[key] = round((float(current) - old) * 100 / old, 1) if old else None

    all_count = len(events)
    known_country = sum(event.country_code is not None for event in events)
    first_event = await session.scalar(select(func.min(AnalyticsEvent.occurred_at)))
    first_rollup = await session.scalar(select(func.min(AnalyticsDailyRollup.day)))
    last_event = await session.scalar(select(func.max(AnalyticsEvent.occurred_at)))
    last_rollup = await session.scalar(select(func.max(AnalyticsDailyRollup.day)))
    authoritative = {
        "registrations": await session.scalar(
            select(func.count(User.id)).where(User.created_at >= start)
        ),
        "completed_searches": await session.scalar(
            select(func.count(SearchRequest.id)).where(
                SearchRequest.created_at >= start, SearchRequest.status == "completed"
            )
        ),
        "trips_created": await session.scalar(
            select(func.count(TripPlan.id)).where(TripPlan.created_at >= start)
        ),
        "affiliate_clicks": await session.scalar(
            select(func.count(AffiliateClick.id)).where(AffiliateClick.created_at >= start)
        ),
    }
    heat: Counter[tuple[int, int]] = Counter(
        (event.occurred_at.astimezone(TAIPEI).weekday(), event.occurred_at.astimezone(TAIPEI).hour)
        for event in events
        if event.event_name == "page_view"
    )
    return {
        "range": value,
        "timezone": "Asia/Taipei",
        "source": "raw",
        "summary": {**summary, "previous": previous, "changes": changes},
        "timeseries": _series(events, bucket),
        "funnel": _funnel(events),
        "top_pages": _ranking(events, "normalized_path", page_only=True),
        "referrers": _ranking(events, "referrer_type"),
        "utm_sources": _ranking(events, "utm_source"),
        "devices": _ranking(events, "device_type"),
        "locales": _ranking(events, "locale"),
        "countries": _ranking(events, "country_code"),
        "heatmap": [
            {"weekday": day, "hour": hour, "value": count}
            for (day, hour), count in sorted(heat.items())
        ],
        "authoritative": {key: int(number or 0) for key, number in authoritative.items()},
        "data_quality": {
            "tracking_started_at": _tracking_start(first_event, first_rollup),
            "last_event_at": last_event,
            "last_rollup_day": last_rollup,
            "country_coverage_percent": round(known_country * 100 / all_count, 1)
            if all_count
            else 0,
            "ga4_enabled": settings.ga4_enabled,
            "ga4_configured": bool(settings.ga4_measurement_id),
            "bots_excluded": not include_bots,
            "raw_retention_days": settings.analytics_retention_days,
            "rollup_retention_months": settings.analytics_rollup_retention_months,
        },
    }


async def rollup_day(session: AsyncSession, target: date) -> int:
    start = datetime.combine(target, time.min, TAIPEI).astimezone(UTC)
    end = start + timedelta(days=1)
    events = list(
        (
            await session.scalars(
                select(AnalyticsEvent).where(
                    AnalyticsEvent.occurred_at >= start, AnalyticsEvent.occurred_at < end
                )
            )
        ).all()
    )
    environments = {event.environment for event in events} or {_environment(get_settings())}
    await session.execute(delete(AnalyticsDailyRollup).where(AnalyticsDailyRollup.day == target))
    total = 0
    for environment in environments:
        for is_bot in (False, True):
            selected = [
                event
                for event in events
                if event.environment == environment and event.is_bot is is_bot
            ]
            counters: Counter[tuple[str, str, str]] = Counter()
            for event in selected:
                counters[("event_count", "event", event.event_name)] += 1
                if event.event_name == "page_view":
                    for dimension, dimension_value_raw in (
                        ("route", event.normalized_path),
                        ("locale", event.locale),
                        ("country", event.country_code or "unknown"),
                        ("device", event.device_type),
                        ("referrer", event.referrer_type),
                        ("utm_source", event.utm_source or "unknown"),
                    ):
                        counters[("page_view", dimension, dimension_value_raw)] += 1
            counters[("unique_sessions", "all", "all")] = len(
                {event.session_hash for event in selected}
            )
            counters[("daily_visitors", "all", "all")] = len(
                {event.visitor_day_hash for event in selected}
            )
            for name in COUNTED_EVENT_NAMES:
                counters[("funnel_sessions", "step", name)] = len(
                    {event.session_hash for event in selected if event.event_name == name}
                )
            for (metric, dimension, dimension_value), count in counters.items():
                session.add(
                    AnalyticsDailyRollup(
                        day=target,
                        environment=environment,
                        is_bot=is_bot,
                        metric=metric,
                        dimension=dimension,
                        dimension_value=dimension_value,
                        value=count,
                    )
                )
                total += 1
    await session.commit()
    return total
