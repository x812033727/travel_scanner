"""The weekly plan (docs/videos/SHORTS.md §排片與時段): the planner model puts topics into the
open slots of the rest of this week and the next, and the server checks the plan before any
slot changes: every topic exists and can be made, one topic to a slot and a slot to a topic,
and no week takes more of a line than its quota. A line without sources this week leaves its
quota to the experiments line, so only the highlights and the drama shorts are held to their
own numbers and the experiments to what the week has in all.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.video_shorts import costs, rules
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsSlot, VideoShortsTopic
from app.video_shorts.schemas import PlanIn, PlanOut
from app.video_shorts.settings import settings_row
from app.video_shorts.slots import slot_facts, slots_out
from app.video_shorts.topics import is_paid

# Statuses of a slot that no longer takes part in the week: it neither counts against a quota
# nor keeps its topic from being planned again.
GONE = ("missed", "skipped")
OWN_QUOTA_LINES = ("cut", "drama")


def week_start(day: date) -> date:
    """The Monday of the week a day falls in."""
    return day - timedelta(days=day.weekday())


def local_week(moment: datetime, timezone: str) -> date:
    return week_start(moment.astimezone(ZoneInfo(timezone)).date())


def plan_window(now: datetime, timezone: str) -> tuple[datetime, datetime]:
    """From now to the end of next week (local time): the slots a plan written now fills."""
    zone = ZoneInfo(timezone)
    end_day = local_week(now, timezone) + timedelta(days=14)
    return now, datetime.combine(end_day, time(0), tzinfo=zone).astimezone(UTC)


def is_open(slot: rules.SlotFacts) -> bool:
    return slot.status == "open" and slot.topic_slug is None and slot.project_slug is None


@dataclass(frozen=True)
class PlanTopic:
    slug: str
    line: str
    status: str
    paid: bool


def week_counts(
    slots: Iterable[rules.SlotFacts], timezone: str, skip: Iterable[UUID] = ()
) -> dict[tuple[date, str], int]:
    """How many slots of each line each week already holds."""
    left_out = set(skip)
    counts: dict[tuple[date, str], int] = {}
    for slot in slots:
        if slot.id in left_out or slot.status in GONE or slot.line is None:
            continue
        key = (local_week(slot.starts_at, timezone), slot.line)
        counts[key] = counts.get(key, 0) + 1
    return counts


def plan_problems(
    items: Sequence[tuple[UUID, str]],
    *,
    slots: Mapping[UUID, rules.SlotFacts],
    topics: Mapping[str, PlanTopic],
    planned_elsewhere: Iterable[str],
    lines: Sequence[str],
    quota: Mapping[str, int],
    existing: Mapping[tuple[date, str], int],
    now: datetime,
    timezone: str,
    window_end: datetime,
    paid_allowed: bool,
) -> list[str]:
    """Why a plan cannot be written as it is; empty when it can."""
    problems: list[str] = []
    elsewhere = set(planned_elsewhere)
    seen_slots: set[UUID] = set()
    seen_topics: set[str] = set()
    counts = dict(existing)
    weeks: set[date] = set()
    for slot_id, slug in items:
        slot = slots.get(slot_id)
        topic = topics.get(slug)
        if slot_id in seen_slots:
            problems.append(f"時段 {slot_id} 排了兩次")
        if slug in seen_topics:
            problems.append(f"題目 {slug} 排了兩次")
        seen_slots.add(slot_id)
        seen_topics.add(slug)
        if slot is None:
            problems.append(f"找不到時段 {slot_id}")
        elif not is_open(slot):
            problems.append(f"時段 {slot_id} 已經有題目或影片")
        elif not (now + rules.MIN_LEAD < slot.starts_at < window_end):
            problems.append(f"時段 {slot_id} 不在這次排片的範圍（到下週日為止）")
        if topic is None:
            problems.append(f"找不到題目 {slug}")
            continue
        if topic.status != "ready":
            problems.append(f"題目 {slug} 還不能做（{topic.status}）")
        elif topic.line not in lines:
            problems.append(f"題目 {slug} 的內容線沒有開")
        elif topic.paid and not paid_allowed:
            problems.append(f"題目 {slug} 要花錢，預算現在不開新的付費工作")
        if slug in elsewhere:
            problems.append(f"題目 {slug} 已經排在別的時段")
        if slot is not None:
            week = local_week(slot.starts_at, timezone)
            weeks.add(week)
            counts[(week, topic.line)] = counts.get((week, topic.line), 0) + 1
    total_quota = sum(int(quota.get(line, 0)) for line in lines)
    for week in sorted(weeks):
        for line in OWN_QUOTA_LINES:
            taken = counts.get((week, line), 0)
            if taken > int(quota.get(line, 0)):
                problems.append(
                    f"{week.isoformat()} 那一週{rules.LINE_NAMES[line]}排了 {taken} 支，"
                    f"超過每週配額 {quota.get(line, 0)} 支"
                )
        taken = sum(count for (each, _line), count in counts.items() if each == week)
        if taken > total_quota:
            problems.append(
                f"{week.isoformat()} 那一週排了 {taken} 支，超過各內容線配額合計 {total_quota} 支"
            )
    return problems


async def apply_plan(
    session: AsyncSession, payload: PlanIn, now: datetime | None = None
) -> PlanOut:
    """Write the planner's week into the calendar, or refuse all of it."""
    moment = now or datetime.now(UTC)
    row = await settings_row(session, lock=True)
    _start, window_end = plan_window(moment, row.timezone)
    ids = [item.slot_id for item in payload.items]
    slugs = [item.topic_slug for item in payload.items]
    with session.no_autoflush:
        chosen = {
            slot.id: slot
            for slot in await session.scalars(
                select(VideoShortsSlot).where(VideoShortsSlot.id.in_(ids)).with_for_update()
            )
        }
        weeks_slots = list(
            await session.scalars(
                select(VideoShortsSlot).where(
                    VideoShortsSlot.starts_at >= moment - timedelta(days=7),
                    VideoShortsSlot.starts_at < window_end + timedelta(days=7),
                )
            )
        )
        topic_rows = {
            topic.slug: topic
            for topic in await session.scalars(
                select(VideoShortsTopic).where(VideoShortsTopic.slug.in_(slugs))
            )
        }
        elsewhere = {
            str(slug)
            for slug in await session.scalars(
                select(VideoShortsSlot.topic_slug).where(
                    VideoShortsSlot.topic_slug.in_(slugs),
                    VideoShortsSlot.starts_at > moment,
                    VideoShortsSlot.status.not_in(GONE),
                )
            )
        }
        budget = await costs.budget(session, row, moment)
    problems = plan_problems(
        [(item.slot_id, item.topic_slug) for item in payload.items],
        slots={slot_id: slot_facts(slot) for slot_id, slot in chosen.items()},
        topics={
            slug: PlanTopic(slug, topic.line, topic.status, is_paid(topic.line, topic.brief or {}))
            for slug, topic in topic_rows.items()
        },
        planned_elsewhere=elsewhere,
        lines=list(row.lines),
        quota=dict(row.weekly_quota),
        existing=week_counts([slot_facts(slot) for slot in weeks_slots], row.timezone),
        now=moment,
        timezone=row.timezone,
        window_end=window_end,
        paid_allowed=budget.paid_work_allowed,
    )
    if problems:
        raise ShortsRefused(422, "video_shorts_plan_invalid", "；".join(problems))
    planned: list[VideoShortsSlot] = []
    for item in payload.items:
        slot = chosen[item.slot_id]
        topic = topic_rows[item.topic_slug]
        slot.status = "planned"
        slot.topic_slug = topic.slug
        slot.line = topic.line
        slot.series = topic.series
        slot.updated_at = moment
        planned.append(slot)
    row.last_plan_at = moment
    await session.commit()
    planned.sort(key=lambda slot: slot.starts_at)
    return PlanOut(planned=await slots_out(session, planned, row.timezone))
