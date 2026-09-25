from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Self, get_args

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.ai.catalog import ModelStatus

# "claude_code": the Claude subscription accounts the host's AI accounts agent manages; the
# others are the site's API keys.
ProviderName = Literal["claude_code", "openai", "anthropic", "minimax", "gemini"]
ApiProviderName = Literal["openai", "anthropic", "minimax", "gemini"]
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


class _SettingsFields(StrictModel):
    enabled: bool
    draft_interval_hours: int = Field(ge=6, le=720)
    topics_per_run: int = Field(ge=1, le=3)
    max_waiting_drafts: int = Field(ge=1, le=10)
    topic_scope: list[TopicWord] = Field(min_length=1, max_length=20)
    topic_avoid: list[TopicWord] = Field(max_length=20)
    topic_from_site: bool
    topic_from_search: bool
    voice: VoiceSettings
    target_minutes_min: int = Field(ge=3, le=30)
    target_minutes_max: int = Field(ge=3, le=30)
    caption_locales: list[CaptionLocale] = Field(max_length=4)
    max_drafts_per_month: int = Field(ge=0, le=60)
    monthly_token_budget_millions: int = Field(ge=1, le=500)
    max_verify_rounds: int = Field(ge=1, le=5)
    max_retake_rounds: int = Field(ge=0, le=5)
    # A subscription account at or above this share of its 5-hour or weekly window is skipped;
    # when every account is, the pipeline waits for a window to reset.
    subscription_max_usage_percent: int = Field(default=80, ge=10, le=100)
    auto_approve_audio: bool

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        if self.target_minutes_min > self.target_minutes_max:
            raise ValueError("target_minutes_min must not exceed target_minutes_max")
        if not (self.topic_from_site or self.topic_from_search):
            raise ValueError("at least one topic source must be on")
        if len(set(self.caption_locales)) != len(self.caption_locales):
            raise ValueError("caption_locales must not repeat")
        return self


def _every_stage(stage_models: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
    missing = set(get_args(Stage)) - set(stage_models)
    if missing:
        raise ValueError(f"stage_models is missing {', '.join(sorted(missing))}")
    return stage_models


class StageModelsWrite(StrictModel):
    """The model of each stage, chosen on the AI settings page (PUT /settings/models)."""

    stage_models: dict[Stage, StageModel]

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
        return _every_stage(value)


class SettingsWrite(_SettingsFields):
    stage_models: dict[Stage, StageModel]

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
        return _every_stage(value)


class SettingsSave(_SettingsFields):
    """A save from the settings tab on /admin/videos.

    The stage models are chosen on the AI settings page; a save that leaves them out keeps
    the stored ones, so the videos page cannot put back models it loaded earlier.
    """

    stage_models: dict[Stage, StageModel] | None = None

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel] | None) -> dict[Stage, StageModel] | None:
        return None if value is None else _every_stage(value)


class ModelOptionView(StrictModel):
    value: str
    label: str
    description: str | None
    status: ModelStatus


class VoiceOptionsView(StrictModel):
    gemini: list[str]
    gemini_models: list[str]
    azure: list[str]


class UsageView(StrictModel):
    # Since the first of this month (UTC): what the budgets on this page are measured against.
    # `tokens` are the API-billed ones the token budget limits; subscription runs are counted
    # apart, since the plan, not the site, pays for them.
    tokens: int
    token_budget: int
    subscription_tokens: int = 0
    drafts: int
    draft_budget: int
    calls: int
    failed_calls: int


class SettingsView(SettingsWrite):
    # The dropdowns: catalog models each vendor can serve, whether the site has that vendor's
    # key, and the voices the narration server accepts.
    model_options: dict[ProviderName, list[ModelOptionView]]
    configured_providers: list[ProviderName]
    voice_options: VoiceOptionsView
    usage: UsageView | None = None
    updated_at: datetime | None


SLUG_PATTERN = r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$"


class StageRunIn(StrictModel):
    stage: Stage
    slug: str = Field(pattern=SLUG_PATTERN)
    # The stage's prompt (the skill's references/prompts/*.md with the video's context) and
    # its inputs. The model is not the caller's to choose: the stage's setting decides.
    instructions: str = Field(min_length=1, max_length=60_000)
    payload: dict[str, object]
    max_output_tokens: int = Field(default=16_000, ge=1_000, le=32_000)


class StageRunOut(StrictModel):
    # The whole output file (brief.md, video.json, a report…), exactly as it should be saved.
    text: str
    provider: ProviderName
    model: str
    input_tokens: int
    output_tokens: int
    usage: UsageView


class TopicView(StrictModel):
    source: Literal["site", "search"]
    title: str
    summary: str
    url: str
    # The site article's slug, so a video can point back to it; None for a search result.
    slug: str | None = None
    date: str | None = None


class TopicsOut(StrictModel):
    topics: list[TopicView]
    # Why a source returned nothing: off in the settings, no key, or the day's budget used.
    notes: list[str]
