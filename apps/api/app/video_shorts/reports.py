"""The weekly report (docs/videos/SHORTS.md §成效與每週報告): what the worker reads to write
it, and the report it sends back.

The numbers are YouTube's. The report job lists every snapshot as it was stored, with its
source and when it was read; the report's ``rows`` are the snapshots it cites, copied from
the store when the report arrives rather than taken from the request, so a number in a row
is always one YouTube reported. Nothing here adds, ranks, averages or scores them: YouTube's
developer policies forbid deriving metrics from API data until the audit grants the
Analytics & Reporting exception. A week has one report; sending it again replaces it.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, cast
from uuid import uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoProject
from app.video_shorts import costs
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import (
    VideoShortsCost,
    VideoShortsMetric,
    VideoShortsReport,
    VideoShortsSettings,
    VideoShortsSlot,
)
from app.video_shorts.overview import metric_out
from app.video_shorts.plan import local_week
from app.video_shorts.schemas import (
    PublishedShort,
    ReportIn,
    ReportJob,
    ReportOut,
    SlotRef,
)
from app.video_shorts.settings import settings_row

LIST_LIMIT = 52
# The values a row keeps: the snapshot's as stored, nothing computed.
ROW_FIELDS = (
    "views",
    "engaged_views",
    "likes",
    "comments",
    "shares",
    "subscribers_gained",
    "avg_view_seconds",
    "avg_view_percent",
    "stayed_percent",
)


def week_bounds(week: date, timezone: str) -> tuple[datetime, datetime]:
    zone = ZoneInfo(timezone)
    start = datetime.combine(week, time(0), tzinfo=zone)
    return start.astimezone(UTC), (start + timedelta(days=7)).astimezone(UTC)


def slot_ref(slot: VideoShortsSlot, timezone: str) -> SlotRef:
    local = slot.starts_at.astimezone(ZoneInfo(timezone))
    return SlotRef(
        id=slot.id,
        starts_at=slot.starts_at,
        local_date=local.date(),
        local_time=local.strftime("%H:%M"),
        status=cast(Any, slot.status),
        line=cast(Any, slot.line),
        series=slot.series,
        topic_slug=slot.topic_slug,
        project_slug=slot.project_slug,
    )


def _plain(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    return value


def snapshot_row(metric: VideoShortsMetric, title: str | None) -> dict[str, Any]:
    """One snapshot as the report keeps it: what YouTube said, where from, and when read."""
    return {
        "slug": metric.project_slug,
        "title": title,
        "youtube_video_id": metric.youtube_video_id,
        "period": metric.period,
        "source": metric.source,
        "captured_at": metric.captured_at.isoformat(),
        "range_start": metric.range_start.isoformat() if metric.range_start else None,
        "range_end": metric.range_end.isoformat() if metric.range_end else None,
        **{field: _plain(getattr(metric, field)) for field in ROW_FIELDS},
    }


async def published_between(
    session: AsyncSession, start: datetime, end: datetime
) -> list[PublishedShort]:
    """The Shorts whose publish time falls in the range, each with every snapshot stored."""
    projects = list(
        await session.scalars(
            select(VideoProject)
            .where(
                VideoProject.shorts_line.is_not(None),
                VideoProject.youtube_video_id.is_not(None),
                VideoProject.youtube_publish_at >= start,
                VideoProject.youtube_publish_at < end,
            )
            .order_by(VideoProject.youtube_publish_at)
        )
    )
    if not projects:
        return []
    snapshots: dict[str, list[VideoShortsMetric]] = {}
    for metric in await session.scalars(
        select(VideoShortsMetric)
        .where(VideoShortsMetric.project_slug.in_([project.slug for project in projects]))
        .order_by(VideoShortsMetric.captured_at)
    ):
        snapshots.setdefault(metric.project_slug, []).append(metric)
    return [
        PublishedShort(
            slug=project.slug,
            title=project.title,
            line=cast(Any, project.shorts_line),
            series=project.shorts_series,
            youtube_video_id=str(project.youtube_video_id),
            published_at=project.youtube_publish_at,
            snapshots=[metric_out(metric) for metric in snapshots.get(project.slug, [])],
        )
        for project in projects
    ]


async def report_job(
    session: AsyncSession, row: VideoShortsSettings, week: date, now: datetime
) -> ReportJob:
    """What the planner reads to write the report on ``week``: what went public that week
    with its numbers as stored, the slots it missed, the week's ledger and where the budget
    stands, and what the next week has planned."""
    start, end = week_bounds(week, row.timezone)
    # The week the report is written in: what is still to come in it, as planned.
    _now_start, coming_end = week_bounds(week + timedelta(days=7), row.timezone)
    missed = list(
        await session.scalars(
            select(VideoShortsSlot)
            .where(
                VideoShortsSlot.starts_at >= start,
                VideoShortsSlot.starts_at < end,
                VideoShortsSlot.status == "missed",
            )
            .order_by(VideoShortsSlot.starts_at)
        )
    )
    coming = list(
        await session.scalars(
            select(VideoShortsSlot)
            .where(VideoShortsSlot.starts_at > now, VideoShortsSlot.starts_at < coming_end)
            .order_by(VideoShortsSlot.starts_at)
        )
    )
    lines = list(
        await session.scalars(
            select(VideoShortsCost)
            .where(VideoShortsCost.occurred_at >= start, VideoShortsCost.occurred_at < end)
            .order_by(VideoShortsCost.occurred_at)
        )
    )
    state = await costs.budget(session, row, now)
    return ReportJob(
        week_start=week,
        week_end=week + timedelta(days=6),
        timezone=row.timezone,
        published=await published_between(session, start, end),
        missed=[slot_ref(slot, row.timezone) for slot in missed],
        costs=[costs.cost_out(line) for line in lines],
        budget=costs.budget_out(state, row),
        next_week=[slot_ref(slot, row.timezone) for slot in coming],
    )


def report_out(row: VideoShortsReport) -> ReportOut:
    return ReportOut(
        id=row.id,
        week_start=row.week_start,
        body_md=row.body_md,
        rows=list(row.rows or []),
        plan=list(row.plan or []),
        provider=row.provider,
        model=row.model,
        generated_at=row.generated_at,
        updated_at=row.updated_at,
    )


async def cited_rows(session: AsyncSession, payload: ReportIn) -> list[dict[str, Any]]:
    """The snapshots the report cites, copied as stored; one it names that is not stored is
    refused, since a number nobody read from YouTube has no place in the table."""
    wanted = {(row.youtube_video_id, row.source, row.period) for row in payload.rows}
    if not wanted:
        return []
    ids = sorted({video for video, _source, _period in wanted})
    stored = {
        (metric.youtube_video_id, metric.source, metric.period): metric
        for metric in await session.scalars(
            select(VideoShortsMetric).where(VideoShortsMetric.youtube_video_id.in_(ids))
        )
    }
    missing = sorted(key for key in wanted if key not in stored)
    if missing:
        named = "、".join(f"{video} {source} {period}" for video, source, period in missing[:5])
        raise ShortsRefused(
            422, "video_shorts_report_row_unknown", f"報告引用了伺服器沒有的數字：{named}"
        )
    titles = {
        project.slug: project.title
        for project in await session.scalars(
            select(VideoProject).where(
                VideoProject.slug.in_(sorted({metric.project_slug for metric in stored.values()}))
            )
        )
    }
    rows: list[dict[str, Any]] = []
    for item in payload.rows:
        metric = stored[(item.youtube_video_id, item.source, item.period)]
        row = snapshot_row(metric, titles.get(metric.project_slug))
        if row not in rows:
            rows.append(row)
    return rows


async def save_report(
    session: AsyncSession, payload: ReportIn, now: datetime | None = None
) -> ReportOut:
    """Keep the planner's report on a week; the same week sent again replaces it."""
    moment = now or datetime.now(UTC)
    settings = await settings_row(session)
    if payload.week_start.weekday() != 0:
        raise ShortsRefused(422, "video_shorts_report_week", "week_start 要是星期一")
    if payload.week_start >= local_week(moment, settings.timezone):
        raise ShortsRefused(
            422, "video_shorts_report_week", "只能寫已經過完的一週（week_start 在本週之前）"
        )
    rows = await cited_rows(session, payload)
    plan = [item.model_dump(mode="json", exclude_none=True) for item in payload.plan]
    report = await session.scalar(
        select(VideoShortsReport)
        .where(VideoShortsReport.week_start == payload.week_start)
        .with_for_update()
    )
    if report is None:
        report = VideoShortsReport(id=uuid4(), week_start=payload.week_start, created_at=moment)
        session.add(report)
    report.body_md = payload.body_md
    report.rows = rows
    report.plan = plan
    report.provider = payload.provider
    report.model = payload.model
    report.generated_at = moment
    report.updated_at = moment
    await session.commit()
    return report_out(report)


async def list_reports(session: AsyncSession, limit: int = LIST_LIMIT) -> list[ReportOut]:
    """Newest week first."""
    rows = await session.scalars(
        select(VideoShortsReport).order_by(VideoShortsReport.week_start.desc()).limit(limit)
    )
    return [report_out(row) for row in rows]


async def reported_weeks(session: AsyncSession, since: date) -> set[date]:
    return set(
        await session.scalars(
            select(VideoShortsReport.week_start).where(VideoShortsReport.week_start >= since)
        )
    )
