"""Search criteria derived from a saved trip.

`POST /searches` with a `trip_id` and the trip page's 「查機票」 entry need the
same answer to "what would this trip search for?": the home airport, the
catalog gateway of the destination, the trip dates, its travelers and its
preferences. A trip saved from a search still has the original request; a
blank trip carries the same keys in `data`. Whatever the trip cannot answer is
reported as an issue with a code the UI can act on (ask for the airport, send
the member to fix the dates) rather than guessed: a wrong airport is a paid
search for the wrong flights.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, cast
from uuid import UUID

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_code, match_destination
from app.i18n import ERROR_DETAILS, GENERIC_DETAILS, Locale
from app.models import SearchRequest, TripPlan
from app.problems import AppError
from app.search.schemas import (
    FlightCabinClass,
    SearchCreate,
    SearchModule,
    SearchPreferences,
    Travelers,
    TripType,
)
from app.trips.stay_areas import trip_timezone

# Airports a member can fly out from today; the planning workbench offers the same three.
ORIGIN_OPTIONS: tuple[str, ...] = ("TPE", "TSA", "KHH")

# Fields a client may pin on a search from a trip. Everything else is the trip's
# to answer: `modules` and `locale` are passed separately, and a multi-city
# `legs` list has no meaning for a round trip built from one destination.
TRIP_SEARCH_OVERRIDES: frozenset[str] = frozenset(
    {
        "origin",
        "destination",
        "destination_region",
        "departure_date",
        "return_date",
        "travelers",
        "preferences",
        "flexible_dates",
        "flex_days",
        "cabin_class",
        "currency",
    }
)


@dataclass(frozen=True)
class TripSearchIssue:
    code: str
    detail: str


@dataclass
class TripSearchDerivation:
    """The criteria a trip yields, plus every reason they are not searchable yet."""

    fields: dict[str, Any]
    issues: list[TripSearchIssue] = field(default_factory=list)

    @property
    def ready(self) -> bool:
        return not self.issues


async def load_owned_trip(session: AsyncSession, user_id: UUID, trip_id: UUID) -> TripPlan:
    trip = await session.scalar(
        select(TripPlan).where(TripPlan.id == trip_id, TripPlan.user_id == user_id)
    )
    if trip is None:
        raise AppError(404, "trip_not_found", "找不到這個已儲存旅程")
    return trip


async def load_trip_search_json(session: AsyncSession, trip: TripPlan) -> dict[str, Any] | None:
    """The request a search-sourced trip was saved from; None for a blank trip."""
    if trip.search_id is None:
        return None
    search = await session.get(SearchRequest, trip.search_id)
    if search is None or not isinstance(search.request_json, dict):
        return None
    return search.request_json


def _base_search(search_json: dict[str, Any] | None) -> SearchCreate | None:
    if not search_json:
        return None
    try:
        return SearchCreate.model_validate(search_json)
    except ValueError:
        # An old request the schema no longer accepts; fall back to the trip's own keys.
        return None


def _airport_code(value: Any) -> str | None:
    code = str(value or "").strip().upper()
    return code if len(code) == 3 and code.isalpha() else None


def trip_origin_airport(trip: TripPlan, base: SearchCreate | None) -> str | None:
    return _airport_code(trip.data.get("origin_airport")) or (
        _airport_code(base.origin) if base else None
    )


def trip_destination_airport(trip: TripPlan, base: SearchCreate | None) -> str | None:
    """The airport a flight search for this trip lands at, or None when unknown.

    A trip saved from a search keeps the airport that search used. A blank trip
    only has a place name, which is resolved through the destination catalog;
    a name the catalog does not know is not turned into a guess.
    """
    if base is not None:
        code = _airport_code(base.destination)
        if code and destination_for_code(code) is not None:
            return code
    for candidate in (trip.destination_name, trip.data.get("destination_city")):
        if isinstance(candidate, str) and candidate.strip():
            profile = match_destination(candidate)
            if profile is not None:
                return profile.primary_gateway
    return None


def derive_trip_search(
    trip: TripPlan,
    search_json: dict[str, Any] | None,
    *,
    modules: list[SearchModule],
    locale: str,
    today: date | None = None,
) -> TripSearchDerivation:
    base = _base_search(search_json)
    origin = trip_origin_airport(trip, base)
    destination = trip_destination_airport(trip, base)
    if base is not None:
        travelers, preferences, cabin_class = base.travelers, base.preferences, base.cabin_class
    else:
        travelers = Travelers.model_validate(cast(dict[str, Any], trip.data.get("travelers") or {}))
        preferences = SearchPreferences.model_validate(
            cast(dict[str, Any], trip.data.get("preferences") or {})
        )
        cabin_class = FlightCabinClass.ECONOMY
    # Extension cities are a planning choice, not a flight route, and their
    # trip-length rule would reject a short trip that is otherwise searchable.
    preferences = preferences.model_copy(update={"extension_destination_ids": []})

    issues: list[TripSearchIssue] = []
    if origin is None:
        issues.append(
            TripSearchIssue("trip_origin_required", "這趟旅程還沒有出發機場，請先選擇出發地")
        )
    if destination is None:
        issues.append(
            TripSearchIssue(
                "trip_destination_unsupported",
                "這趟旅程的目的地不在目前的機票搜尋範圍，請自行選擇抵達機場",
            )
        )
    if trip.start_date is None or trip.end_date is None:
        issues.append(TripSearchIssue("trip_dates_required", "請先設定旅程日期，才能查機票"))
    else:
        current = today or datetime.now(trip_timezone(trip)).date()
        if trip.start_date < current:
            issues.append(
                TripSearchIssue("trip_dates_past", "旅程的出發日已經過了，請先調整旅程日期")
            )
        elif trip.end_date <= trip.start_date:
            issues.append(
                TripSearchIssue(
                    "trip_dates_too_short", "來回機票需要至少兩天的旅程日期，請先調整旅程日期"
                )
            )
    fields: dict[str, Any] = {
        "trip_type": TripType.ROUND_TRIP.value,
        "origin": origin,
        "destination": destination,
        "departure_date": trip.start_date.isoformat() if trip.start_date else None,
        "return_date": trip.end_date.isoformat() if trip.end_date else None,
        "travelers": travelers.model_dump(mode="json"),
        "preferences": preferences.model_dump(mode="json"),
        "modules": [module.value for module in modules],
        "flexible_dates": False,
        "flex_days": 0,
        "cabin_class": cabin_class.value,
        "currency": "TWD",
        "locale": locale,
        "trip_id": str(trip.id),
    }
    return TripSearchDerivation(fields, issues)


def trip_search_criteria(
    trip: TripPlan,
    search_json: dict[str, Any] | None,
    *,
    modules: list[SearchModule],
    locale: str,
    overrides: dict[str, Any] | None = None,
    today: date | None = None,
) -> SearchCreate:
    """The full search a trip stands for, or a 422 naming the first thing missing.

    `overrides` are fields the client pinned explicitly; a pinned origin,
    destination or pair of dates settles the matching issue instead of the trip.
    """
    derivation = derive_trip_search(trip, search_json, modules=modules, locale=locale, today=today)
    explicit = {key: value for key, value in (overrides or {}).items() if value is not None}
    settled: set[str] = set()
    if explicit.get("origin"):
        settled.add("trip_origin_required")
    if explicit.get("destination"):
        settled.add("trip_destination_unsupported")
    pinned_dates = (explicit.get("departure_date"), explicit.get("return_date"))
    if trip.start_date is None or trip.end_date is None:
        if all(pinned_dates):
            settled.update({"trip_dates_required", "trip_dates_past", "trip_dates_too_short"})
    else:
        trip_dates = (trip.start_date.isoformat(), trip.end_date.isoformat())
        # A page that read the trip minutes ago can pin dates the trip no longer has.
        # Searching them would spend a use on flights for the wrong week, and every
        # result would then be refused by the anchors' own date check. Each pinned date
        # is compared on its own: half a stale pair is still the wrong week.
        if any(
            pinned is not None and str(pinned) != current
            for pinned, current in zip(pinned_dates, trip_dates, strict=True)
        ):
            raise AppError(
                422,
                "trip_dates_mismatch",
                f"這次搜尋的日期 {pinned_dates[0] or trip_dates[0]} 至 "
                f"{pinned_dates[1] or trip_dates[1]} 與旅程目前的 "
                f"{trip_dates[0]} 至 {trip_dates[1]} 不同，請重新載入旅程條件",
            )
    remaining = [issue for issue in derivation.issues if issue.code not in settled]
    if remaining:
        raise AppError(422, remaining[0].code, remaining[0].detail)
    try:
        return SearchCreate.model_validate({**derivation.fields, **explicit})
    except ValidationError as exc:
        # Same 422 shape the request body would have produced on its own.
        raise RequestValidationError(exc.errors()) from exc


def localized_issue_detail(issue: TripSearchIssue, locale: Locale) -> str:
    """Same wording the problem handler would use for this code in this locale."""
    if locale == "zh-TW":
        return issue.detail
    return ERROR_DETAILS[locale].get(issue.code, GENERIC_DETAILS[locale])
