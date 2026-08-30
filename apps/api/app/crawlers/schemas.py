from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AirlineCode(StrEnum):
    CHINA_AIRLINES = "CI"
    EVA_AIR = "BR"
    STARLUX = "JX"


class CabinClass(StrEnum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class AirlineFareSearch(BaseModel):
    origin: str = Field(default="TPE", min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    destination: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    departure_date: date | None = None
    return_date: date | None = None
    flex_days: int = Field(default=7, ge=0, le=30)
    cabin_class: CabinClass = CabinClass.ECONOMY
    airlines: list[AirlineCode] = Field(default_factory=lambda: list(AirlineCode), min_length=1)
    limit_per_airline: int = Field(default=10, ge=1, le=30)

    @field_validator("origin", "destination")
    @classmethod
    def uppercase_airport_code(cls, value: str) -> str:
        return value.upper()

    @field_validator("airlines")
    @classmethod
    def unique_airlines(cls, value: list[AirlineCode]) -> list[AirlineCode]:
        return list(dict.fromkeys(value))

    @model_validator(mode="after")
    def validate_dates_and_route(self) -> Self:
        if self.origin == self.destination:
            raise ValueError("origin and destination must differ")
        if self.return_date and not self.departure_date:
            raise ValueError("return_date requires departure_date")
        if self.departure_date and self.return_date and self.return_date < self.departure_date:
            raise ValueError("return_date must not be before departure_date")
        return self


class TripDateRange(BaseModel):
    departure_date: date
    return_date: date

    @model_validator(mode="after")
    def validate_date_order(self) -> Self:
        if self.return_date <= self.departure_date:
            raise ValueError("return_date must be after departure_date")
        return self


class BackToBackFareSearch(BaseModel):
    origin: str = Field(default="TPE", min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    first_destination: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    second_destination: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    first_trip: TripDateRange
    second_trip: TripDateRange
    flex_days: int = Field(default=7, ge=0, le=30)
    cabin_class: CabinClass = CabinClass.ECONOMY
    airlines: list[AirlineCode] = Field(default_factory=lambda: list(AirlineCode), min_length=1)
    limit_per_airline: int = Field(default=10, ge=1, le=30)
    strategy: "BackToBackStrategy" = Field(
        default_factory=lambda: BackToBackStrategy.NESTED_ROUND_TRIPS
    )
    head_one_way_fare: "SupplementalFareInput | None" = None
    middle_two_segment_fare: "SupplementalFareInput | None" = None
    tail_one_way_fare: "SupplementalFareInput | None" = None
    conventional_first_fare: "SupplementalFareInput | None" = None
    conventional_second_fare: "SupplementalFareInput | None" = None

    @model_validator(mode="before")
    @classmethod
    def accept_legacy_single_destination(cls, value: object) -> object:
        if not isinstance(value, dict):
            return value
        normalized = dict(value)
        legacy_destination = normalized.pop("destination", None)
        if legacy_destination is not None:
            normalized.setdefault("first_destination", legacy_destination)
            normalized.setdefault("second_destination", legacy_destination)
        return normalized

    @field_validator("origin", "first_destination", "second_destination")
    @classmethod
    def uppercase_airport_code(cls, value: str) -> str:
        return value.upper()

    @field_validator("airlines")
    @classmethod
    def unique_airlines(cls, value: list[AirlineCode]) -> list[AirlineCode]:
        return list(dict.fromkeys(value))

    @model_validator(mode="after")
    def validate_route_and_trip_order(self) -> Self:
        if self.origin in {self.first_destination, self.second_destination}:
            raise ValueError("origin and both destinations must differ")
        dates = (
            self.first_trip.departure_date,
            self.first_trip.return_date,
            self.second_trip.departure_date,
            self.second_trip.return_date,
        )
        if not all(left < right for left, right in zip(dates, dates[1:], strict=False)):
            raise ValueError(
                "dates must satisfy first departure < first return < "
                "second departure < second return"
            )
        return self


class QuoteType(StrEnum):
    CACHED_PUBLIC_FARE = "cached_public_fare"


class PublicFareQuote(BaseModel):
    id: UUID
    airline_code: AirlineCode
    airline_name: str
    origin: str
    destination: str
    departure_date: date
    return_date: date | None
    trip_type: str
    cabin_class: CabinClass
    total_price: Decimal = Field(ge=0)
    currency: str
    price_last_seen: str | None = None
    source_url: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    quote_type: QuoteType = QuoteType.CACHED_PUBLIC_FARE
    price_scope: str = "per_passenger"
    is_live: bool = False
    is_bookable: bool = False
    is_mock: bool = False
    disclaimer: str = "航空公司公開頁面的近期快取票價，可能已失效，亦可能另有稅費或附加服務費。"


class SourceState(StrEnum):
    READY = "ready"
    SUCCESS = "success"
    DISABLED = "disabled"
    BLOCKED = "blocked"
    FAILED = "failed"


class AirlineCrawlerSource(BaseModel):
    airline_code: AirlineCode
    airline_name: str
    host: str
    state: SourceState
    policy: str
    detail: str
    quote_count: int = 0
    cache_hit: bool = False


class AirlineFareSearchResponse(BaseModel):
    queried_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    quotes: list[PublicFareQuote]
    sources: list[AirlineCrawlerSource]
    warnings: list[str]


class FareTicketRole(StrEnum):
    CONVENTIONAL_FIRST = "conventional_first"
    CONVENTIONAL_SECOND = "conventional_second"
    WRAPPER = "wrapper"
    REVERSE = "reverse"


class ComparisonMode(StrEnum):
    MIXED_AIRLINES = "mixed_airlines"
    SAME_AIRLINE = "same_airline"


class ComparisonVerdict(StrEnum):
    BACK_TO_BACK_CHEAPER = "back_to_back_cheaper"
    CONVENTIONAL_CHEAPER = "conventional_cheaper"
    SAME_PRICE = "same_price"
    COMPARISON_UNAVAILABLE = "comparison_unavailable"


class BackToBackStrategy(StrEnum):
    NESTED_ROUND_TRIPS = "nested_round_trips"
    REVERSE_TWO_SEGMENT = "reverse_two_segment"


class SupplementalFareRole(StrEnum):
    CONVENTIONAL_FIRST_MANUAL = "conventional_first_manual"
    CONVENTIONAL_SECOND_MANUAL = "conventional_second_manual"
    HEAD_ONE_WAY = "head_one_way"
    MIDDLE_TWO_SEGMENT = "middle_two_segment"
    TAIL_ONE_WAY = "tail_one_way"


class SupplementalFareInput(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="TWD", min_length=3, max_length=3)
    airline_code: AirlineCode | None = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class SupplementalFareSegment(BaseModel):
    origin: str
    destination: str
    departure_date: date


class SupplementalFareComponent(BaseModel):
    role: SupplementalFareRole
    origin: str
    destination: str
    departure_date: date
    amount: Decimal = Field(gt=0)
    currency: str
    airline_code: AirlineCode | None = None
    segments: list[SupplementalFareSegment] = Field(default_factory=list, max_length=2)
    estimated_twd: Decimal | None = Field(default=None, ge=0)
    fx_rate: "FxRateSnapshot | None" = None
    source: str = "manual"
    is_live: bool = False


class BackToBackPricingCapability(StrEnum):
    FULL_BACK_TO_BACK = "full_back_to_back"
    OPEN_JAW_PROVIDER_REQUIRED = "open_jaw_provider_required"


class FxRateSnapshot(BaseModel):
    base_currency: str = Field(min_length=3, max_length=3)
    quote_currency: str = Field(default="TWD", min_length=3, max_length=3)
    rate: Decimal = Field(gt=0)
    as_of: date
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_url: str
    is_stale: bool = False


class FareTicketComponent(BaseModel):
    role: FareTicketRole
    quote: PublicFareQuote
    estimated_twd: Decimal | None = Field(default=None, ge=0)
    fx_rate: FxRateSnapshot | None = None


class FareStrategyTotal(BaseModel):
    tickets: list[FareTicketComponent] = Field(default_factory=list, max_length=2)
    supplemental_fares: list[SupplementalFareComponent] = Field(default_factory=list, max_length=3)
    original_currency_totals: dict[str, Decimal]
    estimated_twd: Decimal | None = Field(default=None, ge=0)


class BackToBackComparison(BaseModel):
    mode: ComparisonMode
    conventional: FareStrategyTotal | None = None
    back_to_back: FareStrategyTotal | None = None
    savings_twd: Decimal | None = None
    savings_percent: Decimal | None = None
    verdict: ComparisonVerdict
    detail: str


class FareCandidateSet(BaseModel):
    role: FareTicketRole
    quotes: list[PublicFareQuote]


class BackToBackFareSearchResponse(BaseModel):
    queried_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    query: BackToBackFareSearch
    pricing_capability: BackToBackPricingCapability
    comparisons: list[BackToBackComparison]
    candidates: list[FareCandidateSet]
    fx_rates: list[FxRateSnapshot]
    sources: list[AirlineCrawlerSource]
    warnings: list[str]


class AirlineCrawlerStatusResponse(BaseModel):
    sources: list[AirlineCrawlerSource]
    safety_rules: list[str]


class AirlineBrowserTarget(BaseModel):
    airline_code: AirlineCode
    airline_name: str
    host: str
    state: SourceState
    detail: str
    source_url: str | None = None


class AirlineBrowserTargetsResponse(BaseModel):
    query: AirlineFareSearch
    targets: list[AirlineBrowserTarget]


class BrowserPriceLastSeen(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str | int | float
    unit: str = Field(min_length=1, max_length=30)


class AirlineBrowserFareRow(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    origin_airport_code: str | None = Field(default=None, alias="originAirportCode", max_length=3)
    destination_airport_code: str | None = Field(
        default=None, alias="destinationAirportCode", max_length=3
    )
    departure_date: str | None = Field(default=None, alias="departureDate", max_length=10)
    return_date: str | None = Field(default=None, alias="returnDate", max_length=10)
    flight_type: str | None = Field(default=None, alias="flightType", max_length=40)
    farenet_travel_class: str | None = Field(
        default=None, alias="farenetTravelClass", max_length=50
    )
    formatted_travel_class: str | None = Field(
        default=None, alias="formattedTravelClass", max_length=50
    )
    currency_code: str | None = Field(default=None, alias="currencyCode", max_length=3)
    total_price: Decimal | None = Field(default=None, alias="totalPrice", ge=0)
    price_last_seen: BrowserPriceLastSeen | None = Field(default=None, alias="priceLastSeen")


class AirlineBrowserCapture(BaseModel):
    airline_code: AirlineCode
    query: AirlineFareSearch
    source_url: str = Field(min_length=12, max_length=2048)
    page_title: str = Field(default="", max_length=500)
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    fare_rows: list[AirlineBrowserFareRow] = Field(max_length=2_000)

    @field_validator("source_url")
    @classmethod
    def require_https_source(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("source_url must use HTTPS")
        return value

    @field_validator("captured_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("captured_at must include a timezone")
        return value


class AirlineBrowserCaptureResponse(AirlineFareSearchResponse):
    capture_sha256: str = Field(min_length=64, max_length=64)
