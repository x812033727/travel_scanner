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
    UniqueConstraint,
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
# The channel voice the owner picked on 2026-09-24 (docs/videos/README.md); its style is the
# storytelling register of 2026-09-29 (docs/videos/ILLUSTRATED.md §說書式旁白, the same text as
# STORY_VOICE_STYLE in tools/video/automation/register.mjs). A stored row keeps what the owner
# pasted; this is what a fresh install starts from.
DEFAULT_VOICE: dict[str, Any] = {
    "provider": "gemini",
    "name": "Sulafat",
    "style": (
        "台灣國語說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，"
        "問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。"
        "絕不平、絕不像在念稿。"
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
# flat-explainer (migration 0113) is the illustrated "why" explainer: narrator only, all stills.
STYLE_PRESETS = ("cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "custom")
STYLE_PRESET_CHECK = "style_preset IN ({})".format(
    ", ".join(f"'{preset}'" for preset in STYLE_PRESETS)
)
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
    # A long series (docs/videos/SERIES.md): how many episodes may be in the making at once,
    # whether every episode's script waits for the owner, whether the next episode starts on
    # its own, how many episodes before a chapter's end the next chapter is planned, how many
    # times a document is rewritten from the owner's note before it waits for the owner, and
    # how many episodes a month may start.
    "series_max_in_flight": 1,
    "series_script_gate": True,
    "series_auto_continue": True,
    "series_chapter_ahead": 2,
    "series_doc_rewrites": 2,
    "series_episodes_per_month": 30,
    # A character's sheet is picked by the judge's score (docs/videos/HANDS-OFF.md); off
    # until the owner has looked at a first drama's sheets, like auto_approve_storyboard.
    "auto_pick_look": False,
    # The drama's own copies of the settings a tutorial keeps at the top level
    # (docs/videos/DRAMA-FLOW.md §一; migration 0105): the stage models and the narrator voice
    # (None follows the tutorial's), the standing instructions, the language defaults, the
    # automatic approval of the narration and of the final cut, and the rounds.
    "drama_stage_models": None,
    "drama_stage_instructions": {},
    "drama_voice": None,
    "drama_caption_locales": [],
    "drama_auto_approve_audio": True,
    "drama_auto_approve_final": True,
    "drama_max_verify_rounds": 3,
    "drama_max_retake_rounds": 2,
}
DRAMA_FIELDS: tuple[str, ...] = tuple(DEFAULT_DRAMA)
# Illustrated slides (docs/videos/ILLUSTRATED.md; migration 0114): the tutorial route draws its
# pictures under a switch, an image model and a per-video cap of its own (Flash keeps a long
# video near US$8 to 15 while a drama stays on Pro), its storyboard approves itself from the
# judge's scores (the owner decided that on 2026-09-29 for the first video already), and the
# worker gives every new video the owner's licensed music file and sound-effect set by name.
# The image model NULL follows the drama's choice.
SLIDES_IMAGE_MODEL = "gemini-3.1-flash-image"
DEFAULT_SLIDES: dict[str, Any] = {
    "slides_media_enabled": False,
    "slides_image_model": SLIDES_IMAGE_MODEL,
    "slides_max_usd_per_video": 20,
    "slides_auto_approve_storyboard": True,
    "slides_music_track": None,
    "slides_sfx_set": None,
}
SLIDES_FIELDS: tuple[str, ...] = tuple(DEFAULT_SLIDES)


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
        # The illustrated slides' cap; migration 0114 creates the same constraint.
        CheckConstraint(
            "slides_max_usd_per_video BETWEEN 0 AND 10000", name="ck_video_slides_usd"
        ),
        CheckConstraint("judge_min_score BETWEEN 0 AND 10", name="ck_video_drama_judge"),
        CheckConstraint(
            STYLE_PRESET_CHECK,
            name="ck_video_drama_preset",
        ),
        # The series columns; migration 0099 creates the same constraints under the same names.
        # A binge series (docs/videos/BINGE.md; migration 0103) may keep up to six episodes in
        # the making at once; the constraint is recreated under the same name.
        CheckConstraint(
            "series_max_in_flight BETWEEN 1 AND 6 AND series_chapter_ahead BETWEEN 0 AND 10 "
            "AND series_doc_rewrites BETWEEN 0 AND 5 "
            "AND series_episodes_per_month BETWEEN 0 AND 500",
            name="ck_video_drama_series",
        ),
        # The drama's own rounds; migration 0105 creates the same constraint under the same name.
        CheckConstraint(
            "drama_max_verify_rounds BETWEEN 1 AND 5 AND drama_max_retake_rounds BETWEEN 0 AND 5",
            name="ck_video_drama_rounds",
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
    # Stage -> the owner's standing instructions from the settings tab, which the worker appends
    # to that stage's prompt on every video (docs/videos/AUTOMATION.md).
    stage_instructions: Mapped[dict[str, str]] = mapped_column(
        JSON, default=_default({}), server_default=text("'{}'")
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
    # Gates: publishing always waits for the owner.
    auto_approve_audio: Mapped[bool] = mapped_column(Boolean, default=True)
    # The hands-off switches (docs/videos/HANDS-OFF.md; migration 0100). channel_stance is
    # what this channel believes, the only source the planner writes the owner's viewpoint
    # from; while it is blank Jev does not choose outlines, whatever auto_pick_outline says.
    channel_stance: Mapped[str] = mapped_column(Text, default="", server_default="")
    auto_pick_outline: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    auto_approve_final: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
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
    auto_pick_look: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
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
    series_max_in_flight: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    series_script_gate: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    series_auto_continue: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    series_chapter_ahead: Mapped[int] = mapped_column(Integer, default=2, server_default="2")
    series_doc_rewrites: Mapped[int] = mapped_column(Integer, default=2, server_default="2")
    series_episodes_per_month: Mapped[int] = mapped_column(Integer, default=30, server_default="30")
    # The drama's own copies of the tutorial's settings (docs/videos/DRAMA-FLOW.md §一; migration
    # 0105). The models and the voice are NULL to follow the tutorial's; the instructions and the
    # two switches were copied from the tutorial's columns when 0105 ran.
    drama_stage_models: Mapped[dict[str, dict[str, str]] | None] = mapped_column(
        JSON, nullable=True
    )
    drama_stage_instructions: Mapped[dict[str, str]] = mapped_column(
        JSON, default=_default({}), server_default=text("'{}'")
    )
    drama_voice: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    drama_caption_locales: Mapped[list[str]] = mapped_column(
        JSON, default=_default([]), server_default=text("'[]'")
    )
    drama_auto_approve_audio: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    drama_auto_approve_final: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    drama_max_verify_rounds: Mapped[int] = mapped_column(Integer, default=3, server_default="3")
    drama_max_retake_rounds: Mapped[int] = mapped_column(Integer, default=2, server_default="2")
    # Illustrated slides (docs/videos/ILLUSTRATED.md; migration 0114), see DEFAULT_SLIDES.
    slides_media_enabled: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    slides_image_model: Mapped[str | None] = mapped_column(
        String(128), nullable=True, default=SLIDES_IMAGE_MODEL, server_default=SLIDES_IMAGE_MODEL
    )
    slides_max_usd_per_video: Mapped[int] = mapped_column(
        Integer, default=20, server_default="20"
    )
    slides_auto_approve_storyboard: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    slides_music_track: Mapped[str | None] = mapped_column(String(80), nullable=True)
    slides_sfx_set: Mapped[str | None] = mapped_column(String(64), nullable=True)
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoStagePrompt(Base):
    """The instructions the worker last sent for one stage of one format, kept for the owner.

    The prompt is composed on the worker (the skill's text, the format's variant, then the
    owner's standing instructions), so the server only sees it as it arrives on
    /video/automation/run. One row per stage and format, replaced by every run, is what the
    settings tab shows as the prompt sent.
    """

    __tablename__ = "video_stage_prompts"
    __table_args__ = (
        # A Short's experiment runs on the one stage the tutorials do not have, ``subject``,
        # and the Shorts' prompts are kept under their own format (migration 0117).
        CheckConstraint(
            "stage IN ('planner', 'writer', 'verifier', 'listener', 'translator', "
            "'caption_reviewer', 'subject')",
            name="ck_video_stage_prompt_stage",
        ),
        CheckConstraint(
            "format IN ('slides', 'drama', 'shorts')", name="ck_video_stage_prompt_format"
        ),
    )

    stage: Mapped[str] = mapped_column(String(20), primary_key=True)
    format: Mapped[str] = mapped_column(String(8), primary_key=True)
    # Which of a stage's prompts this is: "" for a video's own, or a series document (setting,
    # outline, chapter), an episode, a recap or a fix (docs/videos/SERIES.md; migration 0099).
    variant: Mapped[str] = mapped_column(
        String(32), primary_key=True, default="", server_default=""
    )
    slug: Mapped[str] = mapped_column(String(80))
    instructions: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


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
            STYLE_PRESET_CHECK,
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
    # An episode of a series (docs/videos/SERIES.md) rather than a one-off request; the series
    # row and the episode number say which. Migration 0099.
    series_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("video_drama_series.id", ondelete="SET NULL"), nullable=True
    )
    episode_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
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


# A long drama series (docs/videos/SERIES.md; migration 0099): the series the owner planned, the
# documents the owner approves (the setting book, the whole-series outline, each chapter's
# detailed outline, one row per version), and the episode table. A one-off drama is a series of
# one episode whose only document is its story bible (docs/videos/DRAMA-FLOW.md §二; 0107). A
# brand-story series (docs/videos/STORY.md; 0111) has no documents at all: its episodes are the
# stories of a planned backlog, imported ready to make.
SERIES_KINDS = ("series", "one-off", "story")
SERIES_STATUSES = ("setting", "outline", "active", "paused", "finished")
# A binge series (docs/videos/BINGE.md; migration 0103): the genre preset the planner writes
# from, who leads, how many shots may be image-to-video clips, and the compilation of every
# episode into one long video once they are all cleared for upload.
SERIES_GENRES = (
    "xianxia-bonds",
    "rebirth-revenge",
    "system-game",
    "urban-return",
    "empress-rise",
    "custom",
)
SERIES_LEADS = ("female", "male", "dual-male")
VISUAL_TIERS = ("clips", "hybrid", "stills")
MIN_TOTAL_MINUTES = 30
MAX_TOTAL_MINUTES = 480
DOC_KINDS = ("setting", "outline", "chapter", "bible")
DOC_STATUSES = ("generating", "review", "approved", "rejected")
EPISODE_STATUSES = ("planned", "ready", "queued", "started", "done", "skipped")


class VideoDramaSeries(Base):
    __tablename__ = "video_drama_series"
    __table_args__ = (
        CheckConstraint(
            "status IN ('setting', 'outline', 'active', 'paused', 'finished')",
            name="ck_video_drama_series_status",
        ),
        # A story runs 12 to 15 minutes (migration 0111); the schemas still hold the other kinds
        # to 8.
        CheckConstraint(
            "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
            "AND target_minutes BETWEEN 1 AND 20",
            name="ck_video_drama_series_numbers",
        ),
        CheckConstraint(
            STYLE_PRESET_CHECK,
            name="ck_video_drama_series_style",
        ),
        CheckConstraint(
            "kind IN ('series', 'one-off', 'story')", name="ck_video_drama_series_kind"
        ),
        CheckConstraint(
            "episodes_per_day IS NULL OR episodes_per_day BETWEEN 1 AND 12",
            name="ck_video_drama_series_per_day",
        ),
        CheckConstraint(
            "genre IN ('xianxia-bonds', 'rebirth-revenge', 'system-game', 'urban-return', "
            "'empress-rise', 'custom')",
            name="ck_video_drama_series_genre",
        ),
        CheckConstraint(
            "lead IN ('female', 'male', 'dual-male')", name="ck_video_drama_series_lead"
        ),
        CheckConstraint(
            "visual_tier IN ('clips', 'hybrid', 'stills')", name="ck_video_drama_series_tier"
        ),
        CheckConstraint(
            "total_minutes IS NULL OR total_minutes BETWEEN 30 AND 480",
            name="ck_video_drama_series_total_minutes",
        ),
        # Named as migration 0103 names it, so a database built from the models (0001's
        # create_all) and one upgraded from 0101 carry the same constraint.
        UniqueConstraint("compilation_slug", name="uq_video_drama_series_compilation_slug"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(40), unique=True)
    # "series": the documents are the setting book, the outline and the chapters' outlines;
    # "one-off": one episode, one story bible (docs/videos/DRAMA-FLOW.md §二); "story": no
    # documents, the episodes are imported from a planned backlog (docs/videos/STORY.md).
    kind: Mapped[str] = mapped_column(String(12), default="series", server_default="series")
    title: Mapped[str] = mapped_column(String(200))
    # The story in the owner's words; the setting book is planned from it.
    premise: Mapped[str] = mapped_column(Text)
    # Which sides of the genre the owner cares about: world, bonds, structure, mood.
    aspects: Mapped[list[str]] = mapped_column(
        JSON, default=_default([]), server_default=text("'[]'")
    )
    tone: Mapped[str] = mapped_column(
        String(40), default="dual-male-leads-subtext", server_default="dual-male-leads-subtext"
    )
    style_preset: Mapped[str] = mapped_column(
        String(40), default="cinematic-3d", server_default="cinematic-3d"
    )
    target_minutes: Mapped[int] = mapped_column(Integer, default=3, server_default="3")
    planned_episodes: Mapped[int] = mapped_column(Integer, default=100, server_default="100")
    episodes_per_chapter: Mapped[int] = mapped_column(Integer, default=10, server_default="10")
    # The first part closes a stage, not the story: threads are left for a sequel.
    open_ended: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    # setting -> outline -> active as the documents are approved; the owner pauses or finishes.
    status: Mapped[str] = mapped_column(String(12), default="setting", server_default="setting")
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    # The owner asked for a chapter's outline ahead of time, or for the next episode to start
    # without waiting for the previous one; the worker's next round clears them.
    requested_chapter: Mapped[int | None] = mapped_column(Integer, nullable=True)
    force_next: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    # The binge columns (docs/videos/BINGE.md; migration 0103). The genre picks the planner's
    # conflict engine and the satisfaction beats the chapter outlines must schedule; a
    # hands-off series has its documents, screenplays, sheets and storyboards decided by the
    # checks instead of the owner; a compilation series joins every episode into one long video
    # once they are all cleared for upload; the visual tier caps how many shots are clips.
    genre: Mapped[str] = mapped_column(
        String(32), default="xianxia-bonds", server_default="xianxia-bonds"
    )
    lead: Mapped[str] = mapped_column(String(12), default="dual-male", server_default="dual-male")
    hands_off: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    compilation: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    visual_tier: Mapped[str] = mapped_column(String(8), default="clips", server_default="clips")
    # The length the owner asked the whole compilation to be; the episode count came from it.
    total_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # The compilation video's slug once the worker started it, and when it started and was
    # cleared for upload; null while the episodes are still being made.
    compilation_slug: Mapped[str | None] = mapped_column(String(80), nullable=True)
    compilation_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    compilation_finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # The brand-story columns (docs/videos/STORY.md; migration 0111). How many episodes may start
    # on one Asia/Taipei calendar day (NULL: no daily limit); the image model this series' media
    # jobs use (NULL: the settings tab's); and the look every story of the series shares,
    # {"style", "negative", "motion"?}, which a story series keeps here because it has no
    # setting book. The other kinds leave the daily count and the look NULL.
    episodes_per_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    look: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoDramaDoc(Base):
    __tablename__ = "video_drama_docs"
    __table_args__ = (
        UniqueConstraint(
            "series_id", "kind", "chapter_number", "version", name="uq_video_drama_doc_version"
        ),
        CheckConstraint(
            "kind IN ('setting', 'outline', 'chapter', 'bible')", name="ck_video_drama_doc_kind"
        ),
        CheckConstraint(
            "status IN ('generating', 'review', 'approved', 'rejected')",
            name="ck_video_drama_doc_status",
        ),
        CheckConstraint("version >= 1 AND chapter_number >= 0", name="ck_video_drama_doc_numbers"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    series_id: Mapped[UUID] = mapped_column(
        ForeignKey("video_drama_series.id", ondelete="CASCADE"), index=True
    )
    kind: Mapped[str] = mapped_column(String(12))
    # 0 for the setting book and the outline; the chapter's number for a chapter outline.
    chapter_number: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    # The document as the owner reads it, and its structured twin the worker plans from.
    body_md: Mapped[str] = mapped_column(Text)
    body_json: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=_default({}), server_default=text("'{}'")
    )
    status: Mapped[str] = mapped_column(String(12), default="review", server_default="review")
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    decided_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


# The discussion thread on every series document and every episode's screenplay
# (docs/videos/DRAMA-FLOW.md §三; migration 0108): the owner writes a line, the worker's next
# round has the planner (documents) or the writer (screenplays) answer it, and a new version of
# the document when the owner asked for a change.
MESSAGE_AUTHORS = ("owner", "planner", "writer")
MESSAGE_SUBJECT_PATTERN = r"^(setting|outline|chapter:\d+|bible|script:\d+)$"
MESSAGE_BODY_MAX_CHARS = 8_000


class VideoDramaMessage(Base):
    __tablename__ = "video_drama_messages"
    __table_args__ = (
        CheckConstraint(
            "author IN ('owner', 'planner', 'writer')", name="ck_video_drama_message_author"
        ),
        Index("ix_video_drama_messages_thread", "series_id", "subject", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    series_id: Mapped[UUID] = mapped_column(ForeignKey("video_drama_series.id", ondelete="CASCADE"))
    # setting | outline | chapter:<n> | bible | script:<episode number>
    subject: Mapped[str] = mapped_column(String(24))
    author: Mapped[str] = mapped_column(String(12))
    body_md: Mapped[str] = mapped_column(Text)
    # What the line was said about: a document's version ("v3") or the first 12 characters of
    # the screenplay's SHA-256, so a reader knows which version it answers.
    refers_to: Mapped[str | None] = mapped_column(String(16), nullable=True)
    # Set on the owner's message once the model answered it; null is "waiting for the model".
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class VideoDramaEpisode(Base):
    __tablename__ = "video_drama_episodes"
    __table_args__ = (
        UniqueConstraint("series_id", "number", name="uq_video_drama_episode_number"),
        CheckConstraint(
            "status IN ('planned', 'ready', 'queued', 'started', 'done', 'skipped')",
            name="ck_video_drama_episode_status",
        ),
        CheckConstraint(
            "number >= 1 AND chapter_number >= 1", name="ck_video_drama_episode_numbers"
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    series_id: Mapped[UUID] = mapped_column(
        ForeignKey("video_drama_series.id", ondelete="CASCADE"), index=True
    )
    number: Mapped[int] = mapped_column(Integer)
    chapter_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    logline: Mapped[str] = mapped_column(Text, default="", server_default="")
    # The chapter outline's row for this episode: hook, conflict, turn, cliffhanger, setups,
    # payoffs, tension, characters, locations, theme.
    beats: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=_default({}), server_default=text("'{}'")
    )
    # planned (from the outline) -> ready (its chapter approved) -> started -> done; skipped.
    status: Mapped[str] = mapped_column(String(12), default="planned", server_default="planned")
    # The video the worker made of it, and the request row it travelled as.
    slug: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    request_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("video_drama_requests.id", ondelete="SET NULL"), nullable=True
    )
    # Written when the episode is done: what happened, the characters' states, the threads.
    recap: Mapped[str | None] = mapped_column(Text, nullable=True)
    state_json: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=_default({}), server_default=text("'{}'")
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
