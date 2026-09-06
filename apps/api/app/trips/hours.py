"""Reading Google's opening hours well enough to avoid a closed door.

The Places payload we already store (``HotspotPlaceProfile.opening_hours_json``) carries
``periods``: pairs of ``{"day": 0-6, "hour": 0-23, "minute": 0-59}`` where day 0 is
Sunday, plus the human ``weekday_descriptions`` we never parse. A period with an open but
no close means open around the clock from then on, which is how Google says "always
open".

Every answer here is a three-way one. ``True`` and ``False`` are claims about a place;
``None`` means we do not know, and the caller must stay quiet rather than guess. A single
"closed" shown for a place that is open would cost the whole strip its credibility, so
anything unparseable, empty or expired lands in ``None``.

Nothing in this module talks to Google: it reads what was already cached.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from typing import Any

WEEK_MINUTES = 7 * 24 * 60
DAY_MINUTES = 24 * 60


@dataclass(frozen=True)
class OpeningInterval:
    """One stretch of opening time, in minutes from Sunday 00:00 in the place's own week."""

    start: int
    end: int

    def contains(self, moment: int) -> bool:
        return self.start <= moment < self.end


def fresh_hours(
    payload: Mapping[str, Any] | None,
    expires_at: datetime | None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """The stored periods, but only while the cached copy is still current.

    Google's terms bound how long a cached place may be used, and a museum that changed
    its closing day since the cache was written is exactly the case this feature must not
    get wrong. An expired or missing cache returns nothing, which every reader treats as
    "we do not know" — and this path never asks Google, because a Place Details call per
    planned stop would spend the month's free tier in an afternoon.
    """
    if not payload or expires_at is None:
        return {}
    observed = now or datetime.now(UTC)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    return dict(payload) if expires_at > observed else {}


def _minute_of_week(entry: Mapping[str, Any]) -> int | None:
    try:
        day = int(entry["day"])
        hour = int(entry.get("hour", 0))
        minute = int(entry.get("minute", 0))
    except (KeyError, TypeError, ValueError):
        return None
    if not (0 <= day <= 6 and 0 <= hour <= 24 and 0 <= minute <= 59):
        return None
    return day * DAY_MINUTES + hour * 60 + minute


def weekly_intervals(payload: Mapping[str, Any] | None) -> list[OpeningInterval] | None:
    """The week's opening stretches, or ``None`` when the payload says nothing usable."""
    if not payload:
        return None
    raw = payload.get("periods")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or not raw:
        return None
    intervals: list[OpeningInterval] = []
    for period in raw:
        if not isinstance(period, Mapping):
            continue
        opens = period.get("open")
        if not isinstance(opens, Mapping):
            continue
        start = _minute_of_week(opens)
        if start is None:
            continue
        closes = period.get("close")
        if not isinstance(closes, Mapping):
            # Google writes an open with no close for a place that never shuts.
            return [OpeningInterval(0, WEEK_MINUTES)]
        end = _minute_of_week(closes)
        if end is None:
            continue
        if end <= start:
            # Closes after midnight: the stretch runs into the following week.
            end += WEEK_MINUTES
        intervals.append(OpeningInterval(start, end))
    return intervals or None


def _moment(when: datetime) -> int:
    """Minutes from Sunday 00:00, in whatever timezone ``when`` already carries."""
    # Python's Monday is 0; Google's Sunday is 0.
    day = (when.weekday() + 1) % 7
    return day * DAY_MINUTES + when.hour * 60 + when.minute


def is_open_at(payload: Mapping[str, Any] | None, when: datetime) -> bool | None:
    """Is the place open at ``when``? ``None`` when the data cannot say."""
    intervals = weekly_intervals(payload)
    if intervals is None:
        return None
    moment = _moment(when)
    return any(
        interval.contains(moment) or interval.contains(moment + WEEK_MINUTES)
        for interval in intervals
    )


def opens_within_day(payload: Mapping[str, Any] | None, when: datetime) -> time | None:
    """The next opening time on the same calendar day, if there is one after ``when``."""
    intervals = weekly_intervals(payload)
    if intervals is None:
        return None
    moment = _moment(when)
    day_end = (moment // DAY_MINUTES + 1) * DAY_MINUTES
    upcoming = [
        interval.start
        for interval in intervals
        if moment < interval.start < day_end
    ]
    if not upcoming:
        return None
    start = min(upcoming)
    return time((start % DAY_MINUTES) // 60, start % 60)


def open_slot(
    payload: Mapping[str, Any] | None,
    day: datetime,
    slots: Sequence[time],
    *,
    stay_minutes: int = 60,
) -> time | None:
    """The first of ``slots`` the place is open for, or ``None`` to leave it alone.

    A place with no usable hours returns the first slot unchanged: silence means the
    caller keeps the behaviour it had before this module existed.
    """
    if not slots:
        return None
    intervals = weekly_intervals(payload)
    if intervals is None:
        return slots[0]
    for slot in slots:
        arrival = day.replace(hour=slot.hour, minute=slot.minute, second=0, microsecond=0)
        leaving = arrival + timedelta(minutes=max(0, stay_minutes))
        if is_open_at(payload, arrival) and (
            leaving == arrival or is_open_at(payload, leaving - timedelta(minutes=1))
        ):
            return slot
    return None
