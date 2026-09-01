from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.models import TripPlan, TripPlanItem
from app.trips.schedule import (
    SYSTEM_ROLES,
    active_route_rows,
    apply_schedule_defaults,
    ensure_system_slots,
    route_pair_count,
    sync_primary_lodging,
)


class AddOnlySession:
    def __init__(self) -> None:
        self.added: list[TripPlanItem] = []

    def add(self, item: TripPlanItem) -> None:
        self.added.append(item)


def trip() -> TripPlan:
    return TripPlan(
        id=uuid4(),
        user_id=uuid4(),
        name="東京三日",
        mode="manual",
        total_price=Decimal("0"),
        currency="TWD",
        data={},
        version=1,
        destination_name="東京",
        start_date=date(2026, 11, 10),
        end_date=date(2026, 11, 11),
        timezone="Asia/Tokyo",
        route_preference="FEWER_TRANSFERS",
    )


def test_system_slots_are_idempotent_and_skipped_meals_leave_route_graph() -> None:
    target = trip()
    activity = TripPlanItem(
        id=uuid4(),
        trip_plan_id=target.id,
        item_type="custom",
        day_date=date(2026, 11, 10),
        position=0,
        title="淺草寺",
        start_time=datetime(2026, 11, 10, 10, tzinfo=ZoneInfo("Asia/Tokyo")),
        duration_minutes=60,
        locked=False,
        fixed_time=False,
        is_estimated=False,
        is_skipped=False,
        data={},
    )
    legacy_hotel = TripPlanItem(
        id=uuid4(),
        trip_plan_id=target.id,
        item_type="hotel",
        day_date=date(2026, 11, 10),
        position=1,
        title="入住 東京飯店",
        location_name="東京飯店",
        locked=True,
        fixed_time=True,
        is_estimated=True,
        is_skipped=False,
        data={"timeline_section": "logistics"},
    )
    rows = [activity, legacy_hotel]
    session = AddOnlySession()

    assert ensure_system_slots(session, target, rows) is True  # type: ignore[arg-type]
    assert len(session.added) == 8
    assert ensure_system_slots(session, target, rows) is False  # type: ignore[arg-type]
    for day_value in (date(2026, 11, 10), date(2026, 11, 11)):
        assert {
            row.system_role for row in rows if row.day_date == day_value and row.system_role
        } == set(SYSTEM_ROLES)

    first_day_route = active_route_rows(rows, date(2026, 11, 10))
    assert first_day_route[0].system_role == "hotel_start"
    assert first_day_route[-1].system_role == "hotel_end"
    assert legacy_hotel not in first_day_route
    original_pairs = route_pair_count(rows)
    lunch = next(
        row
        for row in rows
        if row.day_date == date(2026, 11, 10) and row.system_role == "lunch"
    )
    lunch.is_skipped = True
    without_lunch = active_route_rows(rows, date(2026, 11, 10))
    assert lunch not in without_lunch
    activity_index = without_lunch.index(activity)
    assert without_lunch[activity_index + 1].system_role == "dinner"
    assert route_pair_count(rows) == original_pairs - 1


def test_lodging_and_meal_defaults_sync_across_every_day() -> None:
    target = trip()
    rows: list[TripPlanItem] = []
    session = AddOnlySession()
    ensure_system_slots(session, target, rows)  # type: ignore[arg-type]
    assert all(
        row.data["needs_place_confirmation"] is True
        for row in rows
        if row.system_role in {"hotel_start", "hotel_end"}
    )

    lodging = {
        "name": "丸之內飯店",
        "location_name": "東京都千代田區",
        "provider_place_id": "place-hotel",
        "latitude": 35.6812,
        "longitude": 139.7671,
        "location_source": "google_places",
    }
    sync_primary_lodging(target, rows, lodging)
    hotels = [row for row in rows if row.system_role in {"hotel_start", "hotel_end"}]
    assert len(hotels) == 4
    assert all(row.provider_place_id == "place-hotel" for row in hotels)
    assert all(row.data["needs_place_confirmation"] is False for row in hotels)

    target.data = {
        **target.data,
        "schedule_defaults": {
            "day_start_time": "09:00",
            "lunch_time": "11:45",
            "lunch_duration_minutes": 45,
            "dinner_time": "19:15",
            "dinner_duration_minutes": 120,
        },
    }
    apply_schedule_defaults(target, rows)
    lunches = [row for row in rows if row.system_role == "lunch"]
    dinners = [row for row in rows if row.system_role == "dinner"]
    assert all(row.start_time and row.start_time.strftime("%H:%M") == "11:45" for row in lunches)
    assert all(row.duration_minutes == 45 for row in lunches)
    assert all(row.start_time and row.start_time.strftime("%H:%M") == "19:15" for row in dinners)
    assert all(row.duration_minutes == 120 for row in dinners)
