"""Put a catalog place on a trip day: append a stop, or fill the day's meal card.

Four endpoints add places to trips — ``POST /hotspots/{id}/trip-selections``,
``/restaurants/{place_id}/trip-selections``, ``/foods/{id}/trip-selections`` and
``/foods/merchants/{id}/trip-selections`` — and they used to disagree about what
"add" meant: the hotspot one appended a stop after the day's last position, the
other three wrote the day's lunch or dinner card and could not append at all. Each
router still knows how to describe its own kind of place (a :class:`SelectionPlace`);
what happens to the trip lives here once, so the four answer the same request shape
and fail the same way.

``mode`` chooses the placement:

- ``append`` (the default): a new ordinary row after the day's last position; the
  meal cards are untouched.
- ``replace_meal``: the day's system card whose ``system_role`` is ``meal`` (``lunch``
  or ``dinner``) takes the place. The card keeps its role, its position and its
  time — the same rule ``update_itinerary`` enforces when a lunch or dinner card
  gets a new catalog place: only those two system cards may change place, and no
  row is added for it.

A meal card the traveller already chose a place for (``meal_selection_source ==
"user"``) is *occupied*: ``replace_meal`` answers ``409 meal_slot_occupied`` unless
the request says ``overwrite: true``. Placeholder cards (``unset``) and planner
suggestions (``ai``) are filled without asking, which is the line the rest of the
trip code draws too — ``replan`` rewrites every meal that is not the traveller's,
and ``reschedule`` protects only the traveller's as ``chosen_meal``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal, Self
from uuid import UUID

from pydantic import BaseModel, Field, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.service import record_event
from app.models import TripPlan, TripPlanItem
from app.problems import AppError
from app.trips.replan import MEAL_LOCATION_DATA_KEYS
from app.trips.router import (
    hydrate_legacy_items,
    load_items,
    owned_trip,
    persist_system_schedule_change,
)

TripSelectionMode = Literal["append", "replace_meal"]
MealRole = Literal["lunch", "dinner"]

# ``data`` keys that say *which place* a row points at, across everything the four
# selections and the planner write. A new place replaces all of them, so a lunch card
# filled from a dish and later from a hotspot does not keep the dish's merchant id.
# Schedule keys (``meal_kind``, ``source_mode``) and the traveller's notes stay.
SELECTION_DATA_KEYS: frozenset[str] = MEAL_LOCATION_DATA_KEYS | frozenset(
    {
        "coordinate_source_type",
        "coordinate_source_url",
        "hotspot_id",
        "hotspot_slug",
        "meal_selection_kind",
        "merchant_area_id",
        "merchant_map_links",
        "opening_hours",
        "restaurant_editorial_source",
        "restaurant_maps_url",
        "restaurant_place_id",
        "selection_source",
    }
)


class TripSelectionRequest(BaseModel):
    """The body the four ``trip-selections`` endpoints share.

    ``mode`` defaults to ``append``. ``replace_meal`` needs ``meal``, and ``meal`` is
    only accepted with ``replace_meal``: a client that names a meal and gets a stop
    appended instead would recreate the very bug this contract exists to close.
    ``overwrite`` only matters for ``replace_meal`` (see :func:`meal_slot_occupied`).

    ``meal_role`` is what the first clients sent to the restaurant and food endpoints,
    which only ever wrote a meal card. It still means ``mode: replace_meal`` with that
    meal, so those clients keep working; it may not contradict ``mode`` or ``meal``.
    """

    trip_id: UUID
    version: int = Field(ge=1)
    day_date: date
    mode: TripSelectionMode | None = None
    meal: MealRole | None = None
    meal_role: MealRole | None = None
    overwrite: bool = False

    @model_validator(mode="after")
    def _resolve_placement(self) -> Self:
        if self.meal_role is not None:
            if self.mode == "append":
                raise ValueError("meal_role means mode replace_meal; it cannot go with append")
            if self.meal is not None and self.meal != self.meal_role:
                raise ValueError("meal and meal_role name different meals")
            self.mode = "replace_meal"
            self.meal = self.meal_role
        if self.mode is None:
            self.mode = "append"
        if self.mode == "replace_meal" and self.meal is None:
            raise ValueError("mode replace_meal needs meal: lunch or dinner")
        if self.mode == "append" and self.meal is not None:
            raise ValueError("meal only applies to mode replace_meal")
        return self


@dataclass(frozen=True, slots=True)
class SelectionPlace:
    """One catalog place in the shape a trip row stores it.

    ``item_type`` and ``duration_minutes`` only matter for an appended row; a meal
    card keeps its own type and duration. ``data`` carries the catalog's own keys
    (ids, map links, opening hours); the placement adds the meal bookkeeping itself.
    """

    title: str
    location_name: str | None
    names_json: dict[str, Any]
    latitude: Decimal | None
    longitude: Decimal | None
    provider_place_id: str | None
    location_source: str | None
    data: dict[str, Any] = field(default_factory=dict)
    coordinate_source_type: str | None = None
    coordinate_source_url: str | None = None
    coordinate_verified_at: datetime | None = None
    is_estimated: bool = False
    item_type: str = "activity"
    duration_minutes: int | None = None


def meal_slot_occupied(card: TripPlanItem) -> bool:
    """True when the traveller already chose this meal card's place themselves."""
    return card.data.get("meal_selection_source") == "user"


def find_meal_card(rows: list[TripPlanItem], day_date: date, meal: str) -> TripPlanItem | None:
    return next(
        (row for row in rows if row.day_date == day_date and row.system_role == meal),
        None,
    )


def _append_stop(
    trip: TripPlan, rows: list[TripPlanItem], day_date: date, place: SelectionPlace
) -> TripPlanItem:
    position = max((row.position for row in rows if row.day_date == day_date), default=-1) + 1
    return TripPlanItem(
        trip_plan_id=trip.id,
        item_type=place.item_type,
        day_date=day_date,
        position=position,
        title=place.title,
        location_name=place.location_name,
        names_json=dict(place.names_json),
        latitude=place.latitude,
        longitude=place.longitude,
        coordinate_source_type=place.coordinate_source_type,
        coordinate_source_url=place.coordinate_source_url,
        coordinate_verified_at=place.coordinate_verified_at,
        provider_place_id=place.provider_place_id,
        location_source=place.location_source,
        duration_minutes=place.duration_minutes,
        is_estimated=place.is_estimated,
        data=dict(place.data),
    )


def _fill_meal_card(
    rows: list[TripPlanItem], request: TripSelectionRequest, place: SelectionPlace
) -> TripPlanItem:
    assert request.meal is not None  # the request validator guarantees it
    card = find_meal_card(rows, request.day_date, request.meal)
    if card is None:
        raise AppError(422, "trip_meal_slot_unavailable", "這一天沒有可設定的餐食卡")
    if meal_slot_occupied(card) and not request.overwrite:
        raise AppError(
            409,
            "meal_slot_occupied",
            "這一餐已經有你選的店家；要換成這個地點，請在確認後帶 overwrite 重送",
        )
    # Everything about *when* stays — system_role, position, start and end time,
    # duration, fixed_time, locked — and so do the traveller's notes. Only *where*
    # changes, which is the same set of fields update_itinerary lets a lunch or dinner
    # card take from a catalog selection.
    card.title = place.title
    card.location_name = place.location_name
    card.names_json = dict(place.names_json)
    card.latitude = place.latitude
    card.longitude = place.longitude
    card.coordinate_source_type = place.coordinate_source_type
    card.coordinate_source_url = place.coordinate_source_url
    card.coordinate_verified_at = place.coordinate_verified_at
    card.provider_place_id = place.provider_place_id
    card.location_source = place.location_source
    card.is_estimated = place.is_estimated
    card.is_skipped = False
    kept = {key: value for key, value in card.data.items() if key not in SELECTION_DATA_KEYS}
    card.data = {
        **kept,
        **place.data,
        "meal_kind": card.system_role,
        "meal_selection_source": "user",
        "needs_place_confirmation": False,
    }
    return card


async def place_trip_selection(
    session: AsyncSession,
    user_id: UUID,
    *,
    request: TripSelectionRequest,
    place: SelectionPlace,
    warning: str,
    event_path: str,
    event_properties: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply ``request`` to the traveller's trip and return the re-serialized trip.

    Raises ``404 trip_not_found``, ``422 itinerary_date_out_of_range``,
    ``422 trip_meal_slot_unavailable`` (no such card that day, which only a trip
    without dates can produce), ``409 meal_slot_occupied`` and, from the persist step,
    ``409 trip_version_conflict``. ``event_properties`` is what the endpoint knows
    about the place (its kind); the placement adds ``mode`` and, for a meal, ``slot``.
    """

    trip = await owned_trip(session, user_id, request.trip_id)
    if (
        trip.start_date is None
        or trip.end_date is None
        or not trip.start_date <= request.day_date <= trip.end_date
    ):
        raise AppError(422, "itinerary_date_out_of_range", "行程項目日期超出旅程範圍")
    rows = await hydrate_legacy_items(session, trip, await load_items(session, trip.id))
    if request.mode == "replace_meal":
        _fill_meal_card(rows, request, place)
    else:
        stop = _append_stop(trip, rows, request.day_date, place)
        session.add(stop)
        rows.append(stop)
    # The exploring surfaces used to end in a toast; this is the count that says
    # whether browsing them turns into a trip at all.
    await record_event(
        session,
        "place_added_to_trip",
        path=event_path,
        user_id=user_id,
        properties={
            **event_properties,
            "mode": request.mode,
            **({"slot": request.meal} if request.mode == "replace_meal" else {}),
        },
    )
    return await persist_system_schedule_change(
        session,
        trip,
        user_id,
        request.version,
        rows,
        warning=warning,
        target_day=request.day_date,
    )
