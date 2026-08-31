from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.search.schemas import PropertyType


class FreshnessStatus(StrEnum):
    FRESH = "fresh"
    EXPIRING = "expiring"
    EXPIRED = "expired"


class SourceMode(StrEnum):
    LIVE = "live"
    TEST = "test"
    MOCK = "mock"
    ESTIMATE = "estimate"


class ActionKind(StrEnum):
    DEEP_LINK = "deep_link"
    RECHECK = "recheck"
    NONE = "none"


class NormalizedOffer(BaseModel):
    id: UUID
    provider: str
    provider_offer_id: str
    currency: str = "TWD"
    booking_url: str | None = None
    retrieved_at: datetime
    expires_at: datetime
    freshness_status: FreshnessStatus = FreshnessStatus.FRESH
    source_mode: SourceMode = SourceMode.MOCK
    is_mock: bool = True
    is_fallback: bool = False
    is_bookable: bool = False
    action_kind: ActionKind = ActionKind.NONE
    images: list[str] = Field(default_factory=list)
    attributions: list[str] = Field(default_factory=list)
    attribution_urls: list[str] = Field(default_factory=list)
    cancellation_policy: str | None = None


class FlightSegment(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    airline: str
    flight_number: str
    leg_index: int = Field(default=0, ge=0)
    departure_timezone: str | None = None
    arrival_timezone: str | None = None


class FlightDateOption(BaseModel):
    shift_days: int
    departure_date: date
    return_date: date | None = None
    lowest_price: Decimal
    currency: str = "TWD"
    provider: str
    source_mode: SourceMode
    is_current: bool = False
    offer_count: int = 1


class FlightOffer(NormalizedOffer):
    itinerary_key: str | None = None
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    segments: list[FlightSegment]
    airline: str
    flight_number: str
    cabin_class: str = "economy"
    base_price: Decimal
    taxes: Decimal
    fees: Decimal
    baggage_price: Decimal
    total_price: Decimal
    carry_on: bool
    checked_baggage_kg: int
    refundable: bool
    changeable: bool
    return_departure_time: datetime | None = None
    return_arrival_time: datetime | None = None
    stops: int = 0
    marketing_airline: str | None = None
    operating_airlines: list[str] = Field(default_factory=list)
    selling_agent: str | None = None
    fare_brand: str | None = None
    baggage_summary: str | None = None
    last_verified_at: datetime | None = None
    clickout_available: bool = False
    arrival_day_offset: int = 0
    original_currency: str | None = None
    original_total_price: Decimal | None = None
    exchange_rate: Decimal | None = None
    exchange_rate_retrieved_at: datetime | None = None
    verification_method: str | None = None
    emissions_kg_per_pax: Decimal | None = None
    emissions_cabin: str | None = None
    emissions_source: str | None = None
    emissions_model_version: str | None = None
    emissions_retrieved_at: datetime | None = None
    status_details: list[dict[str, Any]] = Field(default_factory=list)


class HotelOffer(NormalizedOffer):
    hotel_id: str
    hotel_name: str
    latitude: float
    longitude: float
    rating: float
    room_type: str
    check_in: datetime
    check_out: datetime
    nights: int
    base_price: Decimal
    taxes: Decimal
    fees: Decimal
    total_price: Decimal
    breakfast_included: bool
    refundable: bool
    station_walk_minutes: int
    nightly_price: Decimal | None = None
    address: str | None = None
    amenities: list[str] = Field(default_factory=list)
    review_score: float | None = None
    review_count: int | None = None
    distance_to_center_km: float | None = None
    property_type: PropertyType = PropertyType.HOTEL
    max_guests: int | None = None


class ActivityOffer(NormalizedOffer):
    title: str
    city: str
    latitude: float
    longitude: float
    duration_minutes: int
    price: Decimal
    rating: float
    category: str
    description: str | None = None
    address: str | None = None
    opening_hours: list[str] = Field(default_factory=list)


class TransportOffer(NormalizedOffer):
    origin: str
    destination: str
    transport_type: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: Decimal
    convenience_score: float = Field(ge=0, le=100)
    is_estimated: bool = False


Offer = FlightOffer | HotelOffer | ActivityOffer | TransportOffer


class OfferRefreshResult(BaseModel):
    offer_id: UUID
    old_price: Decimal
    new_price: Decimal
    price_change: Decimal
    still_available: bool
    refreshed_at: datetime
    offer: FlightOffer | None = None
