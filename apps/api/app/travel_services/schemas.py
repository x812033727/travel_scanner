from __future__ import annotations

import ipaddress
import re
from datetime import date, datetime
from typing import Literal, Self
from urllib.parse import parse_qsl, urlsplit, urlunsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

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


class Facts(StrictModel):
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


class ReviewInput(StrictModel):
    version: int = Field(ge=1)
    status: Status


class BrandInput(StrictModel):
    code: str
    approval: Literal["unknown", "pending", "approved", "rejected"]
    enabled: bool = False
    evidence_url: str
    version: int | None = Field(None, ge=1)

    @field_validator("evidence_url")
    @classmethod
    def evidence(cls, value: str) -> str:
        value = safe_url(value)
        if urlsplit(value).hostname != "app.travelpayouts.com":
            raise ValueError("Travelpayouts project evidence required")
        return value


class CatalogConfig(StrictModel):
    public_enabled: bool = False
    enabled_kinds: list[Kind] = Field(default_factory=list)
    enabled_destinations: list[str] = Field(default_factory=list)
    airalo_feed_enabled: bool = False

    @field_validator("enabled_destinations")
    @classmethod
    def destinations(cls, value: list[str]) -> list[str]:
        if any(city not in CITIES for city in value):
            raise ValueError("Unsupported destination")
        return list(dict.fromkeys(value))


class ConfigInput(CatalogConfig):
    version: int = Field(ge=0)


class SelectInput(StrictModel):
    product_id: UUID
    version: int = Field(ge=1)
    day_date: date | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    airport: str | None = Field(None, pattern=r"^[A-Z]{3}$")
    direction: Literal["arrival", "departure", "roundtrip"] | None = None
    passengers: int | None = Field(None, ge=1, le=100)

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
