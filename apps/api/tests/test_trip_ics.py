"""The calendar a traveller imports has to hold the same times the planner shows."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.models import TripPlan, TripPlanItem
from app.trips.export_router import filename_for
from app.trips.ics import escape_text, fold, trip_calendar
from app.trips.route_planner import estimated_segment
from app.trips.routing import RoutePoint, RouteSegment, RouteStep


def trip() -> TripPlan:
    return TripPlan(
        id=uuid4(),
        user_id=uuid4(),
        name="東京, 五日",
        timezone="Asia/Tokyo",
        data={},
    )


def item(
    title: str,
    start: datetime,
    *,
    minutes: int = 60,
    skipped: bool = False,
    notes: str | None = None,
    position: int = 0,
) -> TripPlanItem:
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=uuid4(),
        item_type="activity",
        day_date=start.date(),
        position=position,
        title=title,
        location_name=f"{title}前",
        start_time=start,
        end_time=start + timedelta(minutes=minutes),
        duration_minutes=minutes,
        is_skipped=skipped,
        notes=notes,
        latitude=35.7148,
        longitude=139.7967,
        data={},
    )


def parse(text: str) -> list[dict[str, str]]:
    """Unfold the calendar and read it back as one dict per VEVENT."""
    unfolded: list[str] = []
    for line in text.split("\r\n"):
        if line.startswith(" ") and unfolded:
            unfolded[-1] += line[1:]
        elif line:
            unfolded.append(line)
    events: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in unfolded:
        if line == "BEGIN:VEVENT":
            current = {}
        elif line == "END:VEVENT":
            assert current is not None
            events.append(current)
            current = None
        elif current is not None:
            name, _, value = line.partition(":")
            current[name.split(";")[0]] = value
    return events


def test_every_stop_becomes_an_event_at_the_time_the_planner_shows() -> None:
    first_start = datetime(2026, 11, 10, 9, tzinfo=UTC)
    plan = trip()
    rows = [
        item("淺草寺", first_start),
        item("晴空塔", first_start + timedelta(hours=3), position=1),
        item("略過的午餐", first_start + timedelta(hours=5), skipped=True, position=2),
        item("上野公園", datetime(2026, 11, 11, 2, tzinfo=UTC), position=0),
    ]

    calendar = trip_calendar(plan, rows, [], now=datetime(2026, 11, 1, tzinfo=UTC))
    events = parse(calendar)

    assert calendar.startswith("BEGIN:VCALENDAR\r\n")
    assert calendar.endswith("END:VCALENDAR\r\n")
    assert "X-WR-TIMEZONE:Asia/Tokyo" in calendar
    assert [event["SUMMARY"] for event in events] == ["淺草寺", "晴空塔", "上野公園"]
    assert events[0]["DTSTART"] == "20261110T090000Z"
    assert events[0]["DTEND"] == "20261110T100000Z"
    assert events[0]["UID"].endswith("@mokaair.com")
    assert events[0]["GEO"] == "35.714800;139.796700"
    assert events[2]["DTSTART"] == "20261111T020000Z"


def test_the_leg_that_leads_to_a_stop_is_described_on_that_stop() -> None:
    start = datetime(2026, 11, 10, 9, tzinfo=UTC)
    first, second = item("淺草寺", start), item("晴空塔", start + timedelta(hours=3), position=1)
    segment = RouteSegment(
        from_item_id=first.id,
        to_item_id=second.id,
        provider="google_routes",
        attribution="Google Maps",
        generated_at=start,
        duration_minutes=25,
        fare=210,
        currency="JPY",
        steps=[
            RouteStep(
                travel_mode="TRANSIT",
                instruction="搭乘銀座線",
                line_short_name="G",
                platform="3",
            ),
            RouteStep(travel_mode="WALK", instruction="步行"),
            RouteStep(
                travel_mode="TRANSIT",
                instruction="搭乘半藏門線",
                line_short_name="Z",
                exit_name="A2",
            ),
        ],
    )

    events = parse(trip_calendar(trip(), [first, second], [segment], locale="zh-TW"))

    assert "DESCRIPTION" not in events[0]
    description = events[1]["DESCRIPTION"]
    assert "前往方式: 大眾運輸 25 分鐘" in description
    assert "轉乘 1 次" in description
    assert "G · Z" in description
    assert "車資: JPY 210" in description
    assert "月台 3" in description and "出口 A2" in description


def test_an_unrouted_leg_says_it_is_an_estimate_in_the_reader_s_language() -> None:
    start = datetime(2026, 11, 10, 9, tzinfo=UTC)
    first, second = item("淺草寺", start), item("晴空塔", start + timedelta(hours=3), position=1)
    segment = estimated_segment(
        RoutePoint(item_id=first.id, name="淺草寺", latitude=35.7148, longitude=139.7967),
        RoutePoint(item_id=second.id, name="晴空塔", latitude=35.7101, longitude=139.8107),
        "transit",
    )

    for locale, expected in (
        ("zh-TW", "估算"),
        ("zh-CN", "估算"),
        ("en", "estimated"),
        ("ja", "推定"),
        ("ko", "추정"),
    ):
        events = parse(trip_calendar(trip(), [first, second], [segment], locale=locale))
        assert expected in events[1]["DESCRIPTION"], locale


def test_text_is_escaped_and_long_lines_are_folded_below_seventy_five_octets() -> None:
    assert escape_text("a,b;c\\d\ne") == "a\\,b\\;c\\\\d\\ne"
    folded = fold("SUMMARY:" + "東" * 60)
    assert len(folded) > 1
    assert all(len(part.encode("utf-8")) <= 75 for part in folded)
    assert all(part.startswith(" ") for part in folded[1:])
    rebuilt = folded[0] + "".join(part[1:] for part in folded[1:])
    assert rebuilt == "SUMMARY:" + "東" * 60


def test_a_flight_that_crosses_midnight_keeps_both_ends() -> None:
    departure = datetime(2026, 11, 10, 14, 30, tzinfo=UTC)
    flight = item("台北 → 東京", departure, minutes=180)
    events = parse(trip_calendar(trip(), [flight], []))
    assert events[0]["DTSTART"] == "20261110T143000Z"
    assert events[0]["DTEND"] == "20261110T173000Z"


def test_the_download_name_is_ascii_and_identifies_the_trip() -> None:
    trip_id = uuid4()
    assert filename_for("東京 五日", trip_id) == f"trip-{str(trip_id)[:8]}.ics"
    assert filename_for("Tokyo Trip", trip_id) == f"tokyo-trip-{str(trip_id)[:8]}.ics"
