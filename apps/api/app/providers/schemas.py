from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class FreshnessStatus(StrEnum):
    FRESH = "fresh"
    EXPIRING = "expiring"
    EXPIRED = "expired"


class NormalizedOffer(BaseModel):
    id: UUID
    provider: str
    provider_offer_id: str
    currency: str = "TWD"
    booking_url: str
    retrieved_at: datetime
    expires_at: datetime
    freshness_status: FreshnessStatus = FreshnessStatus.FRESH
    is_mock: bool = True


class FlightSegment(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    airline: str
    flight_number: str


class FlightOffer(NormalizedOffer):
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


class ActivityOffer(NormalizedOffer):
    title: str
    city: str
    latitude: float
    longitude: float
    duration_minutes: int
    price: Decimal
    rating: float
    category: str


class TransportOffer(NormalizedOffer):
    origin: str
    destination: str
    transport_type: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: Decimal
    convenience_score: float = Field(ge=0, le=100)


Offer = FlightOffer | HotelOffer | ActivityOffer | TransportOffer


class OfferRefreshResult(BaseModel):
    offer_id: UUID
    old_price: Decimal
    new_price: Decimal
    price_change: Decimal
    still_available: bool
    refreshed_at: datetime
