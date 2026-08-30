from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class TripType(StrEnum):
    ROUND_TRIP = "round_trip"
    ONE_WAY = "one_way"
    MULTI_CITY = "multi_city"


class SearchModule(StrEnum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    ACTIVITIES = "activities"
    TRANSPORT = "transport"


class OptimizationMode(StrEnum):
    CHEAPEST = "cheapest"
    BALANCED = "balanced"
    COMFORTABLE = "comfortable"


class Travelers(BaseModel):
    adults: int = Field(default=1, ge=1, le=9)
    children: int = Field(default=0, ge=0, le=9)


class TripLeg(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination: str = Field(min_length=3, max_length=3)
    departure_date: date


class SearchPreferences(BaseModel):
    budget_twd: int | None = Field(default=None, ge=1)
    avoid_red_eye: bool = False
    hotel_min_rating: int | None = Field(default=None, ge=1, le=5)
    optimization_mode: OptimizationMode | None = None
    interests: list[str] = Field(default_factory=list, max_length=10)


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

    @model_validator(mode="after")
    def validate_route(self) -> "SearchCreate":
        if self.trip_type == TripType.MULTI_CITY:
            if len(self.legs) < 2:
                raise ValueError("multi_city requires at least two legs")
        elif not all((self.origin, self.destination, self.departure_date)):
            raise ValueError("origin, destination and departure_date are required")
        if self.trip_type == TripType.ROUND_TRIP and self.return_date is None:
            raise ValueError("round_trip requires return_date")
        return self
