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


def _kept_instructions(value: dict[Stage, str]) -> dict[Stage, str]:
    """A field emptied on the settings tab drops that stage's standing instructions."""
    return {stage: text for stage, text in value.items() if text}


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


class SettingsSave(_SettingsFields):
    """A save from the settings tab on /admin/videos.

    The stage models are chosen on the AI settings page; a save that leaves them out keeps
    the stored ones, so the videos page cannot put back models it loaded earlier. The drama
    settings, the standing instructions, the channel stance and the hands-off switches follow
    the same rule, so a page built before they existed cannot reset them.
    """

    stage_models: dict[Stage, StageModel] | None = None
    drama: DramaSettings | None = None
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
SeriesStatus = Literal["setting", "outline", "active", "paused", "finished"]
SeriesAspect = Literal["world", "bonds", "structure", "mood"]
SeriesTone = Literal[
    "dual-male-leads-subtext", "dual-male-leads-explicit", "hetero-leads", "no-romance"
]
DocKind = Literal["setting", "outline", "chapter"]
DocStatus = Literal["generating", "review", "approved", "rejected"]
EpisodeStatus = Literal["planned", "ready", "queued", "started", "done", "skipped"]
SeriesJobKind = Literal["setting", "outline", "chapter", "episode", "compilation"]
SeriesAction = Literal["plan-next-chapter", "start-next", "compile"]
# A binge series (docs/videos/BINGE.md): the genre preset, who leads, and the visual tier.
SeriesGenre = Literal[
    "xianxia-bonds", "rebirth-revenge", "system-game", "urban-return", "empress-rise", "custom"
]
SeriesLead = Literal["female", "male", "dual-male"]
VisualTier = Literal["clips", "hybrid", "stills"]
MAX_DOC_MD_CHARS = 200_000
MAX_DOC_JSON_BYTES = 512 * 1024


class SeriesIn(StrictModel):
    """What the owner fills in to start a series; the setting book is planned from it.

    The one-button form (docs/videos/BINGE.md) sends ``total_minutes`` and ``target_minutes``
    and leaves ``slug``, ``title`` and ``premise`` blank: the server derives the episode count
    and the chapter size, names the series after its genre, and lets the planner invent the
    premise from the genre preset. The classic form fills everything in as before.
    """

    slug: str | None = Field(default=None, pattern=SERIES_SLUG_PATTERN)
    title: str | None = Field(default=None, max_length=200)
    premise: str = Field(default="", max_length=4000)
    aspects: list[SeriesAspect] = Field(default_factory=list, max_length=4)
    tone: SeriesTone = "dual-male-leads-subtext"
    style_preset: StylePreset = "cinematic-3d"
    target_minutes: int = Field(default=3, ge=1, le=8)
    planned_episodes: int = Field(default=100, ge=1, le=500)
    episodes_per_chapter: int = Field(default=10, ge=4, le=20)
    open_ended: bool = True
    note: str | None = Field(default=None, min_length=1, max_length=2000)
    genre: SeriesGenre = "xianxia-bonds"
    lead: SeriesLead = "dual-male"
    hands_off: bool = False
    compilation: bool = False
    visual_tier: VisualTier = "clips"
    total_minutes: int | None = Field(default=None, ge=30, le=480)

    @field_validator("title", "premise", "note")
    @classmethod
    def _trimmed(cls, value: str | None) -> str | None:
        return None if value is None else value.strip()

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
        # A genre preset carries its own premise seed; a custom series has nothing else.
        if not self.premise and self.genre == "custom":
            raise ValueError("a custom series needs a premise")
        if self.total_minutes is None and not self.premise and self.genre == "xianxia-bonds":
            raise ValueError("premise must not be blank")
        return self


class SeriesPatch(StrictModel):
    """What the owner may change later; a field left out stays as it is."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    premise: str | None = Field(default=None, min_length=1, max_length=4000)
    aspects: list[SeriesAspect] | None = Field(default=None, max_length=4)
    tone: SeriesTone | None = None
    style_preset: StylePreset | None = None
    target_minutes: int | None = Field(default=None, ge=1, le=8)
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


class SeriesSummary(BaseModel):
    id: UUID
    slug: str
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
    """What the prompts need: the approved documents, the episodes so far and the recaps."""

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
