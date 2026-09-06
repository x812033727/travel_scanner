import re
from datetime import date
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.destinations.catalog import destination_for_code, destination_for_id


class TripType(StrEnum):
    ROUND_TRIP = "round_trip"
    ONE_WAY = "one_way"
    MULTI_CITY = "multi_city"


class FlightCabinClass(StrEnum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class SearchModule(StrEnum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    ACTIVITIES = "activities"
    TRANSPORT = "transport"


class OptimizationMode(StrEnum):
    CHEAPEST = "cheapest"
    BALANCED = "balanced"
    COMFORTABLE = "comfortable"


class TripPace(StrEnum):
    RELAXED = "relaxed"
    BALANCED = "balanced"
    PACKED = "packed"


class PropertyType(StrEnum):
    HOTEL = "hotel"
    SERVICED_APARTMENT = "serviced_apartment"
    VACATION_RENTAL = "vacation_rental"
    GUESTHOUSE = "guesthouse"
    UNKNOWN = "unknown"


class Travelers(BaseModel):
    adults: int = Field(default=1, ge=1, le=9)
    children: int = Field(default=0, ge=0, le=9)
    children_ages: list[int] = Field(default_factory=list, max_length=9)
    rooms: int = Field(default=1, ge=1, le=4)

    @model_validator(mode="after")
    def validate_children(self) -> "Travelers":
        if any(age < 0 or age > 17 for age in self.children_ages):
            raise ValueError("children ages must be between 0 and 17")
        if self.children_ages:
            if self.children not in (0, len(self.children_ages)):
                raise ValueError("children must match children_ages")
            self.children = len(self.children_ages)
        return self


class TripLeg(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination: str = Field(min_length=3, max_length=3)
    departure_date: date


_THEME_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")


class SearchPreferences(BaseModel):
    budget_twd: int | None = Field(default=None, ge=1)
    avoid_red_eye: bool = False
    hotel_min_rating: int | None = Field(default=None, ge=1, le=5)
    hotel_max_nightly_twd: int | None = Field(default=None, ge=1)
    hotel_min_nightly_twd: int | None = Field(default=None, ge=0)
    accepted_property_types: list[PropertyType] = Field(default_factory=list, max_length=5)
    hotel_min_review_score: float | None = Field(default=None, ge=0, le=10)
    hotel_min_review_count: int | None = Field(default=None, ge=0)
    breakfast_required: bool = False
    refundable_required: bool = False
    max_station_walk_minutes: int | None = Field(default=None, ge=0, le=120)
    preferred_area: str | None = Field(default=None, max_length=120)
    preferred_areas: list[str] = Field(default_factory=list, max_length=10)
    pace: TripPace = TripPace.BALANCED
    optimization_mode: OptimizationMode | None = None
    interests: list[str] = Field(default_factory=list, max_length=10)
    # Shop-type theme slugs the planner should favour (hotspot_themes, kind shop).
    # Only meaningful alongside the "shopping" interest, which the validator adds
    # when it is missing so the two cannot disagree. Seasons are not in here: they
    # come from the trip's dates, not from something the traveller ticks.
    shop_themes: list[str] = Field(default_factory=list, max_length=8)
    extension_destination_ids: list[str] = Field(default_factory=list, max_length=2)

    @model_validator(mode="after")
    def validate_hotel_price_range(self) -> "SearchPreferences":
        if (
            self.hotel_min_nightly_twd is not None
            and self.hotel_max_nightly_twd is not None
            and self.hotel_min_nightly_twd > self.hotel_max_nightly_twd
        ):
            raise ValueError("hotel minimum nightly price cannot exceed maximum")
        if self.preferred_area and not self.preferred_areas:
            self.preferred_areas = [self.preferred_area]
        cleaned: list[str] = []
        for theme in self.shop_themes:
            slug = theme.strip().casefold()
            if slug and _THEME_SLUG.fullmatch(slug) and slug not in cleaned:
                cleaned.append(slug)
        self.shop_themes = cleaned
        if cleaned and "shopping" not in self.interests:
            self.interests = [*self.interests, "shopping"][:10]
        return self


class SearchCreate(BaseModel):
    trip_type: TripType = TripType.ROUND_TRIP
    origin: str | None = Field(default=None, min_length=3, max_length=3)
    destination: str | None = Field(default=None, min_length=3, max_length=3)
    destination_region: str | None = None
    departure_date: date | None = None
    return_date: date | None = None
    legs: list[TripLeg] = Field(default_factory=list, max_length=6)
    travelers: Travelers = Field(default_factory=Travelers)
    modules: list[SearchModule] = Field(min_length=1)
    preferences: SearchPreferences = Field(default_factory=SearchPreferences)
    flexible_dates: bool = False
    flex_days: Literal[0, 3, 7] = 0
    cabin_class: FlightCabinClass = FlightCabinClass.ECONOMY
    currency: str = Field(default="TWD", min_length=3, max_length=3)
    locale: str = Field(default="zh-TW", max_length=16)
    # Search from a saved trip. The server fills the route, dates, travelers and
    # preferences from the trip (`app.trips.search_criteria`); a field given
    # here explicitly still wins, so the trip is a source of defaults, not a cage.
    trip_id: UUID | None = None

    @model_validator(mode="after")
    def validate_route(self) -> "SearchCreate":
        if self.flexible_dates and self.flex_days == 0:
            self.flex_days = 7
        if self.flex_days:
            self.flexible_dates = True
        if self.trip_type == TripType.MULTI_CITY:
            if self.trip_id is not None:
                raise ValueError("a search from a saved trip is always a round trip")
            if len(self.legs) < 2:
                raise ValueError("multi_city requires at least two legs")
            if self.flexible_dates:
                raise ValueError("multi_city does not support flexible dates")
        elif self.trip_id is None and not all((self.origin, self.destination, self.departure_date)):
            raise ValueError("origin, destination and departure_date are required")
        if (
            self.trip_type == TripType.ROUND_TRIP
            and self.return_date is None
            and self.trip_id is None
        ):
            raise ValueError("round_trip requires return_date")
        if self.return_date and self.departure_date and self.return_date <= self.departure_date:
            raise ValueError("return_date must be after departure_date")
        self.currency = self.currency.upper()
        if self.preferences.extension_destination_ids and self.departure_date and self.return_date:
            trip_days = (self.return_date - self.departure_date).days + 1
            if trip_days < 4:
                raise ValueError("跨城延伸行程至少需要四天，請延長旅程")
            allowed = 2 if trip_days >= 7 else 1
            if len(self.preferences.extension_destination_ids) > allowed:
                raise ValueError(f"目前旅程天數最多可加入 {allowed} 個跨城延伸城市")
            extension_ids = list(dict.fromkeys(self.preferences.extension_destination_ids))
            if len(extension_ids) != len(self.preferences.extension_destination_ids):
                raise ValueError("跨城延伸城市不可重複")
            parent = destination_for_code(self.destination)
            extensions = [destination_for_id(item) for item in extension_ids]
            if any(
                item is None
                or item.role != "extension"
                or parent is None
                or item.parent_destination_id != parent.id
                for item in extensions
            ):
                raise ValueError("跨城延伸城市必須屬於目前主要目的地")
        return self
