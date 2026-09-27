"""Request and response shapes of ``/video/media`` (docs/videos/DRAMA.md).

The tool side (tools/video/media, ticket 2026-09-26-video-drama-media-client) is written to
these: a job is submitted, polled by id until ``ready``, and its file fetched by SHA-256.
Reference images are always files already in the media store, named by their SHA-256, never
bytes in the request.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.video_automation.schemas import MediaOptionsView, MediaProvider
from app.video_reviews.schemas import SHA256_PATTERN

JobKind = Literal["image", "clip", "music"]
JobStatus = Literal["queued", "submitted", "ready", "failed", "expired"]
ImagePurpose = Literal["character_sheet", "style_frame", "keyframe", "thumbnail"]
ReferenceRole = Literal["character", "style", "previous_frame"]
Aspect = Literal["16:9", "9:16", "1:1"]
JudgeKind = Literal["look", "keyframe", "clip", "continuity"]
SLUG_PATTERN = r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$"
SHOT_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
MAX_REFERENCES = 4
MAX_PROMPT_CHARS = 4000
MAX_CONTEXT_BYTES = 64 * 1024
MAX_JUDGE_FILES = 6
MAX_RUBRIC = 12


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Reference(StrictModel):
    sha256: str = Field(pattern=SHA256_PATTERN)
    # character: a chosen character sheet; style: a style frame; previous_frame: the last frame
    # of the shot before, for a clip that continues its action.
    role: ReferenceRole = "character"


class _JobIn(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)
    prompt: str = Field(min_length=1, max_length=MAX_PROMPT_CHARS)
    negative_prompt: str | None = Field(default=None, max_length=1000)
    seed: int | None = Field(default=None, ge=0, le=2_147_483_647)
    # The tool's own cache key, kept for the logs; the request hash is what dedupes.
    idempotency_key: str | None = Field(default=None, min_length=1, max_length=80)


class ImageJobIn(_JobIn):
    purpose: ImagePurpose
    aspect: Aspect = "16:9"
    references: list[Reference] = Field(default_factory=list, max_length=MAX_REFERENCES)
    shot_id: str | None = Field(default=None, pattern=SHOT_PATTERN, max_length=60)


class ClipJobIn(_JobIn):
    shot_id: str = Field(pattern=SHOT_PATTERN, max_length=60)
    first_frame: str = Field(pattern=SHA256_PATTERN)
    last_frame: str | None = Field(default=None, pattern=SHA256_PATTERN)
    references: list[Reference] = Field(default_factory=list, max_length=MAX_REFERENCES)
    seconds: int = Field(ge=3, le=15)
    # Defaults to the settings row's clip_resolution.
    resolution: str | None = Field(default=None, pattern=r"^(?:\d{3,4}p|2k|4k)$")
    native_audio: bool = False


class MusicJobIn(_JobIn):
    seconds: int = Field(ge=10, le=600)


class JobFile(StrictModel):
    sha256: str
    size: int
    content_type: str


class JobError(StrictModel):
    code: str
    detail: str


class JobOut(StrictModel):
    id: UUID
    slug: str
    kind: JobKind
    status: JobStatus
    provider: MediaProvider
    model: str
    seconds: int
    file: JobFile | None
    error: JobError | None
    # How long the tool should wait before asking again; 0 once the job is terminal.
    retry_after_seconds: int
    attempts: int
    polls: int
    usd_estimate: float
    created_at: datetime
    submitted_at: datetime | None
    ready_at: datetime | None
    expires_at: datetime | None


class JudgeFile(StrictModel):
    sha256: str = Field(pattern=SHA256_PATTERN)
    label: str = Field(min_length=1, max_length=80)


class JudgeCriterion(StrictModel):
    key: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    question: str = Field(min_length=1, max_length=400)
    weight: float = Field(default=1.0, gt=0, le=10)


class JudgeIn(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)
    kind: JudgeKind
    # Images to look at together (a keyframe and its character sheets), or one clip.
    files: list[JudgeFile] = Field(min_length=1, max_length=MAX_JUDGE_FILES)
    rubric: list[JudgeCriterion] = Field(min_length=1, max_length=MAX_RUBRIC)
    # Free-form facts the judge needs: the characters' descriptions, the shot's prompt.
    context: dict[str, Any] = Field(default_factory=dict)
    # Overrides the settings row's judge_min_score for this call.
    min_score: int | None = Field(default=None, ge=0, le=10)

    @field_validator("context")
    @classmethod
    def _small(cls, value: dict[str, Any]) -> dict[str, Any]:
        if len(json.dumps(value, ensure_ascii=False).encode()) > MAX_CONTEXT_BYTES:
            raise ValueError(f"context is larger than {MAX_CONTEXT_BYTES} bytes")
        return value


class JudgeOut(StrictModel):
    # 0-10 per rubric key, the weighted overall, and whether it clears the threshold with no
    # criterion under 4.
    scores: dict[str, float]
    overall: float
    passed: bool
    problems: list[str]
    notes: str
    model: str


class BudgetView(StrictModel):
    unit: str
    limit: int
    used: int
    remaining: int


class StoreView(StrictModel):
    used_bytes: int
    max_file_bytes: int
    max_total_bytes: int
    writable: bool


class ChoiceView(StrictModel):
    provider: MediaProvider
    model: str
    configured: bool
    resolution: str | None = None
    seconds: int | None = None


class MediaStatus(StrictModel):
    enabled: bool
    music_enabled: bool
    image: ChoiceView
    clip: ChoiceView
    music: ChoiceView
    models: MediaOptionsView
    budgets: dict[str, BudgetView]
    # This month's jobs priced with the catalog, submitted or ready.
    estimated_usd: float
    max_usd_per_video: int
    max_clips_per_video: int
    max_retakes_per_shot: int
    judge_min_score: int
    style_preset: str
    store: StoreView
    limits: dict[str, int]


class PruneOut(StrictModel):
    expired_jobs: int
    deleted_files: int
    freed_bytes: int
