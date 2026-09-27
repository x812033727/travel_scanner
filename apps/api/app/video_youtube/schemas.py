"""What the settings tab and the video page exchange with the YouTube publishing routes."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SyncReason = Literal["linked", "languages", "manual"]
StepId = Literal["video", "schedule", "captions", "thumbnail"]


class ConnectionOut(BaseModel):
    """The state of the one channel the owner may connect (docs/videos/HANDS-OFF.md)."""

    # The OAuth client id and secret are filled in on the provider card.
    configured: bool
    connected: bool
    channel_id: str | None = None
    channel_title: str | None = None
    connected_at: datetime | None = None
    # What the owner registers on the Google Cloud client, and the one permission asked for.
    redirect_uri: str
    scope: str


class StartIn(BaseModel):
    """Where the browser comes back to once Google has answered: a site path, never a host."""

    next_path: str = Field(default="/", max_length=500)


class StartOut(BaseModel):
    authorization_url: str
    expires_in: int


class SyncStep(BaseModel):
    id: StepId
    ok: bool
    detail: str


class SyncRecord(BaseModel):
    """What the site last sent for a video and how it went, kept on the project row."""

    at: datetime
    video_id: str | None
    reason: SyncReason
    ok: bool
    steps: list[SyncStep]
    localizations: list[str] = Field(default_factory=list)
    captions: list[str] = Field(default_factory=list)
    scheduled_at: datetime | None = None
    thumbnail_sha256: str | None = None
