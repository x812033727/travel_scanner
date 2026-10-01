"""The top row of the Shorts tab: where publishing stands, today's and tomorrow's slots, the
library, the budget, and everything that waits for the owner, each in a sentence.

The numbers YouTube reported are listed as they were stored. Nothing here adds them up or
ranks them (docs/videos/SHORTS.md §成效與每週報告).
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VideoProject
from app.video_shorts import costs, rules
from app.video_shorts.models import (
    METRIC_PERIODS,
    VideoShortsMetric,
    VideoShortsSettings,
    VideoShortsSlot,
)
from app.video_shorts.schemas import (
    CampaignView,
    ChannelOut,
    MetricOut,
    MetricsOut,
    NeedOut,
    OverviewOut,
    ShortMetrics,
    StockOut,
)
from app.video_shorts.settings import ChannelFacts, channel_facts, consent_view, settings_row
from app.video_shorts.slots import Short, library_of, shorts, slot_facts, slots_out

# The Shorts whose numbers the metrics view lists at once: the latest sixty that are public.
METRICS_LIMIT = 60


def build_needs(
    *,
    row: VideoShortsSettings,
    channel: ChannelFacts,
    consent_state: str,
    consent_problem: str | None,
    slots: Sequence[rules.SlotFacts],
    listed: Sequence[Short],
    budget: rules.BudgetState,
    now: datetime,
) -> list[NeedOut]:
    """What waits for the owner, most pressing first. Fully automatic still asks for these:
    a consent or a channel that stopped holding, the files to upload before the API audit
    passes, a Short the checks could not pass, a stuck one, a budget at its limit, days of
    missed slots, an empty library, a worker that went quiet."""
    needs: list[NeedOut] = []
    running = row.campaign_start is not None and bool(slots)
    if consent_state in ("expired", "invalid", "expiring"):
        needs.append(NeedOut(kind="consent", detail=consent_problem or "自動上架授權要重新同意"))
    elif consent_state == "none" and running:
        needs.append(
            NeedOut(
                kind="consent",
                detail="還沒有自動上架授權：時段到了的 Shorts 會等你自己送到 YouTube",
            )
        )
    if running or consent_state != "none":
        if not channel.linked:
            needs.append(NeedOut(kind="channel", detail="YouTube 頻道還沒有連結，或連結失效了"))
        elif channel.problem:
            needs.append(NeedOut(kind="channel", detail=f"YouTube 頻道：{channel.problem}"))
    if running:
        seen = row.last_tick_at
        if seen is None:
            needs.append(NeedOut(kind="worker", detail="主機工人還沒有回報過，時段不會自己鎖定"))
        elif now - seen > rules.WORKER_SILENT_AFTER:
            minutes = int((now - seen).total_seconds() // 60)
            needs.append(NeedOut(kind="worker", detail=f"主機工人已經 {minutes} 分鐘沒有回報"))
    by_slug = {short.project.slug: short for short in listed}
    # Until the API audit passes the owner uploads the files; with no channel linked there
    # is nowhere for the site to find them, and the line above says so first.
    if running and channel.linked and not channel.audited:
        horizon = now + timedelta(days=row.upload_ahead_days)
        waiting = [
            slot
            for slot in slots
            if slot.status in ("assigned", "locked")
            and now < slot.starts_at <= horizon
            and slot.project_slug in by_slug
            and by_slug[slot.project_slug].project.youtube_video_id is None
        ]
        if waiting:
            needs.append(
                NeedOut(
                    kind="upload",
                    detail=f"接下來 {row.upload_ahead_days} 天有 {len(waiting)} 支等你上傳到 "
                    "YouTube Studio",
                    count=len(waiting),
                )
            )
    for short in listed:
        if short.project.stage == "blocked":
            needs.append(
                NeedOut(
                    kind="blocked",
                    detail=f"「{short.project.title}」卡住了",
                    slug=short.project.slug,
                )
            )
        elif short.pending > 0:
            needs.append(
                NeedOut(
                    kind="review",
                    detail=f"「{short.project.title}」的自動品管沒有全過，等你決定",
                    slug=short.project.slug,
                    count=short.pending,
                )
            )
    if budget.reason is not None:
        needs.append(NeedOut(kind="budget", detail=budget.reason))
    streak = rules.missed_days_in_a_row(slots, now, row.timezone)
    if streak >= rules.MISSED_DAYS_ALERT:
        needs.append(NeedOut(kind="missed", detail=f"已經連續 {streak} 天錯過時段", count=streak))
    if running:
        cover = rules.stock_cover(slots, len(library_of(listed, now)), now, row.timezone)
        if cover == 0:
            needs.append(NeedOut(kind="stock", detail="片庫是空的，下一個時段沒有 Shorts 可以發"))
    return needs


async def _load(
    session: AsyncSession, row: VideoShortsSettings, now: datetime
) -> tuple[list[VideoShortsSlot], list[Short], rules.BudgetState, ChannelFacts]:
    slots = list(await session.scalars(select(VideoShortsSlot).order_by(VideoShortsSlot.starts_at)))
    listed = await shorts(session, public=False, now=now)
    budget = await costs.budget(session, row, now)
    return slots, listed, budget, await channel_facts(session)


async def overview(session: AsyncSession, now: datetime | None = None) -> OverviewOut:
    moment = now or datetime.now(UTC)
    row = await settings_row(session)
    await session.commit()
    slots, listed, budget, channel = await _load(session, row, moment)
    consent = consent_view(row, channel, moment)
    facts = [slot_facts(slot) for slot in slots]
    today = moment.astimezone(ZoneInfo(row.timezone)).date()

    def on(day: date) -> list[VideoShortsSlot]:
        zone = ZoneInfo(row.timezone)
        return [slot for slot in slots if slot.starts_at.astimezone(zone).date() == day]

    needs = build_needs(
        row=row,
        channel=channel,
        consent_state=consent.state,
        consent_problem=consent.problem,
        slots=facts,
        listed=listed,
        budget=budget,
        now=moment,
    )
    library = library_of(listed, moment)
    last_day = (
        row.campaign_start + timedelta(days=rules.pattern_days(row.daily_pattern) - 1)
        if row.campaign_start is not None
        else None
    )
    return OverviewOut(
        autopublish=cast(Any, rules.autopublish_state(consent.state, row.paused_at is not None)),
        autopublish_problem=consent.problem,
        consent_expires_at=row.consent_expires_at,
        paused_at=row.paused_at,
        timezone=row.timezone,
        today=await slots_out(session, on(today), row.timezone),
        tomorrow=await slots_out(session, on(today + timedelta(days=1)), row.timezone),
        stock=StockOut(
            count=len(library),
            days=rules.stock_cover(facts, len(library), moment, row.timezone),
            wanted_days=row.stock_days,
        ),
        budget=costs.budget_out(budget, row),
        channel=ChannelOut(
            linked=channel.linked,
            title=channel.title,
            audited=channel.audited,
            problem=channel.problem,
        ),
        worker_seen_at=row.last_tick_at,
        campaign=CampaignView(
            start=row.campaign_start,
            last_day=last_day,
            slots=sum(1 for slot in slots if slot.status != "skipped"),
            published=sum(1 for slot in slots if slot.status == "published"),
            missed=sum(1 for slot in slots if slot.status == "missed"),
        ),
        needs=needs,
        needs_count=len(needs),
    )


async def owner_needs_count(session: AsyncSession, now: datetime | None = None) -> int:
    """What waits for the owner on the Shorts tab besides reviews, for the sidebar's badge:
    the reviews are in its count already. Nothing is written, and with no settings row yet
    there is no run and nothing waits."""
    moment = now or datetime.now(UTC)
    row = await session.scalar(select(VideoShortsSettings).where(VideoShortsSettings.id == 1))
    if row is None:
        return 0
    slots, listed, budget, channel = await _load(session, row, moment)
    consent = consent_view(row, channel, moment)
    needs = build_needs(
        row=row,
        channel=channel,
        consent_state=consent.state,
        consent_problem=consent.problem,
        slots=[slot_facts(slot) for slot in slots],
        listed=listed,
        budget=budget,
        now=moment,
    )
    return sum(1 for need in needs if need.kind != "review")


# --- the numbers --------------------------------------------------------------------------------


def _number(value: Any) -> float | None:
    return float(value) if value is not None else None


def metric_out(row: VideoShortsMetric) -> MetricOut:
    return MetricOut(
        period=cast(Any, row.period),
        source=cast(Any, row.source),
        captured_at=row.captured_at,
        range_start=row.range_start,
        range_end=row.range_end,
        views=row.views,
        engaged_views=row.engaged_views,
        likes=row.likes,
        comments=row.comments,
        shares=row.shares,
        subscribers_gained=row.subscribers_gained,
        avg_view_seconds=_number(row.avg_view_seconds),
        avg_view_percent=_number(row.avg_view_percent),
        stayed_percent=_number(row.stayed_percent),
    )


async def metrics_view(
    session: AsyncSession, *, limit: int = METRICS_LIMIT, before: datetime | None = None
) -> MetricsOut:
    """The public Shorts, latest first, each with the snapshots stored for it."""
    moment = datetime.now(UTC)
    statement = select(VideoProject).where(
        VideoProject.shorts_line.is_not(None),
        VideoProject.youtube_video_id.is_not(None),
        VideoProject.youtube_publish_at <= moment,
    )
    if before is not None:
        statement = statement.where(VideoProject.youtube_publish_at < before)
    projects = list(
        await session.scalars(
            statement.order_by(VideoProject.youtube_publish_at.desc()).limit(limit)
        )
    )
    if not projects:
        return MetricsOut(items=[])
    rows = await session.scalars(
        select(VideoShortsMetric).where(
            VideoShortsMetric.project_slug.in_([project.slug for project in projects])
        )
    )
    order = {period: index for index, period in enumerate(METRIC_PERIODS)}
    by_slug: dict[str, list[VideoShortsMetric]] = {}
    for row in rows:
        by_slug.setdefault(row.project_slug, []).append(row)
    return MetricsOut(
        items=[
            ShortMetrics(
                slug=project.slug,
                title=project.title,
                line=cast(Any, project.shorts_line),
                series=project.shorts_series,
                youtube_video_id=str(project.youtube_video_id),
                published_at=project.youtube_publish_at,
                removed_at=project.youtube_removed_at,
                dropped_at=project.dropped_at,
                snapshots=[
                    metric_out(row)
                    for row in sorted(
                        # A snapshot of a video the row no longer names is another upload's.
                        (
                            row
                            for row in by_slug.get(project.slug, [])
                            if row.youtube_video_id == project.youtube_video_id
                        ),
                        key=lambda row: (order.get(row.period, len(order)), row.source),
                    )
                ],
            )
            for project in projects
        ]
    )
