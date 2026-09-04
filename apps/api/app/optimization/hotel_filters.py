"""Hotel preference filtering shared by the trip optimizer and the stay-area comparison.

Property type and guest capacity are hard filters. Everything else is a soft
constraint that is relaxed one at a time, in declaration order, until at least one
hotel remains, so the caller can explain exactly which preferences gave way.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from app.providers.schemas import HotelOffer
from app.search.schemas import SearchPreferences

HOTEL_RELAXATION_LABELS: dict[str, str] = {
    "breakfast": "含早餐",
    "refundable": "可免費取消",
    "station_walk": "車站步行距離",
    "review_count": "最低評論筆數",
    "review_score": "最低住客評分",
    "star_rating": "最低星級",
    "preferred_areas": "住宿區域",
    "nightly_min": "住宿每晚最低價格",
    "nightly_max": "住宿每晚最高價格",
}


@dataclass(frozen=True)
class HotelConstraint:
    code: str
    predicate: Callable[[HotelOffer], bool]

    @property
    def label(self) -> str:
        return HOTEL_RELAXATION_LABELS[self.code]


@dataclass(frozen=True)
class HotelFilterResult:
    matches: list[HotelOffer]
    relaxed: list[HotelConstraint]
    # Every soft constraint each hard-matching hotel fails, before any relaxation.
    gaps: dict[UUID, list[str]] = field(default_factory=dict)
    excluded_by_hard_filter: int = 0


def nightly_price(hotel: HotelOffer) -> Decimal:
    return hotel.nightly_price or hotel.total_price / max(1, hotel.nights)


def hotel_preference_constraints(
    preferences: SearchPreferences,
    *,
    include_area_constraint: bool = True,
    ignore_station_walk: bool = False,
) -> list[HotelConstraint]:
    """Soft constraints in relaxation order: the first one is dropped first."""
    constraints: list[HotelConstraint] = []
    if preferences.breakfast_required:
        constraints.append(HotelConstraint("breakfast", lambda item: item.breakfast_included))
    if preferences.refundable_required:
        constraints.append(HotelConstraint("refundable", lambda item: item.refundable))
    if preferences.max_station_walk_minutes is not None and not ignore_station_walk:
        max_walk: int = preferences.max_station_walk_minutes
        constraints.append(
            HotelConstraint("station_walk", lambda item: item.station_walk_minutes <= max_walk)
        )
    if preferences.hotel_min_review_count is not None:
        min_reviews: int = preferences.hotel_min_review_count
        constraints.append(
            HotelConstraint(
                "review_count",
                lambda item: item.review_count is not None and item.review_count >= min_reviews,
            )
        )
    if preferences.hotel_min_review_score is not None:
        min_score: float = preferences.hotel_min_review_score
        constraints.append(
            HotelConstraint(
                "review_score",
                lambda item: item.review_score is not None and item.review_score >= min_score,
            )
        )
    if preferences.hotel_min_rating is not None:
        min_rating: int = preferences.hotel_min_rating
        constraints.append(HotelConstraint("star_rating", lambda item: item.rating >= min_rating))
    if preferences.preferred_areas and include_area_constraint:
        areas = [area.casefold() for area in preferences.preferred_areas]
        constraints.append(
            HotelConstraint(
                "preferred_areas",
                lambda item: any(
                    area in f"{item.address or ''} {item.hotel_name}".casefold() for area in areas
                ),
            )
        )
    if preferences.hotel_min_nightly_twd is not None:
        nightly_min: int = preferences.hotel_min_nightly_twd
        constraints.append(
            HotelConstraint("nightly_min", lambda item: nightly_price(item) >= nightly_min)
        )
    if preferences.hotel_max_nightly_twd is not None:
        nightly_max: int = preferences.hotel_max_nightly_twd
        constraints.append(
            HotelConstraint("nightly_max", lambda item: nightly_price(item) <= nightly_max)
        )
    return constraints


def hotel_hard_matches(
    preferences: SearchPreferences, guests: int, hotels: list[HotelOffer]
) -> list[HotelOffer]:
    return [
        hotel
        for hotel in hotels
        if (
            not preferences.accepted_property_types
            or hotel.property_type in preferences.accepted_property_types
        )
        and (hotel.max_guests is None or hotel.max_guests >= guests)
    ]


def filter_hotels_with_relaxation(
    preferences: SearchPreferences,
    guests: int,
    hotels: list[HotelOffer],
    *,
    include_area_constraint: bool = True,
    ignore_station_walk: bool = False,
) -> HotelFilterResult:
    hard_matches = hotel_hard_matches(preferences, guests, hotels)
    constraints = hotel_preference_constraints(
        preferences,
        include_area_constraint=include_area_constraint,
        ignore_station_walk=ignore_station_walk,
    )
    gaps = {
        hotel.id: [item.code for item in constraints if not item.predicate(hotel)]
        for hotel in hard_matches
    }
    active = list(constraints)
    relaxed: list[HotelConstraint] = []
    while True:
        matches = [hotel for hotel in hard_matches if all(item.predicate(hotel) for item in active)]
        if matches or not active:
            return HotelFilterResult(
                matches=matches,
                relaxed=relaxed,
                gaps=gaps,
                excluded_by_hard_filter=len(hotels) - len(hard_matches),
            )
        relaxed.append(active.pop(0))
