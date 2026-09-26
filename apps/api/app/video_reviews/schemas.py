from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

# look and storyboard belong to the drama format (docs/videos/DRAMA.md): the character sheets
# the owner picks from, one review per character, and the keyframes before any clip is made.
Gate = Literal["outline", "look", "storyboard", "audio", "final", "publish"]
ContentType = Literal["video/mp4", "audio/mp4", "image/png", "image/jpeg"]
MAX_PAYLOAD_BYTES = 256 * 1024
SHA256_PATTERN = r"^[0-9a-f]{64}$"
# One gate can hold several pending reviews when each names a subject: a look review per
# character. The subject is a character id, or "style" for the style frames.
SUBJECT_PATTERN = r"^[a-z0-9][a-z0-9_-]{0,39}$"
# A storyboard carries a keyframe per shot; an outline or a final cut a handful of files.
MAX_REVIEW_FILES = 48


class ChecklistItem(BaseModel):
    key: str = Field(min_length=1, max_length=40)
    label: str = Field(min_length=1, max_length=120)
    done: bool


class ProjectIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    stage: str = Field(min_length=1, max_length=40)
    checklist: list[ChecklistItem] = Field(default_factory=list, max_length=30)
    youtube_video_id: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{6,32}$")
    # The article's slug. Left out, the stored one stays: older tools do not send it.
    source_guide: str | None = Field(default=None, pattern=r"^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$")


class ReviewFile(BaseModel):
    # What the file is to the page: preview, narration, contact_sheet, thumbnail; a drama's
    # storyboard names its keyframes shot_01, shot_02 and its look candidates candidate_a.
    role: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    sha256: str = Field(pattern=SHA256_PATTERN)
    size: int = Field(gt=0)
    content_type: ContentType


class ReviewIn(BaseModel):
    gate: Gate
    content_sha256: str = Field(pattern=SHA256_PATTERN)
    summary: str = Field(min_length=1, max_length=500)
    payload: dict[str, Any] = Field(default_factory=dict)
    files: list[ReviewFile] = Field(default_factory=list, max_length=MAX_REVIEW_FILES)
    subject: str | None = Field(default=None, pattern=SUBJECT_PATTERN)

    @field_validator("payload")
    @classmethod
    def _small(cls, value: dict[str, Any]) -> dict[str, Any]:
        if len(json.dumps(value, ensure_ascii=False).encode()) > MAX_PAYLOAD_BYTES:
            raise ValueError(f"payload is larger than {MAX_PAYLOAD_BYTES} bytes")
        return value


class ReviewOut(BaseModel):
    id: UUID
    gate: Gate
    subject: str | None = None
    content_sha256: str
    summary: str
    payload: dict[str, Any]
    files: list[ReviewFile]
    status: Literal["pending", "approved", "rejected", "superseded"]
    choice: str | None
    note: str | None
    decided_at: datetime | None
    created_at: datetime


class ProjectSummary(BaseModel):
    slug: str
    title: str
    stage: str
    checklist: list[ChecklistItem]
    youtube_video_id: str | None
    last_synced_at: datetime
    pending: int
    source_guide: str | None = None
    dropped_at: datetime | None = None
    dropped_note: str | None = None


class ProjectOut(ProjectSummary):
    reviews: list[ReviewOut]


class DecisionIn(BaseModel):
    decision: Literal["approve", "reject"]
    choice: str | None = Field(default=None, min_length=1, max_length=40)
    note: str | None = Field(default=None, max_length=2000)


class DropIn(BaseModel):
    note: str = Field(min_length=1, max_length=2000)


class PartOut(BaseModel):
    received: list[int]
    complete: bool
