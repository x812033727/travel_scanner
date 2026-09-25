from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, get_args

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from app.ai.catalog import ModelStatus

ProviderName = Literal["openai", "anthropic", "minimax", "gemini"]
Stage = Literal["planner", "writer", "verifier", "listener", "translator", "caption_reviewer"]
CaptionLocale = Literal["en", "ja", "ko", "zh-CN"]
TopicWord = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StageModel(StrictModel):
    provider: ProviderName
    model: str = Field(min_length=1, max_length=128)


class VoiceSettings(StrictModel):
    provider: Literal["azure", "gemini"]
    name: str = Field(min_length=1, max_length=90)
    style: str | None = Field(default=None, min_length=1, max_length=400)
    model: str | None = Field(default=None, min_length=3, max_length=60)
    rate: str = Field(default="+0%", pattern=r"^[+-]\d{1,2}%$")


class SettingsWrite(StrictModel):
    enabled: bool
    draft_interval_hours: int = Field(ge=6, le=720)
    topics_per_run: int = Field(ge=1, le=3)
    max_waiting_drafts: int = Field(ge=1, le=10)
    topic_scope: list[TopicWord] = Field(min_length=1, max_length=20)
    topic_avoid: list[TopicWord] = Field(max_length=20)
    topic_from_site: bool
    topic_from_search: bool
    stage_models: dict[Stage, StageModel]
    voice: VoiceSettings
    target_minutes_min: int = Field(ge=3, le=30)
    target_minutes_max: int = Field(ge=3, le=30)
    caption_locales: list[CaptionLocale] = Field(max_length=4)
    max_drafts_per_month: int = Field(ge=0, le=60)
    monthly_token_budget_millions: int = Field(ge=1, le=500)
    max_verify_rounds: int = Field(ge=1, le=5)
    max_retake_rounds: int = Field(ge=0, le=5)
    auto_approve_audio: bool

    @model_validator(mode="after")
    def _consistent(self) -> SettingsWrite:
        if self.target_minutes_min > self.target_minutes_max:
            raise ValueError("target_minutes_min must not exceed target_minutes_max")
        if not (self.topic_from_site or self.topic_from_search):
            raise ValueError("at least one topic source must be on")
        if len(set(self.caption_locales)) != len(self.caption_locales):
            raise ValueError("caption_locales must not repeat")
        missing = set(get_args(Stage)) - set(self.stage_models)
        if missing:
            raise ValueError(f"stage_models is missing {', '.join(sorted(missing))}")
        return self


class ModelOptionView(StrictModel):
    value: str
    label: str
    description: str | None
    status: ModelStatus


class VoiceOptionsView(StrictModel):
    gemini: list[str]
    gemini_models: list[str]
    azure: list[str]


class SettingsView(SettingsWrite):
    # The dropdowns: catalog models each vendor can serve, whether the site has that vendor's
    # key, and the voices the narration server accepts.
    model_options: dict[ProviderName, list[ModelOptionView]]
    configured_providers: list[ProviderName]
    voice_options: VoiceOptionsView
    updated_at: datetime | None
