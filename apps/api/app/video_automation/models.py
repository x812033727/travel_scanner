from __future__ import annotations

import copy
import json
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.video_media.catalog import DEFAULT_CLIP, DEFAULT_IMAGE, DEFAULT_MUSIC


def utcnow() -> datetime:
    return datetime.now(UTC)


# The writing stages, each run with its own vendor and model. Defaults follow the owner's
# 2026-09-25 choices: Sonnet writes, Opus checks, as on the first three videos, on the Claude
# subscription accounts the host signs in (the owner read the providers' terms themselves).
STAGES = ("planner", "writer", "verifier", "listener", "translator", "caption_reviewer")
DEFAULT_STAGE_MODELS: dict[str, dict[str, str]] = {
    "planner": {"provider": "claude_code", "model": "claude-sonnet-5"},
    "writer": {"provider": "claude_code", "model": "claude-sonnet-5"},
    "verifier": {"provider": "claude_code", "model": "claude-opus-5-5"},
    "listener": {"provider": "claude_code", "model": "claude-opus-5-5"},
    "translator": {"provider": "claude_code", "model": "claude-sonnet-5"},
    "caption_reviewer": {"provider": "claude_code", "model": "claude-opus-5-5"},
}
# The channel voice the owner picked on 2026-09-24 (docs/videos/README.md).
DEFAULT_VOICE: dict[str, Any] = {
    "provider": "gemini",
    "name": "Sulafat",
    "style": (
        "Relaxed, conversational tech explainer talking to a friend, in Taiwan Mandarin with a "
        "natural Taiwanese accent. Natural rise and fall in intonation, light emphasis on key "
        "words, never flat or like reading a script. Medium-brisk pace."
    ),
    "model": None,
    "rate": "+0%",
}
DEFAULT_TOPIC_SCOPE = ["AI", "科技", "AI 工具教學"]
DEFAULT_TOPIC_AVOID = ["投資建議", "醫療建議", "選舉政治"]
DEFAULT_CAPTION_LOCALES = ["en", "ja", "ko", "zh-CN"]
# The AI drama route (docs/videos/DRAMA.md). The owner chose on 2026-09-26 to start without a
# spending cap, so the budgets open wide and are lowered after the pilot; migration 0095 carries
# the same values as server defaults, and the settings tab shows them.
STYLE_PRESETS = ("cinematic-3d", "anime-2d", "ink-wash", "custom")
CLIP_RESOLUTIONS = ("720p", "768p", "1080p", "2k", "4k")
DEFAULT_DRAMA_TOPIC_SCOPE = ["山海經", "民間傳說", "原創玄幻"]
DEFAULT_DRAMA: dict[str, Any] = {
    "drama_enabled": False,
    "image_provider": DEFAULT_IMAGE[0],
    "image_model": DEFAULT_IMAGE[1],
    "clip_provider": DEFAULT_CLIP[0],
    "clip_model": DEFAULT_CLIP[1],
    "music_provider": DEFAULT_MUSIC[0],
    "music_model": DEFAULT_MUSIC[1],
    "clip_resolution": "1080p",
    "clip_seconds_default": 8,
    "clip_native_audio": False,
    "drama_aspect": "16:9",
    "max_clips_per_video": 40,
    "max_retakes_per_shot": 2,
    "monthly_clip_seconds_budget": 3000,
    "monthly_images_budget": 1500,
    "monthly_judge_calls_budget": 3000,
    "monthly_music_budget": 60,
    "max_usd_per_video": 200,
    "judge_min_score": 7,
    "auto_approve_storyboard": False,
    "character_voice_pool": [],
    "music_enabled": True,
    "subtitle_burn_in": True,
    "style_preset": "cinematic-3d",
    "drama_topic_scope": DEFAULT_DRAMA_TOPIC_SCOPE,
}
DRAMA_FIELDS: tuple[str, ...] = tuple(DEFAULT_DRAMA)


def _default(value: Any) -> Callable[[], Any]:
    """A fresh copy per row, so no two rows share one mutable default."""
    return lambda: copy.deepcopy(value)


class VideoAutomationSettings(Base):
    __tablename__ = "video_automation_settings"
    __table_args__ = (
        CheckConstraint("id = 1", name="ck_video_automation_settings_singleton"),
        CheckConstraint(
            "draft_interval_hours BETWEEN 6 AND 720", name="ck_video_automation_interval"
        ),
        CheckConstraint("topics_per_run BETWEEN 1 AND 3", name="ck_video_automation_topics"),
        CheckConstraint("max_waiting_drafts BETWEEN 1 AND 10", name="ck_video_automation_waiting"),
        CheckConstraint(
            "target_minutes_min BETWEEN 3 AND 30 AND target_minutes_max BETWEEN 3 AND 30 "
            "AND target_minutes_min <= target_minutes_max",
            name="ck_video_automation_minutes",
        ),
        CheckConstraint("max_drafts_per_month BETWEEN 0 AND 60", name="ck_video_automation_drafts"),
        CheckConstraint(
            "monthly_token_budget_millions BETWEEN 1 AND 500", name="ck_video_automation_tokens"
        ),
        CheckConstraint("max_verify_rounds BETWEEN 1 AND 5", name="ck_video_automation_verify"),
        CheckConstraint("max_retake_rounds BETWEEN 0 AND 5", name="ck_video_automation_retakes"),
        CheckConstraint(
            "subscription_max_usage_percent BETWEEN 10 AND 100",
            name="ck_video_automation_subscription_cap",
        ),
        # The drama columns; migration 0095 creates the same constraints under the same names.
        CheckConstraint(
            "image_provider IN ('gemini', 'minimax') AND clip_provider IN ('gemini', 'minimax') "
            "AND music_provider IN ('gemini', 'minimax')",
            name="ck_video_drama_providers",
        ),
        CheckConstraint(
            "clip_resolution IN ('720p', '768p', '1080p', '2k', '4k')",
            name="ck_video_drama_resolution",
        ),
        CheckConstraint("drama_aspect IN ('16:9', '9:16')", name="ck_video_drama_aspect"),
        CheckConstraint("clip_seconds_default BETWEEN 4 AND 10", name="ck_video_drama_seconds"),
        CheckConstraint("max_clips_per_video BETWEEN 1 AND 120", name="ck_video_drama_clips"),
        CheckConstraint("max_retakes_per_shot BETWEEN 0 AND 5", name="ck_video_drama_retakes"),
        CheckConstraint(
            "monthly_clip_seconds_budget BETWEEN 0 AND 100000 "
            "AND monthly_images_budget BETWEEN 0 AND 100000 "
            "AND monthly_judge_calls_budget BETWEEN 0 AND 100000 "
            "AND monthly_music_budget BETWEEN 0 AND 100000",
            name="ck_video_drama_budgets",
        ),
        CheckConstraint("max_usd_per_video BETWEEN 0 AND 10000", name="ck_video_drama_usd"),
        CheckConstraint("judge_min_score BETWEEN 0 AND 10", name="ck_video_drama_judge"),
        CheckConstraint(
            "style_preset IN ('cinematic-3d', 'anime-2d', 'ink-wash', 'custom')",
            name="ck_video_drama_preset",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    # Schedule and topics.
    draft_interval_hours: Mapped[int] = mapped_column(Integer, default=72)
    topics_per_run: Mapped[int] = mapped_column(Integer, default=1)
    max_waiting_drafts: Mapped[int] = mapped_column(Integer, default=3)
    topic_scope: Mapped[list[str]] = mapped_column(JSON, default=_default(DEFAULT_TOPIC_SCOPE))
    topic_avoid: Mapped[list[str]] = mapped_column(JSON, default=_default(DEFAULT_TOPIC_AVOID))
    topic_from_site: Mapped[bool] = mapped_column(Boolean, default=True)
    topic_from_search: Mapped[bool] = mapped_column(Boolean, default=True)
    # Models, stage -> {"provider", "model"}.
    stage_models: Mapped[dict[str, dict[str, str]]] = mapped_column(
        JSON, default=_default(DEFAULT_STAGE_MODELS)
    )
    # The finished video.
    voice: Mapped[dict[str, Any]] = mapped_column(JSON, default=_default(DEFAULT_VOICE))
    target_minutes_min: Mapped[int] = mapped_column(Integer, default=8)
    target_minutes_max: Mapped[int] = mapped_column(Integer, default=12)
    caption_locales: Mapped[list[str]] = mapped_column(
        JSON, default=_default(DEFAULT_CAPTION_LOCALES)
    )
    # Budgets. Narration characters and Jev calls keep their existing settings.
    max_drafts_per_month: Mapped[int] = mapped_column(Integer, default=8)
    monthly_token_budget_millions: Mapped[int] = mapped_column(Integer, default=20)
    max_verify_rounds: Mapped[int] = mapped_column(Integer, default=3)
    max_retake_rounds: Mapped[int] = mapped_column(Integer, default=2)
    # Unused since 2026-09-26: runs keep an account until it is full (app.ai.subscription
    # FULL_PERCENT). The column stays so no migration is needed to drop a setting.
    subscription_max_usage_percent: Mapped[int] = mapped_column(
        Integer, default=80, server_default="80"
    )
    # Gates: outline, final cut and publishing always wait for the owner.
    auto_approve_audio: Mapped[bool] = mapped_column(Boolean, default=True)
    # The drama format (docs/videos/DRAMA.md): media models, clip shape, budgets, gates, look.
    drama_enabled: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    image_provider: Mapped[str] = mapped_column(
        String(16), default=DEFAULT_IMAGE[0], server_default=DEFAULT_IMAGE[0]
    )
    image_model: Mapped[str] = mapped_column(
        String(128), default=DEFAULT_IMAGE[1], server_default=DEFAULT_IMAGE[1]
    )
    clip_provider: Mapped[str] = mapped_column(
        String(16), default=DEFAULT_CLIP[0], server_default=DEFAULT_CLIP[0]
    )
    clip_model: Mapped[str] = mapped_column(
        String(128), default=DEFAULT_CLIP[1], server_default=DEFAULT_CLIP[1]
    )
    music_provider: Mapped[str] = mapped_column(
        String(16), default=DEFAULT_MUSIC[0], server_default=DEFAULT_MUSIC[0]
    )
    music_model: Mapped[str] = mapped_column(
        String(128), default=DEFAULT_MUSIC[1], server_default=DEFAULT_MUSIC[1]
    )
    clip_resolution: Mapped[str] = mapped_column(String(8), default="1080p", server_default="1080p")
    clip_seconds_default: Mapped[int] = mapped_column(Integer, default=8, server_default="8")
    clip_native_audio: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    drama_aspect: Mapped[str] = mapped_column(String(8), default="16:9", server_default="16:9")
    max_clips_per_video: Mapped[int] = mapped_column(Integer, default=40, server_default="40")
    max_retakes_per_shot: Mapped[int] = mapped_column(Integer, default=2, server_default="2")
    monthly_clip_seconds_budget: Mapped[int] = mapped_column(
        Integer, default=3000, server_default="3000"
    )
    monthly_images_budget: Mapped[int] = mapped_column(Integer, default=1500, server_default="1500")
    monthly_judge_calls_budget: Mapped[int] = mapped_column(
        Integer, default=3000, server_default="3000"
    )
    monthly_music_budget: Mapped[int] = mapped_column(Integer, default=60, server_default="60")
    max_usd_per_video: Mapped[int] = mapped_column(Integer, default=200, server_default="200")
    judge_min_score: Mapped[int] = mapped_column(Integer, default=7, server_default="7")
    auto_approve_storyboard: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    # [{provider, name, style?, hint?}]: voices the planner casts characters from.
    character_voice_pool: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=_default([]), server_default=text("'[]'")
    )
    music_enabled: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    subtitle_burn_in: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    style_preset: Mapped[str] = mapped_column(
        String(40), default="cinematic-3d", server_default="cinematic-3d"
    )
    drama_topic_scope: Mapped[list[str]] = mapped_column(
        JSON,
        default=_default(DEFAULT_DRAMA_TOPIC_SCOPE),
        server_default=text("'" + json.dumps(DEFAULT_DRAMA_TOPIC_SCOPE, ensure_ascii=True) + "'"),
    )
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoAiRun(Base):
    """One model call a video stage made through the server: what it cost and whether it worked.

    The month's token budget and draft count are sums over these rows, so a call that failed
    upstream is kept too, with the tokens the vendor reported (usually none).
    """

    __tablename__ = "video_ai_runs"
    __table_args__ = (
        CheckConstraint("status IN ('ok', 'failed')", name="ck_video_ai_run_status"),
        Index("ix_video_ai_runs_created", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(80), index=True)
    stage: Mapped[str] = mapped_column(String(32))
    provider: Mapped[str] = mapped_column(String(16))
    model: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(16))
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    token_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("video_tool_tokens.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


# What the owner asked for on /admin/videos: an episode of the drama route to make next, ahead
# of the scheduled drafts (docs/videos/DRAMA.md). The worker claims the oldest queued one.
REQUEST_STATUSES = ("queued", "started", "done", "cancelled")


class VideoDramaRequest(Base):
    __tablename__ = "video_drama_requests"
    __table_args__ = (
        CheckConstraint(
            "status IN ('queued', 'started', 'done', 'cancelled')",
            name="ck_video_drama_request_status",
        ),
        CheckConstraint(
            "style_preset IN ('cinematic-3d', 'anime-2d', 'ink-wash', 'custom')",
            name="ck_video_drama_request_style",
        ),
        Index("ix_video_drama_requests_status_created", "status", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    # The story's premise in the owner's words, or what to make of the article in source_guide.
    premise: Mapped[str] = mapped_column(Text)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # An article of the site to adapt, by slug; None for an original story.
    source_guide: Mapped[str | None] = mapped_column(String(120), nullable=True)
    style_preset: Mapped[str] = mapped_column(String(16), default="cinematic-3d")
    target_minutes: Mapped[int] = mapped_column(Integer, default=3)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(12), default="queued")
    # The video the worker made of it, once it started; the project row carries the rest.
    slug: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    started_by_token_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("video_tool_tokens.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
