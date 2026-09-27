from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal, Self, get_args
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field, field_validator, model_validator

# look and storyboard belong to the drama format (docs/videos/DRAMA.md): the character sheets
# the owner picks from, one review per character, and the keyframes before any clip is made.
# script is an episode's screenplay, read before any image or clip is paid for
# (docs/videos/SERIES.md). dubs was a batch of finished dub tracks (docs/videos/DUBS.md); since
# 2026-09-27 languages carries the whole batch of what the owner chose for a video, descriptions,
# captions and dub tracks (docs/videos/LANGUAGES.md): the site approves a batch with no dub
# track on arrival, one with a dub track waits for the owner to upload it in YouTube Studio.
Gate = Literal[
    "outline", "script", "look", "storyboard", "audio", "final", "publish", "dubs", "languages"
]
SERIES_SLUG_PATTERN = r"^[a-z0-9][a-z0-9-]{1,39}$"
# The previews, the dub tracks (docs/videos/DUBS.md: m4a, mp3 or wav), and since HANDS-OFF.md the
# whole upload package the owner downloads from the "ready to upload" list: the captions (.srt),
# the descriptions (.txt) and metadata.json.
ContentType = Literal[
    "video/mp4",
    "audio/mp4",
    "audio/mpeg",
    "audio/wav",
    "image/png",
    "image/jpeg",
    "application/x-subrip",
    "text/vtt",
    "text/plain",
    "application/json",
]
YOUTUBE_VIDEO_ID_PATTERN = r"^[A-Za-z0-9_-]{11}$"
# The languages a video can be made in besides zh-TW, in the order the page lists them.
DubLocale = Literal["en", "ja", "ko", "zh-CN"]
DUB_LOCALES: tuple[DubLocale, ...] = get_args(DubLocale)
# What a language is made of (docs/videos/LANGUAGES.md): the title, description and tags, the
# captions, and a dub track; a dub needs the captions, since it reads their translation.
LocalePart = Literal["metadata", "captions", "dub"]
LOCALE_PARTS: tuple[LocalePart, ...] = get_args(LocalePart)
# Where a chosen part stands: not made yet, made (in a languages review), given up with a reason,
# or, a dub track, uploaded by the owner (its languages review approved).
LanguageState = Literal["working", "ready", "skipped", "uploaded"]
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


VideoFormat = Literal["slides", "drama"]


class ProjectIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    stage: str = Field(min_length=1, max_length=40)
    checklist: list[ChecklistItem] = Field(default_factory=list, max_length=30)
    # Left out (or null), the stored one stays: the owner records it on /admin/videos before the
    # worker reads it back into video.json (docs/videos/HANDS-OFF.md).
    youtube_video_id: str | None = Field(default=None, pattern=YOUTUBE_VIDEO_ID_PATTERN)
    # The article's slug. Left out, the stored one stays: older tools do not send it.
    source_guide: str | None = Field(default=None, pattern=r"^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$")
    # Slides or the AI drama route (docs/videos/DRAMA.md). Left out, the stored one stays.
    format: VideoFormat | None = None
    # An episode of a long series (docs/videos/SERIES.md). Left out, the stored ones stay.
    series_slug: str | None = Field(default=None, pattern=SERIES_SLUG_PATTERN)
    episode_number: int | None = Field(default=None, ge=1, le=10_000)


class ReviewFile(BaseModel):
    # What the file is to the page: preview, narration, contact_sheet, thumbnail; a drama's
    # storyboard names its keyframes shot_01, shot_02 and its look candidates candidate_a. The
    # upload package names a locale's files captions_zh-TW and description_zh-TW (HANDS-OFF.md).
    role: str = Field(pattern=r"^[a-z][A-Za-z0-9_-]{0,39}$")
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


class LocaleChoice(BaseModel):
    """What the owner chose of one language; a dub track brings the captions with it."""

    metadata: bool = False
    captions: bool = False
    dub: bool = False

    @model_validator(mode="after")
    def _dub_needs_captions(self) -> Self:
        if self.dub:
            self.captions = True
        return self

    def chosen(self) -> list[LocalePart]:
        return [part for part in LOCALE_PARTS if getattr(self, part)]


class LocalesIn(BaseModel):
    """The owner's choice on the language panel: each language with the parts to make of it.

    An empty choice is the decision too ("only Traditional Chinese"); a language with nothing
    ticked is dropped, and the languages are kept in the page's order whatever order they came
    in, so the worker and the audit trail always see one shape for one choice.
    """

    locales: dict[DubLocale, LocaleChoice] = Field(default_factory=dict)

    @field_validator("locales")
    @classmethod
    def _in_page_order_without_empties(
        cls, value: dict[DubLocale, LocaleChoice]
    ) -> dict[DubLocale, LocaleChoice]:
        return {
            locale: value[locale]
            for locale in DUB_LOCALES
            if locale in value and value[locale].chosen()
        }


class LanguagePartOut(BaseModel):
    state: LanguageState
    reason: str | None = None


class ProjectSummary(BaseModel):
    slug: str
    title: str
    format: VideoFormat = "slides"
    stage: str
    checklist: list[ChecklistItem]
    youtube_video_id: str | None
    # When the owner set it to go public on YouTube (docs/videos/HANDS-OFF.md §YouTube API).
    youtube_publish_at: datetime | None = None
    # When the upload confirmation was approved: with no youtube_video_id yet, the video is
    # "ready to upload" and the page lists it second, after what needs the owner.
    publish_approved_at: datetime | None = None
    last_synced_at: datetime
    pending: int
    source_guide: str | None = None
    dropped_at: datetime | None = None
    dropped_note: str | None = None
    # What the drama route's generations have cost so far, from the media jobs (any month).
    media_usd: float = 0.0
    clip_seconds: int = 0
    # The languages the owner chose after the final cut and what of each, empty until they
    # decide; when they first decided; where each chosen part stands, from the languages reviews;
    # and whether the video may be scheduled: its upload confirmation approved, its languages
    # decided and every chosen part ready, skipped or uploaded, and no YouTube id yet
    # (docs/videos/LANGUAGES.md).
    locales: dict[DubLocale, LocaleChoice] = Field(default_factory=dict)
    locales_decided_at: datetime | None = None
    languages: dict[DubLocale, dict[LocalePart, LanguagePartOut]] = Field(default_factory=dict)
    ready_to_upload: bool = False
    # The languages with a dub track chosen, for a page from before the language panel.
    dub_locales: list[DubLocale] = Field(default_factory=list)
    # The series this video is an episode of, if any (docs/videos/SERIES.md).
    series_slug: str | None = None
    episode_number: int | None = None


class ProjectOut(ProjectSummary):
    reviews: list[ReviewOut]


class DecisionIn(BaseModel):
    decision: Literal["approve", "reject"]
    choice: str | None = Field(default=None, min_length=1, max_length=40)
    note: str | None = Field(default=None, max_length=2000)


class DropIn(BaseModel):
    note: str = Field(min_length=1, max_length=2000)


class DubLocalesIn(BaseModel):
    """The owner's choice of languages to dub one video in, from /admin/videos."""

    locales: list[DubLocale] = Field(max_length=4)

    @field_validator("locales")
    @classmethod
    def _each_once_in_page_order(cls, value: list[DubLocale]) -> list[DubLocale]:
        if len(set(value)) != len(value):
            raise ValueError("locales must not repeat")
        # Stored in the page's order whatever order they were ticked in, so the worker and the
        # audit trail always see one shape for one choice.
        return [locale for locale in DUB_LOCALES if locale in value]


class PartOut(BaseModel):
    received: list[int]
    complete: bool


class YoutubeIn(BaseModel):
    """What the owner pastes after uploading the final cut in YouTube Studio themselves.

    ``url`` is any address that names the video (youtu.be, watch?v=, shorts, Studio) or the bare
    eleven-character id; ``publish_at`` is when it goes public, timezone-aware, or null while
    the owner has not decided (docs/videos/HANDS-OFF.md §YouTube API 第一步).
    """

    url: str = Field(min_length=1, max_length=500)
    publish_at: AwareDatetime | None = None
