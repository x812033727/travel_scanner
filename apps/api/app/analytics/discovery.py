"""Read-only, consent-limited discovery measurements; never a browsing history."""

from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.analytics.service import _environment
from app.auth.service import AdminUser
from app.db import get_session
from app.models import AnalyticsEvent

router = APIRouter(prefix="/admin/discovery", tags=["discovery measurement"])
Session = Annotated[AsyncSession, Depends(get_session)]
MEASURED_EVENTS = (
    "discovery_search",
    "discovery_empty",
    "content_saved",
    "place_added_to_trip",
    "post_published",
)
USEFUL_EVENTS = ("content_saved", "place_added_to_trip", "post_published")


def event_summary(counts: dict[str, int]) -> dict[str, Any]:
    searches = counts.get("discovery_search", 0)
    empty = counts.get("discovery_empty", 0)
    return {
        "searches": searches,
        "empty_searches": empty,
        "empty_search_rate": min(empty / searches, 1.0) if searches else None,
        "saves": counts.get("content_saved", 0),
        "places_added": counts.get("place_added_to_trip", 0),
        "published_posts": counts.get("post_published", 0),
    }


@router.get("/metrics")
async def discovery_metrics(
    user: AdminUser, session: Session, response: Response
) -> dict[str, Any]:
    _ = user
    response.headers["Cache-Control"] = "no-store"
    settings = await load_runtime_settings(session)
    now = datetime.now(UTC)
    start = now - timedelta(days=7)
    filters = (
        AnalyticsEvent.occurred_at >= start,
        AnalyticsEvent.occurred_at <= now,
        AnalyticsEvent.environment == _environment(settings),
        AnalyticsEvent.is_bot.is_(False),
    )
    counts: dict[str, int] = {}
    engaged = returning = 0
    if settings.analytics_enabled:
        rows = await session.execute(
            select(AnalyticsEvent.event_name, func.count())
            .where(*filters, AnalyticsEvent.event_name.in_(MEASURED_EVENTS))
            .group_by(AnalyticsEvent.event_name)
        )
        counts = {name: int(count) for name, count in rows}
        useful_action = or_(
            AnalyticsEvent.event_name.in_(("content_saved", "place_added_to_trip")),
            and_(
                AnalyticsEvent.event_name == "post_published",
                AnalyticsEvent.properties_json["publication_source"].as_string() == "author",
            ),
        )
        useful = (
            select(AnalyticsEvent.session_hash)
            .where(*filters, useful_action)
            .group_by(AnalyticsEvent.session_hash)
        )
        engaged = int(
            await session.scalar(select(func.count()).select_from(useful.subquery())) or 0
        )
        # PostgreSQL's date grouping is explicitly UTC, independent of connection TZ.
        day = (
            func.date(func.timezone("UTC", AnalyticsEvent.occurred_at))
            if session.get_bind().dialect.name == "postgresql"
            else func.date(AnalyticsEvent.occurred_at)
        )
        repeat = useful.having(func.count(func.distinct(day)) >= 2)
        returning = int(
            await session.scalar(select(func.count()).select_from(repeat.subquery())) or 0
        )
    return {
        "enabled": settings.analytics_enabled,
        "from": start.isoformat(),
        "to": now.isoformat(),
        "timezone": "UTC",
        "scope": "consented_nonbot_sessions_in_current_environment",
        **event_summary(counts),
        "engaged_sessions": engaged,
        "returning_engaged_sessions": returning,
        "member_day7_retention": None,
        "member_retention_status": "unavailable_without_stable_cross_day_member_identity",
        "save_to_trip_conversion": None,
        "conversion_status": "unavailable_without_attributed_action_sequence",
        "privacy": "no_raw_queries_no_private_itineraries_no_viewing_history",
    }
