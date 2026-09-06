"""Corruption guards for `PATCH /trips/{id}`.

The trip day grid carries five separate identities that are keyed by `day_date`:
the `uq_trip_plan_item_system_role` unique constraint, the
`uq_trip_route_day_setting` unique constraint, absolute `start_time` /
`end_time` stamps, the first/last-day flight anchors, and every
`trip_route_segments` row. These tests pin all five, and they do it against a
store that enforces the real DDL so a naive one-pass shift cannot pass.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Mapping
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import pytest

from app.models import TripPlan, TripPlanItem, TripRouteDaySetting, TripRouteSegment
from app.problems import AppError
from app.trips.reschedule import (
    apply_reschedule,
    day_shift_phases,
    ensure_shrink_confirmed,
    plan_reschedule,
    reschedule_summary,
    reschedule_trip_data,
    resolve_target_range,
)
from app.trips.schedule import ensure_system_slots

TOKYO = ZoneInfo("Asia/Tokyo")
DAY_ONE = date(2026, 11, 10)


# --------------------------------------------------------------------------
# A store that enforces the constraints the real tables carry.
# --------------------------------------------------------------------------


class ConstraintViolation(AssertionError):
    pass


class FakeSession:
    """The slice of AsyncSession the reschedule applier is allowed to use.

    Every flush revalidates the unique constraints and the route-segment
    foreign keys, so a shift that parks two system slots on the same day fails
    here exactly the way PostgreSQL would.
    """

    def __init__(
        self,
        items: list[TripPlanItem],
        day_settings: list[TripRouteDaySetting],
        segments: list[TripRouteSegment],
    ) -> None:
        # Own copies: the store stands in for the tables, the caller's lists
        # stand in for the handler's in-memory view. They must not drift.
        self.items = list(items)
        self.day_settings = list(day_settings)
        self.segments = list(segments)
        self.flushes = 0

    def add(self, instance: object) -> None:
        if isinstance(instance, TripPlanItem):
            self.items.append(instance)
        elif isinstance(instance, TripRouteDaySetting):
            self.day_settings.append(instance)
        elif isinstance(instance, TripRouteSegment):
            self.segments.append(instance)
        else:  # pragma: no cover - the applier never adds anything else
            raise AssertionError(f"unexpected insert: {instance!r}")

    async def delete(self, instance: object) -> None:
        for bucket in (self.items, self.day_settings, self.segments):
            if instance in bucket:
                bucket.remove(instance)
                if isinstance(instance, TripPlanItem):
                    # ON DELETE CASCADE from trip_route_segments.
                    self.segments[:] = [
                        record
                        for record in self.segments
                        if instance.id not in {record.from_item_id, record.to_item_id}
                    ]
                return
        raise AssertionError(f"deleted an instance that is not persistent: {instance!r}")

    async def flush(self) -> None:
        self.flushes += 1
        self.check()

    def check(self) -> None:
        seen: set[Any] = set()
        for item in self.items:
            if item.id in seen:
                raise ConstraintViolation(f"trip_plan_items primary key reused: {item.id}")
            seen.add(item.id)
        self._unique(
            self.items,
            lambda row: (row.trip_plan_id, row.day_date, row.system_role),
            skip=lambda row: row.system_role is None,
            name="uq_trip_plan_item_system_role",
        )
        self._unique(
            self.day_settings,
            lambda row: (row.trip_plan_id, row.day_date),
            skip=lambda row: False,
            name="uq_trip_route_day_setting",
        )
        self._unique(
            self.segments,
            lambda row: (row.trip_plan_id, row.from_item_id, row.to_item_id),
            skip=lambda row: False,
            name="uq_trip_route_segment_pair",
        )
        live = {item.id for item in self.items}
        for segment in self.segments:
            if segment.from_item_id not in live or segment.to_item_id not in live:
                raise ConstraintViolation("trip_route_segments references a deleted item")

    @staticmethod
    def _unique(
        rows: list[Any],
        key: Callable[[Any], tuple[Any, ...]],
        *,
        skip: Callable[[Any], bool],
        name: str,
    ) -> None:
        seen: set[tuple[Any, ...]] = set()
        for row in rows:
            if skip(row):
                continue
            value = key(row)
            if value in seen:
                raise ConstraintViolation(f"{name} violated by {value}")
            seen.add(value)


def phase_is_order_safe(
    before: Mapping[Hashable, date],
    after: Mapping[Hashable, date],
    partition: Callable[[Hashable], tuple[Any, ...]],
) -> bool:
    """True when the phase survives being applied one row at a time, in any order.

    PostgreSQL checks a non-deferrable UNIQUE index per row, so a phase is only
    safe when no row's target day is already occupied by another row that
    shares its partition key and has not moved yet.
    """
    for key, target in after.items():
        for other, current in before.items():
            if other == key:
                continue
            if partition(other) == partition(key) and current == target:
                return False
    return True


# --------------------------------------------------------------------------
# Fixtures: the trip the spec asks for.
# --------------------------------------------------------------------------


def build_trip(start: date = DAY_ONE, days: int = 3) -> TripPlan:
    return TripPlan(
        id=uuid4(),
        user_id=uuid4(),
        name="東京三日",
        mode="manual",
        total_price=Decimal("0"),
        currency="TWD",
        data={
            "primary_lodging": {
                "name": "新宿飯店",
                "location_name": "新宿",
                "latitude": 35.69,
                "longitude": 139.70,
                "location_source": "google_places",
                "selection_source": "user",
                "price_snapshot": {"nights": days - 1, "total_price": "42000"},
            },
            "planning": {
                "status": "live",
                "provider": "openai",
                "scope": "day",
                "day_date": start.isoformat(),
                "unscheduled_slots": [{"date": start.isoformat(), "slot": "dinner"}],
                "warnings": [],
                "generated_at": "2026-09-01T00:00:00+00:00",
            },
            "itinerary": [{"day": start.isoformat(), "items": []}],
            "routing": {"status": "complete", "total": 8, "completed": 8},
        },
        version=4,
        destination_name="東京",
        start_date=start,
        end_date=start + timedelta(days=days - 1),
        timezone="Asia/Tokyo",
        route_preference="FEWER_TRANSFERS",
    )


def system_row(
    trip: TripPlan,
    day: date,
    role: str,
    *,
    data: dict[str, Any] | None = None,
    start_time: datetime | None = None,
) -> TripPlanItem:
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip.id,
        item_type={"lunch": "meal", "dinner": "meal"}.get(role, "hotel_anchor"),
        day_date=day,
        position=0,
        title=role,
        start_time=start_time,
        end_time=start_time,
        locked=True,
        fixed_time=True,
        is_estimated=True,
        latitude=Decimal("35.69"),
        longitude=Decimal("139.70"),
        data=data or {"source_mode": "system"},
        system_role=role,
        is_skipped=False,
    )


def flight_row(trip: TripPlan, day: date, role: str, *, booked: bool) -> TripPlanItem:
    info = {
        "airline": "JAL",
        "flight_number": "JL802",
        "origin": "TPE",
        "destination": "NRT",
        "departure_local": f"{day.isoformat()}T09:00",
        "arrival_local": f"{day.isoformat()}T13:10",
    }
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip.id,
        item_type="flight",
        day_date=day,
        position=0,
        title="JAL JL802" if booked else "去程航班尚未設定",
        locked=True,
        fixed_time=True,
        is_estimated=not booked,
        data={
            "source_mode": "manual" if booked else "system",
            "timeline_section": "flight_anchor",
            "flight_selection_source": "manual" if booked else "unset",
            "flight_info": info if booked else None,
        },
        system_role=role,
        is_skipped=False,
    )


def activity_row(trip: TripPlan, day: date, title: str, hour: int = 10) -> TripPlanItem:
    starts = datetime.combine(day, datetime.min.time(), tzinfo=TOKYO).replace(hour=hour)
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip.id,
        item_type="custom",
        day_date=day,
        position=1,
        title=title,
        start_time=starts,
        end_time=starts + timedelta(minutes=90),
        latitude=Decimal("35.71"),
        longitude=Decimal("139.79"),
        locked=False,
        fixed_time=False,
        is_estimated=False,
        duration_minutes=90,
        data={},
        is_skipped=False,
    )


def segment(
    trip: TripPlan, day: date, first: TripPlanItem, second: TripPlanItem
) -> TripRouteSegment:
    morning = datetime.combine(day, datetime.min.time(), tzinfo=TOKYO)
    return TripRouteSegment(
        id=uuid4(),
        trip_plan_id=trip.id,
        day_date=day,
        from_item_id=first.id,
        to_item_id=second.id,
        provider="ekispert",
        attribution="Ekispert",
        duration_minutes=18,
        departure_time=morning.replace(hour=9),
        arrival_time=morning.replace(hour=9, minute=18),
        is_override=False,
    )


def build_world(
    trip: TripPlan,
) -> tuple[list[TripPlanItem], list[TripRouteDaySetting], list[TripRouteSegment]]:
    """One outbound flight, one return flight, two lodging anchors per day,
    six meal rows across three days, one user activity, day settings and the
    route segments that join them."""
    assert trip.start_date is not None and trip.end_date is not None
    days = [trip.start_date + timedelta(days=offset) for offset in range(3)]
    items: list[TripPlanItem] = [
        flight_row(trip, days[0], "outbound_flight", booked=True),
        flight_row(trip, days[-1], "return_flight", booked=True),
    ]
    for index, day in enumerate(days):
        morning = datetime.combine(day, datetime.min.time(), tzinfo=TOKYO).replace(hour=9)
        items.append(system_row(trip, day, "hotel_start", start_time=morning))
        items.append(system_row(trip, day, "hotel_end"))
        items.append(
            system_row(
                trip,
                day,
                "lunch",
                data={
                    "source_mode": "system",
                    "meal_kind": "lunch",
                    # Day 2's lunch is a restaurant the traveller picked themselves.
                    "meal_selection_source": "user" if index == 1 else "unset",
                    "merchant_id": "m-1" if index == 1 else None,
                },
                start_time=morning.replace(hour=12),
            )
        )
        items.append(
            system_row(
                trip,
                day,
                "dinner",
                data={"source_mode": "system", "meal_kind": "dinner"},
                start_time=morning.replace(hour=18, minute=30),
            )
        )
    items.append(activity_row(trip, days[1], "淺草寺"))

    settings = [
        TripRouteDaySetting(
            id=uuid4(),
            trip_plan_id=trip.id,
            day_date=day,
            default_travel_mode="walk" if index == 1 else "transit",
            default_buffer_minutes=20 if index == 1 else 10,
            route_preference="LESS_WALKING",
            auto_compute=True,
        )
        for index, day in enumerate(days)
    ]

    segments: list[TripRouteSegment] = []
    for day in days:
        day_rows = [
            row
            for row in items
            if row.day_date == day and row.system_role not in {"outbound_flight", "return_flight"}
        ]
        for first, second in zip(day_rows, day_rows[1:], strict=False):
            segments.append(segment(trip, day, first, second))
    return items, settings, segments


def role_days(items: list[TripPlanItem], role: str) -> list[date]:
    return sorted(row.day_date for row in items if row.system_role == role and row.day_date)


# --------------------------------------------------------------------------
# The headline test.
# --------------------------------------------------------------------------


async def test_shifting_a_fully_populated_trip_keeps_every_day_keyed_invariant() -> None:
    trip = build_trip()
    items, settings, segments = build_world(trip)
    original_days = {row.id: row.day_date for row in items}
    lunch_pick = next(
        row for row in items if row.system_role == "lunch" and row.data.get("merchant_id")
    )
    activity = next(row for row in items if row.system_role is None)
    old_activity_start = activity.start_time
    assert old_activity_start is not None

    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=2,
        start_date=None,
        end_date=None,
    )
    assert target is not None
    assert (target.start, target.end) == (DAY_ONE + timedelta(days=2), DAY_ONE + timedelta(days=4))
    assert target.content_offset == 2

    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    assert plan.removed_item_ids == ()
    # A shift deletes no row, but it re-dates both booked anchors and apply clears
    # their bookings; the plan says so up front instead of counting it afterwards.
    assert [row.kind for row in plan.protected_rows] == ["booked_flight", "booked_flight"]
    assert [row.day_date for row in plan.protected_rows] == [DAY_ONE, DAY_ONE + timedelta(days=2)]

    # 1. The item shift is genuinely two-phase and each phase is order-safe.
    item_days = {row.id: row.day_date for row in items if row.day_date is not None}
    phases = day_shift_phases(item_days, plan.content_offset, plan.sentinel_offset)
    assert len(phases) == 2, "a one-pass shift self-collides on uq_trip_plan_item_system_role"
    role_of = {row.id: row.system_role for row in items}
    partition = lambda key: (role_of[key],)  # noqa: E731 - terse on purpose
    current = dict(item_days)
    for phase in phases:
        assert phase_is_order_safe(current, phase, partition)
        current = dict(phase)
    assert all(current[key] == item_days[key] + timedelta(days=2) for key in item_days)

    # 2. Day settings need the same treatment; their day_date is NOT NULL, so
    #    every single row collides on a one-pass shift.
    setting_days = {row.id: row.day_date for row in settings}
    setting_phases = day_shift_phases(setting_days, plan.content_offset, plan.sentinel_offset)
    assert len(setting_phases) == 2
    current_settings = dict(setting_days)
    for phase in setting_phases:
        assert phase_is_order_safe(current_settings, phase, lambda _key: ())
        current_settings = dict(phase)

    session = FakeSession(items, settings, segments)
    session.check()
    trip.start_date, trip.end_date = target.start, target.end
    rows = await apply_reschedule(
        session,  # type: ignore[arg-type]
        trip,
        items=items,
        day_settings=settings,
        segments=segments,
        plan=plan,
    )
    session.check()

    new_days = [target.start + timedelta(days=offset) for offset in range(3)]
    # 3. Nothing is stranded outside the new range - that is what permanently
    #    422s PUT /trips/{id}/itinerary.
    assert {row.day_date for row in rows} == set(new_days)
    assert all(row.day_date == original_days[row.id] + timedelta(days=2) for row in rows
               if row.id in original_days and row.system_role not in {"outbound_flight",
                                                                      "return_flight"})

    # 4. Exactly one flight anchor per role, on the new first and last day.
    assert role_days(rows, "outbound_flight") == [new_days[0]]
    assert role_days(rows, "return_flight") == [new_days[-1]]

    # 5. A booked flight is not silently re-dated; it is cleared and reported.
    for role in ("outbound_flight", "return_flight"):
        anchor = next(row for row in rows if row.system_role == role)
        assert anchor.data.get("flight_info") is None
        assert anchor.data.get("flight_selection_source") == "unset"
        assert anchor.is_estimated is True
    assert set(plan.invalidated_flight_item_ids) == {
        row.id for row in items if row.system_role in {"outbound_flight", "return_flight"}
    }

    # 6. Every route segment is gone; none may survive with a stale day_date.
    assert segments == []

    # 7. Per-day travel settings travel with the day they describe.
    assert sorted(row.day_date for row in settings) == new_days
    moved = next(row for row in settings if row.day_date == new_days[1])
    assert (moved.default_travel_mode, moved.default_buffer_minutes) == ("walk", 20)

    # 8. Absolute timestamps move with the day, keeping the same wall clock.
    assert activity.day_date == new_days[1]
    assert activity.start_time is not None
    assert activity.start_time.astimezone(TOKYO).date() == new_days[1]
    assert activity.start_time.astimezone(TOKYO).timetz() == old_activity_start.astimezone(
        TOKYO
    ).timetz()

    # 9. The traveller's own restaurant choice survives the move.
    assert lunch_pick.day_date == new_days[1]
    assert lunch_pick.data.get("meal_selection_source") == "user"
    assert lunch_pick.data.get("merchant_id") == "m-1"

    # 10. The grid is now stable: a read-path ensure_system_slots adds nothing.
    before = len(items)
    ensure_system_slots(session, trip, rows)  # type: ignore[arg-type]
    session.check()
    assert len(items) == before
    assert role_days(rows, "outbound_flight") == [new_days[0]]


async def test_a_shift_then_extend_does_not_collide_on_a_day_derived_primary_key() -> None:
    """Reachable in two PATCHes with no deletes; it used to 500 every GET.

    System-slot ids were `uuid5(trip, day, role)`, so a shifted row kept an id
    naming its old day. Extending the range back over that day made
    `ensure_system_slots` mint a row with an id another row already held.
    """
    trip = build_trip(days=2)
    items, settings, segments = build_world(trip)
    session = FakeSession(items, settings, segments)

    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=1,
        start_date=None,
        end_date=None,
    )
    assert target is not None
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    trip.start_date, trip.end_date = target.start, target.end
    rows = await apply_reschedule(
        session,  # type: ignore[arg-type]
        trip,
        items=items,
        day_settings=settings,
        segments=segments,
        plan=plan,
    )

    # Now pull the start back over the day the shifted rows used to occupy.
    widened = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=None,
        start_date=DAY_ONE,
        end_date=trip.end_date,
    )
    assert widened is not None
    assert widened.content_offset == 0
    plan_two = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=widened,
        items=rows,
        day_settings=settings,
    )
    trip.start_date, trip.end_date = widened.start, widened.end
    rows = await apply_reschedule(
        session,  # type: ignore[arg-type]
        trip,
        items=rows,
        day_settings=settings,
        segments=segments,
        plan=plan_two,
    )
    session.check()
    assert role_days(rows, "outbound_flight") == [DAY_ONE]
    assert role_days(rows, "return_flight") == [trip.end_date]
    assert len({row.id for row in rows}) == len(rows)


async def test_extending_the_tail_leaves_the_outbound_anchor_and_its_booking_alone() -> None:
    trip = build_trip()
    items, settings, segments = build_world(trip)
    session = FakeSession(items, settings, segments)
    outbound = next(row for row in items if row.system_role == "outbound_flight")
    booking = dict(outbound.data)

    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=None,
        start_date=None,
        end_date=DAY_ONE + timedelta(days=4),
    )
    assert target is not None
    assert target.content_offset == 0
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    assert plan.removed_item_ids == ()
    trip.start_date, trip.end_date = target.start, target.end
    rows = await apply_reschedule(
        session,  # type: ignore[arg-type]
        trip,
        items=items,
        day_settings=settings,
        segments=segments,
        plan=plan,
    )
    session.check()

    assert outbound.data == booking, "an untouched first day must keep its booked flight"
    assert role_days(rows, "outbound_flight") == [DAY_ONE]
    assert role_days(rows, "return_flight") == [DAY_ONE + timedelta(days=4)]
    # ensure_system_slots fills the two new days rather than duplicating anchors.
    assert sorted({row.day_date for row in rows}) == [
        DAY_ONE + timedelta(days=offset) for offset in range(5)
    ]
    for day in (DAY_ONE + timedelta(days=3), DAY_ONE + timedelta(days=4)):
        assert {row.system_role for row in rows if row.day_date == day} >= {
            "hotel_start",
            "hotel_end",
            "lunch",
            "dinner",
        }


async def test_shrinking_reports_the_content_it_would_destroy_before_deleting_it() -> None:
    trip = build_trip()
    items, settings, segments = build_world(trip)
    last_day = DAY_ONE + timedelta(days=2)
    items.append(activity_row(trip, last_day, "台場", hour=15))

    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=None,
        start_date=None,
        end_date=DAY_ONE + timedelta(days=1),
    )
    assert target is not None
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    assert plan.removed_days == (last_day,)
    # The traveller's own activity is deleted outright. The booked return flight
    # relocates to the new last day, but a flight number is tied to its calendar
    # date, so apply clears the booking — and that loss is reported as well.
    kinds = {row.kind for row in plan.protected_rows}
    assert kinds == {"activity", "booked_flight"}
    assert [row.title for row in plan.protected_rows] == ["台場", "JAL JL802"]
    assert [flight.flight_number for flight in plan.invalidated_flights] == ["JL802"]
    assert plan.removed_day_setting_ids == (
        next(row.id for row in settings if row.day_date == last_day),
    )

    session = FakeSession(items, settings, segments)
    trip.start_date, trip.end_date = target.start, target.end
    rows = await apply_reschedule(
        session,  # type: ignore[arg-type]
        trip,
        items=items,
        day_settings=settings,
        segments=segments,
        plan=plan,
    )
    session.check()
    assert {row.day_date for row in rows} == {DAY_ONE, DAY_ONE + timedelta(days=1)}
    assert role_days(rows, "return_flight") == [DAY_ONE + timedelta(days=1)]
    assert all(row.day_date != last_day for row in settings)


async def test_shrinking_from_the_front_removes_the_head_day_and_rehomes_the_outbound() -> None:
    trip = build_trip()
    items, settings, segments = build_world(trip)
    session = FakeSession(items, settings, segments)

    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=None,
        start_date=DAY_ONE + timedelta(days=1),
        end_date=None,
    )
    assert target is not None
    assert target.content_offset == 0
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    assert plan.removed_days == (DAY_ONE,)
    trip.start_date, trip.end_date = target.start, target.end
    rows = await apply_reschedule(
        session,  # type: ignore[arg-type]
        trip,
        items=items,
        day_settings=settings,
        segments=segments,
        plan=plan,
    )
    session.check()
    assert role_days(rows, "outbound_flight") == [DAY_ONE + timedelta(days=1)]
    assert role_days(rows, "return_flight") == [DAY_ONE + timedelta(days=2)]


async def test_a_rename_asks_for_no_date_work_at_all() -> None:
    trip = build_trip()
    assert (
        resolve_target_range(
            old_start=trip.start_date,
            old_end=trip.end_date,
            shift_days=None,
            start_date=None,
            end_date=None,
        )
        is None
    )


@pytest.mark.parametrize(
    ("shift_days", "start_date", "end_date", "code"),
    [
        (None, DAY_ONE + timedelta(days=5), DAY_ONE, "trip_date_range_invalid"),
        (None, DAY_ONE, DAY_ONE + timedelta(days=61), "trip_date_range_too_long"),
        (400_000, None, None, "trip_date_out_of_bounds"),
    ],
)
def test_the_target_range_is_validated_before_any_row_moves(
    shift_days: int | None, start_date: date | None, end_date: date | None, code: str
) -> None:
    with pytest.raises(AppError) as raised:
        resolve_target_range(
            old_start=DAY_ONE,
            old_end=DAY_ONE + timedelta(days=2),
            shift_days=shift_days,
            start_date=start_date,
            end_date=end_date,
        )
    assert raised.value.code == code
    assert raised.value.status == 422


def test_a_past_start_date_is_allowed_because_a_running_trip_stays_editable() -> None:
    yesterday = datetime.now(UTC).date() - timedelta(days=30)
    target = resolve_target_range(
        old_start=yesterday,
        old_end=yesterday + timedelta(days=2),
        shift_days=-1,
        start_date=None,
        end_date=None,
    )
    assert target is not None
    assert target.start == yesterday - timedelta(days=1)


def test_a_trip_with_a_day_less_item_refuses_to_move(monkeypatch: pytest.MonkeyPatch) -> None:
    trip = build_trip()
    items, settings, _segments = build_world(trip)
    stray = activity_row(trip, DAY_ONE, "未排入的地點")
    stray.day_date = None
    items.append(stray)
    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=1,
        start_date=None,
        end_date=None,
    )
    assert target is not None
    with pytest.raises(AppError) as raised:
        plan_reschedule(
            old_start=trip.start_date,
            old_end=trip.end_date,
            target=target,
            items=items,
            day_settings=settings,
        )
    assert raised.value.code == "trip_item_day_missing"


def test_the_sentinel_band_never_overlaps_a_day_the_trip_holds() -> None:
    trip = build_trip()
    items, settings, _segments = build_world(trip)
    for shift in (-4, -1, 1, 4, 365):
        target = resolve_target_range(
            old_start=trip.start_date,
            old_end=trip.end_date,
            shift_days=shift,
            start_date=None,
            end_date=None,
        )
        assert target is not None
        plan = plan_reschedule(
            old_start=trip.start_date,
            old_end=trip.end_date,
            target=target,
            items=items,
            day_settings=settings,
        )
        occupied = {row.day_date for row in items if row.day_date}
        occupied |= {day + timedelta(days=shift) for day in occupied}
        parked = {day + timedelta(days=plan.sentinel_offset) for day in occupied}
        assert not (parked & occupied), f"sentinel band collides for shift {shift}"


def test_uuids_for_new_system_slots_do_not_encode_the_day() -> None:
    """The regression guard for the day-derived primary key."""
    trip = build_trip(days=1)
    session = FakeSession([], [], [])
    rows: list[TripPlanItem] = []
    ensure_system_slots(session, trip, rows)  # type: ignore[arg-type]
    first = {row.system_role: row.id for row in rows}

    other = build_trip(days=1)
    other.id = trip.id
    session_two = FakeSession([], [], [])
    rows_two: list[TripPlanItem] = []
    ensure_system_slots(session_two, other, rows_two)  # type: ignore[arg-type]
    second = {row.system_role: row.id for row in rows_two}

    assert first.keys() == second.keys()
    assert all(first[role] != second[role] for role in first), (
        "slot ids must not be derived from (trip, day, role) or a shifted row "
        "will collide with a freshly minted one"
    )
    assert all(isinstance(value, UUID) for value in first.values())

# --------------------------------------------------------------------------
# The endpoint layer: request contract, shrink gate, trip.data cleanup.
# --------------------------------------------------------------------------


def test_shrinks_that_drop_days_require_an_explicit_confirmation() -> None:
    trip = build_trip()
    items, settings, _segments = build_world(trip)
    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=None,
        start_date=None,
        end_date=DAY_ONE + timedelta(days=1),
    )
    assert target is not None
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    with pytest.raises(AppError) as raised:
        ensure_shrink_confirmed(plan, confirmed=False)
    assert raised.value.status == 422
    assert raised.value.code == "trip_shrink_confirmation_required"
    # Confirmed shrinks pass through untouched.
    ensure_shrink_confirmed(plan, confirmed=True)
    shift = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=2,
        start_date=None,
        end_date=None,
    )
    assert shift is not None
    # A shift drops no day, but build_world's anchors carry real bookings and a
    # booking is tied to its calendar date: the same gate has to catch that.
    booked_shift = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=shift,
        items=items,
        day_settings=settings,
    )
    assert booked_shift.removed_days == ()
    with pytest.raises(AppError) as flights_raised:
        ensure_shrink_confirmed(booked_shift, confirmed=False)
    assert flights_raised.value.code == "trip_shrink_confirmation_required"
    assert "JL802" in flights_raised.value.detail
    # With nothing booked, the same shift destroys nothing and needs no consent.
    unbooked = [
        row for row in items if row.system_role not in {"outbound_flight", "return_flight"}
    ] + [
        flight_row(trip, DAY_ONE, "outbound_flight", booked=False),
        flight_row(trip, DAY_ONE + timedelta(days=2), "return_flight", booked=False),
    ]
    harmless = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=shift,
        items=unbooked,
        day_settings=settings,
    )
    assert harmless.invalidated_flights == ()
    ensure_shrink_confirmed(harmless, confirmed=False)


def test_a_pure_extension_that_clears_a_booked_flight_needs_the_same_consent() -> None:
    """Adding days drops nothing, so the old gate waved it through — and apply then
    wiped the hand-typed return flight without a word. The plan now names the
    flight, the gate refuses without confirmation, and the summary says which
    booking moved from which day."""
    trip = build_trip()
    items, settings, _segments = build_world(trip)
    return_flight = next(row for row in items if row.system_role == "return_flight")
    booked_day = DAY_ONE + timedelta(days=2)
    target = resolve_target_range(
        old_start=trip.start_date,
        old_end=trip.end_date,
        shift_days=None,
        start_date=None,
        end_date=DAY_ONE + timedelta(days=4),
    )
    assert target is not None
    plan = plan_reschedule(
        old_start=trip.start_date,
        old_end=trip.end_date,
        target=target,
        items=items,
        day_settings=settings,
    )
    assert plan.removed_days == ()
    assert plan.removed_item_ids == ()
    assert plan.invalidated_flight_item_ids == (return_flight.id,)
    assert [row.kind for row in plan.protected_rows] == ["booked_flight"]
    assert plan.protected_rows[0].title == "JAL JL802"
    assert plan.protected_rows[0].day_date == booked_day

    with pytest.raises(AppError) as raised:
        ensure_shrink_confirmed(plan, confirmed=False)
    assert raised.value.status == 422
    assert raised.value.code == "trip_shrink_confirmation_required"
    assert "JL802" in raised.value.detail
    ensure_shrink_confirmed(plan, confirmed=True)

    summary = reschedule_summary(plan, segments_cleared=0)
    assert summary["invalidated_flight_anchors"] == 1
    assert summary["invalidated_flights"] == [
        {
            "role": "return_flight",
            "title": "JAL JL802",
            "flight_number": "JL802",
            "from_day": booked_day.isoformat(),
            "to_day": (DAY_ONE + timedelta(days=4)).isoformat(),
        }
    ]
    assert summary["removed_protected"] == [
        {"kind": "booked_flight", "title": "JAL JL802", "day_date": booked_day.isoformat()}
    ]


def test_reschedule_trip_data_rebuilds_every_date_stamped_blob() -> None:
    trip = build_trip()
    items, _settings, _segments = build_world(trip)
    data = reschedule_trip_data(trip.data, items)

    # The legacy day list would re-materialise items at the OLD dates if the
    # trip ever reached zero rows, and it leaks to share links verbatim.
    assert "itinerary" not in data
    # Planning chips point at calendar days; the day-scoped bits must go while
    # provider attribution survives.
    assert data["planning"]["provider"] == "openai"
    assert "day_date" not in data["planning"]
    assert "unscheduled_slots" not in data["planning"]
    # The lodging identity is user-chosen and survives; its price snapshot was
    # quoted for a night count the trip may no longer have.
    assert data["primary_lodging"]["name"] == "新宿飯店"
    assert data["primary_lodging"]["selection_source"] == "user"
    assert "price_snapshot" not in data["primary_lodging"]
    # The routing summary is recomputed from the post-move rows, not carried.
    assert data["routing"]["status"] == "stale"
    assert data["routing"]["completed"] == 0
    assert data["routing"]["total"] > 0
    assert data["edited"] is True
    # The input dict is not mutated in place.
    assert trip.data["routing"]["status"] == "complete"
    assert "itinerary" in trip.data


def test_reschedule_trip_data_reports_idle_when_nothing_is_routable() -> None:
    trip = build_trip()
    data = reschedule_trip_data(trip.data, [])
    assert data["routing"] == {
        "status": "idle",
        "total": 0,
        "completed": 0,
        "warnings": [],
        "updated_at": data["routing"]["updated_at"],
    }


def test_patch_request_normalizes_name_and_rejects_blank_or_empty_updates() -> None:
    from pydantic import ValidationError

    from app.trips.router import TripMetadataPatchRequest

    request = TripMetadataPatchRequest.model_validate(
        {"version": 3, "name": "  東京五日  "}
    )
    assert request.name == "東京五日"
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate({"version": 3, "name": "   "})
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate({"version": 3})
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate({"version": 3, "name": "x" * 256})


def test_patch_request_pins_status_and_cover_image_rules() -> None:
    from pydantic import ValidationError

    from app.trips.router import TripMetadataPatchRequest

    request = TripMetadataPatchRequest.model_validate(
        {"version": 1, "status": "travelling"}
    )
    assert request.status == "travelling"
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate({"version": 1, "status": "archived"})
    covered = TripMetadataPatchRequest.model_validate(
        {"version": 1, "cover_image_url": " https://cdn.example.com/tokyo.jpg "}
    )
    assert covered.cover_image_url == "https://cdn.example.com/tokyo.jpg"
    assert "cover_image_url" in covered.model_fields_set
    cleared = TripMetadataPatchRequest.model_validate(
        {"version": 1, "cover_image_url": None, "name": "東京"}
    )
    assert cleared.cover_image_url is None
    assert "cover_image_url" in cleared.model_fields_set
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate(
            {"version": 1, "cover_image_url": "javascript:alert(1)"}
        )
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate(
            {"version": 1, "cover_image_url": "http://insecure.example.com/a.jpg"}
        )


def test_patch_request_bounds_shift_days_and_omits_route_preference() -> None:
    from pydantic import ValidationError

    from app.trips.router import TripMetadataPatchRequest

    request = TripMetadataPatchRequest.model_validate({"version": 1, "shift_days": -7})
    assert request.shift_days == -7
    with pytest.raises(ValidationError):
        TripMetadataPatchRequest.model_validate({"version": 1, "shift_days": 400_000})
    # route_preference stays on PUT /trips/{id}/itinerary, which owns the
    # all-pairs invalidation that must accompany it. A second write path here
    # would skip that invalidation.
    assert "route_preference" not in TripMetadataPatchRequest.model_fields


def test_reprice_is_refused_once_the_trip_dates_left_the_original_search() -> None:
    """A reprice rebuilds the itinerary from the SearchRequest's dates, so a
    moved trip must not be able to re-import rows at its old dates."""
    from app.trips.router import search_dates_diverged

    start, end = DAY_ONE, DAY_ONE + timedelta(days=2)
    assert search_dates_diverged(start, end, start, end) is False
    assert search_dates_diverged(start + timedelta(days=1), end, start, end) is True
    assert search_dates_diverged(start, end + timedelta(days=1), start, end) is True
    # A one-way search has no return_date; only the start can diverge.
    assert search_dates_diverged(start, end, start, None) is False
    assert search_dates_diverged(start, None, start, end) is False
