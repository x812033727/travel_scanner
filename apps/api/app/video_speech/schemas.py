from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SpeechPartIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=1500)
    # The spoken form of a dictionary term, e.g. "L L M" for "LLM"; becomes <sub alias>.
    alias: str | None = Field(default=None, min_length=1, max_length=200)


class SpeechSegmentIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    parts: list[SpeechPartIn] = Field(min_length=1, max_length=200)
    break_after_ms: int = Field(default=0, ge=0, le=5000)


class SpeechRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    voice: str = Field(min_length=3, max_length=80)
    rate: str = Field(default="+0%", pattern=r"^[+-]\d{1,2}%$")
    segments: list[SpeechSegmentIn] = Field(min_length=1, max_length=200)


class SpeechStatus(BaseModel):
    configured: bool
    region: str | None
    voices: list[str]
    output_format: str
    max_request_characters: int
    monthly_limit: int
    used: int | None
    remaining: int | None


class VideoToolTokenCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=80)


class VideoToolTokenView(BaseModel):
    id: UUID
    name: str
    token_prefix: str
    created_at: datetime
    last_used_at: datetime | None
    revoked_at: datetime | None


class VideoToolTokenCreated(VideoToolTokenView):
    # Shown once. Only its SHA-256 is kept.
    token: str
