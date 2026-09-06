"""Move a trip's day grid without corrupting anything keyed to a day.

Five separate identities hang off `trip_plan_items.day_date`, and a naive
`UPDATE ... SET day_date = day_date + 1` breaks four of them:

* ``uq_trip_plan_item_system_role`` and ``uq_trip_route_day_setting`` are plain,
  non-deferrable unique constraints, so PostgreSQL checks them per row while the
  statement walks the table. Every move therefore runs in two phases through a
  sentinel band that is provably disjoint from both the old and the new grid.
* ``start_time`` / ``end_time`` are absolute timestamps that do not travel with
  ``day_date``; they are re-stamped on the new day at the same wall clock.
* The outbound and return flight anchors are chosen by day *index*, so a range
  that grows at either end otherwise mints a duplicate anchor that the unique
  constraint happily allows and ``update_flight_anchor`` then edits by mistake.
* ``trip_route_segments`` is keyed on the item pair with no day in it, so a
  stale row stays invisible to the day-scoped lookup and only surfaces as an
  IntegrityError inside the routing worker. Every segment is dropped instead.

Anything left outside ``[start_date, end_date]`` permanently 422s
``PUT /trips/{id}/itinerary`` (it re-injects system rows into its own range
check), so the plan also guarantees that no row survives off-grid.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any, Literal, cast
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TripPlan, TripPlanItem, TripRouteDaySetting, TripRouteSegment
from app.problems import AppError
from app.trips.schedule import (
    FLIGHT_SYSTEM_ROLES,
    apply_schedule_defaults,
    clear_flight_anchor,
    ensure_system_slots,
    route_pair_count,
)

# The create path already caps a trip at 61 inclusive days; PATCH must not be a
# way around it, or ensure_system_slots writes more system rows than the 500-item
# itinerary payload can carry back.
MAX_TRIP_SPAN_DAYS = 60
MAX_SHIFT_DAYS = 3_650
MIN_TRIP_DATE = date(1970, 1, 1)
MAX_TRIP_DATE = date(2999, 12, 31)

ProtectedKind = Literal["activity", "chosen_meal", "booked_flight"]
FlightRole = Literal["outbound_flight", "return_flight"]


@dataclass(frozen=True)
class TargetRange:
    """The day grid the trip should end up on, plus how far content travels."""

    start: date
    end: date
    content_offset: int


@dataclass(frozen=True)
class ProtectedRow:
    """Traveller-made content the move would destroy: a row a shrink deletes, or a
    booked flight whose anchor is re-dated and therefore cleared."""

    item_id: UUID
    day_date: date
    kind: ProtectedKind
    title: str


@dataclass(frozen=True)
class InvalidatedFlight:
    """A booked anchor the move re-dates. The booking is tied to its calendar day, so
    apply clears it; the plan records which flight and which day so the traveller is
    told before it happens, not counted afterwards."""

    item_id: UUID
    role: FlightRole
    title: str
    flight_number: str | None
    old_day: date
    new_day: date


@dataclass(frozen=True)
class ReschedulePlan:
    new_start: date
    new_end: date
    new_days: tuple[date, ...]
    content_offset: int
    sentinel_offset: int
    removed_days: tuple[date, ...]
    removed_item_ids: tuple[UUID, ...]
    removed_day_setting_ids: tuple[UUID, ...]
    protected_rows: tuple[ProtectedRow, ...]
    flight_relocations: tuple[tuple[UUID, date], ...]
    invalidated_flight_item_ids: tuple[UUID, ...]
    invalidated_flights: tuple[InvalidatedFlight, ...] = ()


def resolve_target_range(
    *,
    old_start: date | None,
    old_end: date | None,
    shift_days: int | None,
    start_date: date | None,
    end_date: date | None,
) -> TargetRange | None:
    """Turn the request's date fields into one target grid, or ``None`` for a rename.

    ``shift_days`` moves the whole trip and keeps its length; ``start_date`` /
    ``end_date`` set an absolute range and leave every surviving row on the
    calendar day it already occupies. The two are mutually exclusive precisely
    because "start a day earlier" and "the whole trip moved back a day" are
    different intents that one date pair cannot tell apart.
    """
    if shift_days and (start_date is not None or end_date is not None):
        raise AppError(
            422,
            "trip_date_change_ambiguous",
            "請選擇整趟平移，或直接指定開始與結束日期，不能同時使用",
        )
    if shift_days:
        if old_start is None or old_end is None:
            raise AppError(422, "trip_dates_unset", "這趟旅程還沒有日期，請先指定開始與結束日期")
        try:
            new_start = old_start + timedelta(days=shift_days)
            new_end = old_end + timedelta(days=shift_days)
        except (OverflowError, ValueError) as error:
            raise AppError(422, "trip_date_out_of_bounds", "旅程日期超出可支援的範圍") from error
        offset = shift_days
    else:
        merged_start = start_date or old_start
        merged_end = end_date or old_end
        if merged_start is None or merged_end is None:
            if start_date is None and end_date is None:
                return None
            raise AppError(422, "trip_dates_required", "請同時提供開始日期與結束日期")
        new_start, new_end = merged_start, merged_end
        offset = 0
    if not MIN_TRIP_DATE <= new_start <= MAX_TRIP_DATE:
        raise AppError(422, "trip_date_out_of_bounds", "旅程日期超出可支援的範圍")
    if not MIN_TRIP_DATE <= new_end <= MAX_TRIP_DATE:
        raise AppError(422, "trip_date_out_of_bounds", "旅程日期超出可支援的範圍")
    if new_end < new_start:
        raise AppError(422, "trip_date_range_invalid", "結束日期不可早於開始日期")
    if (new_end - new_start).days > MAX_TRIP_SPAN_DAYS:
        raise AppError(
            422,
            "trip_date_range_too_long",
            f"旅程最長 {MAX_TRIP_SPAN_DAYS + 1} 天",
        )
    if (new_start, new_end, offset) == (old_start, old_end, 0):
        return None
    return TargetRange(start=new_start, end=new_end, content_offset=offset)


def day_shift_phases[K: Hashable](
    current: Mapping[K, date], content_offset: int, sentinel_offset: int
) -> list[dict[K, date]]:
    """Split a day move into passes that are safe applied one row at a time.

    Phase one parks every row in a band that no row occupies and no row will
    occupy; phase two lands them on the target. Collapsing this into a single
    pass is what makes day 2's lunch land on day 1's lunch mid-statement.
    """
    if not content_offset:
        return []
    return [
        {key: value + timedelta(days=sentinel_offset) for key, value in current.items()},
        {key: value + timedelta(days=content_offset) for key, value in current.items()},
    ]


def _sentinel_offset(occupied: Iterable[date], content_offset: int, target: TargetRange) -> int:
    days = set(occupied)
    if not days or not content_offset:
        return 0
    days |= {day + timedelta(days=content_offset) for day in days}
    days |= {target.start, target.end}
    return (max(days) - min(days)).days + 1


def _protected_kind(item: TripPlanItem) -> ProtectedKind | None:
    """What a shrink would irreversibly destroy, as opposed to regenerate."""
    if item.system_role is None:
        return "activity"
    if item.system_role in {"lunch", "dinner"}:
        return "chosen_meal" if item.data.get("meal_selection_source") == "user" else None
    if item.system_role in FLIGHT_SYSTEM_ROLES:
        return "booked_flight" if item.data.get("flight_info") else None
    # hotel_start / hotel_end are projections of trip.data["primary_lodging"].
    return None


def _flight_keeper(rows: list[TripPlanItem]) -> TripPlanItem:
    """Prefer a configured anchor over an empty one when a trip already has both."""
    booked = [row for row in rows if row.data.get("flight_info")]
    pool = booked or rows
    return min(pool, key=lambda row: (row.day_date or date.min, row.position))


def plan_reschedule(
    *,
    old_start: date | None,
    old_end: date | None,
    target: TargetRange,
    items: Sequence[TripPlanItem],
    day_settings: Sequence[TripRouteDaySetting],
) -> ReschedulePlan:
    missing_day = [item for item in items if item.day_date is None]
    if missing_day:
        # A NULL day poisons adjacent_pairs, which reads None as "no day filter"
        # and then pairs rows across day boundaries for the whole trip.
        raise AppError(
            422,
            "trip_item_day_missing",
            "旅程中有尚未指定日期的項目，請先安排它們再調整旅程日期",
        )
    offset = target.content_offset
    new_days = tuple(
        target.start + timedelta(days=index)
        for index in range((target.end - target.start).days + 1)
    )
    grid = set(new_days)

    def landing(day_value: date) -> date:
        return day_value + timedelta(days=offset)

    flight_targets: dict[str, date] = {
        "outbound_flight": target.start,
        "return_flight": target.end,
    }
    relocations: list[tuple[UUID, date]] = []
    invalidated: list[UUID] = []
    invalidated_flights: list[InvalidatedFlight] = []
    keepers: set[UUID] = set()
    surplus: set[UUID] = set()
    for role, day_target in flight_targets.items():
        anchors = [row for row in items if row.system_role == role]
        if not anchors:
            continue
        keeper = _flight_keeper(anchors)
        keepers.add(keeper.id)
        surplus.update(row.id for row in anchors if row is not keeper)
        if landing(keeper.day_date or day_target) != day_target:
            relocations.append((keeper.id, day_target))
        if keeper.day_date != day_target and keeper.data.get("flight_info"):
            # A booked flight number carries its own calendar date. Re-dating it
            # would assert a booking that does not exist, so it is cleared.
            invalidated.append(keeper.id)
            info = keeper.data.get("flight_info") or {}
            number = str(info.get("flight_number") or "").strip() or None
            invalidated_flights.append(
                InvalidatedFlight(
                    item_id=keeper.id,
                    role=cast(FlightRole, role),
                    title=keeper.title or "",
                    flight_number=number,
                    old_day=keeper.day_date or day_target,
                    new_day=day_target,
                )
            )

    removed_items: list[TripPlanItem] = []
    for item in items:
        if item.id in keepers:
            continue
        assert item.day_date is not None
        if item.id in surplus or landing(item.day_date) not in grid:
            removed_items.append(item)
    removed_days = sorted(
        {
            landing(item.day_date)
            for item in removed_items
            if item.day_date is not None and landing(item.day_date) not in grid
        }
    )
    protected = tuple(
        ProtectedRow(
            item_id=item.id,
            day_date=landing(item.day_date) if item.day_date else target.start,
            kind=kind,
            title=item.title or "",
        )
        for item in removed_items
        if (kind := _protected_kind(item)) is not None
    )
    # The kept anchor is never in removed_items, so its cleared booking would
    # otherwise be invisible to the protected list and to the confirmation gate:
    # a pure extension that re-dates the return flight destroys a hand-typed
    # booking without dropping a single day.
    protected += tuple(
        ProtectedRow(
            item_id=flight.item_id,
            day_date=flight.old_day,
            kind="booked_flight",
            title=flight.title,
        )
        for flight in invalidated_flights
    )
    removed_settings = tuple(
        setting.id for setting in day_settings if landing(setting.day_date) not in grid
    )
    occupied = {item.day_date for item in items if item.day_date is not None}
    occupied |= {setting.day_date for setting in day_settings}
    if old_start is not None:
        occupied.add(old_start)
    if old_end is not None:
        occupied.add(old_end)
    return ReschedulePlan(
        new_start=target.start,
        new_end=target.end,
        new_days=new_days,
        content_offset=offset,
        sentinel_offset=_sentinel_offset(occupied, offset, target),
        removed_days=tuple(removed_days),
        removed_item_ids=tuple(item.id for item in removed_items),
        removed_day_setting_ids=removed_settings,
        protected_rows=protected,
        flight_relocations=tuple(relocations),
        invalidated_flight_item_ids=tuple(invalidated),
        invalidated_flights=tuple(invalidated_flights),
    )


def _trip_timezone(trip: TripPlan) -> ZoneInfo:
    try:
        return ZoneInfo(trip.timezone or "UTC")
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def _shift_wall_clock(value: datetime | None, offset: int, timezone: ZoneInfo) -> datetime | None:
    """Keep the time of day the traveller entered, on the new calendar day."""
    if value is None or not offset:
        return value
    local = value.astimezone(timezone) if value.tzinfo is not None else value.replace(
        tzinfo=timezone
    )
    return datetime.combine(
        local.date() + timedelta(days=offset), local.time(), tzinfo=timezone
    )


async def apply_reschedule(
    session: AsyncSession,
    trip: TripPlan,
    *,
    items: list[TripPlanItem],
    day_settings: list[TripRouteDaySetting],
    segments: list[TripRouteSegment],
    plan: ReschedulePlan,
) -> list[TripPlanItem]:
    """Move the grid inside the caller's transaction. Returns the surviving rows.

    The caller is expected to have already won the ``trip_plans.version``
    compare-and-swap; every write below rides on that single transaction so an
    interrupted move can never leave rows off-grid.
    """
    trip.start_date = plan.new_start
    trip.end_date = plan.new_end

    # Segments are dropped wholesale: their unique key omits day_date, so a
    # day-scoped delete leaves stale rows the next recompute collides with, and
    # every departure/arrival stamp they carry is absolute.
    for record in list(segments):
        await session.delete(record)
    segments.clear()

    removed = set(plan.removed_item_ids)
    for row in [row for row in items if row.id in removed]:
        await session.delete(row)
    items[:] = [row for row in items if row.id not in removed]
    removed_settings = set(plan.removed_day_setting_ids)
    for setting in [row for row in day_settings if row.id in removed_settings]:
        await session.delete(setting)
    day_settings[:] = [row for row in day_settings if row.id not in removed_settings]
    # Land the deletes before anything moves, or a surviving row shifts onto a
    # day a doomed row still occupies.
    await session.flush()

    if plan.content_offset:
        item_days = {row.id: row.day_date for row in items if row.day_date is not None}
        by_id = {row.id: row for row in items}
        for phase in day_shift_phases(item_days, plan.content_offset, plan.sentinel_offset):
            for item_id, day_value in phase.items():
                by_id[item_id].day_date = day_value
            await session.flush()
        setting_days = {row.id: row.day_date for row in day_settings}
        settings_by_id = {row.id: row for row in day_settings}
        for phase in day_shift_phases(setting_days, plan.content_offset, plan.sentinel_offset):
            for setting_id, day_value in phase.items():
                settings_by_id[setting_id].day_date = day_value
            await session.flush()
        timezone = _trip_timezone(trip)
        for row in items:
            if row.system_role is not None:
                # apply_schedule_defaults re-derives these from the new day.
                continue
            row.start_time = _shift_wall_clock(row.start_time, plan.content_offset, timezone)
            row.end_time = _shift_wall_clock(row.end_time, plan.content_offset, timezone)

    if plan.flight_relocations:
        by_id = {row.id: row for row in items}
        for item_id, day_value in plan.flight_relocations:
            by_id[item_id].day_date = day_value
        await session.flush()

    invalidated = set(plan.invalidated_flight_item_ids)
    for row in items:
        if row.id in invalidated and row.system_role in FLIGHT_SYSTEM_ROLES:
            clear_flight_anchor(row, cast(FlightRole, row.system_role))

    ensure_system_slots(session, trip, items)
    apply_schedule_defaults(trip, items)
    return items


def ensure_shrink_confirmed(plan: ReschedulePlan, *, confirmed: bool) -> None:
    """Refuse a destructive date change the caller has not explicitly signed off on.

    Dropping a day always destroys rows — at minimum that day's system slots,
    at worst hand-picked restaurants and locked activities — with no undo. So
    does re-dating a booked flight anchor: the flight number is tied to its
    calendar day and apply clears it, which a pure extension or shift can do
    without dropping any day at all. Both need ``confirm_removed_days: true``;
    the client can show exactly what is at stake because it already holds the
    items. The error code keeps its original name for the clients that match it.
    """
    if confirmed or not (plan.removed_days or plan.invalidated_flights):
        return
    if plan.removed_days:
        protected = len(plan.protected_rows)
        raise AppError(
            422,
            "trip_shrink_confirmation_required",
            f"縮短旅程會刪除 {len(plan.removed_days)} 天的安排"
            + (f"（含 {protected} 筆自訂內容）" if protected else "")
            + "，請確認後再執行",
        )
    flights = "、".join(flight.flight_number or flight.title for flight in plan.invalidated_flights)
    raise AppError(
        422,
        "trip_shrink_confirmation_required",
        f"調整日期會清掉已填的航班訂位（{flights}），請確認後再執行",
    )


def reschedule_trip_data(data: Mapping[str, Any], rows: Sequence[TripPlanItem]) -> dict[str, Any]:
    """Rebuild the date-stamped blobs inside ``trip_plans.data`` for a new grid.

    Four blobs encode calendar dates the move just changed: the legacy
    ``itinerary`` day list (replayed verbatim if the trip ever reaches zero
    rows, and handed to share links), the ``planning`` day scope with its
    unscheduled-slot chips, the routing progress summary, and the lodging
    price snapshot whose night count was quoted for the old length. The
    lodging identity itself is user-chosen and survives.
    """
    next_data = {key: value for key, value in data.items() if key != "itinerary"}
    planning = next_data.get("planning")
    if isinstance(planning, Mapping):
        next_data["planning"] = {
            key: value
            for key, value in planning.items()
            if key not in {"day_date", "unscheduled_slots"}
        }
    lodging = next_data.get("primary_lodging")
    if isinstance(lodging, Mapping) and "price_snapshot" in lodging:
        next_data["primary_lodging"] = {
            key: value for key, value in lodging.items() if key != "price_snapshot"
        }
    total = route_pair_count(list(rows))
    next_data["edited"] = True
    # total_price was quoted for the old dates. The column stays (the header can
    # still say what the last quote was) but nothing may present it as current:
    # prices_checked flips off, the quote timestamp goes, and prices_stale is the
    # flag serialize_trip turns into price_status. A successful reoptimize rebuilds
    # the whole blob without it.
    next_data["prices_checked"] = False
    next_data.pop("reoptimized_at", None)
    next_data["prices_stale"] = True
    next_data["routing"] = {
        # "stale" rather than "queued": recomputing every leg hits the paid
        # transit providers, so a date nudge leaves the user in control of
        # when that spend happens, exactly like an itinerary edit does.
        "status": "stale" if total else "idle",
        "total": total,
        "completed": 0,
        "warnings": ["旅程日期已變更，移動時間需要重新計算。"] if total else [],
        "updated_at": datetime.now(UTC).isoformat(),
    }
    return next_data


def reschedule_summary(plan: ReschedulePlan, *, segments_cleared: int) -> dict[str, Any]:
    """What the PATCH actually destroyed, so the client can say so out loud."""
    return {
        "removed_days": [day.isoformat() for day in plan.removed_days],
        "removed_item_count": len(plan.removed_item_ids),
        "removed_protected": [
            {"kind": row.kind, "title": row.title, "day_date": row.day_date.isoformat()}
            for row in plan.protected_rows
        ],
        "invalidated_flight_anchors": len(plan.invalidated_flight_item_ids),
        "invalidated_flights": [
            {
                "role": flight.role,
                "title": flight.title,
                "flight_number": flight.flight_number,
                "from_day": flight.old_day.isoformat(),
                "to_day": flight.new_day.isoformat(),
            }
            for flight in plan.invalidated_flights
        ],
        "route_segments_cleared": segments_cleared,
    }
