from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

Kind = Literal["hotspot", "food", "merchant", "hotel", "article", "video", "post", "itinerary"]
KINDS = ("hotspot", "food", "merchant", "hotel", "article", "video", "post", "itinerary")


class DiscoveryItem(BaseModel):
    id: str
    kind: Kind
    title: str
    summary: str
    destination: dict[str, str] | None = None
    locale: str
    href: str
    source: dict[str, str | None]
    published_at: str | None = None
    updated_at: str | None = None
    thumbnail_url: str | None = None
    collection_ref: dict[str, str]
    topics: list[str] = Field(default_factory=list)
    place_ref: dict[str, str] | None = None
    video: dict[str, Any] | None = None
    author: dict[str, Any] | None = None
    recommendation_reason: str | None = None
    content: dict[str, Any] | None = None


class PreferenceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int = Field(ge=0)
    destinations: list[str] = Field(default_factory=list, max_length=20)
    topics: list[str] = Field(default_factory=list, max_length=20)
    include_saved: bool = False
    include_following: bool = False

    @field_validator("destinations", "topics")
    @classmethod
    def normalize(cls, values: list[str], info: ValidationInfo) -> list[str]:
        import re

        result = list(dict.fromkeys(value.strip().lower() for value in values))
        if any(not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", value) for value in result):
            raise ValueError("Expected bounded destination/topic identifiers")
        if info.field_name == "destinations":
            from app.discovery.policy import destination_id

            result = list(dict.fromkeys(destination_id(value) for value in result))
        return result


class DismissInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(max_length=64)
    dismissed: bool = True
