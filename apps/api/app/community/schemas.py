from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from app.auth.schemas import Locale


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class CommunitySettings(Input):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, strict=True)
    enabled: bool = False
    posting_enabled: bool = True
    comments_enabled: bool = True
    messaging_enabled: bool = True
    translation_enabled: bool = False
    pet_reports_enabled: bool = True
    uploads_per_day: int = Field(default=50, ge=1, le=500)
    posts_per_day: int = Field(default=10, ge=1, le=100)
    interactions_per_minute: int = Field(default=30, ge=1, le=200)
    translation_characters_per_month: int = Field(default=100_000, ge=0, le=100_000_000)
    pet_verification_days: int = Field(default=180, ge=1, le=365)
    risk_terms: list[str] = Field(default_factory=list, max_length=100)

    @field_validator("risk_terms")
    @classmethod
    def valid_terms(cls, value: list[str]) -> list[str]:
        if any(not item.strip() or len(item) > 100 for item in value):
            raise ValueError("invalid risk term")
        return list(dict.fromkeys(item.strip().casefold() for item in value))


class SettingsUpdate(Input):
    settings: CommunitySettings
    reason: str = Field(min_length=3, max_length=1000)


class ProfileInput(Input):
    handle: str = Field(pattern=r"^[a-z][a-z0-9_]{2,29}$")
    display_name: str = Field(min_length=1, max_length=80)
    bio: str = Field(default="", max_length=1000)
    languages: list[Locale] = Field(default_factory=list, max_length=5)
    destinations: list[str] = Field(default_factory=list, max_length=10)
    avatar_id: UUID | None = None

    @field_validator("handle")
    @classmethod
    def reserved_handles(cls, value: str) -> str:
        if value.startswith("deleted_") or value in {
            "admin",
            "support",
            "mokaair",
            "api",
            "system",
            "deleted",
            "me",
        }:
            raise ValueError("reserved handle")
        return value


class PostInput(Input):
    version: int | None = Field(default=None, ge=1)
    title: str = Field(default="", max_length=160)
    body: str = Field(default="", max_length=20_000)
    locale: Locale = "zh-TW"
    destination: str = Field(default="", max_length=160)
    kind: Literal["story", "guide", "pet_visit"] = "story"
    topics: list[str] = Field(default_factory=list, max_length=8)
    place_ids: list[UUID] = Field(default_factory=list, max_length=20)
    media_ids: list[UUID] = Field(default_factory=list, max_length=10)
    # None deliberately removes the public itinerary on save. The editor includes
    # a saved snapshot unless the author explicitly selects another source trip.
    source_trip_id: UUID | None = None
    keep_itinerary: bool = False
    allow_fork: bool = False

    @field_validator("topics")
    @classmethod
    def bounded_topics(cls, value: list[str]) -> list[str]:
        if any(not topic.strip() or len(topic) > 40 for topic in value):
            raise ValueError("invalid topic")
        return list(dict.fromkeys(value))


class VersionInput(Input):
    version: int = Field(ge=1)


class CommentInput(Input):
    body: str = Field(min_length=1, max_length=2000)
    locale: Locale = "zh-TW"
    parent_id: UUID | None = None


class CollectionInput(Input):
    name: str = Field(min_length=1, max_length=80)


class CollectionItemInput(Input):
    kind: Literal["post", "pet_place", "hotspot", "merchant", "restaurant", "food"]
    target: str = Field(min_length=1, max_length=160)


class ForkInput(Input):
    start_date: date
    idempotency_key: str = Field(min_length=8, max_length=100)


class MessageInput(Input):
    body: str = Field(default="", max_length=2000)
    card_post_id: UUID | None = None
    idempotency_key: str = Field(min_length=8, max_length=100)

    @model_validator(mode="after")
    def has_content(self) -> MessageInput:
        if not self.body and self.card_post_id is None:
            raise ValueError("message has no content")
        return self


class ReadInput(Input):
    through_id: int = Field(ge=0)


class NotificationPreferences(Input):
    follow: bool = True
    like: bool = True
    comment: bool = True
    reply: bool = True
    mention: bool = True
    message: bool = True
    review: bool = True


class ReportInput(Input):
    kind: Literal["post", "comment", "profile", "message"]
    target: str = Field(min_length=1, max_length=120)
    reason: str = Field(min_length=3, max_length=2000)
    message_ids: list[int] = Field(default_factory=list, max_length=5)


class ModerationInput(Input):
    action: Literal["approve", "return", "hide", "restore", "feature", "unfeature"]
    reason: str = Field(min_length=3, max_length=1000)
    version: int = Field(ge=1)


class ReasonInput(Input):
    reason: str = Field(min_length=3, max_length=1000)


class RestrictionInput(ReasonInput):
    restricted: bool


class ReviewCommentInput(ReasonInput):
    hidden: bool


class ResolveReportInput(ReasonInput):
    status: Literal["resolved", "dismissed"]


class UploadInput(Input):
    content_type: Literal["image/jpeg", "image/png", "image/webp"]
    size: int = Field(gt=0, le=10 * 1024 * 1024)
    alt: str = Field(default="", max_length=300)


class TranslateInput(Input):
    kind: Literal["post", "comment"]
    target_id: UUID
    locale: Locale


class EmailRequest(Input):
    email: EmailStr
    locale: Locale = "zh-TW"


class TokenInput(Input):
    token: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")


class ResetInput(TokenInput):
    password: str = Field(min_length=10, max_length=128)


class DeleteAccountInput(Input):
    token: str = Field(min_length=32, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    confirmation: Literal["DELETE"]
