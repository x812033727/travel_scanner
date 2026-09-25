from __future__ import annotations

import copy
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Boolean, CheckConstraint, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


# The writing stages, each run with its own vendor and model. Defaults follow the owner's
# 2026-09-25 choice: Sonnet writes, Opus checks, as on the first three videos.
STAGES = ("planner", "writer", "verifier", "listener", "translator", "caption_reviewer")
DEFAULT_STAGE_MODELS: dict[str, dict[str, str]] = {
    "planner": {"provider": "anthropic", "model": "claude-sonnet-5"},
    "writer": {"provider": "anthropic", "model": "claude-sonnet-5"},
    "verifier": {"provider": "anthropic", "model": "claude-opus-5-5"},
    "listener": {"provider": "anthropic", "model": "claude-opus-5-5"},
    "translator": {"provider": "anthropic", "model": "claude-sonnet-5"},
    "caption_reviewer": {"provider": "anthropic", "model": "claude-opus-5-5"},
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
    # Gates: outline, final cut and publishing always wait for the owner.
    auto_approve_audio: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
