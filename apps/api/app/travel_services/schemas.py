from __future__ import annotations

import ipaddress
import re
from datetime import date, datetime
from typing import Annotated, Literal, Self
from urllib.parse import parse_qsl, urlsplit, urlunsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.affiliates.schemas import AffiliateChannel, AffiliateModule
from app.destinations.catalog import DESTINATIONS
from app.i18n import Locale

Kind = Literal["hotel", "transfer", "tour", "esim"]
Status = Literal["pending", "approved", "disabled"]
KINDS: tuple[Kind, ...] = ("hotel", "transfer", "tour", "esim")
# Osaka and Kyoto remain distinct even though the existing search gateway is shared.
CITIES = {
    "tokyo": ("JP", "NRT", (35.6812, 139.7671), ("NRT", "HND")),
    "osaka": ("JP", "KIX", (34.6937, 135.5023), ("KIX", "ITM")),
    "kyoto": ("JP", "KIX", (35.0116, 135.7681), ("KIX", "ITM")),
    "seoul": ("KR", "ICN", (37.5665, 126.9780), ("ICN", "GMP")),
    "busan": ("KR", "PUS", (35.1796, 129.0756), ("PUS",)),
    "taipei": ("TW", "TPE", (25.0330, 121.5654), ("TPE", "TSA")),
}
PUBLIC_DESTINATION_IDS = frozenset(destination.id for destination in DESTINATIONS)
SERVICE_DESTINATION_IDS = PUBLIC_DESTINATION_IDS | frozenset(CITIES)


def safe_url(value: str) -> str:
    if len(value) > 2048 or any(ord(c) < 33 for c in value) or "\\" in value:
        raise ValueError("Invalid HTTPS URL")
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host or parsed.username or parsed.password:
        raise ValueError("HTTPS URL required")
    if (
        parsed.port not in (None, 443)
        or "." not in host
        or host.endswith((".local", ".internal", ".localhost"))
    ):
        raise ValueError("Public HTTPS host required")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("Literal IP targets are forbidden")
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host):
        raise ValueError("Invalid host")
    return urlunsplit(("https", host, parsed.path or "/", parsed.query, ""))


def untracked_url(value: str) -> str:
    value = safe_url(value)
    if {k.lower() for k, _ in parse_qsl(urlsplit(value).query)} & {
        "marker",
        "trs",
        "aid",
        "cid",
        "aff",
        "affiliate_id",
        "aff_id",
        "sub_id",
        "tag",
        "sid",
        "clickid",
        "irclickid",
        "utm_source",
    }:
        raise ValueError("Supply an original non-affiliate product URL")
    return value


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


HotelProvider = Literal[
    "official", "booking", "trip_com", "agoda", "expedia", "rakuten", "klook", "kkday"
]
HOTEL_PROVIDERS = (
    "official",
    "booking",
    "trip_com",
    "agoda",
    "expedia",
    "rakuten",
    "klook",
    "kkday",
)


class HotelLink(StrictModel):
    provider: HotelProvider
    url: str
    evidence_url: str

    @field_validator("url", "evidence_url")
    @classmethod
    def urls(cls, value: str) -> str:
        return untracked_url(value)

    @model_validator(mode="after")
    def identity(self) -> Self:
        from app.travel_services.registry import BRANDS, affiliate_target, brand_target

        host = urlsplit(self.url).hostname or ""
        # Ordinary links must not conceal a redirect or another affiliate's tracking.
        if any(
            key.lower().startswith("utm_")
            or key.lower()
            in {
                "url",
                "redirect",
                "redirect_url",
                "redirect_uri",
                "next",
                "ref",
                "refid",
                "affiliate",
                "affid",
                "partner_id",
            }
            for key, _ in parse_qsl(urlsplit(self.url).query)
        ):
            raise ValueError("Original hotel page required")
        if self.provider == "official":
            evidence_host = urlsplit(self.evidence_url).hostname or ""
            if host.removeprefix("www.") != evidence_host.removeprefix("www."):
                raise ValueError("Official website evidence must belong to the same host")
            if any(host == h or host.endswith("." + h) for b in BRANDS.values() for h in b.hosts):
                raise ValueError("A booking platform is not the hotel's official website")
            if host == "tpx.gr" or host.endswith(".tpx.gr"):
                raise ValueError("Affiliate links are not ordinary hotel links")
            try:
                affiliate_target(self.url)
            except ValueError:
                pass
            else:
                raise ValueError("Affiliate links are not ordinary hotel links")
        else:
            brand_target(self.provider, self.url)
            path = urlsplit(self.url).path.lower()
            if path == "/" or re.search(
                r"(?:^|/)(?:search(?:results)?(?:\.html)?|hotel-search|hotels-list|searchresult)(?:/|$)",
                path,
            ):
                raise ValueError("An exact hotel page, not a platform homepage, is required")
        return self


class SourceCredit(StrictModel):
    title: str = Field(min_length=1, max_length=255)
    publisher: str = Field(min_length=1, max_length=255)
    url: str
    license_name: str = Field(min_length=1, max_length=128)
    license_url: str
    changes: str = Field(min_length=1, max_length=1000)

    @field_validator("url", "license_url")
    @classmethod
    def urls(cls, value: str) -> str:
        return safe_url(value)


class HotelOptionInput(StrictModel):
    provider: HotelProvider
    url: str | None = None
    property_id: str | None = Field(None, min_length=1, max_length=255)
    evidence_url: str | None = None
    identity_note: str = Field(default="", max_length=1000)
    discovery_status: Literal["found", "not_found", "unconfirmed"] = "found"

    @field_validator("evidence_url")
    @classmethod
    def evidence(cls, value: str | None) -> str | None:
        return safe_url(value) if value else None

    @model_validator(mode="after")
    def link(self) -> Self:
        if self.discovery_status == "found":
            if not self.url or not self.evidence_url:
                raise ValueError("Exact hotel URL and identity evidence required")
            validated = HotelLink(
                provider=self.provider, url=self.url, evidence_url=self.evidence_url
            )
            self.url, self.evidence_url = validated.url, validated.evidence_url
        elif self.url or self.property_id:
            raise ValueError("Unconfirmed discovery cannot assert a hotel identity")
        return self


class HotelOptionEdit(HotelOptionInput):
    version: int = Field(ge=0)


class HotelOptionReview(StrictModel):
    version: int = Field(ge=1)
    status: Status
    browser_verified: bool = False
    identity_note: str = Field(default="", max_length=1000)


class HotelBookingContext(StrictModel):
    """Optional user-selected stay, independent of live rate-search constraints.

    Historical dates may be serialized for editing. The clickout boundary must
    additionally call validate_booking_context before forwarding any dates.
    """

    check_in: date | None = None
    check_out: date | None = None
    adults: int | None = Field(default=None, strict=True, ge=1, le=9)
    children: int | None = Field(default=None, strict=True, ge=0, le=9)
    rooms: int | None = Field(default=None, strict=True, ge=1, le=4)
    children_ages: list[Annotated[int, Field(strict=True, ge=0, le=17)]] = Field(
        default_factory=list, max_length=9
    )

    @field_validator("check_in", "check_out", mode="before")
    @classmethod
    def calendar_date(cls, value: object) -> object:
        if value is None or (isinstance(value, date) and not isinstance(value, datetime)):
            return value
        if isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            return value
        raise ValueError("Calendar date in YYYY-MM-DD format required")

    @model_validator(mode="after")
    def stay(self) -> Self:
        from app.search.schemas import Travelers

        if (self.check_in is None) != (self.check_out is None):
            raise ValueError("Both check-in and check-out dates are required")
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValueError("Check-out must be after check-in")
        if self.children_ages and self.children is not None:
            if len(self.children_ages) != self.children:
                raise ValueError("Children must match children ages")
        # Reuse the search domain's traveler policy without injecting its defaults
        # into the optional context sent to an external booking platform.
        Travelers.model_validate(
            self.model_dump(
                include={"adults", "children", "rooms", "children_ages"}, exclude_none=True
            )
        )
        return self


Stay22Provider = Literal["booking", "agoda", "expedia"]
STAY22_PROVIDERS: tuple[Stay22Provider, ...] = ("booking", "agoda", "expedia")


class Stay22Config(StrictModel):
    enabled: bool = Field(default=False, strict=True)
    aid: str = Field(default="mokaair", pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
    enabled_providers: list[Stay22Provider] = Field(default_factory=list, max_length=3)
    integration_mode: Literal["allez", "script"] = "allez"
    lma_id: str | None = Field(default=None, pattern=r"^[a-f0-9]{24}$")

    @field_validator("enabled_providers")
    @classmethod
    def providers(cls, value: list[Stay22Provider]) -> list[Stay22Provider]:
        if len(set(value)) != len(value):
            raise ValueError("Only one entry per Stay22 provider")
        return [provider for provider in STAY22_PROVIDERS if provider in value]

    @model_validator(mode="after")
    def script_identity(self) -> Self:
        if self.enabled and self.integration_mode == "script" and not self.lma_id:
            raise ValueError("An enabled Stay22 script requires its public LMA ID")
        return self


class Facts(StrictModel):
    source_credits: list[SourceCredit] = Field(default_factory=list, max_length=10)
    hotel_links: list[HotelLink] = Field(default_factory=list, max_length=8)
    country_codes: list[str] = Field(default_factory=list, max_length=50)
    area_code: str | None = Field(None, max_length=64)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    coordinate_source_url: str | None = None
    google_place_id: str | None = Field(None, pattern=r"^[A-Za-z0-9_-]{5,255}$")
    naver_map_url: str | None = None
    map_verified: bool = False
    facilities: list[Literal["wifi", "breakfast", "accessible", "family", "laundry"]] = Field(
        default_factory=list
    )
    airport: str | None = Field(None, pattern=r"^[A-Z]{3}$")
    direction: Literal["arrival", "departure", "roundtrip"] | None = None
    passengers: int | None = Field(None, ge=1, le=100)
    luggage: int | None = Field(None, ge=0, le=100)
    languages: list[Locale] = Field(default_factory=list)
    attraction_ids: list[UUID] = Field(default_factory=list, max_length=30)
    meeting_point: str | None = Field(None, max_length=255)
    duration_minutes: int | None = Field(None, ge=15, le=1440)
    available_start: str | None = Field(None, pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    available_end: str | None = Field(None, pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    validity_days: int | None = Field(None, ge=1, le=365)
    data_gb: float | None = Field(None, gt=0, le=10000)
    unlimited: bool | None = None
    tethering: bool | None = None
    reference_price: float | None = Field(None, ge=0, le=1000000)
    currency: str | None = Field(None, pattern=r"^[A-Z]{3}$")
    price_checked_at: datetime | None = None

    @field_validator("country_codes")
    @classmethod
    def countries(cls, values: list[str]) -> list[str]:
        if any(not re.fullmatch(r"[A-Z]{2}", value) for value in values):
            raise ValueError("ISO country codes required")
        return sorted(set(values))

    @field_validator("coordinate_source_url", "naver_map_url")
    @classmethod
    def urls(cls, value: str | None) -> str | None:
        return safe_url(value) if value else None

    @model_validator(mode="after")
    def paired(self) -> Self:
        if len({link.provider for link in self.hotel_links}) != len(self.hotel_links):
            raise ValueError("Only one verified hotel link per provider")
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("Coordinates must be paired")
        if self.price_checked_at and self.price_checked_at.tzinfo is None:
            raise ValueError("Timezone required")
        if (self.available_start is None) != (self.available_end is None):
            raise ValueError("Both availability window bounds required")
        return self


class ProductInput(StrictModel):
    source_key: str = Field(min_length=1, max_length=255)
    kind: Kind
    destination_id: str
    title: str = Field(min_length=1, max_length=255)
    names_json: dict[Locale, str] = Field(default_factory=dict)
    source_url: str
    facts: Facts = Field(default_factory=Facts)

    @model_validator(mode="after")
    def hotel_only(self) -> Self:
        if self.kind != "hotel" and self.facts.hotel_links:
            raise ValueError("Ordinary booking links are only supported for hotels")
        return self

    @field_validator("source_url")
    @classmethod
    def source(cls, value: str) -> str:
        return safe_url(value)

    @field_validator("destination_id")
    @classmethod
    def city(cls, value: str) -> str:
        if value not in CITIES:
            raise ValueError("Unsupported destination")
        return value

    @field_validator("names_json")
    @classmethod
    def names(cls, value: dict[Locale, str]) -> dict[Locale, str]:
        if any(not name.strip() or len(name) > 255 for name in value.values()):
            raise ValueError("Invalid localized name")
        return value


class OfferInput(StrictModel):
    product_id: UUID
    brand_id: UUID
    target_url: str
    static_url: str | None = None
    scope: Literal["product", "destination"] = "product"
    expires_at: datetime | None = None

    @field_validator("target_url")
    @classmethod
    def target(cls, value: str) -> str:
        return untracked_url(value)

    @field_validator("static_url")
    @classmethod
    def static(cls, value: str | None) -> str | None:
        return safe_url(value) if value else None

    @field_validator("expires_at")
    @classmethod
    def aware(cls, value: datetime | None) -> datetime | None:
        if value and value.tzinfo is None:
            raise ValueError("Timezone required")
        return value


class DestinationOfferInput(StrictModel):
    brand_id: UUID
    destination_id: str
    module: AffiliateModule
    target_url: str
    static_url: str | None = None
    expires_at: datetime | None = None

    @field_validator("destination_id")
    @classmethod
    def destination(cls, value: str) -> str:
        from app.destinations.catalog import destination_for_id

        normalized = value.casefold()
        if not destination_for_id(normalized):
            raise ValueError("Unsupported destination")
        return normalized

    @field_validator("target_url")
    @classmethod
    def target(cls, value: str) -> str:
        return untracked_url(value)

    @field_validator("static_url")
    @classmethod
    def static(cls, value: str | None) -> str | None:
        return safe_url(value) if value else None

    @field_validator("expires_at")
    @classmethod
    def aware(cls, value: datetime | None) -> datetime | None:
        if value and value.tzinfo is None:
            raise ValueError("Timezone required")
        return value


class DestinationOfferVersion(StrictModel):
    id: UUID
    version: int = Field(ge=1)


class DestinationOfferBatchReview(StrictModel):
    offers: list[DestinationOfferVersion] = Field(min_length=1, max_length=50)
    status: Status


class ReviewInput(StrictModel):
    version: int = Field(ge=1)
    status: Status
    browser_verified: bool = False
    evidence_url: str | None = None

    @field_validator("evidence_url")
    @classmethod
    def evidence(cls, value: str | None) -> str | None:
        return safe_url(value) if value else None

    @model_validator(mode="after")
    def attestation(self) -> Self:
        if self.browser_verified and not self.evidence_url:
            raise ValueError("Browser verification requires exact destination evidence")
        return self


class BrandInput(StrictModel):
    channel: AffiliateChannel = "travelpayouts"
    code: str
    approval: Literal["unknown", "pending", "approved", "rejected"]
    enabled: bool = False
    evidence_url: str
    version: int | None = Field(None, ge=1)

    @field_validator("evidence_url")
    @classmethod
    def evidence(cls, value: str) -> str:
        return safe_url(value)

    @model_validator(mode="after")
    def enrollment(self) -> Self:
        if self.channel == "klook_direct":
            if (
                self.code != "klook"
                or urlsplit(self.evidence_url).hostname != "affiliate.klook.com"
            ):
                raise ValueError("Official Klook enrollment evidence required")
        elif urlsplit(self.evidence_url).hostname != "app.travelpayouts.com":
            raise ValueError("Travelpayouts project evidence required")
        return self


class HotelQuotePolicy(StrictModel):
    enabled: bool = False
    comparison_allowed: bool = False
    terms_url: str | None = None
    daily_limit: int = Field(default=0, ge=0, le=100000)
    per_minute_limit: int = Field(default=10, ge=1, le=1000)
    timeout_seconds: int = Field(default=8, ge=1, le=20)
    cache_seconds: int = Field(default=0, ge=0, le=3600)

    @field_validator("terms_url")
    @classmethod
    def terms(cls, value: str | None) -> str | None:
        return safe_url(value) if value else None

    @model_validator(mode="after")
    def authorized(self) -> Self:
        if self.enabled and (
            not self.comparison_allowed or not self.terms_url or not self.daily_limit
        ):
            raise ValueError("Explicit comparison rights and budget required")
        # Persistent caching is deliberately not implemented until a provider's rules are reviewed.
        if self.cache_seconds:
            raise ValueError("Price caching is not enabled in this release")
        return self


class CatalogConfig(StrictModel):
    stay22: Stay22Config = Field(default_factory=Stay22Config)
    hotel_quote_policies: dict[HotelProvider, HotelQuotePolicy] = Field(default_factory=dict)
    public_enabled: bool = False
    direct_hotel_links_enabled: bool = False
    enabled_kinds: list[Kind] = Field(default_factory=list)
    enabled_destinations: list[str] = Field(default_factory=list)
    airalo_feed_enabled: bool = False

    @field_validator("enabled_destinations")
    @classmethod
    def destinations(cls, value: list[str]) -> list[str]:
        if any(city not in SERVICE_DESTINATION_IDS for city in value):
            raise ValueError("Unsupported destination")
        return list(dict.fromkeys(value))


class ConfigInput(CatalogConfig):
    version: int = Field(ge=0)


class HotelConfigPatch(StrictModel):
    version: int = Field(ge=0)
    hotel_enabled: bool | None = None
    direct_hotel_links_enabled: bool | None = None
    hotel_quote_policies: dict[HotelProvider, HotelQuotePolicy] | None = None
    stay22: Stay22Config | None = None

    @model_validator(mode="after")
    def nonempty(self) -> Self:
        fields = self.model_fields_set - {"version"}
        if not fields or any(getattr(self, field) is None for field in fields):
            raise ValueError("At least one non-null hotel setting is required")
        return self


class SelectInput(StrictModel):
    product_id: UUID
    version: int = Field(ge=1)
    day_date: date | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    airport: str | None = Field(None, pattern=r"^[A-Z]{3}$")
    direction: Literal["arrival", "departure", "roundtrip"] | None = None
    passengers: int | None = Field(None, ge=1, le=100)
    flight_number: str | None = Field(None, pattern=r"^[A-Z0-9]{2,3}[0-9]{1,4}[A-Z]?$")

    @model_validator(mode="after")
    def time_pair(self) -> Self:
        if (self.start_time is None) != (self.end_time is None):
            raise ValueError("Both times required")
        if self.start_time and self.end_time:
            if not self.start_time.tzinfo or not self.end_time.tzinfo:
                raise ValueError("Timezone required")
            if not self.day_date or self.end_time <= self.start_time:
                raise ValueError("Invalid schedule")
        return self


class SelectionStatus(StrictModel):
    version: int = Field(ge=1)
    status: Literal["planned", "booked", "cancelled"]


class CsvInput(StrictModel):
    csv: str = Field(min_length=1, max_length=500000)
