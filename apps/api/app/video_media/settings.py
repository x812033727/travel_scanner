"""Where the media store lives and how large it may grow (``VIDEO_MEDIA_*`` in ``.env``).

These sit in their own settings object rather than ``app.config.Settings`` because that file
belongs to ticket 2026-09-25-run-the-site-s-claude-features while it is in progress; fold them
in when it lands. Same env file and same "ignore what you do not know" rule as ``Settings``.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MediaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

    video_media_dir: str = "/var/lib/mokaair/video-media"
    # A 1080p 10-second clip is 10-40 MB; a character sheet a few MB.
    video_media_max_file_bytes: int = Field(default=200_000_000, ge=1_000_000, le=2_000_000_000)
    video_media_max_total_bytes: int = Field(
        default=30_000_000_000, ge=100_000_000, le=1_000_000_000_000
    )
    # Generated files are a pipeline cache: the work directory keeps its own copy.
    video_media_keep_days: int = Field(default=14, ge=1, le=365)
    video_media_submit_timeout_seconds: float = Field(default=60.0, ge=5, le=280)
    video_media_poll_timeout_seconds: float = Field(default=30.0, ge=5, le=120)
    video_media_fetch_timeout_seconds: float = Field(default=240.0, ge=10, le=280)
    # Gemini takes at most 20 MB of inline parts in one request; larger clips need a proxy.
    video_media_inline_judge_bytes: int = Field(default=20_000_000, ge=1_000_000, le=20_000_000)


@lru_cache
def get_media_settings() -> MediaSettings:
    return MediaSettings()
