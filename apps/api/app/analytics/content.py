"""Raw first-party continuation clicks; never impressions, completed reads or revenue."""

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.analytics.schemas import AnalyticsRange, ContentLinkInput, content_path
from app.analytics.service import _environment, _range_bounds
from app.models import AnalyticsEvent

LIMIT = 20


async def content_report(
    session: AsyncSession,
    value: AnalyticsRange,
    include_bots: bool = False,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(UTC)
    settings = await load_runtime_settings(session)
    requested_start, end, _ = _range_bounds(value, now)
    retained_from = now - timedelta(days=settings.analytics_retention_days)
    start = max(requested_start, retained_from)
    report: dict[str, Any] = {
        "range": value,
        "timezone": "Asia/Taipei",
        "available": value != "12m",
        "reason": "raw_window_only" if value == "12m" else None,
        "from": start.isoformat(),
        "to": end.isoformat(),
        "retention_days": settings.analytics_retention_days,
        "window_clipped": start > requested_start,
        "first_recorded_at": None,
        "total_clicks": 0,
        "rows": [],
    }
    if value == "12m":
        return report

    base = [
        AnalyticsEvent.event_name == "content_link_click",
        AnalyticsEvent.environment == _environment(settings),
    ]
    if not include_bots:
        base.append(AnalyticsEvent.is_bot.is_(False))
    first = await session.scalar(
        select(func.min(AnalyticsEvent.occurred_at)).where(
            *base, AnalyticsEvent.occurred_at >= retained_from, AnalyticsEvent.occurred_at <= end
        )
    )
    report["first_recorded_at"] = (
        (first if first.tzinfo else first.replace(tzinfo=UTC)).isoformat() if first else None
    )
    window = [*base, AnalyticsEvent.occurred_at >= start, AnalyticsEvent.occurred_at <= end]
    report["total_clicks"] = int(
        await session.scalar(select(func.count()).select_from(AnalyticsEvent).where(*window)) or 0
    )
    target = AnalyticsEvent.properties_json["target_path"].as_string()
    placement = AnalyticsEvent.properties_json["placement"].as_string()
    groups = (AnalyticsEvent.normalized_path, target, placement, AnalyticsEvent.locale)
    rows = await session.execute(
        select(*groups, func.count())
        .where(*window)
        .group_by(*groups)
        .order_by(func.count().desc(), *groups)
        .limit(LIMIT)
    )
    for source, destination, position, locale, clicks in rows:
        # Never echo an arbitrary value if a historical/corrupt row bypassed ingest.
        try:
            safe_source = content_path(source, article_only=True)
            link = ContentLinkInput.model_validate(
                {"target_path": destination, "placement": position}
            )
        except (ValueError, TypeError):
            continue
        report["rows"].append(
            {
                "source_path": safe_source,
                "target_path": link.target_path,
                "placement": link.placement,
                "locale": locale,
                "clicks": int(clicks),
            }
        )
    return report
