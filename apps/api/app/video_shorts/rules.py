"""The Shorts' rules, as pure functions (docs/videos/SHORTS.md).

Nothing here reads a database or a clock: the callers pass what they loaded and the moment
they mean, so every rule can be tested with plain values. ``slots.py``, ``costs.py`` and
``settings.py`` load the rows and apply what these functions decide.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

# How long before its time a slot can still be scheduled on YouTube: a publish time in the
# past makes a video public at once, so a slot this close to its time is given up instead.
MIN_LEAD = timedelta(minutes=5)
# The owner's consent lasts as long as one run of the calendar, and is asked for again a
# week before it ends.
CONSENT_DAYS = 90
CONSENT_WARN_DAYS = 7
# Days in a row with a missed slot before the owner is told.
MISSED_DAYS_ALERT = 3
# The worker knocks every five minutes; three rounds without a knock is worth a line.
WORKER_SILENT_AFTER = timedelta(minutes=15)
PERIOD_DAYS = 30
TOTAL_DAYS = 90
LINE_NAMES = {"lab": "實測", "cut": "長片精華", "drama": "漫劇直式短篇"}
# The statuses of a slot that holds its Short; a missed or skipped slot holds none.
HOLDING = ("assigned", "locked", "scheduled", "published")


# --- the calendar -------------------------------------------------------------------------------


@dataclass(frozen=True)
class SlotPlan:
    """A slot to create: its moment, the day of the run it falls on and its thirty days."""

    starts_at: datetime
    day: int
    phase: int


def slot_time(value: str) -> time:
    hours, minutes = value.split(":")
    return time(int(hours), int(minutes))


def build_slots(
    first_day: date,
    daily_pattern: Sequence[Mapping[str, Any]],
    slot_times: Sequence[str],
    timezone: str,
) -> list[SlotPlan]:
    """The run's slots from its first day: each segment of the pattern publishes its counts
    in turn, a day's count taking that many of the slot times in the order they are listed.

    With the defaults that is one a day at 19:30 for thirty days, then sixty days of two
    (12:30 added) and one in turn: 30, 45 and 45 slots, 120 in ninety days.
    """
    zone = ZoneInfo(timezone)
    times = [slot_time(value) for value in slot_times]
    plans: list[SlotPlan] = []
    day = 0
    for segment in daily_pattern:
        counts = [int(count) for count in segment["counts"]]
        for index in range(int(segment["days"])):
            local_day = first_day + timedelta(days=day)
            for moment in sorted(times[: counts[index % len(counts)]]):
                plans.append(
                    SlotPlan(
                        starts_at=datetime.combine(local_day, moment, tzinfo=zone).astimezone(UTC),
                        day=day + 1,
                        phase=day // PERIOD_DAYS + 1,
                    )
                )
            day += 1
    return plans


def pattern_days(daily_pattern: Sequence[Mapping[str, Any]]) -> int:
    return sum(int(segment["days"]) for segment in daily_pattern)


# --- where a Short stands -----------------------------------------------------------------------


@dataclass(frozen=True)
class ShortFacts:
    """What is known of one Short when its state is asked for."""

    dropped: bool = False
    blocked: bool = False
    pending_reviews: int = 0
    package_approved: bool = False
    youtube_video_id: str | None = None
    youtube_publish_at: datetime | None = None
    # Whether the site's last run on YouTube finished; None when it never ran.
    sync_done: bool | None = None
    # The status of the slot that holds it, and how many slots it has missed.
    slot_status: str | None = None
    missed_slots: int = 0


def shorts_state(facts: ShortFacts, now: datetime) -> str:
    """One of the eight states the tab groups Shorts by.

    Dropped wins over everything, then public, then what waits for the owner: a Short the
    owner must look at is never hidden behind its slot. A Short whose slot was missed is back
    in the library and says so until it is given another slot.
    """
    if facts.dropped:
        return "dropped"
    on_youtube = facts.youtube_video_id is not None
    publish_at = facts.youtube_publish_at
    if facts.slot_status == "published" or (
        on_youtube and publish_at is not None and publish_at <= now
    ):
        return "published"
    if facts.blocked or facts.pending_reviews > 0:
        return "needs_you"
    if facts.slot_status == "scheduled" or (
        on_youtube and publish_at is not None and facts.sync_done is not False
    ):
        return "scheduled"
    if facts.slot_status in ("assigned", "locked"):
        return "slotted"
    if facts.package_approved:
        return "missed" if facts.missed_slots > 0 else "library"
    return "making"


# --- giving Shorts their slots ------------------------------------------------------------------


@dataclass(frozen=True)
class SlotFacts:
    id: UUID
    starts_at: datetime
    status: str
    line: str | None = None
    topic_slug: str | None = None
    project_slug: str | None = None


@dataclass(frozen=True)
class LibraryShort:
    """An approved Short that holds no slot."""

    slug: str
    line: str
    approved_at: datetime
    topic_slug: str | None = None
    # The owner already uploaded its file to YouTube (before the API audit passes).
    uploaded: bool = False


@dataclass(frozen=True)
class SlotChange:
    slot_id: UUID
    status: str
    project_slug: str | None
    note: str | None = None


def assign_slot(slots: Iterable[SlotFacts], short: LibraryShort, now: datetime) -> SlotFacts | None:
    """The slot an approved Short goes to: the one it holds already, else the one planned for
    its topic, else the earliest open slot still ahead that is not kept for another line.

    A slot it holds counts whenever it is and whatever came of it: a Short that is scheduled
    or public, and whose package is approved again, is not given a second slot.
    """
    every = sorted(slots, key=lambda slot: slot.starts_at)
    for slot in every:
        if slot.project_slug == short.slug and slot.status in HOLDING:
            return slot
    ahead = [slot for slot in every if slot.starts_at - MIN_LEAD > now]
    if short.topic_slug is not None:
        for slot in ahead:
            if (
                slot.status == "planned"
                and slot.project_slug is None
                and slot.topic_slug == short.topic_slug
            ):
                return slot
    for slot in ahead:
        if slot.status == "open" and slot.project_slug is None and slot.line in (None, short.line):
            return slot
    return None


def _pick(
    library: list[LibraryShort], line: str | None, prefer_uploaded: bool
) -> LibraryShort | None:
    """The earliest approved Short, of the slot's line when there is one, and one the owner
    already uploaded when that is what can still go out."""
    if not library:
        return None
    return min(
        library,
        key=lambda short: (
            not short.uploaded if prefer_uploaded else False,
            line is not None and short.line != line,
            short.approved_at,
            short.slug,
        ),
    )


def lock_due(
    slots: Iterable[SlotFacts],
    library: Iterable[LibraryShort],
    ready: Iterable[str],
    now: datetime,
    lock_hours: int,
    *,
    prefer_uploaded: bool = False,
) -> list[SlotChange]:
    """What happens to the slots whose time has come, earliest first.

    ``lock_hours`` before its time a slot is locked to the Short it holds. One that holds
    none, or one whose Short is no longer ``ready`` (dropped, or its package sent back),
    takes the earliest approved Short from the library; with the library empty it is missed.
    A slot that reaches MIN_LEAD before its time without being scheduled is missed too, and
    its Short goes back to the library: nothing is published late.
    """
    waiting = list(library)
    usable = set(ready)
    window = timedelta(hours=lock_hours)
    changes: list[SlotChange] = []
    for slot in sorted(slots, key=lambda item: item.starts_at):
        if slot.status not in ("open", "planned", "assigned", "locked"):
            continue
        if slot.starts_at - window > now:
            continue
        if slot.starts_at - MIN_LEAD <= now:
            held = slot.project_slug if slot.status in ("assigned", "locked") else None
            changes.append(
                SlotChange(
                    slot.id,
                    "missed",
                    held,
                    "時段到了，這支還沒有排上 YouTube" if held else "時段到了，沒有可以發的 Shorts",
                )
            )
            continue
        if slot.status == "locked":
            continue
        if slot.status == "assigned" and slot.project_slug in usable:
            changes.append(SlotChange(slot.id, "locked", slot.project_slug))
            continue
        chosen = _pick(waiting, slot.line, prefer_uploaded)
        if chosen is None:
            changes.append(SlotChange(slot.id, "missed", None, "片庫是空的"))
            continue
        waiting.remove(chosen)
        changes.append(SlotChange(slot.id, "locked", chosen.slug, "從片庫補上"))
    return changes


def missed_days_in_a_row(slots: Iterable[SlotFacts], now: datetime, timezone: str) -> int:
    """How many of the latest days with slots each had a missed one, counting back from the
    most recent day whose slots are past."""
    zone = ZoneInfo(timezone)
    days: dict[date, list[str]] = {}
    for slot in slots:
        if slot.starts_at <= now and slot.status != "skipped":
            days.setdefault(slot.starts_at.astimezone(zone).date(), []).append(slot.status)
    streak = 0
    for day in sorted(days, reverse=True):
        if "missed" not in days[day]:
            break
        streak += 1
    return streak


def stock_cover(
    slots: Iterable[SlotFacts], library_count: int, now: datetime, timezone: str
) -> int | None:
    """How many coming days of slots are filled, counting what the library could fill.

    None when there is no slot ahead: before the run starts the library is only a count.
    """
    zone = ZoneInfo(timezone)
    days: dict[date, int] = {}
    for slot in slots:
        if slot.starts_at <= now or slot.status in ("skipped", "missed"):
            continue
        day = slot.starts_at.astimezone(zone).date()
        empty = slot.status in ("open", "planned") or slot.project_slug is None
        days[day] = days.get(day, 0) + (1 if empty else 0)
    if not days:
        return None
    left = library_count
    covered = 0
    for day in sorted(days):
        if days[day] > left:
            break
        left -= days[day]
        covered += 1
    return covered


# --- the budget ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class CostFacts:
    occurred_at: datetime
    status: str
    amount_ntd: Decimal | None


@dataclass(frozen=True)
class BudgetWindow:
    period_start: datetime
    period_end: datetime
    total_start: datetime


@dataclass(frozen=True)
class BudgetState:
    window: BudgetWindow
    spent: Decimal
    reserved: Decimal
    unknown: int
    total_spent: Decimal
    paid_work_allowed: bool
    reason: str | None


def budget_window(now: datetime, campaign_start: date | None, timezone: str) -> BudgetWindow:
    """The thirty days the spending is counted in, and where the run's total starts.

    Once the run has started the periods are its own thirty-day blocks; before that, and
    with no run, they are the thirty and ninety days up to now. A period takes its first
    moment and not its last, so those end a second after now: a line entered this instant
    counts.
    """
    period = timedelta(days=PERIOD_DAYS)
    if campaign_start is not None:
        start = datetime.combine(campaign_start, time(0), tzinfo=ZoneInfo(timezone)).astimezone(UTC)
        if now >= start:
            blocks = (now - start) // period
            return BudgetWindow(start + blocks * period, start + (blocks + 1) * period, start)
    end = now + timedelta(seconds=1)
    return BudgetWindow(end - period, end, end - timedelta(days=TOTAL_DAYS))


def budget_state(
    costs: Iterable[CostFacts],
    window: BudgetWindow,
    *,
    limit: int,
    soft: int,
    total_limit: int,
) -> BudgetState:
    """Whether new paid work may start (docs/videos/SHORTS.md §花費與預算).

    A line without a known amount stops it, whatever the sums say: an unknown is not a zero.
    Reserved amounts count as spent, so work in hand cannot be promised twice.
    """
    spent = reserved = total = Decimal(0)
    unknown = 0
    for cost in costs:
        if cost.occurred_at < window.total_start:
            continue
        if cost.status == "unknown":
            unknown += 1
            continue
        amount = cost.amount_ntd or Decimal(0)
        total += amount
        if window.period_start <= cost.occurred_at < window.period_end:
            if cost.status == "reserved":
                reserved += amount
            else:
                spent += amount
    reason: str | None = None
    if unknown:
        reason = f"有 {unknown} 筆花費還不知道金額，付費工作先停；補上金額後會繼續"
    elif total >= total_limit:
        reason = f"這一輪已經花了 NT${total:,.0f}，到了上限 NT${total_limit:,}"
    elif spent + reserved >= limit:
        reason = f"這 30 天已經花了 NT${spent + reserved:,.0f}，到了上限 NT${limit:,}"
    elif spent + reserved >= soft:
        reason = (
            f"這 30 天已經花了 NT${spent + reserved:,.0f}，到了 NT${soft:,}："
            "不開新的付費工作，手上的會做完"
        )
    return BudgetState(window, spent, reserved, unknown, total, reason is None, reason)


# --- the owner's standing consent ---------------------------------------------------------------


def consent_scope(
    *,
    channel_id: str,
    channel_title: str | None,
    lines: Sequence[str],
    max_per_day: int,
    slot_times: Sequence[str],
    timezone: str,
) -> dict[str, Any]:
    """What a consent covers: the channel, the content lines, how many a day and when."""
    return {
        "channel_id": channel_id,
        "channel_title": channel_title or "",
        "lines": [line for line in LINE_NAMES if line in lines],
        "max_per_day": int(max_per_day),
        "slot_times": sorted(slot_times),
        "timezone": timezone,
    }


def consent_text(scope: Mapping[str, Any]) -> str:
    """The wording the owner agrees to, written from the scope so the two cannot differ.

    YouTube's developer policies ask that an automated upload has the user's prior, specific
    and express consent, that the user is told what will be written and how the privacy
    status will change, and that the user keeps the final say.
    """
    lines = "、".join(LINE_NAMES[line] for line in scope["lines"])
    times = "、".join(scope["slot_times"])
    channel = scope["channel_title"] or scope["channel_id"]
    return "\n".join(
        [
            f"我同意 Mokaair 網站在下面的範圍內，替我在 YouTube 頻道「{channel}」"
            f"（{scope['channel_id']}）上架 Shorts，不用每一支再問我：",
            f"一、內容線：{lines}。",
            f"二、一天最多 {scope['max_per_day']} 支，公開時間是 {times}（{scope['timezone']}）。",
            "三、網站會替每一支設定：標題、說明、標籤、分類、字幕、"
            "「是否為兒童打造」與「變造或合成內容」的揭露。",
            "四、瀏覽權限：網站只會把影片設成私人並排定公開時間，"
            "時間到了由 YouTube 公開；網站不會自己把影片設成公開，也不會修改已經公開的影片。",
            "五、通過 YouTube API 稽核之後，網站也會替我上傳影片檔；"
            "在那之前，檔案由我自己上傳到 YouTube Studio。",
            "六、每一支在公開之前，我都可以改標題與說明、換時段或抽掉；"
            "我可以隨時暫停、撤回已經排程的影片，或撤銷這份同意。",
            f"七、這份同意 {CONSENT_DAYS} 天後到期；"
            "換頻道、增加內容線、調高每天上限或更改公開時間，都要重新同意。",
        ]
    )


def consent_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def scope_problems(granted: Mapping[str, Any], current: Mapping[str, Any]) -> list[str]:
    """Why what was agreed to no longer covers the settings; empty while it does.

    Narrowing is covered (a line dropped, fewer a day); widening and any change of channel
    or of the publish times is not.
    """
    problems: list[str] = []
    if granted.get("channel_id") != current.get("channel_id"):
        problems.append("連結的頻道換了")
    added = [line for line in current.get("lines", []) if line not in granted.get("lines", [])]
    if added:
        problems.append("多了內容線：" + "、".join(LINE_NAMES.get(line, line) for line in added))
    if int(current.get("max_per_day", 0)) > int(granted.get("max_per_day", 0)):
        problems.append("每天上限調高了")
    if sorted(current.get("slot_times", [])) != sorted(granted.get("slot_times", [])) or (
        current.get("timezone") != granted.get("timezone")
    ):
        problems.append("公開時間改了")
    return problems


def consent_state(
    *,
    autopublish: bool,
    granted: Mapping[str, Any] | None,
    expires_at: datetime | None,
    current: Mapping[str, Any] | None,
    now: datetime,
) -> tuple[str, str | None]:
    """Where the consent stands and, when it does not hold, why.

    ``current`` is the scope the settings ask for now, or None while no channel is linked.
    """
    if granted is None or expires_at is None:
        return "none", None
    if expires_at <= now:
        return "expired", "自動上架授權到期了，要重新同意"
    if current is None:
        return "invalid", "YouTube 頻道沒有連結，授權沒有對象"
    problems = scope_problems(granted, current)
    if problems or not autopublish:
        return "invalid", "授權的範圍變了（" + "；".join(problems or ["已停用"]) + "），要重新同意"
    if expires_at - now <= timedelta(days=CONSENT_WARN_DAYS):
        days = max((expires_at - now).days, 0)
        return "expiring", f"自動上架授權再 {days} 天到期"
    return "valid", None


def autopublish_state(consent: str, paused: bool) -> str:
    """The one word the top row shows for publishing."""
    if consent == "none":
        return "off"
    if consent in ("expired", "invalid"):
        return consent
    if paused:
        return "paused"
    return "expiring" if consent == "expiring" else "on"
