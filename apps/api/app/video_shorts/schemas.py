"""What the Shorts endpoints take and answer (docs/videos/SHORTS.md §端點)."""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal, Self, get_args
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from app.video_automation.schemas import Stage, StageModel, VoiceSettings
from app.video_shorts.models import DEFAULT_MAX_PER_MONTH

ShortsLine = Literal["lab", "cut", "drama"]
SubjectVariant = Literal["a", "b"]
ShortsFilter = Literal["only", "exclude"]
# Where a Short stands, as the tab groups them (docs/videos/SHORTS.md §一支 Shorts 的一生).
ShortsState = Literal[
    "making", "needs_you", "library", "slotted", "scheduled", "published", "missed", "dropped"
]
SlotStatus = Literal[
    "open", "planned", "assigned", "locked", "scheduled", "published", "missed", "skipped"
]
MetricPeriod = Literal["d1", "d3", "d7", "now"]
MetricSource = Literal["data_api", "analytics_api", "studio_export"]
CostStatus = Literal["confirmed", "reserved", "unknown"]
CostSource = Literal["auto", "manual"]
CostCategory = Literal[
    "narration",
    "models",
    "checks",
    "media",
    "image",
    "clip",
    "music",
    "subscription",
    "tool",
    "other",
]
ShortsLocale = Literal["en", "ja", "ko", "zh-CN"]
ConsentState = Literal["none", "valid", "expiring", "expired", "invalid"]
AutopublishState = Literal["off", "on", "paused", "expiring", "expired", "invalid"]
SlotAction = Literal["move", "assign", "clear", "skip", "reopen", "note"]

LINES: tuple[ShortsLine, ...] = ("lab", "cut", "drama")
SHORTS_LOCALES: tuple[ShortsLocale, ...] = ("en", "ja", "ko", "zh-CN")
SLUG_PATTERN = r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$"
# A series of the experiments line (daily, blind, prompts), or the slug of the tutorial or the
# drama a highlight or a vertical short was cut from.
SHORTS_SERIES_PATTERN = r"^[a-z0-9][a-z0-9-]{0,39}$"
SLOT_TIME = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
SlotTime = Annotated[str, StringConstraints(pattern=SLOT_TIME.pattern)]
CurrencyCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]
Note = Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]
MAX_PATTERN_DAYS = 366


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --- settings -----------------------------------------------------------------------------------


class PatternSegment(StrictModel):
    """A stretch of the run: for ``days`` days, publish ``counts`` a day, in turn."""

    days: int = Field(ge=1, le=MAX_PATTERN_DAYS)
    counts: list[Annotated[int, Field(ge=0, le=4)]] = Field(min_length=1, max_length=14)


class SettingsWrite(StrictModel):
    enabled: bool
    lines: list[ShortsLine] = Field(min_length=1, max_length=3)
    weekly_quota: dict[ShortsLine, Annotated[int, Field(ge=0, le=28)]]
    daily_pattern: list[PatternSegment] = Field(min_length=1, max_length=12)
    slot_times: list[SlotTime] = Field(min_length=1, max_length=4)
    timezone: str = Field(min_length=1, max_length=64)
    stock_days: int = Field(ge=0, le=30)
    lock_hours: int = Field(ge=1, le=72)
    upload_ahead_days: int = Field(ge=1, le=30)
    max_per_day: int = Field(ge=1, le=4)
    seconds_min: int = Field(ge=10, le=180)
    seconds_max: int = Field(ge=10, le=180)
    voice: VoiceSettings
    locales: list[ShortsLocale] = Field(default_factory=list, max_length=4)
    made_for_kids: bool = False
    auto_approve: bool = True
    budget_ntd_30d: int = Field(ge=0, le=1_000_000)
    budget_soft_ntd: int = Field(ge=0, le=1_000_000)
    budget_total_ntd: int = Field(ge=0, le=10_000_000)
    # Phase two: the models an experiment tests under a and b (b left out tests a's model),
    # and how many Shorts the worker may start in a month (docs/videos/SHORTS.md §端點).
    subject_models: dict[SubjectVariant, StageModel] = Field(default_factory=dict)
    max_per_month: int = Field(default=DEFAULT_MAX_PER_MONTH, ge=0, le=400)
    # The Shorts' own model for each of the six stages, chosen on the AI settings page; None
    # follows the tutorial's (app/video_automation/ai.py stage_choice). Like the drama's, a
    # choice names every stage.
    stage_models: dict[Stage, StageModel] | None = None

    @field_validator("stage_models")
    @classmethod
    def _every_stage_or_none(
        cls, value: dict[Stage, StageModel] | None
    ) -> dict[Stage, StageModel] | None:
        if not value:
            return None
        missing = set(get_args(Stage)) - set(value)
        if missing:
            raise ValueError(f"stage_models is missing {', '.join(sorted(missing))}")
        return value

    @field_validator("lines")
    @classmethod
    def _lines_once_in_order(cls, value: list[ShortsLine]) -> list[ShortsLine]:
        if len(set(value)) != len(value):
            raise ValueError("lines must not repeat")
        return [line for line in LINES if line in value]

    @field_validator("locales")
    @classmethod
    def _locales_once_in_order(cls, value: list[ShortsLocale]) -> list[ShortsLocale]:
        if len(set(value)) != len(value):
            raise ValueError("locales must not repeat")
        return [locale for locale in SHORTS_LOCALES if locale in value]

    @field_validator("timezone")
    @classmethod
    def _known_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise ValueError(f"{value} is not a timezone the server knows") from error
        return value

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        if len(set(self.slot_times)) != len(self.slot_times):
            raise ValueError("slot_times must not repeat")
        if self.seconds_min > self.seconds_max:
            raise ValueError("seconds_min must not exceed seconds_max")
        if self.budget_soft_ntd > self.budget_ntd_30d:
            raise ValueError("budget_soft_ntd must not exceed budget_ntd_30d")
        if sum(segment.days for segment in self.daily_pattern) > MAX_PATTERN_DAYS:
            raise ValueError(f"daily_pattern covers more than {MAX_PATTERN_DAYS} days")
        most = max(count for segment in self.daily_pattern for count in segment.counts)
        if most < 1:
            raise ValueError("daily_pattern publishes nothing")
        if most > self.max_per_day:
            raise ValueError("daily_pattern asks for more a day than max_per_day")
        if most > len(self.slot_times):
            raise ValueError("daily_pattern asks for more a day than there are slot_times")
        for line in self.weekly_quota:
            if line not in self.lines and self.weekly_quota[line] > 0:
                raise ValueError(f"weekly_quota names {line}, which is not one of lines")
        return self


class SettingsSave(StrictModel):
    """A save from the Shorts settings: a field left out (or null) keeps its stored value,
    except ``stage_models``, where null means the Shorts follow the tutorial's models."""

    enabled: bool | None = None
    lines: list[ShortsLine] | None = None
    weekly_quota: dict[ShortsLine, int] | None = None
    daily_pattern: list[PatternSegment] | None = None
    slot_times: list[SlotTime] | None = None
    timezone: str | None = None
    stock_days: int | None = None
    lock_hours: int | None = None
    upload_ahead_days: int | None = None
    max_per_day: int | None = None
    seconds_min: int | None = None
    seconds_max: int | None = None
    voice: VoiceSettings | None = None
    locales: list[ShortsLocale] | None = None
    made_for_kids: bool | None = None
    auto_approve: bool | None = None
    budget_ntd_30d: int | None = None
    budget_soft_ntd: int | None = None
    budget_total_ntd: int | None = None
    subject_models: dict[SubjectVariant, StageModel] | None = None
    max_per_month: int | None = None
    stage_models: dict[Stage, StageModel] | None = None

    def merged_over(self, current: dict[str, Any]) -> dict[str, Any]:
        sent = self.model_dump(exclude_unset=True)
        values = {**current, **{key: value for key, value in sent.items() if value is not None}}
        if "stage_models" in self.model_fields_set and self.stage_models is None:
            values["stage_models"] = None
        return values


class ConsentOffer(BaseModel):
    """What the owner would agree to now: the wording, its hash and the scope it names."""

    text: str
    text_sha256: str
    scope: dict[str, Any]


class ConsentView(BaseModel):
    state: ConsentState
    problem: str | None = None
    granted_at: datetime | None = None
    granted_by_user_id: UUID | None = None
    expires_at: datetime | None = None
    text_sha256: str | None = None
    scope: dict[str, Any] | None = None
    # None while no channel is linked: there is nothing to agree to yet.
    offer: ConsentOffer | None = None


class SettingsView(SettingsWrite):
    campaign_start: date | None = None
    autopublish: bool = False
    paused_at: datetime | None = None
    consent: ConsentView
    updated_at: datetime | None = None


class ToolSettingsView(SettingsWrite):
    """What the tool and the worker read: the settings, and whether publishing is held."""

    campaign_start: date | None = None
    paused: bool = False
    updated_at: datetime | None = None


class AutopublishIn(StrictModel):
    """The owner's agreement, naming the wording they read by its hash."""

    text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class CampaignStartIn(StrictModel):
    first_day: date


class CampaignOut(BaseModel):
    campaign_start: date
    last_day: date
    slots: int
    assigned: int


# --- the calendar -------------------------------------------------------------------------------


class SlotOut(BaseModel):
    id: UUID
    starts_at: datetime
    local_date: date
    local_time: str
    phase: int
    line: ShortsLine | None = None
    series: str | None = None
    topic_slug: str | None = None
    project_slug: str | None = None
    project_title: str | None = None
    project_line: ShortsLine | None = None
    youtube_video_id: str | None = None
    status: SlotStatus
    locked_at: datetime | None = None
    note: str | None = None


class SlotsOut(BaseModel):
    timezone: str
    slots: list[SlotOut]


class SlotPatch(StrictModel):
    """One change to a slot: move it, give it a Short, take the Short out, skip the slot,
    open a skipped one again, or write a note."""

    action: SlotAction
    starts_at: AwareDatetime | None = None
    project_slug: str | None = Field(default=None, pattern=SLUG_PATTERN)
    note: Note | None = None

    @model_validator(mode="after")
    def _carries_what_the_action_needs(self) -> Self:
        if self.action == "move" and self.starts_at is None:
            raise ValueError("move needs starts_at")
        if self.action == "assign" and self.project_slug is None:
            raise ValueError("assign needs project_slug")
        if self.action == "note" and self.note is None:
            raise ValueError("note needs note")
        return self


# --- the ledger ---------------------------------------------------------------------------------

Money = Annotated[Decimal, Field(ge=0, le=1_000_000, max_digits=12, decimal_places=4)]
Rate = Annotated[Decimal, Field(gt=0, le=100_000, max_digits=14, decimal_places=6)]


class CostIn(StrictModel):
    """A line the owner enters: a subscription, a tool fee. An amount the vendor did not
    report is entered as unknown, never as zero."""

    occurred_at: AwareDatetime | None = None
    project_slug: str | None = Field(default=None, pattern=SLUG_PATTERN)
    category: CostCategory
    status: Literal["confirmed", "unknown"] = "confirmed"
    amount: Money | None = None
    currency: CurrencyCode = "TWD"
    # Left out, the server looks the day's rate up.
    fx_rate: Rate | None = None
    note: Note | None = None

    @model_validator(mode="after")
    def _amount_matches_status(self) -> Self:
        if self.status == "confirmed" and self.amount is None:
            raise ValueError("a confirmed line needs an amount")
        if self.status == "unknown" and self.amount is not None:
            raise ValueError("an unknown line carries no amount")
        return self


class CostPatch(StrictModel):
    """A correction to a line: what is left out stays."""

    occurred_at: AwareDatetime | None = None
    category: CostCategory | None = None
    status: Literal["confirmed", "unknown"] | None = None
    amount: Money | None = None
    currency: CurrencyCode | None = None
    fx_rate: Rate | None = None
    note: Note | None = None


class CostOut(BaseModel):
    id: UUID
    occurred_at: datetime
    project_slug: str | None = None
    category: str
    amount: float | None = None
    currency: str
    fx_rate: float | None = None
    amount_ntd: float | None = None
    status: CostStatus
    source: CostSource
    units: dict[str, Any] | None = None
    note: str | None = None
    created_at: datetime


class BudgetOut(BaseModel):
    """Where the spending stands against the owner's limits, in New Taiwan dollars."""

    period_start: datetime
    period_end: datetime
    spent_ntd: float
    reserved_ntd: float
    unknown: int
    limit_ntd: int
    soft_ntd: int
    total_start: datetime
    total_spent_ntd: float
    total_limit_ntd: int
    paid_work_allowed: bool
    reason: str | None = None


class PeriodTotal(BaseModel):
    start: datetime
    end: datetime
    spent_ntd: float
    reserved_ntd: float
    unknown: int
    lines: int


class CostsOut(BaseModel):
    items: list[CostOut]
    budget: BudgetOut
    periods: list[PeriodTotal]


# What a final review's ``payload.usage`` carries, written by ``tools/video/shorts`` when it
# pushes: the server cannot attribute narration or model calls to one video itself, since
# /video/speech takes no slug. Read leniently, as a payload from an older tool may lack parts.


class NarrationUsage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    seconds: float = Field(default=0, ge=0, le=36_000)
    characters: int = Field(default=0, ge=0, le=1_000_000)
    calls: int = Field(default=0, ge=0, le=100_000)
    provider: str | None = Field(default=None, max_length=40)
    model: str | None = Field(default=None, max_length=128)


class StageUsage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    calls: int = Field(default=0, ge=0, le=100_000)
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    provider: str | None = Field(default=None, max_length=40)
    model: str | None = Field(default=None, max_length=128)


class UsageReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    narration: NarrationUsage | None = None
    stages: dict[str, StageUsage] = Field(default_factory=dict)
    checks: dict[str, Annotated[int, Field(ge=0, le=100_000)]] = Field(default_factory=dict)


# --- the numbers --------------------------------------------------------------------------------


class MetricOut(BaseModel):
    period: MetricPeriod
    source: MetricSource
    captured_at: datetime
    range_start: date | None = None
    range_end: date | None = None
    views: int | None = None
    engaged_views: int | None = None
    likes: int | None = None
    comments: int | None = None
    shares: int | None = None
    subscribers_gained: int | None = None
    avg_view_seconds: float | None = None
    avg_view_percent: float | None = None
    stayed_percent: float | None = None


class ShortMetrics(BaseModel):
    slug: str
    title: str
    line: ShortsLine | None = None
    series: str | None = None
    youtube_video_id: str
    published_at: datetime | None = None
    removed_at: datetime | None = None
    # A dropped Short is read no more (stats.read_due), so its open windows stay empty.
    dropped_at: datetime | None = None
    snapshots: list[MetricOut]


class MetricsOut(BaseModel):
    items: list[ShortMetrics]


# --- the top row --------------------------------------------------------------------------------


class NeedOut(BaseModel):
    """One thing that waits for the owner, in a sentence, with what it is about."""

    kind: Literal[
        "consent", "channel", "worker", "missed", "budget", "upload", "review", "blocked", "stock"
    ]
    detail: str
    slug: str | None = None
    count: int = 1


class ChannelOut(BaseModel):
    linked: bool
    title: str | None = None
    audited: bool = False
    problem: str | None = None


class StockOut(BaseModel):
    # Approved Shorts that hold no slot, and how many coming days of slots they would fill;
    # None before the run has a calendar.
    count: int
    days: int | None = None
    wanted_days: int


class CampaignView(BaseModel):
    start: date | None = None
    last_day: date | None = None
    slots: int = 0
    published: int = 0
    missed: int = 0


class OverviewOut(BaseModel):
    autopublish: AutopublishState
    autopublish_problem: str | None = None
    consent_expires_at: datetime | None = None
    paused_at: datetime | None = None
    timezone: str
    today: list[SlotOut]
    tomorrow: list[SlotOut]
    stock: StockOut
    budget: BudgetOut
    channel: ChannelOut
    worker_seen_at: datetime | None = None
    campaign: CampaignView
    needs: list[NeedOut]
    needs_count: int


# --- sending to YouTube -------------------------------------------------------------------------

ClaimResult = Literal["matched", "not_found", "not_private", "length_differs", "duplicate"]


class UploadWaiting(BaseModel):
    """A Short the owner uploads to YouTube Studio themselves, until the API audit passes."""

    slug: str
    title: str
    line: ShortsLine | None = None
    slot_at: datetime
    file_name: str
    size: int | None = None
    seconds: float | None = None


class UploadsOut(BaseModel):
    ahead_days: int
    items: list[UploadWaiting]


class ClaimItem(BaseModel):
    slug: str
    file_name: str
    result: ClaimResult
    detail: str
    youtube_video_id: str | None = None


class ClaimOut(BaseModel):
    claimed: int
    items: list[ClaimItem]


class RecallItem(BaseModel):
    slug: str
    youtube_video_id: str
    recalled: bool
    detail: str


class RecallOut(BaseModel):
    recalled: int
    items: list[RecallItem]


class TickOut(BaseModel):
    """What one knock of the worker did. Counts only: no address, token or content."""

    ran: bool
    skipped: str | None = None
    locked: int = 0
    missed: int = 0
    sent: int = 0
    held: int = 0
    scheduled: int = 0
    published: int = 0
    snapshots: int = 0
    removed: int = 0
    verified: bool = False
    quota_units: int = 0


# --- phase two: topics, the weekly plan, the worker's jobs and the weekly report ----------------

TopicStatus = Literal["idea", "ready", "needs_assets", "making", "made", "dropped"]
TopicOrigin = Literal["campaign", "planner", "owner", "auto"]
# What an experiment needs beyond text in and text out. The subscription runner takes text
# only, so a model that must look at a picture or edit one needs a keyed vision model; a
# program a model wrote needs an isolated place to run it; a generated picture costs money.
Requirement = Literal["vision", "image_edit", "sandbox", "image_generation"]
JobKind = Literal["report", "plan", "brief", "make"]
# A topic's slug is the Short's video slug, so it follows the Shorts tool's rule (a letter
# first, at least three characters) and the stores' (no hyphen at the end).
TOPIC_SLUG_PATTERN = r"^[a-z][a-z0-9-]{1,78}[a-z0-9]$"
NEED_KEY_PATTERN = r"^[a-z][a-z0-9-]{0,39}$"
TEST_PROTOCOL_FIELDS: tuple[str, ...] = (
    "setup",
    "input",
    "condition_a",
    "condition_b",
    "runs",
    "scoring",
    "failure_path",
)
SpecText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]
SpecLine = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=600)]
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Hook = Annotated[str, StringConstraints(strip_whitespace=True, max_length=300)]


class ProtocolSpec(StrictModel):
    """The experiment, frozen before it runs: the setup, the input, the two conditions, how
    many runs, how it is scored, and what happens when a run fails."""

    setup: SpecText | None = None
    input: SpecText | None = None
    condition_a: SpecText | None = None
    condition_b: SpecText | None = None
    runs: SpecText | None = None
    scoring: SpecText | None = None
    failure_path: SpecText | None = None


class OutlineBeat(StrictModel):
    seconds: str | None = Field(default=None, max_length=20)
    voice: str | None = Field(default=None, max_length=400)
    visual: str | None = Field(default=None, max_length=400)


class TopicBrief(StrictModel):
    """A topic's spec. The experiments line needs the seven protocol fields, at least one
    truth check and at least one acceptance item before it is ready; a highlight or a drama
    short needs its source video, which is the topic's ``source_slug``."""

    test_protocol: ProtocolSpec = Field(default_factory=ProtocolSpec)
    truth_check: list[SpecLine] = Field(default_factory=list, max_length=20)
    acceptance: list[SpecLine] = Field(default_factory=list, max_length=20)
    narration_outline: list[OutlineBeat] = Field(default_factory=list, max_length=20)
    titles: list[SpecLine] = Field(default_factory=list, max_length=6)
    source_material: list[SpecLine] = Field(default_factory=list, max_length=20)
    source_ids: list[Annotated[str, StringConstraints(max_length=120)]] = Field(
        default_factory=list, max_length=20
    )
    estimated_seconds: int | None = Field(default=None, ge=10, le=180)
    requires: list[Requirement] = Field(default_factory=list, max_length=4)
    notes: str | None = Field(default=None, max_length=4000)

    @field_validator("requires")
    @classmethod
    def _once(cls, value: list[Requirement]) -> list[Requirement]:
        return sorted(set(value))


class AssetNeed(StrictModel):
    """Something only the owner can supply: ``count`` files under ``key``."""

    key: str = Field(pattern=NEED_KEY_PATTERN)
    label: str = Field(min_length=1, max_length=200)
    count: int = Field(default=1, ge=1, le=10)


class TopicIn(StrictModel):
    """A topic the planner wrote, or an idea the owner typed. The planner names its slug;
    the owner's idea is given one."""

    slug: str | None = Field(default=None, pattern=TOPIC_SLUG_PATTERN)
    line: ShortsLine = "lab"
    series: str | None = Field(default=None, pattern=SHORTS_SERIES_PATTERN)
    title: Title
    hook: Hook | None = None
    brief: TopicBrief = Field(default_factory=TopicBrief)
    source_slug: str | None = Field(default=None, pattern=SLUG_PATTERN)
    assets_needed: list[AssetNeed] = Field(default_factory=list, max_length=6)
    release_order: int | None = Field(default=None, ge=0, le=100_000)

    @model_validator(mode="after")
    def _needs_once(self) -> Self:
        keys = [need.key for need in self.assets_needed]
        if len(set(keys)) != len(keys):
            raise ValueError("assets_needed keys must not repeat")
        return self


class TopicsIn(StrictModel):
    topics: list[TopicIn] = Field(min_length=1, max_length=30)

    @model_validator(mode="after")
    def _named(self) -> Self:
        slugs = [topic.slug for topic in self.topics]
        if any(slug is None for slug in slugs):
            raise ValueError("every topic the planner writes names its slug")
        if len(set(slugs)) != len(slugs):
            raise ValueError("a slug appears twice")
        return self


class TopicPatch(StrictModel):
    """The owner's change to a topic: what is left out stays. ``dropped`` true gives it up,
    false takes a dropped one back."""

    title: Title | None = None
    hook: Hook | None = None
    series: str | None = Field(default=None, pattern=SHORTS_SERIES_PATTERN)
    brief: TopicBrief | None = None
    assets_needed: list[AssetNeed] | None = Field(default=None, max_length=6)
    release_order: int | None = Field(default=None, ge=0, le=100_000)
    note: Note | None = None
    dropped: bool | None = None


class AssetOut(BaseModel):
    id: UUID
    need: str
    sha256: str
    filename: str
    content_type: str
    size: int
    author: str
    taken_on: date | None = None
    rights_note: str
    created_at: datetime
    # Where the worker reads the file with its video tool token.
    download_path: str


class TopicOut(BaseModel):
    slug: str
    line: ShortsLine
    series: str | None = None
    title: str
    hook: str | None = None
    status: TopicStatus
    brief: dict[str, Any]
    source_slug: str | None = None
    origin: TopicOrigin
    release_order: int | None = None
    assets_needed: list[dict[str, Any]]
    assets: list[AssetOut]
    # Why the topic cannot be made yet, in the owner's words; empty when it can.
    waiting_for: list[str]
    paid: bool
    project_slug: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    note: str | None = None
    created_at: datetime
    updated_at: datetime


class TopicsOut(BaseModel):
    items: list[TopicOut]


class TopicResult(BaseModel):
    slug: str
    result: Literal["created", "updated", "exists"]
    # None when the slug is a video's rather than a topic's.
    status: TopicStatus | None = None


class TopicsWrittenOut(BaseModel):
    created: int
    updated: int = 0
    skipped: int
    items: list[TopicResult]


# campaign.json (docs/videos/ai-shorts/campaign), read leniently: the import takes the file as
# it is and keeps what a topic needs.


class CampaignProtocol(BaseModel):
    model_config = ConfigDict(extra="ignore")
    setup_zh: str | None = None
    input_zh: str | None = None
    condition_a_zh: str | None = None
    condition_b_zh: str | None = None
    runs_zh: str | None = None
    scoring_zh: str | None = None
    failure_path_zh: str | None = None


class CampaignBeat(BaseModel):
    model_config = ConfigDict(extra="ignore")
    seconds: str | None = None
    voice_zh: str | None = None
    visual_zh: str | None = None


class CampaignTopic(BaseModel):
    model_config = ConfigDict(extra="ignore")
    slug: str = Field(pattern=TOPIC_SLUG_PATTERN)
    series: str | None = Field(default=None, pattern=SHORTS_SERIES_PATTERN)
    series_id: str | None = Field(default=None, pattern=SHORTS_SERIES_PATTERN)
    release_order: int | None = Field(default=None, ge=0, le=100_000)
    topic_zh: str = Field(min_length=1, max_length=200)
    hook_zh: str | None = Field(default=None, max_length=300)
    estimated_seconds: int | None = Field(default=None, ge=10, le=180)
    test_protocol: CampaignProtocol | None = None
    source_material: list[str] = Field(default_factory=list, max_length=20)
    truth_check: list[str] = Field(default_factory=list, max_length=20)
    provisional_titles: list[str] = Field(default_factory=list, max_length=6)
    narration_outline: list[CampaignBeat] = Field(default_factory=list, max_length=20)
    acceptance: list[str] = Field(default_factory=list, max_length=20)
    source_ids: list[str] = Field(default_factory=list, max_length=20)


class CampaignIn(BaseModel):
    model_config = ConfigDict(extra="ignore")
    campaign_id: str | None = Field(default=None, max_length=80)
    topics: list[CampaignTopic] = Field(min_length=1, max_length=200)


# The worker's next job (GET /video/automation/shorts/next).


class SlotRef(BaseModel):
    id: UUID
    starts_at: datetime
    local_date: date
    local_time: str
    status: SlotStatus
    line: ShortsLine | None = None
    series: str | None = None
    topic_slug: str | None = None
    project_slug: str | None = None


class TopicSummary(BaseModel):
    slug: str
    line: ShortsLine
    series: str | None = None
    title: str
    hook: str | None = None
    status: TopicStatus
    origin: TopicOrigin
    release_order: int | None = None
    paid: bool


class PublishedShort(BaseModel):
    """A Short that went public, with every snapshot YouTube reported for it as stored."""

    slug: str
    title: str
    line: ShortsLine | None = None
    series: str | None = None
    youtube_video_id: str
    published_at: datetime | None = None
    snapshots: list[MetricOut]


class ReportJob(BaseModel):
    week_start: date
    week_end: date
    timezone: str
    published: list[PublishedShort]
    missed: list[SlotRef]
    costs: list[CostOut]
    budget: BudgetOut
    next_week: list[SlotRef]


class PlanJob(BaseModel):
    window_start: datetime
    window_end: datetime
    timezone: str
    lines: list[ShortsLine]
    weekly_quota: dict[str, int]
    open_slots: list[SlotRef]
    planned: list[SlotRef]
    topics: list[TopicSummary]
    last_week: list[PublishedShort]
    budget: BudgetOut


class BriefJob(BaseModel):
    lines: list[ShortsLine]
    weekly_quota: dict[str, int]
    # Topics that could be planned now, against two weeks of the quotas.
    have: int
    want: int
    by_line: dict[str, int]
    # The owner's ideas and the planner's unfinished ones, to be completed; and every topic
    # the pool holds, so a new one does not repeat one.
    ideas: list[TopicOut]
    existing: list[TopicSummary]


class SourceVideo(BaseModel):
    slug: str
    title: str
    format: str
    youtube_video_id: str | None = None
    youtube_publish_at: datetime | None = None
    source_guide: str | None = None
    category: str | None = None
    series_slug: str | None = None
    episode_number: int | None = None


class MakeJob(BaseModel):
    slot: SlotRef
    topic: TopicOut
    line: ShortsLine
    # The video the Short is made under when the worker resumes one it started; a new one is
    # named by POST shorts/{topic}/start.
    project_slug: str | None = None
    resume: bool
    source: SourceVideo | None = None
    channel_stance: str
    seconds_min: int
    seconds_max: int


class NextOut(BaseModel):
    kind: JobKind | None
    # Why a job that might have come did not, in the owner's words.
    holds: list[str]
    report: ReportJob | None = None
    plan: PlanJob | None = None
    brief: BriefJob | None = None
    make: MakeJob | None = None


# What the worker writes back.


class PlanItem(StrictModel):
    slot_id: UUID
    topic_slug: str = Field(pattern=TOPIC_SLUG_PATTERN)


class PlanIn(StrictModel):
    """The planner's week: a topic for each slot it fills. An empty plan says it found
    nothing to put in the open slots, and is recorded so it is not asked again at once."""

    items: list[PlanItem] = Field(default_factory=list, max_length=60)


class PlanOut(BaseModel):
    planned: list[SlotOut]


class StartOut(BaseModel):
    topic: TopicOut
    project_slug: str
    created: bool


class DoneIn(StrictModel):
    """The worker finished a topic: its Short was pushed (``made``), or the topic turned
    out not to make one (``dropped``, with the reason)."""

    outcome: Literal["made", "dropped"] = "made"
    note: Note | None = None


class ReportRowIn(StrictModel):
    """A snapshot the report cites; the server copies its values as they were stored."""

    youtube_video_id: str = Field(pattern=r"^[A-Za-z0-9_-]{6,32}$")
    period: MetricPeriod
    source: MetricSource


class ReportPlanItem(StrictModel):
    starts_at: AwareDatetime | None = None
    topic_slug: str | None = Field(default=None, pattern=TOPIC_SLUG_PATTERN)
    line: ShortsLine | None = None
    note: Note | None = None


class ReportIn(StrictModel):
    week_start: date
    body_md: str = Field(min_length=1, max_length=40_000)
    rows: list[ReportRowIn] = Field(default_factory=list, max_length=400)
    plan: list[ReportPlanItem] = Field(default_factory=list, max_length=60)
    provider: str | None = Field(default=None, max_length=40)
    model: str | None = Field(default=None, max_length=128)


class ReportOut(BaseModel):
    id: UUID
    week_start: date
    body_md: str
    rows: list[dict[str, Any]]
    plan: list[dict[str, Any]]
    provider: str | None = None
    model: str | None = None
    generated_at: datetime
    updated_at: datetime


class ReportsOut(BaseModel):
    items: list[ReportOut]


class AssetPartOut(BaseModel):
    received: list[int]
    complete: bool
    asset: AssetOut | None = None
    topic: TopicOut | None = None
