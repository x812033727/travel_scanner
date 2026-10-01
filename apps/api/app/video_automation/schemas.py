from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Any, Literal, Self, get_args
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
from app.video_automation.models import SLIDES_IMAGE_MODEL
from app.video_media.catalog import MEDIA_VENDORS, find_model

# "claude_code" and "codex" use the host's subscription accounts; the others use API keys.
ProviderName = Literal["claude_code", "codex", "openai", "anthropic", "minimax", "gemini"]
ApiProviderName = Literal["openai", "anthropic", "minimax", "gemini"]
Stage = Literal["planner", "writer", "verifier", "listener", "translator", "caption_reviewer"]
CaptionLocale = Literal["en", "ja", "ko", "zh-CN"]
TopicWord = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]
# The owner's standing instructions for one stage: the settings tab's text, which the worker
# appends to that stage's prompt. Which prompt a stage gets depends on the video's format.
StandingText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=4000)]
PromptFormat = Literal["slides", "drama"]
# The drama format's media settings (docs/videos/DRAMA.md); the vendors are the site's keys.
MediaProvider = Literal["gemini", "minimax"]
ClipResolution = Literal["720p", "768p", "1080p", "2k", "4k"]
StylePreset = Literal["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "custom"]
# The illustrated explainer (docs/videos/so-thats-why/): narrator only, no cast. Only a one-off
# may use it; a long series and a story series are written from prompts that need a cast.
EXPLAINER_PRESET: StylePreset = "flat-explainer"
# The slides route and other long-form videos have an eight-minute minimum (migration 0117).
EPISODE_MIN_MINUTES = 8
EXPLAINER_MIN_MINUTES = 8
EXPLAINER_MAX_MINUTES = 20
EXPLAINER_DEFAULT_MINUTES = 10
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


def _kept_instructions(value: dict[Stage, str]) -> dict[Stage, str]:
    """A field emptied on the settings tab drops that stage's standing instructions."""
    return {stage: text for stage, text in value.items() if text}


def _every_stage(stage_models: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
    missing = set(get_args(Stage)) - set(stage_models)
    if missing:
        raise ValueError(f"stage_models is missing {', '.join(sorted(missing))}")
    return stage_models


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
    # A character's sheet is picked by the judge's score (docs/videos/HANDS-OFF.md); a page
    # from before this existed sends the stored value back, since it sends the whole object.
    auto_pick_look: bool = False
    character_voice_pool: list[CharacterVoice] = Field(max_length=8)
    music_enabled: bool
    subtitle_burn_in: bool
    style_preset: StylePreset
    drama_topic_scope: list[TopicWord] = Field(max_length=20)
    # A long series (docs/videos/SERIES.md); a page from before these existed sends the stored
    # values back unchanged, since it sends the whole drama object.
    series_max_in_flight: int = Field(default=1, ge=1, le=6)
    series_script_gate: bool = True
    series_auto_continue: bool = True
    series_chapter_ahead: int = Field(default=2, ge=0, le=10)
    series_doc_rewrites: int = Field(default=2, ge=0, le=5)
    series_episodes_per_month: int = Field(default=30, ge=0, le=500)
    # The drama's own copies of the settings a tutorial keeps at the top level
    # (docs/videos/DRAMA-FLOW.md §一): the models and the narrator voice (None follows the
    # tutorial's), the standing instructions, the language defaults, the automatic approval of
    # the narration and of the final cut, and the rounds. Each has a default so a settings tab
    # from before it existed, which sends the drama object without it, still validates; the
    # save route then keeps what is stored for whatever was not sent.
    drama_stage_models: dict[Stage, StageModel] | None = None
    drama_stage_instructions: dict[Stage, StandingText] = Field(default_factory=dict)
    drama_voice: VoiceSettings | None = None
    drama_caption_locales: list[CaptionLocale] = Field(default_factory=list, max_length=4)
    drama_auto_approve_audio: bool = True
    drama_auto_approve_final: bool = True
    drama_max_verify_rounds: int = Field(default=3, ge=1, le=5)
    drama_max_retake_rounds: int = Field(default=2, ge=0, le=5)

    @field_validator("drama_stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel] | None) -> dict[Stage, StageModel] | None:
        return None if value is None else _every_stage(value)

    @field_validator("drama_stage_instructions")
    @classmethod
    def _kept(cls, value: dict[Stage, str]) -> dict[Stage, str]:
        return _kept_instructions(value)

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        voices = [(voice.provider, voice.name) for voice in self.character_voice_pool]
        if len(set(voices)) != len(voices):
            raise ValueError("character_voice_pool must not repeat a voice")
        if len(set(self.drama_caption_locales)) != len(self.drama_caption_locales):
            raise ValueError("drama_caption_locales must not repeat")
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
    target_minutes_min: int = Field(ge=EPISODE_MIN_MINUTES, le=30)
    target_minutes_max: int = Field(ge=EPISODE_MIN_MINUTES, le=30)
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


class StageModelsWrite(StrictModel):
    """The model of each stage, chosen on the AI settings page (PUT /settings/models).

    ``drama_stage_models`` sent as null means the drama follows the tutorial's; left out, the
    stored choice stays (docs/videos/DRAMA-FLOW.md §一).
    """

    stage_models: dict[Stage, StageModel]
    drama_stage_models: dict[Stage, StageModel] | None = None

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
        return _every_stage(value)

    @field_validator("drama_stage_models")
    @classmethod
    def _complete_drama(
        cls, value: dict[Stage, StageModel] | None
    ) -> dict[Stage, StageModel] | None:
        return None if value is None else _every_stage(value)


# The owner's licensed music file and sound-effect set, as tools/video names them (core/drama.mjs
# MUSIC_TRACK and SFX_SET): a bare file name under <work base>/_music/, a folder name under _sfx/.
MusicTrack = Annotated[
    str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9._-]{0,63}\.(?:mp3|m4a|wav|flac)$")
]
SfxSet = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9._-]{0,63}$")]


class SlidesSettings(StrictModel):
    """Illustrated slides (docs/videos/ILLUSTRATED.md): the pictures' switch, image model and
    per-video cap, whether the storyboard approves itself from the judge's scores, and the
    licensed music file and sound-effect set the worker gives every new video. Every field has
    a default, so a settings tab from before these existed, which sends nothing of them, still
    validates and keeps what is stored."""

    slides_media_enabled: bool = False
    # None follows the drama's image model.
    slides_image_model: str | None = Field(default=SLIDES_IMAGE_MODEL, min_length=1, max_length=128)
    slides_max_usd_per_video: int = Field(default=20, ge=0, le=10_000)
    slides_auto_approve_storyboard: bool = True
    slides_music_track: MusicTrack | None = None
    slides_sfx_set: SfxSet | None = None

    @field_validator("slides_image_model")
    @classmethod
    def _image_model(cls, value: str | None) -> str | None:
        return _known_image_model(value)


class SettingsWrite(_SettingsFields):
    stage_models: dict[Stage, StageModel]
    drama: DramaSettings
    # Illustrated slides (docs/videos/ILLUSTRATED.md), beside the drama's object.
    slides: SlidesSettings = Field(default_factory=SlidesSettings)
    stage_instructions: dict[Stage, StandingText] = Field(default_factory=dict)
    # The hands-off switches (docs/videos/HANDS-OFF.md). The stance is what this channel
    # believes, at most 4,000 characters; while it is blank Jev does not choose outlines.
    channel_stance: StandingText = ""
    auto_pick_outline: bool = True
    auto_approve_final: bool = True

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel]) -> dict[Stage, StageModel]:
        return _every_stage(value)

    @field_validator("stage_instructions")
    @classmethod
    def _kept(cls, value: dict[Stage, str]) -> dict[Stage, str]:
        return _kept_instructions(value)


class SettingsSave(StrictModel):
    """A save from the settings tab on /admin/videos.

    Every field may be left out, and a field left out (or sent as null) keeps its stored value:
    the tab is three parts (tutorial, drama, shared) each saved on its own
    (docs/videos/DRAMA-FLOW.md §一), the stage models are chosen on the AI settings page, and a
    page built before a field existed sends none of it. The route lays what was sent over what is
    stored and validates the whole as ``SettingsWrite``, which holds the bounds and the
    consistency rules; inside ``drama`` too, only the fields sent change.
    """

    enabled: bool | None = None
    draft_interval_hours: int | None = None
    topics_per_run: int | None = None
    max_waiting_drafts: int | None = None
    topic_scope: list[TopicWord] | None = None
    topic_avoid: list[TopicWord] | None = None
    topic_from_site: bool | None = None
    topic_from_search: bool | None = None
    voice: VoiceSettings | None = None
    target_minutes_min: int | None = None
    target_minutes_max: int | None = None
    caption_locales: list[CaptionLocale] | None = None
    max_drafts_per_month: int | None = None
    monthly_token_budget_millions: int | None = None
    max_verify_rounds: int | None = None
    max_retake_rounds: int | None = None
    auto_approve_audio: bool | None = None
    stage_models: dict[Stage, StageModel] | None = None
    drama: DramaSettings | None = None
    slides: SlidesSettings | None = None
    stage_instructions: dict[Stage, StandingText] | None = None
    channel_stance: StandingText | None = None
    auto_pick_outline: bool | None = None
    auto_approve_final: bool | None = None

    @field_validator("stage_models")
    @classmethod
    def _complete(cls, value: dict[Stage, StageModel] | None) -> dict[Stage, StageModel] | None:
        return None if value is None else _every_stage(value)

    @field_validator("stage_instructions")
    @classmethod
    def _kept(cls, value: dict[Stage, str] | None) -> dict[Stage, str] | None:
        return None if value is None else _kept_instructions(value)

    def merged_over(self, current: dict[str, Any]) -> dict[str, Any]:
        """The stored values with the fields this save sent laid over them.

        ``current`` is ``SettingsWrite.model_dump()`` of what is stored. A field left out or sent
        as null stays; ``drama`` and ``slides`` merge field by field, so a page from before one
        of their fields existed cannot reset it by sending the object without it.
        """
        sent = self.model_dump(exclude_unset=True)
        drama = sent.pop("drama", None)
        slides = sent.pop("slides", None)
        values = {**current, **{key: value for key, value in sent.items() if value is not None}}
        if drama is not None:
            values["drama"] = {**current["drama"], **drama}
        if slides is not None:
            values["slides"] = {**(current.get("slides") or {}), **slides}
        return values


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
    target_minutes: int = Field(default=3, ge=1, le=EXPLAINER_MAX_MINUTES, strict=True)
    note: str | None = Field(default=None, min_length=1, max_length=2000)

    @model_validator(mode="after")
    def _episode_length(self) -> Self:
        if self.style_preset == EXPLAINER_PRESET:
            if "target_minutes" not in self.model_fields_set:
                self.target_minutes = EXPLAINER_DEFAULT_MINUTES
            if self.target_minutes < EXPLAINER_MIN_MINUTES:
                raise ValueError(f"an explainer is at least {EXPLAINER_MIN_MINUTES} minutes")
        elif self.target_minutes > SERIES_MAX_MINUTES:
            raise ValueError(f"a drama episode is at most {SERIES_MAX_MINUTES} minutes")
        return self

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
    # The series this request is an episode of: a one-off drama's own one-episode series
    # (docs/videos/DRAMA-FLOW.md §二), or the long series it belongs to.
    series_slug: str | None = None
    episode_number: int | None = None
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
    # The video's format, so the prompt is kept under the right heading for the owner to read;
    # a worker from before the drama route sends none and is filed under slides.
    format: PromptFormat = "slides"
    # A series document (setting, outline, chapter), an episode, a recap or a fix: kept under
    # its own heading, and not counted as one of the month's drafts (docs/videos/SERIES.md).
    variant: str | None = Field(default=None, pattern=r"^[a-z][a-z0-9_-]{0,31}$")


class StageRunOut(StrictModel):
    # The whole output file (brief.md, video.json, a report…), exactly as it should be saved.
    text: str
    provider: ProviderName
    model: str
    input_tokens: int
    output_tokens: int
    usage: UsageView


class StagePromptView(StrictModel):
    """The instructions a stage was last sent for a format, as the worker composed them."""

    stage: Stage
    format: PromptFormat
    variant: str = ""
    slug: str
    instructions: str
    sent_at: datetime


class StagePromptsOut(StrictModel):
    prompts: list[StagePromptView]


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


# A long drama series (docs/videos/SERIES.md): the series, the documents the owner approves
# (the setting book, the whole-series outline, each chapter's detailed outline), the episode
# table, and what the worker asks for and reports.
SERIES_SLUG_PATTERN = r"^[a-z0-9][a-z0-9-]{1,39}$"
# A long series, a one-off drama (one episode, one story bible; docs/videos/DRAMA-FLOW.md §二), or
# a brand-story series (no documents; its episodes are a planned backlog; docs/videos/STORY.md).
SeriesKind = Literal["series", "one-off", "story"]
# How long one episode may run: a drama's episode, and a story, which is 12 to 15 minutes. The
# database allows the longer one for every kind (migration 0111); the schemas hold the rest to 8.
SERIES_MAX_MINUTES = 8
STORY_MAX_MINUTES = 20
# How many stories may start on one Asia/Taipei calendar day, at most.
STORY_MAX_PER_DAY = 12
SeriesStatus = Literal["setting", "outline", "active", "paused", "finished"]
SeriesAspect = Literal["world", "bonds", "structure", "mood"]
SeriesTone = Literal[
    "dual-male-leads-subtext", "dual-male-leads-explicit", "hetero-leads", "no-romance"
]
DocKind = Literal["setting", "outline", "chapter", "bible"]
DocStatus = Literal["generating", "review", "approved", "rejected"]
EpisodeStatus = Literal["planned", "ready", "queued", "started", "done", "skipped"]
SeriesJobKind = Literal["setting", "outline", "chapter", "bible", "episode", "compilation"]
# What the owner fills in for a one-off drama: every number is fixed at one.
ONE_OFF_EPISODES = 1
SeriesAction = Literal["plan-next-chapter", "start-next", "compile"]
# How much of every episode's ``beats`` a read of a series carries: all of it (the worker and the
# drama pages), or only what a list of a hundred stories shows (SUMMARY_BEAT_KEYS in series.py);
# one episode's whole plan is read on its own, from /series/{slug}/episodes/{number}.
SeriesBeatsRead = Literal["full", "summary"]
# A binge series (docs/videos/BINGE.md): the genre preset, who leads, and the visual tier.
SeriesGenre = Literal[
    "xianxia-bonds", "rebirth-revenge", "system-game", "urban-return", "empress-rise", "custom"
]
SeriesLead = Literal["female", "male", "dual-male"]
VisualTier = Literal["clips", "hybrid", "stills"]
MAX_DOC_MD_CHARS = 200_000
MAX_DOC_JSON_BYTES = 512 * 1024


class StoryLook(StrictModel):
    """The look every story of a story series shares (docs/videos/STORY.md §一支故事影片的規格):
    the image prompt's style, what the pictures must never show, and how the camera moves over
    a still. A story series has no setting book, so the series row keeps it (migration 0111)."""

    style: str = Field(min_length=1, max_length=600)
    negative: str = Field(min_length=1, max_length=400)
    motion: str | None = Field(default=None, min_length=1, max_length=400)

    @field_validator("style", "negative", "motion")
    @classmethod
    def _not_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("must not be blank")
        return value


def image_model_problem(model_id: str) -> str | None:
    """Why a series cannot name this image model, or None: it must be an image model of the
    media catalog that is not retired (app.video_media.catalog)."""
    found = [
        model
        for vendor in MEDIA_VENDORS
        if (model := find_model(vendor, "image", model_id)) is not None
    ]
    if not found:
        return f"{model_id} is not an image model of the media catalog"
    if all(model.status == "retired" for model in found):
        return f"{model_id} is retired"
    return None


def _known_image_model(value: str | None) -> str | None:
    if value is not None and (problem := image_model_problem(value)):
        raise ValueError(problem)
    return value


class SeriesIn(StrictModel):
    """What the owner fills in to start a series; the setting book is planned from it.

    The one-button form (docs/videos/BINGE.md) sends ``total_minutes`` and ``target_minutes``
    and leaves ``slug``, ``title`` and ``premise`` blank: the server derives the episode count
    and the chapter size, names the series after its genre, and lets the planner invent the
    premise from the genre preset. The classic form fills everything in as before.

    A ``one-off`` is one episode with one story bible: its numbers are fixed at one whatever
    was sent, and aspects and tone may be left out (docs/videos/DRAMA-FLOW.md §二). Only a
    one-off may take EXPLAINER_PRESET: the explainer has no cast, and the other kinds' prompts
    write one that the drama lint then refuses on every episode.

    A ``story`` series (docs/videos/STORY.md) is always hands-off, stills only and never
    compiled, needs its title, premise and shared look, and may run to STORY_MAX_MINUTES; its
    episodes come from the backlog import, not from documents. The daily count and the look
    belong to a story series only. A one-off explainer runs 8–20 minutes; drama episodes
    stay at SERIES_MAX_MINUTES.
    """

    slug: str | None = Field(default=None, pattern=SERIES_SLUG_PATTERN)
    kind: SeriesKind = "series"
    title: str | None = Field(default=None, max_length=200)
    premise: str = Field(default="", max_length=4000)
    aspects: list[SeriesAspect] = Field(default_factory=list, max_length=4)
    tone: SeriesTone = "dual-male-leads-subtext"
    style_preset: StylePreset = "cinematic-3d"
    target_minutes: int = Field(default=3, ge=1, le=STORY_MAX_MINUTES, strict=True)
    planned_episodes: int = Field(default=100, ge=1, le=500)
    episodes_per_chapter: int = Field(default=10, ge=1, le=20)
    open_ended: bool = True
    note: str | None = Field(default=None, min_length=1, max_length=2000)
    genre: SeriesGenre = "xianxia-bonds"
    lead: SeriesLead = "dual-male"
    hands_off: bool = False
    compilation: bool = False
    visual_tier: VisualTier = "clips"
    total_minutes: int | None = Field(default=None, ge=30, le=480)
    episodes_per_day: int | None = Field(default=None, ge=1, le=STORY_MAX_PER_DAY)
    image_model: str | None = Field(default=None, min_length=1, max_length=128)
    look: StoryLook | None = None

    @field_validator("title", "premise", "note")
    @classmethod
    def _trimmed(cls, value: str | None) -> str | None:
        return None if value is None else value.strip()

    @field_validator("image_model")
    @classmethod
    def _image_model(cls, value: str | None) -> str | None:
        return _known_image_model(value)

    @field_validator("aspects")
    @classmethod
    def _distinct(cls, value: list[SeriesAspect]) -> list[SeriesAspect]:
        if len(set(value)) != len(value):
            raise ValueError("aspects must not repeat")
        return value

    @model_validator(mode="after")
    def _enough_to_plan_from(self) -> Self:
        if self.note is not None and not self.note:
            raise ValueError("note must not be blank")
        if self.title is not None and not self.title:
            raise ValueError("title must not be blank")
        if self.style_preset == EXPLAINER_PRESET and self.kind != "one-off":
            raise ValueError(
                f'style_preset "{EXPLAINER_PRESET}" is for a one-off explainer only: '
                "a long series and a story series have a cast"
            )
        if self.style_preset == EXPLAINER_PRESET:
            if "target_minutes" not in self.model_fields_set:
                self.target_minutes = EXPLAINER_DEFAULT_MINUTES
            if self.target_minutes < EXPLAINER_MIN_MINUTES:
                raise ValueError(f"an explainer is at least {EXPLAINER_MIN_MINUTES} minutes")
        # A genre preset carries its own premise seed; a custom series has nothing else.
        if not self.premise and self.genre == "custom":
            raise ValueError("a custom series needs a premise")
        if self.total_minutes is None and not self.premise and self.genre == "xianxia-bonds":
            raise ValueError("premise must not be blank")
        if self.kind == "story":
            if not self.hands_off or self.visual_tier != "stills" or self.compilation:
                raise ValueError(
                    'a story series is hands_off, visual_tier "stills" and never a compilation'
                )
            if self.total_minutes is not None:
                raise ValueError("a story series takes its episodes from the backlog import")
            if not self.title or not self.premise:
                raise ValueError("a story series needs a title and a premise")
            if self.look is None:
                raise ValueError("a story series needs the look every story shares")
        else:
            if self.style_preset != EXPLAINER_PRESET and self.target_minutes > SERIES_MAX_MINUTES:
                raise ValueError(
                    f"a drama episode is at most {SERIES_MAX_MINUTES} minutes; "
                    "a story or a one-off explainer may run longer"
                )
            if self.episodes_per_day is not None or self.look is not None:
                raise ValueError("only a story series has a daily count and a shared look")
        if self.kind == "one-off":
            if self.total_minutes is not None:
                raise ValueError("a one-off drama is one episode, not a binge series")
            self.planned_episodes = ONE_OFF_EPISODES
            self.episodes_per_chapter = ONE_OFF_EPISODES
            self.open_ended = False
            self.compilation = False
        elif self.episodes_per_chapter < 4:
            raise ValueError("a series has at least 4 episodes per chapter")
        return self


class SeriesPatch(StrictModel):
    """What the owner may change later; a field left out stays as it is.

    The length may reach STORY_MAX_MINUTES and the daily count and the look may be set only on
    a story series; the service refuses them on the other kinds, which keep their limits.
    ``episodes_per_day`` or ``image_model`` sent as null lifts the daily limit or follows the
    settings tab again. EXPLAINER_PRESET stays a one-off's, and a one-off's bible fixes which
    side of it the one-off is on (series.patch_problem).
    """

    title: str | None = Field(default=None, min_length=1, max_length=200)
    premise: str | None = Field(default=None, min_length=1, max_length=4000)
    aspects: list[SeriesAspect] | None = Field(default=None, max_length=4)
    tone: SeriesTone | None = None
    style_preset: StylePreset | None = None
    target_minutes: int | None = Field(default=None, ge=1, le=STORY_MAX_MINUTES, strict=True)
    planned_episodes: int | None = Field(default=None, ge=1, le=500)
    episodes_per_chapter: int | None = Field(default=None, ge=4, le=20)
    open_ended: bool | None = None
    note: str | None = Field(default=None, max_length=2000)
    # Only these three: the others are set by the documents' decisions.
    status: Literal["active", "paused", "finished"] | None = None
    # The binge switches (docs/videos/BINGE.md): the owner may take a series back into their
    # own hands, or let it run, at any time; the tier is fixed once an episode started.
    lead: SeriesLead | None = None
    hands_off: bool | None = None
    compilation: bool | None = None
    visual_tier: VisualTier | None = None
    # A story series (docs/videos/STORY.md).
    episodes_per_day: int | None = Field(default=None, ge=1, le=STORY_MAX_PER_DAY)
    image_model: str | None = Field(default=None, min_length=1, max_length=128)
    look: StoryLook | None = None

    @field_validator("image_model")
    @classmethod
    def _image_model(cls, value: str | None) -> str | None:
        return _known_image_model(value)


class SeriesWithdrawnOut(BaseModel):
    """A drama the owner withdrew before any episode started, and how many of its queued
    requests were cancelled with it."""

    slug: str
    requests_cancelled: int


class SeriesDocOut(BaseModel):
    id: UUID
    kind: DocKind
    chapter_number: int
    version: int
    body_md: str
    body_json: dict[str, object]
    status: DocStatus
    note: str | None
    decided_at: datetime | None
    created_at: datetime
    # The owner's lines on this document's thread still waiting for the model
    # (docs/videos/DRAMA-FLOW.md §三).
    unanswered: int = 0
    # A Markdown-only edit is a draft until its production data is explicitly reconciled.
    needs_reconciliation: bool = False


class SeriesEpisodeOut(BaseModel):
    number: int
    chapter_number: int
    title: str
    logline: str
    beats: dict[str, object]
    status: EpisodeStatus
    slug: str | None
    recap: str | None
    started_at: datetime | None
    finished_at: datetime | None
    # The video the worker made of it, once it started, as /admin/videos lists it.
    video: dict[str, object] | None = None


# Why no story starts now (docs/videos/STORY.md §每日配額與排程): the series is paused or over, the
# day's count is reached (the Asia/Taipei calendar day), the episodes in the making fill
# ``series_max_in_flight``, the month's ``series_episodes_per_month`` is reached, the stories
# cleared for upload that the owner has not uploaded fill the buffer, or no story is ready.
StoryHold = Literal[
    "not_active", "per_day", "in_flight", "per_month", "upload_buffer", "none_ready"
]


class StoryQuotaOut(BaseModel):
    """Where a story series stands against its limits, and the reason no story starts now
    (``hold`` and the sentence the owner reads, ``hold_detail``), or None for both when the
    next one may. The same function decides the worker's next job, so the page and the worker
    cannot disagree. ``day`` is the Asia/Taipei calendar day ``started_today`` counts."""

    day: date
    started_today: int
    episodes_per_day: int | None
    in_flight: int
    max_in_flight: int
    started_this_month: int
    episodes_per_month: int
    awaiting_upload: int
    upload_buffer: int
    ready: int
    hold: StoryHold | None = None
    hold_detail: str | None = None


class SeriesSummary(BaseModel):
    id: UUID
    slug: str
    kind: SeriesKind = "series"
    title: str
    premise: str
    aspects: list[SeriesAspect]
    tone: SeriesTone
    style_preset: StylePreset
    target_minutes: int
    planned_episodes: int
    episodes_per_chapter: int
    chapters: int
    open_ended: bool
    status: SeriesStatus
    note: str | None
    requested_chapter: int | None
    force_next: bool
    episodes_done: int
    episodes_started: int
    episodes_ready: int
    docs_pending: int
    # The owner's lines on every thread of this series still waiting for the model.
    messages_pending: int = 0
    media_usd: float = 0.0
    clip_seconds: int = 0
    # The binge columns (docs/videos/BINGE.md); an older row reads as the classic series.
    genre: SeriesGenre = "xianxia-bonds"
    lead: SeriesLead = "dual-male"
    hands_off: bool = False
    compilation: bool = False
    visual_tier: VisualTier = "clips"
    total_minutes: int | None = None
    compilation_slug: str | None = None
    compilation_started_at: datetime | None = None
    compilation_finished_at: datetime | None = None
    # The brand-story columns (docs/videos/STORY.md): the daily count, the image model (None
    # follows the settings tab) and the shared look; the other kinds leave them None. The worker's
    # episode job reads them here with the kind and the length, and needs no second request.
    episodes_per_day: int | None = None
    image_model: str | None = None
    look: dict[str, object] | None = None
    # A story series' standing against its limits, on the owner's reads (the list and the series
    # page); None for the other kinds and wherever the worker reads a summary.
    quota: StoryQuotaOut | None = None
    created_at: datetime
    updated_at: datetime


class SeriesOut(SeriesSummary):
    # The latest version of every document, and every planned episode.
    docs: list[SeriesDocOut]
    episodes: list[SeriesEpisodeOut]


class SeriesListOut(BaseModel):
    series: list[SeriesSummary]


class SeriesDocDecisionIn(StrictModel):
    decision: Literal["approve", "reject"]
    note: str | None = Field(default=None, max_length=2000)
    expected_version: int = Field(ge=1)


class SeriesDocEditIn(StrictModel):
    """The owner rewrites a document: a new version, already approved or waiting as asked."""

    body_md: str = Field(min_length=1, max_length=MAX_DOC_MD_CHARS)
    body_json: dict[str, object] | None = None
    approve: bool = False


class SeriesEpisodeEditIn(StrictModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    logline: str | None = Field(default=None, max_length=2000)
    beats: dict[str, object] | None = None


class SeriesActionOut(BaseModel):
    series: SeriesSummary
    detail: str


class SeriesDocSubmitIn(StrictModel):
    """A document the worker planned: a new version that waits for the owner.

    A hands-off series (docs/videos/BINGE.md) sends the checker's ``judge`` verdict with it:
    the server approves the version on arrival when the verdict passes, or sends it back for a
    rewrite with the verdict's problems as the note.
    """

    kind: DocKind
    chapter_number: int = Field(default=0, ge=0, le=200)
    body_md: str = Field(min_length=1, max_length=MAX_DOC_MD_CHARS)
    body_json: dict[str, object] = Field(default_factory=dict)
    judge: dict[str, object] | None = None


class SeriesContextOut(BaseModel):
    """Production uses approved documents; discussion may read explicitly labelled drafts."""

    series: SeriesSummary
    setting: SeriesDocOut | None
    outline: SeriesDocOut | None
    chapter: SeriesDocOut | None
    chapter_number: int | None
    chapter_range: tuple[int, int] | None
    episode: SeriesEpisodeOut | None
    episodes: list[SeriesEpisodeOut]
    recaps: list[dict[str, object]]
    mysteries: list[dict[str, object]]
    # Every finished episode's recap, one line each, for the compilation's title and
    # description (docs/videos/BINGE.md); the three above are the full recent ones.
    all_recaps: list[dict[str, object]] = Field(default_factory=list)


class SeriesJob(BaseModel):
    kind: SeriesJobKind
    series: SeriesSummary
    chapter_number: int | None = None
    episode: SeriesEpisodeOut | None = None
    # The version the worker is rewriting, with the owner's note, when a document was sent back.
    previous: SeriesDocOut | None = None
    rewrites_left: int = 0
    context: SeriesContextOut


class SeriesJobOut(BaseModel):
    job: SeriesJob | None


class SeriesEpisodeStartIn(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)


class SeriesEpisodeStartOut(BaseModel):
    request: DramaRequestOut
    episode: SeriesEpisodeOut
    context: SeriesContextOut


class SeriesEpisodeRecapIn(StrictModel):
    recap: str = Field(min_length=1, max_length=4000)
    state: dict[str, object] = Field(default_factory=dict)


# The discussion thread on a document or a screenplay (docs/videos/DRAMA-FLOW.md §三): the owner
# writes a line, the worker's next round has the planner or the writer answer it, with a new
# version of the document when the owner asked for a change.
MESSAGE_SUBJECT_PATTERN = r"^(setting|outline|chapter:\d+|bible|script:\d+)$"
MESSAGE_BODY_MAX_CHARS = 8_000
MessageAuthor = Literal["owner", "planner", "writer"]
MessageTarget = Literal["doc", "script"]


class MessageIn(StrictModel):
    subject: str = Field(pattern=MESSAGE_SUBJECT_PATTERN)
    body: str = Field(min_length=1, max_length=MESSAGE_BODY_MAX_CHARS)

    @field_validator("body")
    @classmethod
    def _trimmed(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("must not be blank")
        return text


class MessageOut(BaseModel):
    id: UUID
    subject: str
    author: MessageAuthor
    body_md: str
    # The version the line was said about: a document's "v3", or the screenplay's SHA-256
    # cut to 12 characters; None when the document did not exist yet.
    refers_to: str | None
    answered_at: datetime | None
    created_at: datetime
    created_by_user_id: UUID | None


class MessagesOut(BaseModel):
    messages: list[MessageOut]


class MessageJob(BaseModel):
    """The oldest line waiting for the model, with everything the model reads to answer it."""

    message: MessageOut
    thread: list[MessageOut]
    series: SeriesSummary
    subject: str
    target: MessageTarget
    # The document's latest version, for a document thread; None before the first version.
    doc: SeriesDocOut | None
    # The episode whose screenplay is discussed, for a script thread (its slug names the video).
    episode: SeriesEpisodeOut | None
    context: SeriesContextOut
    # Echo this opaque snapshot with a revised document; stale answers keep only their reply.
    revision_context: str | None = None


class MessageJobOut(BaseModel):
    job: MessageJob | None


class RevisedDocIn(StrictModel):
    body_md: str = Field(min_length=1, max_length=MAX_DOC_MD_CHARS)
    body_json: dict[str, object] = Field(default_factory=dict)


class MessageAnswerIn(StrictModel):
    """The model's answer: a reply, and the revised document when the owner asked for a change.
    A screenplay's revision is written by the worker itself, so ``revised`` is ignored there."""

    reply_md: str = Field(min_length=1, max_length=MESSAGE_BODY_MAX_CHARS)
    revised: RevisedDocIn | None = None
    revision_context: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")


class MessageAnswerOut(BaseModel):
    reply: MessageOut
    # The new version filed from ``revised``, waiting for the owner; None when nothing was
    # revised, or the document was approved meanwhile.
    revision: SeriesDocOut | None
    revision_refused: str | None = None


class SeriesCompilationStartIn(StrictModel):
    slug: str = Field(pattern=SLUG_PATTERN)


class SeriesCompilationStartOut(BaseModel):
    """The compilation the worker just started: the episodes to join, in order, and the
    context its title, description and thumbnail are planned from."""

    series: SeriesSummary
    episodes: list[SeriesEpisodeOut]
    context: SeriesContextOut


class BudgetLine(BaseModel):
    needed: int
    monthly: int
    ok: bool


class BingeQuoteOut(BaseModel):
    """What one binge series would take (docs/videos/BINGE.md): the shape the server derives
    from the minutes, the media it needs at the settings' prices, and the month's budgets."""

    episodes: int
    chapters: int
    episodes_per_chapter: int
    clip_seconds: int
    images: int
    judge_calls: int
    usd: float
    budgets: dict[str, BudgetLine]
    ok: bool
