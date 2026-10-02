"""The Shorts' own tables (docs/videos/SHORTS.md §資料模型; migration 0109).

``video_projects`` carries which videos are Shorts (``shorts_line``); these tables hold the
rest: the one row of settings with the owner's standing consent, the slot calendar, the
numbers YouTube reported and the cost ledger. The migration creates the same columns and
constraints under the same names, so a database built from these models and one upgraded to
0109 are the same.
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.video_automation.models import DEFAULT_VOICE


def utcnow() -> datetime:
    return datetime.now(UTC)


def _default(value: Any) -> Callable[[], Any]:
    return lambda: copy.deepcopy(value)


# The three content lines the owner chose on 2026-09-28: experiments, highlights cut from the
# tutorials, and vertical drama shorts.
LINES: tuple[str, ...] = ("lab", "cut", "drama")
SLOT_STATUSES: tuple[str, ...] = (
    "open",
    "planned",
    "assigned",
    "locked",
    "scheduled",
    "published",
    "missed",
    "skipped",
)
# A slot that still holds its Short: a Short has at most one of these at a time. A missed or
# skipped slot keeps the slug it had, as a record, and no longer holds the Short.
HOLDING_STATUSES: tuple[str, ...] = ("assigned", "locked", "scheduled", "published")
METRIC_PERIODS: tuple[str, ...] = ("d1", "d3", "d7", "now")
METRIC_SOURCES: tuple[str, ...] = ("data_api", "analytics_api", "studio_export")
COST_STATUSES: tuple[str, ...] = ("confirmed", "reserved", "unknown")
COST_SOURCES: tuple[str, ...] = ("auto", "manual")
# A topic's life (migration 0117): written down (idea), its spec complete (ready), waiting for
# the owner's material or a tool the site does not have (needs_assets), being made, made, or
# given up. Where it came from: the fifteen-topic campaign, the planner model, the owner, or
# the server itself from a public tutorial or an approved drama episode.
TOPIC_STATUSES: tuple[str, ...] = ("idea", "ready", "needs_assets", "making", "made", "dropped")
TOPIC_ORIGINS: tuple[str, ...] = ("campaign", "planner", "owner", "auto")
# How many Shorts the worker may start in a calendar month (UTC), whatever the calendar asks.
DEFAULT_MAX_PER_MONTH = 60
# The pace of the pilot (docs/videos/ai-shorts, PR #871): one a day at 19:30 for thirty days,
# then sixty days alternating two (12:30 added) and one; 120 slots in ninety days.
DEFAULT_WEEKLY_QUOTA: dict[str, int] = {"lab": 5, "cut": 2, "drama": 0}
DEFAULT_DAILY_PATTERN: list[dict[str, Any]] = [
    {"days": 30, "counts": [1]},
    {"days": 60, "counts": [2, 1]},
]
DEFAULT_SLOT_TIMES: list[str] = ["19:30", "12:30"]
DEFAULT_TIMEZONE = "Asia/Taipei"


class VideoShortsSettings(Base):
    """The one row of Shorts settings (id 1), created with its defaults on first read.

    Its own table rather than more columns on ``video_automation_settings``: the owner asked
    on 2026-09-27 that every format keeps its settings apart.
    """

    __tablename__ = "video_shorts_settings"
    __table_args__ = (
        CheckConstraint("id = 1", name="ck_video_shorts_settings_singleton"),
        CheckConstraint(
            "stock_days BETWEEN 0 AND 30 AND lock_hours BETWEEN 1 AND 72 "
            "AND upload_ahead_days BETWEEN 1 AND 30 AND max_per_day BETWEEN 1 AND 4",
            name="ck_video_shorts_settings_calendar",
        ),
        CheckConstraint(
            "seconds_min BETWEEN 10 AND 180 AND seconds_max BETWEEN 10 AND 180 "
            "AND seconds_min <= seconds_max",
            name="ck_video_shorts_settings_seconds",
        ),
        CheckConstraint(
            "budget_ntd_30d BETWEEN 0 AND 1000000 AND budget_soft_ntd BETWEEN 0 AND 1000000 "
            "AND budget_soft_ntd <= budget_ntd_30d AND budget_total_ntd BETWEEN 0 AND 10000000",
            name="ck_video_shorts_settings_budget",
        ),
        CheckConstraint("max_per_month BETWEEN 0 AND 400", name="ck_video_shorts_settings_month"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    # Whether the host worker makes Shorts by itself (phase two). Shorts made elsewhere and
    # pushed to the site are reviewed, slotted and published whatever this says.
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    lines: Mapped[list[str]] = mapped_column(JSON, default=_default(list(LINES)))
    weekly_quota: Mapped[dict[str, int]] = mapped_column(
        JSON, default=_default(DEFAULT_WEEKLY_QUOTA)
    )
    # The calendar: the day the first Short goes public, how many a day over how many days, at
    # which local times, and in which timezone those times are read.
    campaign_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    daily_pattern: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=_default(DEFAULT_DAILY_PATTERN)
    )
    slot_times: Mapped[list[str]] = mapped_column(JSON, default=_default(DEFAULT_SLOT_TIMES))
    timezone: Mapped[str] = mapped_column(String(64), default=DEFAULT_TIMEZONE)
    stock_days: Mapped[int] = mapped_column(Integer, default=5)
    lock_hours: Mapped[int] = mapped_column(Integer, default=24)
    upload_ahead_days: Mapped[int] = mapped_column(Integer, default=10)
    max_per_day: Mapped[int] = mapped_column(Integer, default=2)
    seconds_min: Mapped[int] = mapped_column(Integer, default=25)
    seconds_max: Mapped[int] = mapped_column(Integer, default=55)
    # The narrator: the channel voice unless the owner picks another for Shorts.
    voice: Mapped[dict[str, Any]] = mapped_column(JSON, default=_default(DEFAULT_VOICE))
    # Phase two's: stage -> {"provider", "model"} (empty follows the tutorial's), the models an
    # experiment is run on ({"a": {...}, "b": {...}}), and the owner's standing instructions.
    stage_models: Mapped[dict[str, Any]] = mapped_column(JSON, default=_default({}))
    subject_models: Mapped[dict[str, Any]] = mapped_column(JSON, default=_default({}))
    stage_instructions: Mapped[dict[str, str]] = mapped_column(JSON, default=_default({}))
    # The languages a Short's title, description and captions are also sent in; empty is
    # Traditional Chinese only.
    locales: Mapped[list[str]] = mapped_column(JSON, default=_default([]))
    made_for_kids: Mapped[bool] = mapped_column(Boolean, default=False)
    # A final cut whose twelve checks all passed is approved as it arrives.
    auto_approve: Mapped[bool] = mapped_column(Boolean, default=True)
    # The owner's standing consent to publish on the calendar without asking each time
    # (docs/videos/SHORTS.md §自動上架授權): who agreed, when, to which wording and to what
    # scope. ``autopublish`` goes off when the scope no longer covers the settings.
    autopublish: Mapped[bool] = mapped_column(Boolean, default=False)
    paused_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    consent_id: Mapped[UUID | None] = mapped_column(nullable=True)
    consent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    consent_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    consent_text_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    consent_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    consent_scope: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    # New Taiwan dollars: what thirty days may cost, where new paid work stops so the work in
    # hand can finish, and what the ninety days may cost.
    budget_ntd_30d: Mapped[int] = mapped_column(Integer, default=3000)
    budget_soft_ntd: Mapped[int] = mapped_column(Integer, default=2400)
    budget_total_ntd: Mapped[int] = mapped_column(Integer, default=9000)
    # When the worker last knocked (POST shorts/tick) and what that round did.
    last_tick_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_tick: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    # Phase two (migration 0117): how many Shorts the worker may start in a month, and when
    # it last wrote a weekly plan and new topics, so a plan or a brief that left slots open
    # is not asked for again on every round.
    max_per_month: Mapped[int] = mapped_column(
        Integer, default=DEFAULT_MAX_PER_MONTH, server_default=text(str(DEFAULT_MAX_PER_MONTH))
    )
    last_plan_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_brief_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoShortsSlot(Base):
    """One square of the calendar: a Short goes public at ``starts_at``."""

    __tablename__ = "video_shorts_slots"
    __table_args__ = (
        UniqueConstraint("starts_at", name="uq_video_shorts_slot_starts_at"),
        CheckConstraint(
            "status IN ('open', 'planned', 'assigned', 'locked', 'scheduled', 'published', "
            "'missed', 'skipped')",
            name="ck_video_shorts_slot_status",
        ),
        CheckConstraint(
            "line IS NULL OR line IN ('lab', 'cut', 'drama')", name="ck_video_shorts_slot_line"
        ),
        CheckConstraint("phase BETWEEN 1 AND 99", name="ck_video_shorts_slot_phase"),
        # A Short holds one slot at a time; the slots it missed keep its slug as a record.
        Index(
            "uq_video_shorts_slot_project",
            "project_slug",
            unique=True,
            postgresql_where=text(
                "project_slug IS NOT NULL AND status NOT IN ('missed', 'skipped')"
            ),
            sqlite_where=text("project_slug IS NOT NULL AND status NOT IN ('missed', 'skipped')"),
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # Which thirty days of the run the slot falls in, from 1.
    phase: Mapped[int] = mapped_column(Integer, default=1)
    # What the weekly plan put here (phase two): a content line, a series, a topic.
    line: Mapped[str | None] = mapped_column(String(8), nullable=True)
    series: Mapped[str | None] = mapped_column(String(40), nullable=True)
    topic_slug: Mapped[str | None] = mapped_column(String(80), nullable=True)
    project_slug: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[str] = mapped_column(String(12), default="open")
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoShortsMetric(Base):
    """What YouTube reported for one Short at one moment, stored as it came.

    ``period`` is the snapshot window: ``d1``, ``d3`` and ``d7`` are written once and never
    overwritten, ``now`` is updated in place. The server derives nothing from these numbers
    (YouTube's developer policies; docs/videos/SHORTS.md §成效與每週報告).
    """

    __tablename__ = "video_shorts_metrics"
    __table_args__ = (
        UniqueConstraint(
            "youtube_video_id", "source", "period", name="uq_video_shorts_metric_snapshot"
        ),
        CheckConstraint(
            "period IN ('d1', 'd3', 'd7', 'now')", name="ck_video_shorts_metric_period"
        ),
        CheckConstraint(
            "source IN ('data_api', 'analytics_api', 'studio_export')",
            name="ck_video_shorts_metric_source",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    project_slug: Mapped[str] = mapped_column(String(80), index=True)
    youtube_video_id: Mapped[str] = mapped_column(String(32))
    period: Mapped[str] = mapped_column(String(4))
    source: Mapped[str] = mapped_column(String(16))
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # The days a report covers (the Analytics API answers by day); null for a live count.
    range_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    range_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    views: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    engaged_views: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    likes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    comments: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    shares: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    subscribers_gained: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    avg_view_seconds: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    avg_view_percent: Mapped[Decimal | None] = mapped_column(Numeric(7, 2), nullable=True)
    stayed_percent: Mapped[Decimal | None] = mapped_column(Numeric(7, 2), nullable=True)
    raw: Mapped[dict[str, Any]] = mapped_column(JSON, default=_default({}))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoShortsCost(Base):
    """One line of the ledger: what was spent, reserved, or spent without a known amount.

    An amount is kept in its own currency with the rate it was converted at; the budgets are
    read in New Taiwan dollars. ``dedupe_key`` names what an automatic line stands for, so the
    same final cut reported twice is entered once, and a reservation becomes the confirmed
    line by updating the row that carries its key.
    """

    __tablename__ = "video_shorts_costs"
    __table_args__ = (
        UniqueConstraint("dedupe_key", name="uq_video_shorts_cost_dedupe"),
        CheckConstraint(
            "status IN ('confirmed', 'reserved', 'unknown')", name="ck_video_shorts_cost_status"
        ),
        CheckConstraint("source IN ('auto', 'manual')", name="ck_video_shorts_cost_source"),
        # An unknown line has no amount, and any other line has one: zero is an amount. The
        # IS NOT NULL is spelled out because a check that evaluates to NULL passes.
        CheckConstraint(
            "(status = 'unknown' AND amount IS NULL AND amount_ntd IS NULL) "
            "OR (status <> 'unknown' AND amount IS NOT NULL AND amount_ntd IS NOT NULL "
            "AND amount >= 0 AND amount_ntd >= 0)",
            name="ck_video_shorts_cost_amount",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    project_slug: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    category: Mapped[str] = mapped_column(String(24))
    amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="TWD")
    fx_rate: Mapped[Decimal | None] = mapped_column(Numeric(14, 6), nullable=True)
    amount_ntd: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(12))
    source: Mapped[str] = mapped_column(String(8))
    # What was used, as the tool reported it: seconds and characters of narration, calls.
    units: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    dedupe_key: Mapped[str | None] = mapped_column(String(160), nullable=True)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoShortsTopic(Base):
    """A Short still to be made (docs/videos/SHORTS.md §資料模型; migration 0117).

    ``brief`` is the topic's whole spec as the worker gets it from ``shorts/next``: the
    experiment's seven protocol fields, the truth checks and the acceptance list for the
    experiments line, the narration outline, title options and sources; ``requires`` in it
    names tools the experiment needs beyond text. ``assets_needed`` lists what only the owner
    can supply (``[{"key", "label", "count"}]``), filled by ``video_shorts_assets`` rows.
    ``dedupe_key`` names what an automatic topic was made from, so a source gives its topics
    once. The Short made from a topic is the video under ``project_slug``.
    """

    __tablename__ = "video_shorts_topics"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_video_shorts_topic_slug"),
        UniqueConstraint("dedupe_key", name="uq_video_shorts_topic_dedupe"),
        CheckConstraint(
            "status IN ('idea', 'ready', 'needs_assets', 'making', 'made', 'dropped')",
            name="ck_video_shorts_topic_status",
        ),
        CheckConstraint(
            "origin IN ('campaign', 'planner', 'owner', 'auto')",
            name="ck_video_shorts_topic_origin",
        ),
        CheckConstraint("line IN ('lab', 'cut', 'drama')", name="ck_video_shorts_topic_line"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(80))
    line: Mapped[str] = mapped_column(String(8))
    series: Mapped[str | None] = mapped_column(String(40), nullable=True)
    title: Mapped[str] = mapped_column(String(200))
    hook: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(12), default="idea")
    brief: Mapped[dict[str, Any]] = mapped_column(JSON, default=_default({}))
    source_slug: Mapped[str | None] = mapped_column(String(80), nullable=True)
    origin: Mapped[str] = mapped_column(String(12))
    release_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assets_needed: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=_default([]))
    dedupe_key: Mapped[str | None] = mapped_column(String(160), nullable=True)
    project_slug: Mapped[str | None] = mapped_column(String(80), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class VideoShortsAsset(Base):
    """A file the owner supplied for a topic: a photo they took, a sketch they drew.

    The file itself is in the media store under the topic's slug and its SHA-256, where the
    worker downloads it (``/video/media/files``); this row says who made it, when, and on
    what terms it may be used. ``need`` is the ``assets_needed`` key it fills.
    """

    __tablename__ = "video_shorts_assets"
    __table_args__ = (UniqueConstraint("topic_slug", "sha256", name="uq_video_shorts_asset_file"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    topic_slug: Mapped[str] = mapped_column(String(80), index=True)
    need: Mapped[str] = mapped_column(String(40))
    sha256: Mapped[str] = mapped_column(String(64))
    filename: Mapped[str] = mapped_column(String(200))
    content_type: Mapped[str] = mapped_column(String(40))
    size: Mapped[int] = mapped_column(BigInteger)
    author: Mapped[str] = mapped_column(String(120))
    taken_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    rights_note: Mapped[str] = mapped_column(Text)
    uploaded_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class VideoShortsReport(Base):
    """The planner's report on one week, Monday to Sunday in the settings' timezone.

    ``rows`` are the numbers YouTube reported that the report cites, copied from
    ``video_shorts_metrics`` with their source and read time when the report arrived; the
    server derives nothing from them. ``plan`` is the next week's slots as the planner
    described them. A week has one report: sending it again replaces it.
    """

    __tablename__ = "video_shorts_reports"
    __table_args__ = (UniqueConstraint("week_start", name="uq_video_shorts_report_week"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    week_start: Mapped[date] = mapped_column(Date)
    body_md: Mapped[str] = mapped_column(Text)
    rows: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=_default([]))
    plan: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=_default([]))
    provider: Mapped[str | None] = mapped_column(String(40), nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
