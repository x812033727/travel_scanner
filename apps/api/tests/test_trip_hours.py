"""Opening hours may only speak when they are sure."""

from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest

from app.trips.hours import is_open_at, open_slot, opens_within_day, weekly_intervals

TOKYO = ZoneInfo("Asia/Tokyo")


def period(open_day: int, open_hour: int, close_day: int, close_hour: int) -> dict[str, object]:
    return {
        "open": {"day": open_day, "hour": open_hour, "minute": 0},
        "close": {"day": close_day, "hour": close_hour, "minute": 0},
    }


# A museum that closes on Mondays: open 09:30–17:00 every day except Monday (day 1).
MUSEUM = {
    "weekday_descriptions": ["星期一: 休息"],
    "periods": [
        {
            "open": {"day": day, "hour": 9, "minute": 30},
            "close": {"day": day, "hour": 17, "minute": 0},
        }
        for day in (0, 2, 3, 4, 5, 6)
    ],
}
ALWAYS_OPEN = {"periods": [{"open": {"day": 0, "hour": 0, "minute": 0}}]}
LATE_BAR = {"periods": [period(5, 18, 6, 2)]}  # Friday 18:00 to Saturday 02:00


def test_a_museum_that_closes_on_mondays_says_so_and_only_then() -> None:
    monday = datetime(2026, 11, 9, 11, 0, tzinfo=TOKYO)
    tuesday = datetime(2026, 11, 10, 11, 0, tzinfo=TOKYO)

    assert monday.weekday() == 0
    assert is_open_at(MUSEUM, monday) is False
    assert is_open_at(MUSEUM, tuesday) is True
    assert is_open_at(MUSEUM, tuesday.replace(hour=8)) is False
    assert is_open_at(MUSEUM, tuesday.replace(hour=17)) is False


def test_an_open_without_a_close_is_a_place_that_never_shuts() -> None:
    intervals = weekly_intervals(ALWAYS_OPEN)
    assert intervals is not None and len(intervals) == 1
    assert is_open_at(ALWAYS_OPEN, datetime(2026, 11, 9, 3, 0, tzinfo=TOKYO)) is True


def test_a_stretch_that_runs_past_midnight_still_covers_the_small_hours() -> None:
    assert is_open_at(LATE_BAR, datetime(2026, 11, 13, 23, 0, tzinfo=TOKYO)) is True  # Friday
    assert (
        is_open_at(LATE_BAR, datetime(2026, 11, 14, 1, 0, tzinfo=TOKYO)) is True
    )  # Saturday 01:00
    assert is_open_at(LATE_BAR, datetime(2026, 11, 14, 3, 0, tzinfo=TOKYO)) is False


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"weekday_descriptions": ["星期一: 09:00–19:00"]},
        {"periods": []},
        {"periods": "x"},
    ],
)
def test_hours_we_cannot_read_stay_silent_rather_than_guess(payload: object) -> None:
    assert weekly_intervals(payload) is None  # type: ignore[arg-type]
    assert is_open_at(payload, datetime(2026, 11, 9, 11, 0, tzinfo=TOKYO)) is None  # type: ignore[arg-type]
    assert opens_within_day(payload, datetime(2026, 11, 9, 8, 0, tzinfo=TOKYO)) is None  # type: ignore[arg-type]


def test_the_next_opening_is_only_offered_for_the_same_day() -> None:
    tuesday_early = datetime(2026, 11, 10, 8, 0, tzinfo=TOKYO)
    assert opens_within_day(MUSEUM, tuesday_early) == time(9, 30)
    assert opens_within_day(MUSEUM, tuesday_early.replace(hour=18)) is None
    assert opens_within_day(MUSEUM, datetime(2026, 11, 9, 8, 0, tzinfo=TOKYO)) is None


def test_a_slot_is_moved_to_one_the_place_is_open_for() -> None:
    tuesday = datetime(2026, 11, 10, tzinfo=TOKYO)
    slots = [time(9, 0), time(10, 0), time(13, 30)]

    assert open_slot(MUSEUM, tuesday, slots, stay_minutes=90) == time(10, 0)
    # 16:30 plus ninety minutes runs past closing, so it is refused.
    assert open_slot(MUSEUM, tuesday, [time(16, 30)], stay_minutes=90) is None


def test_a_day_the_place_is_shut_offers_no_slot_at_all() -> None:
    monday = datetime(2026, 11, 9, tzinfo=TOKYO)
    assert open_slot(MUSEUM, monday, [time(10, 0), time(13, 30)]) is None


def test_a_place_with_no_hours_keeps_the_slot_the_planner_chose() -> None:
    monday = datetime(2026, 11, 9, tzinfo=TOKYO)
    assert open_slot(None, monday, [time(10, 0), time(13, 30)]) == time(10, 0)
    assert open_slot({}, monday, [time(13, 30)]) == time(13, 30)
