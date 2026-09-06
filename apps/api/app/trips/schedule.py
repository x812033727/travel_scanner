from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, Literal, cast
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy.ext.asyncio import AsyncSession

from app.localized_names import item_names
from app.models import TripPlan, TripPlanItem
from app.providers.schemas import HotelOffer

# Titles of a meal card that has no restaurant yet, per site locale.
MEAL_PLACEHOLDER_LABELS: dict[str, dict[str, str]] = {
    "lunch": {
        "zh-TW": "午餐尚未安排",
        "zh-CN": "午餐尚未安排",
        "en": "Lunch not planned yet",
        "ja": "昼食は未定",
        "ko": "점심 식사 미정",
    },
    "dinner": {
        "zh-TW": "晚餐尚未安排",
        "zh-CN": "晚餐尚未安排",
        "en": "Dinner not planned yet",
        "ja": "夕食は未定",
        "ko": "저녁 식사 미정",
    },
}

SystemRole = Literal[
    "outbound_flight",
    "hotel_start",
    "lunch",
    "dinner",
    "hotel_end",
    "return_flight",
]
DailySystemRole = Literal["hotel_start", "lunch", "dinner", "hotel_end"]
FlightSystemRole = Literal["outbound_flight", "return_flight"]
DAILY_SYSTEM_ROLES: tuple[DailySystemRole, ...] = (
    "hotel_start",
    "lunch",
    "dinner",
    "hotel_end",
)
FLIGHT_SYSTEM_ROLES = frozenset({"outbound_flight", "return_flight"})
SYSTEM_ROLES: tuple[SystemRole, ...] = (
    "outbound_flight",
    *DAILY_SYSTEM_ROLES,
    "return_flight",
)
LOGISTICS_ITEM_TYPES = frozenset({"flight", "transport", "hotel"})
DEFAULT_SCHEDULE: dict[str, Any] = {
    "day_start_time": "09:00",
    "lunch_time": "12:00",
    "lunch_duration_minutes": 60,
    "dinner_time": "18:30",
    "dinner_duration_minutes": 90,
}


def schedule_defaults(trip: TripPlan) -> dict[str, Any]:
    raw = cast(dict[str, Any], trip.data.get("schedule_defaults") or {})
    return {**DEFAULT_SCHEDULE, **raw}


def primary_lodging(trip: TripPlan, rows: list[TripPlanItem]) -> dict[str, Any] | None:
    configured = trip.data.get("primary_lodging")
    if isinstance(configured, dict) and configured.get("name"):
        return cast(dict[str, Any], configured)
    hotel = next(
        (
            row
            for row in rows
            if row.item_type == "hotel"
            and row.system_role is None
            and (row.location_name or row.title)
        ),
        None,
    )
    if hotel is None:
        return None
    title = (hotel.title or hotel.location_name or "主要飯店").removeprefix("入住 ")
    if title.startswith("從 ") and title.endswith(" 退房"):
        title = title[2:-3]
    return {
        "name": title,
        "location_name": hotel.location_name or title,
        "provider_place_id": hotel.provider_place_id,
        "latitude": float(hotel.latitude) if hotel.latitude is not None else None,
        "longitude": float(hotel.longitude) if hotel.longitude is not None else None,
        "location_source": hotel.location_source,
        "offer_id": str(hotel.offer_id) if hotel.offer_id else None,
    }


USER_LODGING_KEPT_WARNING = "已保留你選擇的主要飯店，本次重新查價未更換住宿。"


def merge_reoptimized_lodging(
    current: dict[str, Any] | None, hotel: HotelOffer | None
) -> tuple[dict[str, Any] | None, str | None]:
    """Keep a lodging the member chose themselves; otherwise adopt the repriced hotel."""
    if hotel is None:
        return current, None
    if current and current.get("selection_source") == "user":
        return current, USER_LODGING_KEPT_WARNING
    return (
        {
            "name": hotel.hotel_name,
            "location_name": hotel.address or hotel.hotel_name,
            "provider_place_id": None,
            "latitude": hotel.latitude,
            "longitude": hotel.longitude,
            "location_source": "provider",
            "offer_id": str(hotel.id),
            "selection_source": "reoptimize",
        },
        None,
    )


def is_logistics_item(item: TripPlanItem) -> bool:
    return item.system_role is None and (
        item.item_type in LOGISTICS_ITEM_TYPES
        or item.data.get("timeline_section") == "logistics"
    )


def is_active_route_item(item: TripPlanItem) -> bool:
    location_ready = (
        getattr(item, "latitude", None) is not None
        and getattr(item, "longitude", None) is not None
    )
    return (
        not item.is_skipped
        and item.system_role not in FLIGHT_SYSTEM_ROLES
        and not is_logistics_item(item)
        and (
            item.system_role not in {"hotel_start", "hotel_end", "lunch", "dinner"}
            or location_ready
        )
    )


def active_route_rows(
    rows: list[TripPlanItem], day_value: date | None = None
) -> list[TripPlanItem]:
    selected = [
        item
        for item in rows
        if is_active_route_item(item)
        and (day_value is None or item.day_date == day_value)
    ]
    return sorted(selected, key=lambda item: (item.day_date or date.min, item.position))


def route_pair_count(rows: list[TripPlanItem]) -> int:
    days = {item.day_date for item in rows if item.day_date is not None}
    return sum(max(0, len(active_route_rows(rows, day_value)) - 1) for day_value in days)


def _timezone(trip: TripPlan) -> ZoneInfo:
    try:
        return ZoneInfo(trip.timezone or "UTC")
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def _local_at(day_value: date, value: str, timezone: ZoneInfo) -> datetime:
    hour, minute = (int(part) for part in value.split(":"))
    return datetime.combine(day_value, time(hour, minute), tzinfo=timezone)


def _days(trip: TripPlan, rows: list[TripPlanItem]) -> list[date]:
    if trip.start_date and trip.end_date:
        return [
            trip.start_date + timedelta(days=offset)
            for offset in range((trip.end_date - trip.start_date).days + 1)
        ]
    return sorted({item.day_date for item in rows if item.day_date is not None})


def clear_flight_anchor(item: TripPlanItem, role: FlightSystemRole) -> None:
    """Reset a flight anchor to the unset state, keeping the row and its slot.

    Used both by the flight-anchor endpoint and by a date change: a booked
    flight number carries its own calendar date, so re-dating it would assert a
    booking that does not exist.
    """
    label = "去程" if role == "outbound_flight" else "回程"
    item.item_type = "flight"
    item.locked = True
    item.fixed_time = True
    item.is_skipped = False
    item.offer_id = None
    item.start_time = None
    item.end_time = None
    item.duration_minutes = None
    item.latitude = None
    item.longitude = None
    item.provider_place_id = None
    item.location_source = None
    item.is_estimated = True
    item.title = f"{label}航班尚未設定"
    item.location_name = None
    # An unset anchor has no quote either; the snapshot belonged to the offer that is gone.
    item.data = {
        **{key: value for key, value in item.data.items() if key != "price_snapshot"},
        "source_mode": "system",
        "timeline_section": "flight_anchor",
        "flight_selection_source": "unset",
        "flight_info": None,
    }


# Slot ids are random, never uuid5(trip, day, role). A day-derived id survives a
# date shift naming the day it used to sit on, so pulling the range back over
# that day made this function mint a row whose primary key another row already
# held - an IntegrityError raised from ensure_system_slots, which runs on every
# read through hydrate_legacy_items, i.e. a permanent 500 on GET /trips/{id}.
# uq_trip_plan_item_system_role already guarantees one row per (trip, day, role).
def _new_slot(
    trip: TripPlan,
    day_value: date,
    role: SystemRole,
    lodging: dict[str, Any] | None,
) -> TripPlanItem:
    defaults = schedule_defaults(trip)
    timezone = _timezone(trip)
    if role in {"hotel_start", "hotel_end"}:
        name = str((lodging or {}).get("name") or "尚未設定飯店")
        lodging_ready = bool(
            lodging
            and lodging.get("latitude") is not None
            and lodging.get("longitude") is not None
        )
        starts = (
            _local_at(day_value, str(defaults["day_start_time"]), timezone)
            if role == "hotel_start"
            else None
        )
        return TripPlanItem(
            id=uuid4(),
            trip_plan_id=trip.id,
            item_type="hotel_anchor",
            day_date=day_value,
            position=0,
            title=f"從 {name} 出發" if role == "hotel_start" else f"返回 {name}",
            location_name=(lodging or {}).get("location_name"),
            start_time=starts,
            end_time=starts,
            latitude=(
                Decimal(str(lodging["latitude"]))
                if lodging and lodging.get("latitude") is not None
                else None
            ),
            longitude=(
                Decimal(str(lodging["longitude"]))
                if lodging and lodging.get("longitude") is not None
                else None
            ),
            locked=True,
            fixed_time=role == "hotel_start",
            is_estimated=not lodging_ready,
            data={
                "source_mode": "system",
                "needs_place_confirmation": not lodging_ready,
            },
            provider_place_id=(lodging or {}).get("provider_place_id"),
            location_source=(lodging or {}).get("location_source"),
            duration_minutes=0,
            system_role=role,
            is_skipped=False,
        )
    is_lunch = role == "lunch"
    start_key = "lunch_time" if is_lunch else "dinner_time"
    duration_key = "lunch_duration_minutes" if is_lunch else "dinner_duration_minutes"
    starts = _local_at(day_value, str(defaults[start_key]), timezone)
    duration = int(defaults[duration_key])
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip.id,
        item_type="meal",
        day_date=day_value,
        position=0,
        title=MEAL_PLACEHOLDER_LABELS[role]["zh-TW"],
        location_name=None,
        names_json=item_names(title=MEAL_PLACEHOLDER_LABELS[role]),
        start_time=starts,
        end_time=starts + timedelta(minutes=duration),
        locked=True,
        fixed_time=True,
        is_estimated=True,
        data={
            "source_mode": "system",
            "meal_kind": role,
            "meal_selection_source": "unset",
            "needs_place_confirmation": True,
        },
        duration_minutes=duration,
        system_role=role,
        is_skipped=False,
    )


def _new_flight_slot(
    trip: TripPlan, day_value: date, role: FlightSystemRole
) -> TripPlanItem:
    label = "去程" if role == "outbound_flight" else "回程"
    return TripPlanItem(
        id=uuid4(),
        trip_plan_id=trip.id,
        item_type="flight",
        day_date=day_value,
        position=0,
        title=f"{label}航班尚未設定",
        locked=True,
        fixed_time=True,
        is_estimated=True,
        data={
            "source_mode": "system",
            "timeline_section": "flight_anchor",
            "flight_selection_source": "unset",
            "flight_info": None,
        },
        system_role=role,
        is_skipped=False,
    )


def _promote_legacy_flights(
    trip: TripPlan, rows: list[TripPlanItem], days: list[date]
) -> bool:
    if not days:
        return False
    changed = False
    assigned = {
        item.system_role
        for item in rows
        if item.system_role in FLIGHT_SYSTEM_ROLES
    }
    candidates = [
        item
        for item in rows
        if item.item_type == "flight"
        and item.system_role is None
        and item.day_date in {days[0], days[-1]}
    ]
    candidates.sort(key=lambda item: (item.day_date or date.min, item.position))

    def is_return(item: TripPlanItem) -> bool:
        marker = str(item.data.get("flight_leg") or "").casefold()
        title = (item.title or "").casefold()
        return marker in {"return", "inbound"} or "返回" in title or "回程" in title

    outbound = next(
        (item for item in candidates if item.day_date == days[0] and not is_return(item)),
        None,
    )
    returning = next(
        (item for item in reversed(candidates) if item.day_date == days[-1] and is_return(item)),
        None,
    )
    if returning is None:
        returning = next(
            (
                item
                for item in reversed(candidates)
                if item.day_date == days[-1] and item is not outbound
            ),
            None,
        )
    for role, item in (("outbound_flight", outbound), ("return_flight", returning)):
        if role in assigned or item is None:
            continue
        item.system_role = role
        item.locked = True
        item.fixed_time = True
        item.is_skipped = False
        item.data = {
            **item.data,
            "timeline_section": "flight_anchor",
            "flight_selection_source": item.data.get("flight_selection_source", "provider"),
        }
        assigned.add(role)
        changed = True
    return changed


def _sync_lodging(item: TripPlanItem, lodging: dict[str, Any] | None) -> bool:
    if item.system_role not in {"hotel_start", "hotel_end"}:
        return False
    name = str((lodging or {}).get("name") or "尚未設定飯店")
    lodging_ready = bool(
        lodging
        and lodging.get("latitude") is not None
        and lodging.get("longitude") is not None
    )
    values = {
        "title": (
            f"從 {name} 出發" if item.system_role == "hotel_start" else f"返回 {name}"
        ),
        "location_name": (lodging or {}).get("location_name"),
        "provider_place_id": (lodging or {}).get("provider_place_id"),
        "location_source": (lodging or {}).get("location_source"),
        "latitude": (
            Decimal(str(lodging["latitude"]))
            if lodging and lodging.get("latitude") is not None
            else None
        ),
        "longitude": (
            Decimal(str(lodging["longitude"]))
            if lodging and lodging.get("longitude") is not None
            else None
        ),
        "is_estimated": not lodging_ready,
    }
    changed = any(getattr(item, key) != value for key, value in values.items())
    for key, value in values.items():
        setattr(item, key, value)
    item.data = {
        **item.data,
        "source_mode": "system",
        "needs_place_confirmation": not lodging_ready,
    }
    return changed


def canonicalize_positions(rows: list[TripPlanItem]) -> bool:
    changed = False
    for day_value in sorted({item.day_date for item in rows if item.day_date is not None}):
        day_rows = [item for item in rows if item.day_date == day_value]
        outbound = [item for item in day_rows if item.system_role == "outbound_flight"]
        returning = [item for item in day_rows if item.system_role == "return_flight"]
        route_rows = [
            item
            for item in day_rows
            if not is_logistics_item(item)
            and item.system_role not in FLIGHT_SYSTEM_ROLES
        ]
        logistics = [item for item in day_rows if is_logistics_item(item)]

        def route_key(item: TripPlanItem) -> tuple[int, datetime, int]:
            if item.system_role == "hotel_start":
                rank = 0
            elif item.system_role == "hotel_end":
                rank = 2
            else:
                rank = 1
            return (
                rank,
                item.start_time or datetime.max.replace(tzinfo=UTC),
                item.position,
            )

        ordered = [
            *outbound,
            *sorted(route_rows, key=route_key),
            *returning,
            *sorted(logistics, key=lambda row: row.position),
        ]
        for position, item in enumerate(ordered):
            if item.position != position:
                item.position = position
                changed = True
    return changed


def ensure_system_slots(
    session: AsyncSession, trip: TripPlan, rows: list[TripPlanItem]
) -> bool:
    changed = False
    lodging = primary_lodging(trip, rows)
    if lodging and trip.data.get("primary_lodging") != lodging:
        trip.data = {**trip.data, "primary_lodging": lodging}
        changed = True
    if "schedule_defaults" not in trip.data:
        trip.data = {**trip.data, "schedule_defaults": schedule_defaults(trip)}
        changed = True
    days = _days(trip, rows)
    changed = _promote_legacy_flights(trip, rows, days) or changed
    by_role = {
        (item.day_date, cast(SystemRole, item.system_role)): item
        for item in rows
        if item.day_date is not None and item.system_role in SYSTEM_ROLES
    }
    for day_index, day_value in enumerate(days):
        roles: list[SystemRole] = []
        if day_index == 0:
            roles.append("outbound_flight")
        roles.extend(DAILY_SYSTEM_ROLES)
        if day_index == len(days) - 1:
            roles.append("return_flight")
        for role in roles:
            item = by_role.get((day_value, role))
            if item is None:
                item = (
                    _new_flight_slot(trip, day_value, cast(FlightSystemRole, role))
                    if role in FLIGHT_SYSTEM_ROLES
                    else _new_slot(trip, day_value, cast(DailySystemRole, role), lodging)
                )
                session.add(item)
                rows.append(item)
                changed = True
            elif role in {"hotel_start", "hotel_end"}:
                changed = _sync_lodging(item, lodging) or changed
    return canonicalize_positions(rows) or changed


def apply_schedule_defaults(trip: TripPlan, rows: list[TripPlanItem]) -> None:
    defaults = schedule_defaults(trip)
    timezone = _timezone(trip)
    for item in rows:
        if item.day_date is None or item.system_role not in {"hotel_start", "lunch", "dinner"}:
            continue
        if item.system_role == "hotel_start":
            starts = _local_at(item.day_date, str(defaults["day_start_time"]), timezone)
            item.start_time = starts
            item.end_time = starts
            item.duration_minutes = 0
            continue
        is_lunch = item.system_role == "lunch"
        starts = _local_at(
            item.day_date,
            str(defaults["lunch_time" if is_lunch else "dinner_time"]),
            timezone,
        )
        duration = int(
            defaults[
                "lunch_duration_minutes" if is_lunch else "dinner_duration_minutes"
            ]
        )
        item.start_time = starts
        item.end_time = starts + timedelta(minutes=duration)
        item.duration_minutes = duration
    canonicalize_positions(rows)


def sync_primary_lodging(
    trip: TripPlan, rows: list[TripPlanItem], lodging: dict[str, Any]
) -> None:
    trip.data = {**trip.data, "primary_lodging": lodging}
    for item in rows:
        _sync_lodging(item, lodging)
