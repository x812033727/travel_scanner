"""The slot calendar: building it, giving Shorts their slots, locking them, and the owner's
changes on the calendar. The decisions are ``rules``'; this module loads the rows and
applies them.

``assign_approved`` and ``lock_due_slots`` write on the caller's session and leave the
commit to it; their reads never flush the caller's pending rows.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Any, cast
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import and_, delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_shorts import rules
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import (
    HOLDING_STATUSES,
    VideoShortsSettings,
    VideoShortsSlot,
    VideoShortsTopic,
)
from app.video_shorts.schemas import CampaignOut, SlotOut, SlotPatch, SlotsOut
from app.video_shorts.settings import channel_facts, settings_row

# A slot the run has already acted on: from here on the calendar is history too.
STARTED_STATUSES = ("locked", "scheduled", "published", "missed")
# What the owner may still change on the calendar. A slot that is on YouTube is recalled
# first; one that is past stays as it happened.
CHANGEABLE_STATUSES = ("open", "planned", "assigned", "locked", "skipped")


@dataclass(frozen=True)
class Hold:
    """The slot a Short holds, if any, and how many it has missed."""

    starts_at: datetime | None = None
    status: str | None = None
    missed: int = 0


@dataclass(frozen=True)
class Short:
    """A Short with what its state is read from."""

    project: VideoProject
    pending: int
    approved_at: datetime | None
    hold: Hold

    def state_at(self, now: datetime) -> str:
        return state_of(self.project, self.pending, self.approved_at, self.hold, now)

    @property
    def state(self) -> str:
        return self.state_at(datetime.now(UTC))


def slot_facts(row: VideoShortsSlot) -> rules.SlotFacts:
    return rules.SlotFacts(
        id=row.id,
        starts_at=row.starts_at,
        status=row.status,
        line=row.line,
        topic_slug=row.topic_slug,
        project_slug=row.project_slug,
    )


def short_facts(
    project: VideoProject, pending: int, approved_at: datetime | None, hold: Hold | None
) -> rules.ShortFacts:
    sync = project.youtube_sync if isinstance(project.youtube_sync, dict) else None
    return rules.ShortFacts(
        dropped=project.dropped_at is not None,
        blocked=project.stage == "blocked",
        pending_reviews=pending,
        package_approved=approved_at is not None,
        youtube_video_id=project.youtube_video_id,
        youtube_publish_at=project.youtube_publish_at,
        sync_done=None if sync is None else sync.get("status") == "done",
        slot_status=hold.status if hold else None,
        missed_slots=hold.missed if hold else 0,
    )


def state_of(
    project: VideoProject,
    pending: int,
    approved_at: datetime | None,
    hold: Hold | None,
    now: datetime | None = None,
) -> str:
    return rules.shorts_state(
        short_facts(project, pending, approved_at, hold), now or datetime.now(UTC)
    )


async def holds(session: AsyncSession, slugs: Sequence[str]) -> dict[str, Hold]:
    """For each of these Shorts, the slot it holds and how many it missed."""
    if not slugs:
        return {}
    rows = await session.scalars(
        select(VideoShortsSlot).where(VideoShortsSlot.project_slug.in_(list(slugs)))
    )
    found: dict[str, Hold] = {}
    for row in rows:
        slug = str(row.project_slug)
        hold = found.get(slug, Hold())
        if row.status in HOLDING_STATUSES:
            hold = Hold(row.starts_at, row.status, hold.missed)
        elif row.status == "missed":
            hold = Hold(hold.starts_at, hold.status, hold.missed + 1)
        found[slug] = hold
    return found


async def shorts(
    session: AsyncSession,
    *,
    slugs: Sequence[str] | None = None,
    public: bool | None = None,
    now: datetime | None = None,
) -> list[Short]:
    """The Shorts that are not dropped, each with what its state is read from.

    ``public`` False leaves out the ones whose publish time is past, which is every Short
    the calendar still has to deal with; the public ones only grow.
    """
    pending = (
        select(VideoReview.project_id, func.count().label("pending"))
        .where(VideoReview.status == "pending")
        .group_by(VideoReview.project_id)
        .subquery()
    )
    confirmed = (
        select(VideoReview.project_id, func.max(VideoReview.decided_at).label("decided_at"))
        .where(VideoReview.gate == "publish", VideoReview.status == "approved")
        .group_by(VideoReview.project_id)
        .subquery()
    )
    statement = (
        select(VideoProject, func.coalesce(pending.c.pending, 0), confirmed.c.decided_at)
        .outerjoin(pending, pending.c.project_id == VideoProject.id)
        .outerjoin(confirmed, confirmed.c.project_id == VideoProject.id)
        .where(VideoProject.shorts_line.is_not(None), VideoProject.dropped_at.is_(None))
    )
    if slugs is not None:
        statement = statement.where(VideoProject.slug.in_(list(slugs)))
    if public is not None:
        moment = now or datetime.now(UTC)
        statement = statement.where(
            and_(
                VideoProject.youtube_video_id.is_not(None),
                VideoProject.youtube_publish_at <= moment,
            )
            if public
            else or_(
                VideoProject.youtube_video_id.is_(None),
                VideoProject.youtube_publish_at.is_(None),
                VideoProject.youtube_publish_at > moment,
            )
        )
    rows = list((await session.execute(statement)).all())
    held = await holds(session, [project.slug for project, _count, _at in rows])
    return [
        Short(project, int(count), approved_at, held.get(project.slug, Hold()))
        for project, count, approved_at in rows
    ]


def library_of(listed: Iterable[Short], now: datetime | None = None) -> list[rules.LibraryShort]:
    """The approved Shorts that hold no slot, as the rules take them."""
    moment = now or datetime.now(UTC)
    return [
        rules.LibraryShort(
            slug=short.project.slug,
            line=str(short.project.shorts_line),
            approved_at=short.approved_at or short.project.last_synced_at,
            uploaded=short.project.youtube_video_id is not None,
        )
        for short in listed
        if short.state_at(moment) in ("library", "missed")
    ]


def _take(slot: VideoShortsSlot, slug: str, status: str, now: datetime) -> None:
    slot.project_slug = slug
    slot.status = status
    slot.locked_at = now if status == "locked" else None
    slot.updated_at = now


def _empty(slot: VideoShortsSlot, now: datetime) -> None:
    slot.project_slug = None
    slot.status = "planned" if slot.topic_slug else "open"
    slot.locked_at = None
    slot.updated_at = now


async def _slots_for(session: AsyncSession, slug: str, now: datetime) -> list[VideoShortsSlot]:
    """The slots still ahead and the one this Short holds, locked for this transaction so
    two Shorts approved at the same moment cannot take the same one."""
    return list(
        await session.scalars(
            select(VideoShortsSlot)
            .where(
                or_(
                    VideoShortsSlot.starts_at > now,
                    and_(
                        VideoShortsSlot.project_slug == slug,
                        VideoShortsSlot.status.in_(HOLDING_STATUSES),
                    ),
                )
            )
            .order_by(VideoShortsSlot.starts_at)
            .with_for_update()
        )
    )


async def assign_approved(
    session: AsyncSession, project: VideoProject, now: datetime | None = None
) -> VideoShortsSlot | None:
    """Give a Short whose upload package was just approved its slot, when the run has one
    for it; without a calendar it waits in the library. The caller commits."""
    if project.shorts_line is None or project.dropped_at is not None:
        return None
    moment = now or datetime.now(UTC)
    with session.no_autoflush:
        found = await _slots_for(session, project.slug, moment)
        # A Short the worker made from a topic goes to the slot the weekly plan gave the topic.
        topic = await session.scalar(
            select(VideoShortsTopic.slug).where(VideoShortsTopic.project_slug == project.slug)
        )
    chosen = rules.assign_slot(
        [slot_facts(slot) for slot in found],
        rules.LibraryShort(project.slug, project.shorts_line, moment, topic_slug=topic),
        moment,
    )
    if chosen is None:
        return None
    slot = next(slot for slot in found if slot.id == chosen.id)
    if slot.project_slug != project.slug:
        _take(slot, project.slug, "assigned", moment)
    return slot


async def release(session: AsyncSession, slug: str, now: datetime | None = None) -> int:
    """Empty the slots a Short holds that are not on YouTube yet, when it is dropped. The
    caller commits."""
    moment = now or datetime.now(UTC)
    with session.no_autoflush:
        held = list(
            await session.scalars(
                select(VideoShortsSlot)
                .where(
                    VideoShortsSlot.project_slug == slug,
                    VideoShortsSlot.status.in_(("assigned", "locked")),
                )
                .with_for_update()
            )
        )
    for slot in held:
        _empty(slot, moment)
    return len(held)


async def unplan(session: AsyncSession, topic_slug: str, now: datetime | None = None) -> int:
    """Give the plan back the slots still ahead that it gave a topic now dropped and that no
    Short holds: open again, with no topic, line or series, so the next weekly plan can fill
    them and the week's line quotas no longer count them. A slot that is past, or that holds
    a Short, stays as it is. The caller commits."""
    moment = now or datetime.now(UTC)
    with session.no_autoflush:
        planned = list(
            await session.scalars(
                select(VideoShortsSlot)
                .where(
                    VideoShortsSlot.topic_slug == topic_slug,
                    VideoShortsSlot.status == "planned",
                    VideoShortsSlot.project_slug.is_(None),
                    VideoShortsSlot.starts_at > moment,
                )
                .with_for_update()
            )
        )
    for slot in planned:
        slot.status = "open"
        slot.topic_slug = None
        slot.line = None
        slot.series = None
        slot.updated_at = moment
    return len(planned)


async def lock_due_slots(
    session: AsyncSession, now: datetime | None = None
) -> list[rules.SlotChange]:
    """Lock the slots whose time has come, fill the empty ones from the library, and give
    up the ones that can no longer go out (``rules.lock_due``). The caller commits."""
    moment = now or datetime.now(UTC)
    row = await settings_row(session)
    due = list(
        await session.scalars(
            select(VideoShortsSlot)
            .where(
                VideoShortsSlot.status.in_(("open", "planned", "assigned", "locked")),
                VideoShortsSlot.starts_at <= moment + timedelta(hours=row.lock_hours),
            )
            .order_by(VideoShortsSlot.starts_at)
            .with_for_update()
        )
    )
    if not due:
        return []
    waiting = await shorts(session, public=False, now=moment)
    channel = await channel_facts(session)
    changes = rules.lock_due(
        [slot_facts(slot) for slot in due],
        library_of(waiting, moment),
        [
            short.project.slug
            for short in waiting
            if short.state_at(moment) in ("library", "missed", "slotted")
        ],
        moment,
        row.lock_hours,
        # Until the API audit passes only a file the owner uploaded can go out.
        prefer_uploaded=not channel.audited,
    )
    by_id = {slot.id: slot for slot in due}
    for change in changes:
        slot = by_id[change.slot_id]
        slot.status = change.status
        slot.project_slug = change.project_slug
        slot.locked_at = moment if change.status == "locked" else slot.locked_at
        slot.note = change.note or slot.note
        slot.updated_at = moment
    return changes


# --- the run ------------------------------------------------------------------------------------


async def start_campaign(
    session: AsyncSession, actor: User, first_day: date, now: datetime | None = None
) -> CampaignOut:
    """Build the run's calendar from the day its first Short goes public.

    Until the run has acted on a slot the calendar can be rebuilt from another day; the
    Shorts that held slots, and the ones waiting in the library, are given the new slots in
    the order they were approved. Once a slot was locked the calendar is changed slot by
    slot instead.
    """
    moment = now or datetime.now(UTC)
    row = await settings_row(session, lock=True)
    plans = rules.build_slots(first_day, row.daily_pattern, row.slot_times, row.timezone)
    if not plans:
        raise ShortsRefused(422, "video_shorts_pattern_empty", "照現在的節奏排不出任何時段")
    if plans[0].starts_at - rules.MIN_LEAD <= moment:
        raise ShortsRefused(
            422, "video_shorts_campaign_past", "第一支公開的時間已經過了，請選之後的日期"
        )
    existing = list(await session.scalars(select(VideoShortsSlot).with_for_update()))
    if any(slot.status in STARTED_STATUSES for slot in existing):
        raise ShortsRefused(
            409,
            "video_shorts_campaign_running",
            "這一輪已經開始了，不能整個重排；要改時段請在月曆上一格一格調整",
        )
    if existing:
        await session.execute(delete(VideoShortsSlot))
        await session.flush()
    created = [
        VideoShortsSlot(id=uuid4(), starts_at=plan.starts_at, phase=plan.phase, status="open")
        for plan in plans
    ]
    session.add_all(created)
    waiting = sorted(
        library_of(await shorts(session, public=False, now=moment), moment),
        key=lambda short: short.approved_at,
    )
    # The Shorts that held a slot a moment ago read as slotted above only if their slots
    # were still there; they were deleted, so they are in the library with the rest.
    facts = [slot_facts(slot) for slot in created]
    assigned = 0
    for short in waiting:
        chosen = rules.assign_slot(facts, short, moment)
        if chosen is None:
            break
        slot = next(slot for slot in created if slot.id == chosen.id)
        _take(slot, short.slug, "assigned", moment)
        facts = [slot_facts(slot) for slot in created]
        assigned += 1
    row.campaign_start = first_day
    row.updated_by_user_id = actor.id
    last_day = first_day + timedelta(days=rules.pattern_days(row.daily_pattern) - 1)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_campaign_started",
            target="video-shorts-settings:1",
            metadata_json={
                "first_day": first_day.isoformat(),
                "last_day": last_day.isoformat(),
                "slots": len(created),
                "assigned": assigned,
                "rebuilt": bool(existing),
            },
        )
    )
    await session.commit()
    return CampaignOut(
        campaign_start=first_day, last_day=last_day, slots=len(created), assigned=assigned
    )


# --- the calendar page --------------------------------------------------------------------------


def slot_out(slot: VideoShortsSlot, zone: ZoneInfo, projects: dict[str, VideoProject]) -> SlotOut:
    local = slot.starts_at.astimezone(zone)
    project = projects.get(slot.project_slug or "")
    return SlotOut(
        id=slot.id,
        starts_at=slot.starts_at,
        local_date=local.date(),
        local_time=local.strftime("%H:%M"),
        phase=slot.phase,
        line=cast(Any, slot.line),
        series=slot.series,
        topic_slug=slot.topic_slug,
        project_slug=slot.project_slug,
        project_title=project.title if project else None,
        project_line=cast(Any, project.shorts_line) if project else None,
        youtube_video_id=project.youtube_video_id if project else None,
        status=cast(Any, slot.status),
        locked_at=slot.locked_at,
        note=slot.note,
    )


async def _projects(session: AsyncSession, slugs: Iterable[str]) -> dict[str, VideoProject]:
    wanted = sorted({slug for slug in slugs if slug})
    if not wanted:
        return {}
    rows = await session.scalars(select(VideoProject).where(VideoProject.slug.in_(wanted)))
    return {row.slug: row for row in rows}


async def slots_out(
    session: AsyncSession, rows: Sequence[VideoShortsSlot], timezone: str
) -> list[SlotOut]:
    projects = await _projects(session, [str(row.project_slug or "") for row in rows])
    zone = ZoneInfo(timezone)
    return [slot_out(row, zone, projects) for row in rows]


def day_bounds(day: date, timezone: str) -> tuple[datetime, datetime]:
    """The moments a local day starts and ends."""
    zone = ZoneInfo(timezone)
    start = datetime.combine(day, time(0), tzinfo=zone)
    return start.astimezone(UTC), (start + timedelta(days=1)).astimezone(UTC)


async def list_slots(
    session: AsyncSession, first: date | None = None, last: date | None = None
) -> SlotsOut:
    """The calendar between two local days, both included; all of it when neither is given."""
    row = await settings_row(session)
    statement = select(VideoShortsSlot)
    if first is not None:
        statement = statement.where(VideoShortsSlot.starts_at >= day_bounds(first, row.timezone)[0])
    if last is not None:
        statement = statement.where(VideoShortsSlot.starts_at < day_bounds(last, row.timezone)[1])
    rows = list(await session.scalars(statement.order_by(VideoShortsSlot.starts_at)))
    await session.commit()
    return SlotsOut(timezone=row.timezone, slots=await slots_out(session, rows, row.timezone))


async def _move(
    session: AsyncSession,
    row: VideoShortsSettings,
    slot: VideoShortsSlot,
    starts_at: datetime,
    now: datetime,
) -> None:
    target = starts_at.astimezone(UTC)
    if target - rules.MIN_LEAD <= now:
        raise ShortsRefused(422, "video_shorts_slot_past", "新的時間已經過了，或離現在太近")
    start, end = day_bounds(target.astimezone(ZoneInfo(row.timezone)).date(), row.timezone)
    same_day = list(
        await session.scalars(
            select(VideoShortsSlot).where(
                VideoShortsSlot.starts_at >= start,
                VideoShortsSlot.starts_at < end,
                VideoShortsSlot.id != slot.id,
                VideoShortsSlot.status != "skipped",
            )
        )
    )
    if any(other.starts_at == target for other in same_day):
        raise ShortsRefused(409, "video_shorts_slot_taken", "那個時間已經有一格了")
    if len(same_day) >= row.max_per_day:
        raise ShortsRefused(
            409,
            "video_shorts_day_full",
            f"那一天已經有 {len(same_day)} 格，一天最多 {row.max_per_day} 支",
        )
    slot.starts_at = target
    if row.campaign_start is not None:
        first = day_bounds(row.campaign_start, row.timezone)[0]
        slot.phase = max((target - first).days // rules.PERIOD_DAYS + 1, 1)
    if slot.status == "locked":
        # Locked again on the next round if the new time is inside the lock window.
        slot.status = "assigned"
        slot.locked_at = None


async def _assign(session: AsyncSession, slot: VideoShortsSlot, slug: str, now: datetime) -> None:
    found = await shorts(session, slugs=[slug])
    if not found:
        raise ShortsRefused(404, "video_shorts_not_found", "找不到這支 Shorts，或它已經被放棄")
    short = found[0]
    if short.state_at(now) not in ("library", "missed", "slotted"):
        raise ShortsRefused(
            409,
            "video_shorts_not_ready",
            "這支 Shorts 還不能排：上傳包要先核准，而且還沒有排上 YouTube",
        )
    if slot.project_slug == slug:
        return
    other = await session.scalar(
        select(VideoShortsSlot)
        .where(
            VideoShortsSlot.project_slug == slug,
            VideoShortsSlot.status.in_(HOLDING_STATUSES),
            VideoShortsSlot.id != slot.id,
        )
        .with_for_update()
    )
    if other is not None:
        if other.status not in ("assigned", "locked"):
            raise ShortsRefused(
                409, "video_shorts_slot_fixed", "這支已經排上 YouTube，要先撤回才能換時段"
            )
        _empty(other, now)
        # The unique index counts the old slot until it is written.
        await session.flush()
    _take(slot, slug, "assigned", now)


async def patch_slot(
    session: AsyncSession,
    actor: User,
    slot_id: UUID,
    payload: SlotPatch,
    now: datetime | None = None,
) -> SlotOut:
    """One change the owner makes on the calendar; every change is logged."""
    moment = now or datetime.now(UTC)
    row = await settings_row(session)
    slot = await session.scalar(
        select(VideoShortsSlot).where(VideoShortsSlot.id == slot_id).with_for_update()
    )
    if slot is None:
        raise ShortsRefused(404, "video_shorts_slot_not_found", "找不到這一格")
    if payload.action != "note" and slot.status not in CHANGEABLE_STATUSES:
        raise ShortsRefused(
            409,
            "video_shorts_slot_fixed",
            "這一格已經排上 YouTube 或已經過去，不能在這裡改；已排程的請先撤回",
        )
    before = {"starts_at": slot.starts_at.isoformat(), "status": slot.status}
    held = slot.project_slug
    if payload.action == "move":
        await _move(session, row, slot, cast(datetime, payload.starts_at), moment)
    elif payload.action == "assign":
        if slot.status == "skipped":
            raise ShortsRefused(409, "video_shorts_slot_skipped", "這一格標成不發了，先重新開啟")
        await _assign(session, slot, cast(str, payload.project_slug), moment)
    elif payload.action == "clear":
        if slot.status == "skipped":
            raise ShortsRefused(409, "video_shorts_slot_skipped", "這一格標成不發了，先重新開啟")
        _empty(slot, moment)
    elif payload.action == "skip":
        slot.project_slug = None
        slot.status = "skipped"
        slot.locked_at = None
    elif payload.action == "reopen":
        if slot.status != "skipped":
            raise ShortsRefused(409, "video_shorts_slot_not_skipped", "這一格沒有標成不發")
        if slot.starts_at - rules.MIN_LEAD <= moment:
            raise ShortsRefused(422, "video_shorts_slot_past", "這一格的時間已經過了")
        _empty(slot, moment)
    if payload.note is not None:
        slot.note = payload.note or None
    slot.updated_at = moment
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_slot_changed",
            target=f"video_shorts_slot:{slot.id}",
            metadata_json={
                "action": payload.action,
                "before": before,
                "starts_at": slot.starts_at.isoformat(),
                "status": slot.status,
                "slug": slot.project_slug,
                "released": held if held != slot.project_slug else None,
            },
        )
    )
    await session.commit()
    return (await slots_out(session, [slot], row.timezone))[0]
