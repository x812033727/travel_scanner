import asyncio
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import Date, cast, delete, func, select

from app.admin.service import load_runtime_settings
from app.analytics.service import rollup_day
from app.db import SessionFactory
from app.models import AnalyticsDailyRollup, AnalyticsEvent


def _month_cutoff(months: int) -> date:
    today = datetime.now(ZoneInfo("Asia/Taipei")).date()
    month = today.month - months
    year = today.year
    while month <= 0:
        month += 12
        year -= 1
    return today.replace(year=year, month=month, day=1)


async def _run() -> dict[str, int]:
    today = datetime.now(ZoneInfo("Asia/Taipei")).date()
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        yesterday = today - timedelta(days=1)
        raw_start = today - timedelta(days=settings.analytics_retention_days)
        event_days = set(
            (
                await session.scalars(
                    select(
                        cast(
                            func.timezone("Asia/Taipei", AnalyticsEvent.occurred_at),
                            Date,
                        )
                    )
                    .where(
                        AnalyticsEvent.occurred_at
                        >= datetime.combine(
                            raw_start, datetime.min.time(), tzinfo=ZoneInfo("Asia/Taipei")
                        )
                    )
                    .distinct()
                )
            ).all()
        )
        completed_days = set(
            (
                await session.scalars(
                    select(AnalyticsDailyRollup.day)
                    .where(AnalyticsDailyRollup.day >= raw_start)
                    .distinct()
                )
            ).all()
        )
        targets = sorted({yesterday, *(event_days - completed_days)})
        rows = 0
        for target in targets:
            if target <= yesterday:
                rows += await rollup_day(session, target)
        raw_cutoff = datetime.now(ZoneInfo("UTC")) - timedelta(
            days=settings.analytics_retention_days
        )
        event_delete_result = await session.execute(
            delete(AnalyticsEvent).where(AnalyticsEvent.occurred_at < raw_cutoff)
        )
        deleted_events = int(getattr(event_delete_result, "rowcount", 0) or 0)
        rollup_delete_result = await session.execute(
            delete(AnalyticsDailyRollup).where(
                AnalyticsDailyRollup.day < _month_cutoff(settings.analytics_rollup_retention_months)
            )
        )
        deleted_rollups = int(getattr(rollup_delete_result, "rowcount", 0) or 0)
        await session.commit()
    return {
        "rollup_rows": rows,
        "deleted_events": deleted_events,
        "deleted_rollups": deleted_rollups,
    }


def run_analytics_maintenance() -> dict[str, int]:
    return asyncio.run(_run())
