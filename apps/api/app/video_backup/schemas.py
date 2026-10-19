"""What the backup card, the backup status and the worker send and receive."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.video_backup.target import SERIES_KEY_PATTERN, Tier

# A state the worker reports, and the two the site adds: never queued, and a series set to off.
ReportedState = Literal["pending", "done", "failed", "blocked_quota", "partial"]
BackupState = Literal[
    "pending", "done", "failed", "blocked_quota", "partial", "stale", "not_queued", "off"
]
CopiedTier = Literal["basic", "full"]
SeriesKey = Annotated[str, StringConstraints(pattern=SERIES_KEY_PATTERN)]
Locale = Annotated[str, StringConstraints(pattern=r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$")]
Sha256 = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]
MissingFile = Annotated[str, StringConstraints(min_length=1, max_length=300)]


class SettingsIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_updated_at: datetime | None
    enabled: bool | None = None
    # Any of the spellings target.normalise_path accepts.
    path: str | None = Field(default=None, max_length=500)
    tiers: dict[SeriesKey, Tier] | None = Field(default=None, max_length=100)
    folder_names: dict[SeriesKey, str] | None = Field(default=None, max_length=100)


class ProbeView(BaseModel):
    # A test the worker has not answered yet: it writes and deletes a probe file next round.
    pending_id: UUID | None = None
    requested_at: datetime | None = None
    status: Literal["success", "failed"] | None = None
    message: str | None = None
    tested_at: datetime | None = None


class SpaceView(BaseModel):
    free_bytes: int | None = None
    total_bytes: int | None = None
    at: datetime | None = None


class SettingsView(BaseModel):
    enabled: bool
    path: str
    # The Drive folder the host's rclone remote is locked to (VIDEO_BACKUP_LOCK_PATH), as the
    # worker last reported it, and why the worker cannot back up with these settings, if so.
    lock_path: str | None
    lock_reported_at: datetime | None
    problem: str | None
    tiers: dict[str, Tier]
    folder_names: dict[str, str]
    default_folder_names: dict[str, str]
    full_categories: list[str]
    updated_at: datetime | None
    test: ProbeView
    space: SpaceView


class SkippedParts(BaseModel):
    model_config = ConfigDict(extra="forbid")

    descriptions: list[Locale] = Field(default_factory=list, max_length=20)
    captions: list[Locale] = Field(default_factory=list, max_length=20)
    dubs: list[Locale] = Field(default_factory=list, max_length=20)


class BackupContents(BaseModel):
    """What the worker found in Drive after ``rclone check``, by kind, for the site's own count
    of what a backup must hold (target.missing_files)."""

    model_config = ConfigDict(extra="forbid")

    final: bool = False
    metadata: bool = False
    thumbnail: bool = False
    descriptions: list[Locale] = Field(default_factory=list, max_length=20)
    captions: list[Locale] = Field(default_factory=list, max_length=20)
    dubs: list[Locale] = Field(default_factory=list, max_length=20)
    # The parts the upload package skipped with a reason (metadata.json's skipped_*_locales).
    skipped: SkippedParts = Field(default_factory=SkippedParts)
    clips: int = Field(default=0, ge=0, le=100_000)
    keyframes: int = Field(default=0, ge=0, le=100_000)


class ReportIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    state: ReportedState
    folder: str = Field(min_length=1, max_length=500)
    tier: CopiedTier
    bytes: int | None = Field(default=None, ge=0)
    files: int | None = Field(default=None, ge=0, le=1_000_000)
    files_hash: Sha256 | None = None
    contents: BackupContents | None = None
    # Files the worker could not copy because the host no longer has them (tidied before
    # backups existed), for a partial backup.
    missing: list[MissingFile] = Field(default_factory=list, max_length=200)
    error: str | None = Field(default=None, max_length=1000)
    attempts: int = Field(default=0, ge=0, le=10_000)
    free_bytes: int | None = Field(default=None, ge=0)
    total_bytes: int | None = Field(default=None, ge=0)


class BackupView(BaseModel):
    slug: str
    title: str
    youtube_video_id: str | None
    series_key: str
    # Relative to the configured path; the first backup's folder once there was one.
    folder: str
    # What the settings ask for now, and what the last backup copied.
    tier: Tier
    copied_tier: CopiedTier | None = None
    # "done" only when every file the settings and the language choice ask for is in Drive;
    # "stale" when it was, and the choice or the tier has asked for more since.
    state: BackupState
    complete: bool
    bytes: int | None = None
    files: int | None = None
    files_hash: str | None = None
    at: datetime | None = None
    checked_at: datetime | None = None
    queued_at: datetime | None = None
    reported_at: datetime | None = None
    attempts: int = 0
    error: str | None = None
    missing: list[str] = Field(default_factory=list)
    # Queued for longer than OVERDUE_HOURS without a finished backup.
    overdue: bool = False


class StatusView(BaseModel):
    enabled: bool
    path: str
    # Every video with a YouTube id, by state; "all_backed_up" is true only when backups are on
    # and each of them is done (series set to off aside).
    uploaded: int
    counts: dict[BackupState, int]
    all_backed_up: bool
    overdue_hours: int
    # Those not complete, oldest first; every uploaded video with ?all=true.
    videos: list[BackupView]


class LockIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # VIDEO_BACKUP_LOCK_PATH, or None when the host has no rclone-videos.conf.
    lock_path: str | None = Field(default=None, max_length=500)
    problem: str | None = Field(default=None, max_length=500)


class ProbeAnswerIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool
    message: str = Field(min_length=1, max_length=500)
    free_bytes: int | None = Field(default=None, ge=0)
    total_bytes: int | None = Field(default=None, ge=0)


class ExpectedParts(BaseModel):
    # The package's own files: final.mp4 and metadata.json, a Short's final.mp4.
    required: list[str]
    descriptions: list[str]
    captions: list[str]
    dubs: list[str]


class WorkerVideo(BaseModel):
    slug: str
    youtube_video_id: str
    category: str | None
    series_key: str
    series_slug: str | None
    episode_number: int | None
    folder: str
    shared_folder: str
    tier: Tier
    expected: ExpectedParts
    # The record as the worker last reported it, or None before its first report.
    backup: dict[str, object] | None


class WorkerProbe(BaseModel):
    id: UUID
    requested_at: datetime


class WorkerConfig(BaseModel):
    enabled: bool
    path: str
    lock_path: str | None
    # ``path`` relative to the remote's root, which is the lock; None when the worker must not
    # copy (backups off, no lock reported, or the path outside it), and ``problem`` says why.
    remote_prefix: str | None
    problem: str | None
    test: WorkerProbe | None
    # Every video with a YouTube id, oldest first.
    videos: list[WorkerVideo]
