from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]
EventName = Literal[
    "page_view",
    "registration_completed",
    "search_completed",
    "trip_created",
    "outbound_click",
]


class AnalyticsEventInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: UUID
    name: EventName
    occurred_at: datetime
    path: str = Field(min_length=1, max_length=512)
    locale: Locale
    referrer: str | None = Field(default=None, max_length=2048)
    utm_source: str | None = Field(default=None, max_length=100)
    utm_medium: str | None = Field(default=None, max_length=100)
    utm_campaign: str | None = Field(default=None, max_length=100)

    @field_validator("occurred_at")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("occurred_at must include a timezone")
        return value


class AnalyticsEventBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: UUID
    events: list[AnalyticsEventInput] = Field(min_length=1, max_length=20)


class AnalyticsIngestResponse(BaseModel):
    accepted: int
    duplicates: int = 0
    enabled: bool


class AnalyticsConfigResponse(BaseModel):
    first_party_enabled: bool
    ga4_enabled: bool
    ga4_measurement_id: str | None


AnalyticsRange = Literal["24h", "7d", "30d", "90d", "12m"]
