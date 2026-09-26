from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Self, get_args
from uuid import UUID

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
# The drama format's media settings (docs/videos/DRAMA.md); the vendors are the site's keys.
MediaProvider = Literal["gemini", "minimax"]
ClipResolution = Literal["720p", "768p", "1080p", "2k", "4k"]
StylePreset = Literal["cinematic-3d", "anime-2d", "ink-wash", "custom"]
DramaAspect = Literal["16:9", "9:16"]
MediaKindName = Literal["image", "clip", "music"]


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


class CharacterVoice(StrictModel):
    """One voice the planner may cast a character with; `hint` says what it suits."""

    provider: Literal["azure", "gemini"]
    name: str = Field(min_length=1, max_length=90)
    style: str | None = Field(default=None, min_length=1, max_length=400)
    hint: str | None = Field(default=None, min_length=1, max_length=40)


class DramaSettings(StrictModel):
    """The drama format's media settings, one nested object on the settings row."""

    drama_enabled: bool
    image_provider: MediaProvider
    image_model: str = Field(min_length=1, max_length=128)
    clip_provider: MediaProvider
    clip_model: str = Field(min_length=1, max_length=128)
    music_provider: MediaProvider
    music_model: str = Field(min_length=1, max_length=128)
    clip_resolution: ClipResolution
    clip_seconds_default: int = Field(ge=4, le=10)
    clip_native_audio: bool
    drama_aspect: DramaAspect
    max_clips_per_video: int = Field(ge=1, le=120)
    max_retakes_per_shot: int = Field(ge=0, le=5)
    monthly_clip_seconds_budget: int = Field(ge=0, le=100_000)
    monthly_images_budget: int = Field(ge=0, le=100_000)
    monthly_judge_calls_budget: int = Field(ge=0, le=100_000)
    monthly_music_budget: int = Field(ge=0, le=100_000)
    max_usd_per_video: int = Field(ge=0, le=10_000)
    judge_min_score: int = Field(ge=0, le=10)
    auto_approve_storyboard: bool
    character_voice_pool: list[CharacterVoice] = Field(max_length=8)
    music_enabled: bool
    subtitle_burn_in: bool
    style_preset: StylePreset
    drama_topic_scope: list[TopicWord] = Field(max_length=20)

    @model_validator(mode="after")
    def _distinct_voices(self) -> Self:
        voices = [(voice.provider, voice.name) for voice in self.character_voice_pool]
        if len(set(voices)) != len(voices):
            raise ValueError("character_voice_pool must not repeat a voice")
        return self


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
    drama: DramaSettings

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
        return _every_stage(value)


class SettingsSave(_SettingsFields):
    """A save from the settings tab on /admin/videos.

    The stage models are chosen on the AI settings page; a save that leaves them out keeps
    the stored ones, so the videos page cannot put back models it loaded earlier. The drama
    settings follow the same rule, so a page built before they existed cannot reset them.
    """

    stage_models: dict[Stage, StageModel] | None = None
    drama: DramaSettings | None = None

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


class MediaOptionView(StrictModel):
    """One image, clip or music model the settings tab can offer, from app.video_media.catalog."""

    value: str
    label: str
    description: str | None
    status: ModelStatus
    resolutions: list[str]
    durations: list[int]
    reference_images: int
    native_audio: bool
    usd_per_second: float | None
    usd_per_image: float | None
    usd_per_track: float | None


class MediaOptionsView(StrictModel):
    images: dict[MediaProvider, list[MediaOptionView]]
    clips: dict[MediaProvider, list[MediaOptionView]]
    music: dict[MediaProvider, list[MediaOptionView]]


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
    media_options: MediaOptionsView
    style_presets: list[StylePreset]
    usage: UsageView | None = None
    updated_at: datetime | None


SLUG_PATTERN = r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$"
GUIDE_SLUG_PATTERN = r"^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$"
RequestStatus = Literal["queued", "started", "done", "cancelled"]


class DramaRequestIn(StrictModel):
    """What the owner asks for on /admin/videos: an episode of the drama route to make next.

    ``premise`` is the story in the owner's words; with ``source_guide`` it says what to make of
    that article. The worker takes the oldest request before any scheduled draft.
    """

    premise: str = Field(min_length=1, max_length=4000)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    source_guide: str | None = Field(default=None, pattern=GUIDE_SLUG_PATTERN)
    style_preset: StylePreset = "cinematic-3d"
    target_minutes: int = Field(default=3, ge=1, le=8)
    note: str | None = Field(default=None, min_length=1, max_length=2000)

    @field_validator("premise", "title", "note")
    @classmethod
    def _trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        text = value.strip()
        if not text:
            raise ValueError("must not be blank")
        return text


class DramaRequestStart(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)


class DramaRequestOut(BaseModel):
    id: UUID
    premise: str
    title: str | None
    source_guide: str | None
    style_preset: StylePreset
    target_minutes: int
    note: str | None
    status: RequestStatus
    slug: str | None
    created_by_user_id: UUID | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    cancelled_at: datetime | None


class DramaRequestsOut(BaseModel):
    requests: list[DramaRequestOut]


class NextDramaRequestOut(BaseModel):
    request: DramaRequestOut | None


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
