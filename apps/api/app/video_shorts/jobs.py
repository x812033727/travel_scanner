"""The worker's next Shorts job (docs/videos/SHORTS.md §排片與時段), and a Short's start and
finish.

``next_job_for`` is the rule, as a pure function in the way of
``app.video_automation.series.next_job_for``: given what is known now it answers, in this
order, ``report`` (last week's report is not written), ``plan`` (Monday, or the library is
under ``stock_days``, and the plan window still has open slots), ``brief`` (the pool cannot
fill two weeks of the quotas, or the owner left ideas), ``make`` (the earliest planned slot
whose topic has no Short yet), or nothing. ``next_job`` loads the facts, writes the topics the
server makes itself, and builds the job the worker is given: for ``make`` the topic's whole
spec, its line, the owner's material, the source video and the channel's stance, since the
worker cannot read the Shorts documents in the repository.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, VideoProject, VideoReview
from app.video_automation.models import VideoAutomationSettings
from app.video_automation.usage import month_start
from app.video_shorts import costs, rules
from app.video_shorts import slots as shorts_slots
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsSettings, VideoShortsSlot, VideoShortsTopic
from app.video_shorts.plan import is_open, local_week, plan_window
from app.video_shorts.reports import published_between, report_job, reported_weeks, slot_ref
from app.video_shorts.schemas import (
    BriefJob,
    DoneIn,
    MakeJob,
    NextOut,
    PlanJob,
    SourceVideo,
    StartOut,
    TopicOut,
)
from app.video_shorts.settings import settings_row
from app.video_shorts.slots import library_of, shorts, slot_facts
from app.video_shorts.topics import (
    assets_of,
    ensure_auto_topics,
    is_paid,
    order_key,
    topic_out,
    topic_row,
    topic_summary,
    topic_view,
)

# A plan or a brief that left slots open, or the pool short, is not asked for again until
# this much later: the planner may have had nothing better to give.
PLAN_EVERY = timedelta(hours=12)
BRIEF_EVERY = timedelta(hours=12)
# The pool should hold this many weeks of the quotas in topics that can be planned now.
POOL_WEEKS = 2
# A topic the worker is making, or may make.
MAKEABLE = ("ready", "making")
STATUS_NAMES = {
    "idea": "規格還沒寫完",
    "needs_assets": "缺素材或工具",
    "made": "已經做完",
    "dropped": "已經放棄",
}


@dataclass(frozen=True)
class TopicFacts:
    slug: str
    line: str
    status: str
    paid: bool = False
    # The video it is being made under is dropped: the Short gave up, not the topic.
    project_dropped: bool = False
    # Its video is blocked and the owner has not asked for a retry the worker has yet to take:
    # the worker would do nothing with the make job, and the slots after it would wait.
    project_blocked: bool = False


@dataclass(frozen=True)
class JobFacts:
    """Everything the rule reads, loaded by ``next_job``."""

    now: datetime
    timezone: str
    enabled: bool
    paused: bool
    lines: tuple[str, ...]
    weekly_quota: Mapping[str, int]
    campaign_start: date | None
    stock_days: int
    # How many coming days of slots are filled, counting the library; None before the run.
    cover: int | None
    reported_weeks: frozenset[date]
    # Open slots between now and the end of next week.
    open_slots: int
    last_plan_at: datetime | None
    last_brief_at: datetime | None
    # Ready topics in the lines that are on and in no slot still to come, by line.
    pool: Mapping[str, int]
    owner_ideas: int
    # Slots still to come that the plan gave a topic and no Short holds, earliest first.
    planned: Sequence[rules.SlotFacts]
    topics: Mapping[str, TopicFacts]
    started_this_month: int
    max_per_month: int
    paid_allowed: bool
    budget_reason: str | None = None
    subject_chosen: bool = True


@dataclass(frozen=True)
class Decision:
    kind: str | None
    holds: tuple[str, ...] = ()
    report_week: date | None = None
    slot_id: UUID | None = None
    topic_slug: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


def report_week_due(
    now: datetime, timezone: str, campaign_start: date | None, reported: frozenset[date]
) -> date | None:
    """Last week, when the run had begun by its end and nobody wrote its report yet.

    Due from Monday on, through the week: a worker that was down on Monday still writes it.
    """
    if campaign_start is None:
        return None
    week = local_week(now, timezone) - timedelta(days=7)
    if campaign_start > week + timedelta(days=6) or week in reported:
        return None
    return week


def _cooled(last: datetime | None, every: timedelta, now: datetime) -> bool:
    return last is None or now - last >= every


def pool_want(lines: Sequence[str], quota: Mapping[str, int]) -> int:
    return POOL_WEEKS * sum(int(quota.get(line, 0)) for line in lines)


def next_job_for(facts: JobFacts) -> Decision:
    """The worker's next Shorts job, or none, and why the ones that might have come did not."""
    if not facts.enabled:
        return Decision(None, ("Shorts 的自動製作關著",))
    holds: list[str] = []
    week = report_week_due(facts.now, facts.timezone, facts.campaign_start, facts.reported_weeks)
    if week is not None:
        return Decision("report", report_week=week)
    monday = facts.now.astimezone(ZoneInfo(facts.timezone)).weekday() == 0
    low = facts.cover is not None and facts.cover < facts.stock_days
    have = sum(facts.pool.get(line, 0) for line in facts.lines)
    if (monday or low) and facts.open_slots > 0:
        if have == 0:
            holds.append("題庫沒有可以排的題目，先補題")
        elif _cooled(facts.last_plan_at, PLAN_EVERY, facts.now):
            return Decision("plan", tuple(holds))
    want = pool_want(facts.lines, facts.weekly_quota)
    if (have < want or facts.owner_ideas > 0) and _cooled(
        facts.last_brief_at, BRIEF_EVERY, facts.now
    ):
        return Decision("brief", tuple(holds), extra={"have": have, "want": want})
    if facts.paused:
        holds.append("Shorts 暫停中，不開始新的製作")
        return Decision(None, tuple(holds))
    for slot in facts.planned:
        if slot.starts_at <= facts.now or slot.topic_slug is None:
            continue
        topic = facts.topics.get(slot.topic_slug)
        if topic is None or topic.line not in facts.lines:
            continue
        if topic.status not in MAKEABLE or (topic.status == "making" and topic.project_dropped):
            continue
        if topic.status == "making" and topic.project_blocked:
            holds.append(f"「{topic.slug}」卡住了，等站主處理")
            continue
        new = topic.status == "ready"
        if new and facts.started_this_month >= facts.max_per_month:
            holds.append(
                f"本月已經開始 {facts.started_this_month} 支 Shorts，每月上限 "
                f"{facts.max_per_month} 支"
            )
            continue
        if new and topic.paid and not facts.paid_allowed:
            holds.append(f"「{topic.slug}」要花錢：{facts.budget_reason or '預算不開新的付費工作'}")
            continue
        if topic.line == "lab" and not facts.subject_chosen:
            holds.append("Shorts 設定還沒選受測模型，實測線不能做")
            continue
        return Decision("make", tuple(dict.fromkeys(holds)), slot_id=slot.id, topic_slug=topic.slug)
    return Decision(None, tuple(dict.fromkeys(holds)))


# --- loading and building the job ---------------------------------------------------------------


def _future_topic_slots(slots: Sequence[VideoShortsSlot], now: datetime) -> set[str]:
    return {
        str(slot.topic_slug)
        for slot in slots
        if slot.topic_slug and slot.starts_at > now and slot.status not in ("missed", "skipped")
    }


async def _started_this_month(session: AsyncSession, now: datetime) -> int:
    """The topics started this month, against ``max_per_month``. A topic given up counts only
    when its Short was made after all: its video reached the owner (it has a review, which
    ``_drop_empty_video`` also reads as made) or YouTube. One given up before that made no
    Short and leaves its place in the month to another."""
    reviewed = exists().where(VideoReview.project_id == VideoProject.id)
    return int(
        await session.scalar(
            select(func.count(VideoShortsTopic.id))
            .outerjoin(VideoProject, VideoProject.slug == VideoShortsTopic.project_slug)
            .where(
                VideoShortsTopic.started_at >= month_start(now),
                or_(
                    VideoShortsTopic.status != "dropped",
                    VideoProject.youtube_video_id.is_not(None),
                    reviewed,
                ),
            )
        )
        or 0
    )


async def _projects(session: AsyncSession, slugs: Sequence[str]) -> dict[str, VideoProject]:
    wanted = sorted({slug for slug in slugs if slug})
    if not wanted:
        return {}
    rows = await session.scalars(select(VideoProject).where(VideoProject.slug.in_(wanted)))
    return {row.slug: row for row in rows}


def _waits_for_owner(project: VideoProject) -> bool:
    """Blocked with no retry the worker still has to pick up."""
    pending_retry = (
        project.retry_request_id is not None
        and project.retry_request_id != project.retry_acknowledged_id
    )
    return project.stage == "blocked" and not pending_retry


def source_video(project: VideoProject | None) -> SourceVideo | None:
    if project is None:
        return None
    return SourceVideo(
        slug=project.slug,
        title=project.title,
        format=project.format,
        youtube_video_id=project.youtube_video_id,
        youtube_publish_at=project.youtube_publish_at,
        source_guide=project.source_guide,
        category=project.category,
        series_slug=project.series_slug,
        episode_number=project.episode_number,
    )


async def next_job(session: AsyncSession, now: datetime | None = None) -> NextOut:
    moment = now or datetime.now(UTC)
    row = await settings_row(session)
    if row.enabled:
        await ensure_auto_topics(session, moment)
        await session.flush()
    slots = list(await session.scalars(select(VideoShortsSlot).order_by(VideoShortsSlot.starts_at)))
    topics = sorted(
        await session.scalars(
            select(VideoShortsTopic).where(
                VideoShortsTopic.status.in_(("idea", "ready", "needs_assets", "making"))
            )
        ),
        key=order_key,
    )
    projects = await _projects(session, [str(topic.project_slug or "") for topic in topics])
    listed = await shorts(session, public=False, now=moment)
    facts_slots = [slot_facts(slot) for slot in slots]
    cover = rules.stock_cover(facts_slots, len(library_of(listed, moment)), moment, row.timezone)
    _start, window_end = plan_window(moment, row.timezone)
    open_slots = [
        slot
        for slot in slots
        if is_open(slot_facts(slot)) and moment + rules.MIN_LEAD < slot.starts_at < window_end
    ]
    in_slots = _future_topic_slots(slots, moment)
    lines = tuple(row.lines)
    pool_rows = [
        topic
        for topic in topics
        if topic.status == "ready" and topic.line in lines and topic.slug not in in_slots
    ]
    pool: dict[str, int] = {}
    for topic in pool_rows:
        pool[topic.line] = pool.get(topic.line, 0) + 1
    budget = await costs.budget(session, row, moment)
    facts = JobFacts(
        now=moment,
        timezone=row.timezone,
        enabled=row.enabled,
        paused=row.paused_at is not None,
        lines=lines,
        weekly_quota=dict(row.weekly_quota),
        campaign_start=row.campaign_start,
        stock_days=row.stock_days,
        cover=cover,
        reported_weeks=frozenset(
            await reported_weeks(session, local_week(moment, row.timezone) - timedelta(days=21))
        ),
        open_slots=len(open_slots),
        last_plan_at=row.last_plan_at,
        last_brief_at=row.last_brief_at,
        pool=pool,
        owner_ideas=sum(
            1 for topic in topics if topic.status == "idea" and topic.origin == "owner"
        ),
        planned=[
            slot_facts(slot)
            for slot in slots
            if slot.status == "planned" and slot.topic_slug and slot.project_slug is None
        ],
        topics={
            topic.slug: TopicFacts(
                slug=topic.slug,
                line=topic.line,
                status=topic.status,
                paid=is_paid(topic.line, topic.brief or {}),
                project_dropped=(
                    topic.project_slug in projects
                    and projects[topic.project_slug].dropped_at is not None
                ),
                project_blocked=(
                    topic.project_slug in projects
                    and _waits_for_owner(projects[topic.project_slug])
                ),
            )
            for topic in topics
        },
        started_this_month=await _started_this_month(session, moment),
        max_per_month=row.max_per_month,
        paid_allowed=budget.paid_work_allowed,
        budget_reason=budget.reason,
        subject_chosen=bool((row.subject_models or {}).get("a")),
    )
    decision = next_job_for(facts)
    out = NextOut(kind=cast(Any, decision.kind), holds=list(decision.holds))
    if decision.kind == "report" and decision.report_week is not None:
        out.report = await report_job(session, row, decision.report_week, moment)
    elif decision.kind == "plan":
        out.plan = await _plan_job(session, row, moment, open_slots, slots, pool_rows, budget)
    elif decision.kind == "brief":
        out.brief = await _brief_job(session, row, topics, decision)
    elif decision.kind == "make":
        out.make = await _make_job(session, row, slots, topics, decision)
    await session.commit()
    return out


async def _plan_job(
    session: AsyncSession,
    row: VideoShortsSettings,
    now: datetime,
    open_slots: Sequence[VideoShortsSlot],
    slots: Sequence[VideoShortsSlot],
    pool_rows: Sequence[VideoShortsTopic],
    budget: rules.BudgetState,
) -> PlanJob:
    start, end = plan_window(now, row.timezone)
    last_week = local_week(now, row.timezone) - timedelta(days=7)
    zone = ZoneInfo(row.timezone)
    week_begin = datetime.combine(last_week, datetime.min.time(), tzinfo=zone).astimezone(UTC)
    return PlanJob(
        window_start=start,
        window_end=end,
        timezone=row.timezone,
        lines=cast(Any, list(row.lines)),
        weekly_quota=dict(row.weekly_quota),
        open_slots=[slot_ref(slot, row.timezone) for slot in open_slots],
        planned=[
            slot_ref(slot, row.timezone)
            for slot in slots
            if start < slot.starts_at < end and not is_open(slot_facts(slot))
        ],
        topics=[
            topic_summary(topic)
            for topic in pool_rows
            if budget.paid_work_allowed or not is_paid(topic.line, topic.brief or {})
        ],
        last_week=await published_between(session, week_begin, week_begin + timedelta(days=7)),
        budget=costs.budget_out(budget, row),
    )


async def _brief_job(
    session: AsyncSession,
    row: VideoShortsSettings,
    topics: Sequence[VideoShortsTopic],
    decision: Decision,
) -> BriefJob:
    ideas = [topic for topic in topics if topic.status == "idea"]
    found = await assets_of(session, [topic.slug for topic in ideas])
    every = sorted(
        await session.scalars(select(VideoShortsTopic).where(VideoShortsTopic.status != "dropped")),
        key=order_key,
    )
    by_line: dict[str, int] = {}
    for topic in topics:
        if topic.status == "ready":
            by_line[topic.line] = by_line.get(topic.line, 0) + 1
    return BriefJob(
        lines=cast(Any, list(row.lines)),
        weekly_quota=dict(row.weekly_quota),
        have=int(decision.extra.get("have", 0)),
        want=int(decision.extra.get("want", 0)),
        by_line=by_line,
        ideas=[topic_out(topic, found.get(topic.slug, [])) for topic in ideas],
        existing=[topic_summary(topic) for topic in every],
    )


async def _make_job(
    session: AsyncSession,
    row: VideoShortsSettings,
    slots: Sequence[VideoShortsSlot],
    topics: Sequence[VideoShortsTopic],
    decision: Decision,
) -> MakeJob:
    slot = next(slot for slot in slots if slot.id == decision.slot_id)
    topic = next(topic for topic in topics if topic.slug == decision.topic_slug)
    source = (await _projects(session, [topic.source_slug or ""])).get(topic.source_slug or "")
    automation = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    return MakeJob(
        slot=slot_ref(slot, row.timezone),
        topic=await topic_view(session, topic),
        line=cast(Any, topic.line),
        project_slug=topic.project_slug if topic.status == "making" else None,
        resume=topic.status == "making",
        source=source_video(source),
        channel_stance=(automation.channel_stance if automation is not None else "") or "",
        seconds_min=row.seconds_min,
        seconds_max=row.seconds_max,
    )


# --- a Short's start and finish -----------------------------------------------------------------


async def _free_slug(session: AsyncSession, base: str) -> str:
    """The video slug for a topic: its own, or with -2, -3… when a video already has it."""
    for number in range(1, 20):
        candidate = base if number == 1 else f"{base[: 80 - len(str(number)) - 1]}-{number}"
        taken = await session.scalar(select(VideoProject.id).where(VideoProject.slug == candidate))
        if taken is None:
            return candidate
    raise ShortsRefused(409, "video_shorts_topic_slug_taken", "這個題目的影片代號都被用掉了")


async def start_topic(session: AsyncSession, slug: str, now: datetime | None = None) -> StartOut:
    """The worker starts a topic: the topic is ``making`` and its Short is a video, so the
    tab lists it while it is made. Starting a topic already in the making answers with the
    same video, so a worker that lost its place picks it up again."""
    moment = now or datetime.now(UTC)
    row = await settings_row(session)
    topic = await topic_row(session, slug, lock=True)
    current = (
        await session.scalar(select(VideoProject).where(VideoProject.slug == topic.project_slug))
        if topic.project_slug
        else None
    )
    if topic.status == "making" and current is not None and current.dropped_at is None:
        return StartOut(
            topic=await topic_view(session, topic), project_slug=current.slug, created=False
        )
    if topic.status not in MAKEABLE:
        raise ShortsRefused(
            409,
            "video_shorts_topic_not_ready",
            f"這個題目還不能開始做（{STATUS_NAMES.get(topic.status, topic.status)}）",
        )
    if not row.enabled:
        raise ShortsRefused(409, "video_shorts_off", "Shorts 的自動製作關著")
    if row.paused_at is not None:
        raise ShortsRefused(409, "video_shorts_paused", "Shorts 暫停中，不開始新的製作")
    started = await _started_this_month(session, moment)
    if started >= row.max_per_month:
        raise ShortsRefused(
            409,
            "video_shorts_month_full",
            f"本月已經開始 {started} 支 Shorts，每月上限 {row.max_per_month} 支",
        )
    if is_paid(topic.line, topic.brief or {}):
        budget = await costs.budget(session, row, moment)
        if not budget.paid_work_allowed:
            raise ShortsRefused(
                409, "video_shorts_budget_stops", budget.reason or "預算不開新的付費工作"
            )
    project_slug = await _free_slug(session, topic.slug)
    session.add(
        VideoProject(
            slug=project_slug,
            title=topic.title[:200],
            stage="brief",
            format="drama" if topic.line == "drama" else "shorts",
            shorts_line=topic.line,
            shorts_series=topic.series,
            source_slug=topic.source_slug,
            checklist=[],
            last_synced_at=moment,
            created_at=moment,
            updated_at=moment,
        )
    )
    topic.status = "making"
    topic.project_slug = project_slug
    topic.started_at = moment
    topic.updated_at = moment
    await session.commit()
    return StartOut(topic=await topic_view(session, topic), project_slug=project_slug, created=True)


async def finish_topic(
    session: AsyncSession, slug: str, payload: DoneIn, now: datetime | None = None
) -> TopicOut:
    """The worker is done with a topic: its Short was pushed, or the topic gives no Short
    (a tutorial with no second point worth a highlight). Sending the same again is a no-op."""
    moment = now or datetime.now(UTC)
    topic = await topic_row(session, slug, lock=True)
    final = "made" if payload.outcome == "made" else "dropped"
    if topic.status == final:
        return await topic_view(session, topic)
    if topic.status != "making":
        raise ShortsRefused(
            409, "video_shorts_topic_not_making", "這個題目沒有在製作中，不能標成做完"
        )
    topic.status = final
    topic.finished_at = moment
    if payload.note is not None:
        topic.note = payload.note or None
    topic.updated_at = moment
    if final == "dropped":
        if topic.project_slug:
            # The reason is this drop's own; a note the topic carried from before is not one.
            await _drop_empty_video(session, topic.project_slug, payload.note or None, moment)
        await shorts_slots.unplan(session, topic.slug, moment)
    await session.commit()
    return await topic_view(session, topic)


async def _drop_empty_video(
    session: AsyncSession, slug: str, note: str | None, moment: datetime
) -> None:
    """A topic given up before anything reached the owner leaves its video with nothing in it
    (a tutorial with one highlight: start_topic made the video, the worker found no passage).
    Drop that video too, as the owner would, so it leaves 製作中 and the calendar. A video
    that already has a review is the owner's to judge and stays. The caller commits."""
    project = await session.scalar(
        select(VideoProject).where(VideoProject.slug == slug).with_for_update()
    )
    if project is None or project.dropped_at is not None:
        return
    reviews = await session.scalar(
        select(func.count()).select_from(VideoReview).where(VideoReview.project_id == project.id)
    )
    if reviews:
        return
    project.dropped_at = moment
    project.dropped_note = note or "Shorts 題目放棄，影片還沒有任何內容"
    project.updated_at = moment
    await shorts_slots.release(session, slug, moment)
    session.add(
        AdminAuditLog(
            actor_user_id=None,
            action="video_project_dropped",
            target=f"video_project:{project.id}",
            metadata_json={"slug": slug, "by": "shorts_topic_dropped"},
        )
    )
