from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from app.models import TripPlan, TripPlanItem
from app.trips.itinerary import ItineraryItem
from app.trips.replan import sync_ai_meal_slots
from app.trips.router import (
    FlightAnchorDetails,
    ItineraryUpdateRequest,
    ScheduleDefaultsUpdateRequest,
    _planner_availability,
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
    assert first_day_route == [activity]
    assert legacy_hotel not in first_day_route
    assert not any(row.system_role for row in first_day_route)
    original_pairs = route_pair_count(rows)
    lunch = next(
        row
        for row in rows
        if row.day_date == date(2026, 11, 10) and row.system_role == "lunch"
    )
    assert lunch.title == "午餐尚未安排"
    assert lunch.data["meal_selection_source"] == "unset"
    lunch.is_skipped = True
    without_lunch = active_route_rows(rows, date(2026, 11, 10))
    assert lunch not in without_lunch
    assert without_lunch == [activity]
    assert route_pair_count(rows) == original_pairs


def test_ai_refresh_clears_catalog_meal_placeholders_without_touching_user_choice() -> None:
    target = trip()
    lunch = TripPlanItem(
        id=uuid4(),
        trip_plan_id=target.id,
        item_type="meal",
        day_date=target.start_date,
        position=1,
        title="築地場外市場早餐",
        location_name="東京",
        latitude=Decimal("35.665000"),
        longitude=Decimal("139.770000"),
        provider_place_id="stale-place",
        location_source="google_places_auto",
        locked=True,
        fixed_time=True,
        is_estimated=True,
        system_role="lunch",
        data={
            "source_mode": "catalog",
            "meal_kind": "lunch",
            "meal_selection_source": "catalog",
            "candidate_key": "merchant:stale",
            "merchant_id": "stale",
        },
    )
    dinner = TripPlanItem(
        id=uuid4(),
        trip_plan_id=target.id,
        item_type="meal",
        day_date=target.start_date,
        position=2,
        title="使用者已選餐廳",
        location_name="銀座",
        locked=True,
        fixed_time=True,
        is_estimated=False,
        system_role="dinner",
        data={"meal_kind": "dinner", "meal_selection_source": "user"},
    )

    sync_ai_meal_slots([lunch, dinner], [])

    assert lunch.title == "午餐尚未安排"
    assert lunch.location_name is None
    assert lunch.latitude is None and lunch.longitude is None
    assert lunch.provider_place_id is None and lunch.location_source is None
    assert lunch.data["meal_selection_source"] == "unset"
    assert "candidate_key" not in lunch.data and "merchant_id" not in lunch.data
    assert dinner.title == "使用者已選餐廳"


def test_ai_refresh_assigns_only_exact_merchant_to_open_meal_slot() -> None:
    target = trip()
    lunch = TripPlanItem(
        id=uuid4(),
        trip_plan_id=target.id,
        item_type="meal",
        day_date=target.start_date,
        position=1,
        title="午餐尚未安排",
        locked=True,
        fixed_time=True,
        is_estimated=True,
        system_role="lunch",
        data={"meal_kind": "lunch", "meal_selection_source": "unset"},
    )
    exact_meal = ItineraryItem(
        id=uuid4(),
        item_type="meal",
        day_date=target.start_date,
        position=1,
        title="核准壽司店",
        location_name="銀座 核准壽司店",
        latitude=35.6717,
        longitude=139.7650,
        provider_place_id="verified-place",
        location_source="food_merchant_catalog",
        duration_minutes=75,
        locked=True,
        fixed_time=True,
        is_estimated=False,
        system_role="lunch",
        data={"candidate_key": "merchant:verified", "merchant_id": "verified"},
    )

    sync_ai_meal_slots([lunch], [exact_meal])

    assert lunch.title == "核准壽司店"
    assert lunch.provider_place_id == "verified-place"
    assert lunch.data["meal_selection_source"] == "ai"


def test_ai_single_day_refresh_does_not_change_meals_on_other_dates() -> None:
    target = trip()
    untouched = TripPlanItem(
        id=uuid4(),
        trip_plan_id=target.id,
        item_type="meal",
        day_date=target.end_date,
        position=1,
        title="第二天原有餐廳",
        location_name="銀座",
        locked=True,
        fixed_time=True,
        is_estimated=False,
        system_role="lunch",
        data={"meal_kind": "lunch", "meal_selection_source": "ai"},
    )

    sync_ai_meal_slots([untouched], [], target.start_date)

    assert untouched.title == "第二天原有餐廳"
    assert untouched.location_name == "銀座"
    assert untouched.data["meal_selection_source"] == "ai"


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
    assert active_route_rows(rows) == []


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


def test_planner_availability_uses_flight_times_and_transfer_buffers() -> None:
    target = trip()
    rows: list[TripPlanItem] = []
    session = AddOnlySession()
    ensure_system_slots(session, target, rows)  # type: ignore[arg-type]
    outbound = next(item for item in rows if item.system_role == "outbound_flight")
    returning = next(item for item in rows if item.system_role == "return_flight")
    apply_flight_anchor_details(
        outbound,
        "outbound_flight",
        FlightAnchorDetails(
            airline="長榮航空",
            flight_number="BR 198",
            origin="TPE",
            destination="NRT",
            departure_local="2026-11-10T08:50",
            arrival_local="2026-11-10T13:10",
        ),
    )
    apply_flight_anchor_details(
        returning,
        "return_flight",
        FlightAnchorDetails(
            airline="長榮航空",
            flight_number="BR 197",
            origin="NRT",
            destination="TPE",
            departure_local="2026-11-11T19:00",
            arrival_local="2026-11-11T22:00",
        ),
    )

    availability = _planner_availability(
        rows,
        trip_start=target.start_date,  # type: ignore[arg-type]
        trip_end=target.end_date,  # type: ignore[arg-type]
        target_date=None,
    )

    assert availability == {
        "first_day_available_from": "15:10",
        "last_day_available_until": "16:00",
        "used_outbound_flight": True,
        "used_return_flight": True,
    }


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
    changed = sync_primary_lodging(target, rows, lodging)
    hotels = [row for row in rows if row.system_role in {"hotel_start", "hotel_end"}]
    assert len(hotels) == 4
    assert all(row.provider_place_id == "place-hotel" for row in hotels)
    assert all(row.data["needs_place_confirmation"] is False for row in hotels)
    # Only the hotel anchors moved, so only their legs need new routes.
    assert changed == {row.id for row in hotels}
    assert sync_primary_lodging(target, rows, lodging) == set()

    target.data = {
        **target.data,
        "schedule_defaults": {
            "day_start_time": "08:15",
            "lunch_time": "11:45",
            "lunch_duration_minutes": 45,
            "dinner_time": "19:15",
            "dinner_duration_minutes": 120,
        },
    }
    apply_schedule_defaults(target, rows)
    lunches = [row for row in rows if row.system_role == "lunch"]
    dinners = [row for row in rows if row.system_role == "dinner"]
    departures = [row for row in rows if row.system_role == "hotel_start"]
    assert all(row.start_time and row.start_time.strftime("%H:%M") == "11:45" for row in lunches)
    assert all(row.duration_minutes == 45 for row in lunches)
    assert all(row.start_time and row.start_time.strftime("%H:%M") == "19:15" for row in dinners)
    assert all(row.duration_minutes == 120 for row in dinners)
    assert departures
    assert all(row.start_time and row.start_time.strftime("%H:%M") == "08:15" for row in departures)
    assert all(row.end_time == row.start_time for row in departures)


def test_schedule_defaults_request_keeps_the_day_start_optional_and_ordered() -> None:
    base = {
        "version": 1,
        "lunch_time": "12:00",
        "lunch_duration_minutes": 60,
        "dinner_time": "18:30",
        "dinner_duration_minutes": 90,
    }

    # Older clients that never send a departure time must not blank the stored one.
    omitted = ScheduleDefaultsUpdateRequest.model_validate(base)
    assert omitted.day_start_time is None
    assert "day_start_time" not in omitted.model_dump(exclude={"version"}, exclude_none=True)

    accepted = ScheduleDefaultsUpdateRequest.model_validate({**base, "day_start_time": "08:15"})
    assert accepted.day_start_time == "08:15"

    with pytest.raises(ValidationError):
        ScheduleDefaultsUpdateRequest.model_validate({**base, "day_start_time": "13:00"})
    with pytest.raises(ValidationError):
        ScheduleDefaultsUpdateRequest.model_validate({**base, "day_start_time": "8:15"})


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
