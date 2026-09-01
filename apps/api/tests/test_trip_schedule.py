from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.models import TripPlan, TripPlanItem
from app.trips.router import (
    FlightAnchorDetails,
    ItineraryUpdateRequest,
    apply_flight_anchor_details,
    localize_itinerary_time,
)
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


def test_offset_free_editor_time_is_localized_to_trip_timezone() -> None:
    localized = localize_itinerary_time(datetime(2026, 11, 10, 15), "Asia/Tokyo")

    assert localized is not None
    assert localized.isoformat() == "2026-11-10T15:00:00+09:00"
    assert localize_itinerary_time(localized, "Asia/Taipei") is localized


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
    assert len(session.added) == 10
    assert ensure_system_slots(session, target, rows) is False  # type: ignore[arg-type]
    assert {
        row.system_role
        for row in rows
        if row.day_date == date(2026, 11, 10) and row.system_role
    } == {"outbound_flight", "hotel_start", "lunch", "dinner", "hotel_end"}
    assert {
        row.system_role
        for row in rows
        if row.day_date == date(2026, 11, 11) and row.system_role
    } == {"hotel_start", "lunch", "dinner", "hotel_end", "return_flight"}
    assert len([row for row in rows if row.system_role in SYSTEM_ROLES]) == 10

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


def test_legacy_flights_are_promoted_without_changing_identity_or_entering_routes() -> None:
    target = trip()
    outbound_id = uuid4()
    return_id = uuid4()
    offer_id = uuid4()
    outbound = TripPlanItem(
        id=outbound_id,
        trip_plan_id=target.id,
        item_type="flight",
        offer_id=offer_id,
        day_date=target.start_date,
        position=0,
        title="BR 198 抵達旅程",
        locked=True,
        fixed_time=False,
        is_estimated=False,
        is_skipped=False,
        data={"timeline_section": "logistics"},
    )
    returning = TripPlanItem(
        id=return_id,
        trip_plan_id=target.id,
        item_type="flight",
        offer_id=offer_id,
        day_date=target.end_date,
        position=5,
        title="搭乘 BR 197 返回",
        locked=True,
        fixed_time=False,
        is_estimated=False,
        is_skipped=False,
        data={"timeline_section": "logistics"},
    )
    rows = [outbound, returning]
    session = AddOnlySession()

    assert ensure_system_slots(session, target, rows) is True  # type: ignore[arg-type]
    assert outbound.id == outbound_id
    assert outbound.offer_id == offer_id
    assert outbound.system_role == "outbound_flight"
    assert outbound.fixed_time is True
    assert returning.id == return_id
    assert returning.system_role == "return_flight"
    assert all(item not in active_route_rows(rows) for item in (outbound, returning))
    assert ensure_system_slots(session, target, rows) is False  # type: ignore[arg-type]


def test_single_day_trip_places_both_flights_outside_the_city_route() -> None:
    target = trip()
    target.end_date = target.start_date
    rows: list[TripPlanItem] = []
    session = AddOnlySession()

    ensure_system_slots(session, target, rows)  # type: ignore[arg-type]
    ordered = sorted(rows, key=lambda item: item.position)
    assert ordered[0].system_role == "outbound_flight"
    assert ordered[-1].system_role == "return_flight"
    assert [item.system_role for item in active_route_rows(rows)] == [
        "hotel_start",
        "lunch",
        "dinner",
        "hotel_end",
    ]


def test_manual_flight_uses_local_wall_clock_strings_and_can_be_cleared() -> None:
    target = trip()
    rows: list[TripPlanItem] = []
    session = AddOnlySession()
    ensure_system_slots(session, target, rows)  # type: ignore[arg-type]
    outbound = next(item for item in rows if item.system_role == "outbound_flight")
    details = FlightAnchorDetails(
        airline=" 長榮航空 ",
        flight_number=" BR 198 ",
        origin="tpe",
        destination="nrt",
        departure_local="2026-11-10T08:50",
        arrival_local="2026-11-10T13:10",
    )

    apply_flight_anchor_details(outbound, "outbound_flight", details)
    assert outbound.start_time is None
    assert outbound.end_time is None
    assert outbound.data["flight_selection_source"] == "manual"
    assert outbound.data["flight_info"] == {
        "airline": "長榮航空",
        "flight_number": "BR 198",
        "origin": "TPE",
        "destination": "NRT",
        "departure_local": "2026-11-10T08:50",
        "arrival_local": "2026-11-10T13:10",
        "departure_timezone": None,
        "arrival_timezone": None,
    }

    apply_flight_anchor_details(outbound, "outbound_flight", None)
    assert outbound.title == "去程航班尚未設定"
    assert outbound.data["flight_info"] is None


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


def test_itinerary_update_accepts_zero_duration_hotel_anchors() -> None:
    starts = datetime(2026, 11, 10, 9, tzinfo=ZoneInfo("Asia/Tokyo"))

    payload = ItineraryUpdateRequest.model_validate(
        {
            "version": 1,
            "items": [
                {
                    "item_type": "hotel_anchor",
                    "day_date": "2026-11-10",
                    "position": 0,
                    "title": "從飯店出發",
                    "start_time": starts.isoformat(),
                    "end_time": starts.isoformat(),
                    "duration_minutes": 0,
                    "locked": True,
                    "fixed_time": True,
                    "system_role": "hotel_start",
                }
            ],
        }
    )

    assert payload.items[0].end_time == payload.items[0].start_time
