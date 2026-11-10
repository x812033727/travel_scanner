import re
from datetime import datetime
from typing import Literal, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Locale = Literal["en", "ja", "ko", "zh-TW", "zh-CN"]
# What a browser may claim. `trip_created` is still accepted and then dropped by
# ingest (see SERVER_OWNED_EVENTS): the server owns that count now, but a tab left
# open across the deploy still sends it, and rejecting the name would 422 the whole
# batch — losing that session's page views to fix a duplicate we can just ignore.
EventName = Literal[
    "page_view",
    "registration_completed",
    "search_completed",
    "trip_created",
    "outbound_click",
    "discover_requested",
    "login_resumed",
    "content_link_click",
]

_CONTENT_LOCALE = re.compile(r"^/(?:en|ja|ko|zh-TW|zh-CN)(?=/)")
_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_ARTICLE_PATH = re.compile(rf"/(?:life/{_SLUG}|guides/(?:intel|howto)/{_SLUG})")
_TOPIC_PATH = re.compile(rf"/(?:life|guides)/topics/{_SLUG}")


def content_path(value: str, *, article_only: bool = False) -> str:
    """Public canonical content routes only; never queries, tokens or external URLs."""
    path = _CONTENT_LOCALE.sub("", value)
    article = path != "/life/topics" and _ARTICLE_PATH.fullmatch(path) is not None
    topic = path == "/ai" or _TOPIC_PATH.fullmatch(path) is not None
    if len(path) > 128 or not (article or (not article_only and topic)):
        raise ValueError("expected a canonical public content path")
    return path


class ContentLinkInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    placement: Literal["related", "topic"]
    target_path: str = Field(min_length=1, max_length=140)

    @field_validator("target_path")
    @classmethod
    def public_target(cls, value: str) -> str:
        return content_path(value)

    @model_validator(mode="after")
    def target_matches_placement(self) -> Self:
        if self.placement == "related":
            content_path(self.target_path, article_only=True)
        elif self.target_path != "/ai" and _TOPIC_PATH.fullmatch(self.target_path) is None:
            raise ValueError("topic links require a topic hub")
        return self


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
    content_link: ContentLinkInput | None = None

    @model_validator(mode="after")
    def content_fields_match_event(self) -> Self:
        if self.name == "content_link_click":
            if self.content_link is None:
                raise ValueError("content_link is required for content_link_click")
            content_path(self.path, article_only=True)
        elif self.content_link is not None:
            raise ValueError("content_link is only accepted for content_link_click")
        return self

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
    content_link_click_enabled: bool = False


AnalyticsRange = Literal["24h", "7d", "30d", "90d", "12m"]
