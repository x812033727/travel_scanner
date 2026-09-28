"""Shorts on the server: which videos are Shorts, their settings, slots, numbers and costs.

Revision ID: 0109_video_shorts
Revises: 0108_video_drama_messages

The owner asked on 2026-09-28 for a Shorts tab on /admin/videos (docs/videos/SHORTS.md).
``video_projects`` gains ``shorts_line`` (a video with a content line is a Short),
``shorts_series`` and ``source_slug``, and ``youtube_removed_at`` for a video the site found
gone from YouTube; ``ck_video_project_format`` admits ``shorts``, the card pipeline. Four
tables are the Shorts' own: the one row of settings with the owner's standing consent to
publish, the slot calendar, the numbers YouTube reported, and the cost ledger.

0001 builds a fresh database from the current models, so every column, check and table is
added only when it is missing; the format check is replaced under its name, as 0101 and 0106
replaced the gate check. The downgrade refuses while any video is a Short: the narrow check
and the missing columns could not hold it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0109_video_shorts"
down_revision: str | None = "0108_video_drama_messages"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
SETTINGS = "video_shorts_settings"
SLOTS = "video_shorts_slots"
METRICS = "video_shorts_metrics"
COSTS = "video_shorts_costs"
FORMAT_CHECK = "ck_video_project_format"
OLD_FORMATS = "format IN ('slides', 'drama')"
NEW_FORMATS = "format IN ('slides', 'drama', 'shorts')"
LINE_CHECK = (
    "ck_video_project_shorts_line",
    "shorts_line IS NULL OR shorts_line IN ('lab', 'cut', 'drama')",
)
PROJECT_COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object]], ...] = (
    ("shorts_line", sa.String(8)),
    ("shorts_series", sa.String(40)),
    ("source_slug", sa.String(80)),
    ("youtube_removed_at", sa.DateTime(timezone=True)),
)
SLOT_PROJECT_INDEX = "uq_video_shorts_slot_project"
HOLDS_A_SHORT = "project_slug IS NOT NULL AND status NOT IN ('missed', 'skipped')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _columns(table: str) -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _checks(table: str) -> set[str]:
    if _offline():
        return set()
    return {
        str(check.get("name")) for check in sa.inspect(op.get_bind()).get_check_constraints(table)
    }


def _timestamps() -> tuple[sa.Column[object], sa.Column[object]]:
    return (
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def _user(column: str, name: str) -> sa.Column[object]:
    return sa.Column(
        column,
        sa.Uuid(),
        sa.ForeignKey("users.id", name=name, ondelete="SET NULL"),
        nullable=True,
    )


def _create_settings() -> None:
    op.create_table(
        SETTINGS,
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("lines", sa.JSON(), nullable=False),
        sa.Column("weekly_quota", sa.JSON(), nullable=False),
        sa.Column("campaign_start", sa.Date(), nullable=True),
        sa.Column("daily_pattern", sa.JSON(), nullable=False),
        sa.Column("slot_times", sa.JSON(), nullable=False),
        sa.Column("timezone", sa.String(64), nullable=False),
        sa.Column("stock_days", sa.Integer(), nullable=False),
        sa.Column("lock_hours", sa.Integer(), nullable=False),
        sa.Column("upload_ahead_days", sa.Integer(), nullable=False),
        sa.Column("max_per_day", sa.Integer(), nullable=False),
        sa.Column("seconds_min", sa.Integer(), nullable=False),
        sa.Column("seconds_max", sa.Integer(), nullable=False),
        sa.Column("voice", sa.JSON(), nullable=False),
        sa.Column("stage_models", sa.JSON(), nullable=False),
        sa.Column("subject_models", sa.JSON(), nullable=False),
        sa.Column("stage_instructions", sa.JSON(), nullable=False),
        sa.Column("locales", sa.JSON(), nullable=False),
        sa.Column("made_for_kids", sa.Boolean(), nullable=False),
        sa.Column("auto_approve", sa.Boolean(), nullable=False),
        sa.Column("autopublish", sa.Boolean(), nullable=False),
        sa.Column("paused_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("consent_id", sa.Uuid(), nullable=True),
        sa.Column("consent_at", sa.DateTime(timezone=True), nullable=True),
        _user("consent_by_user_id", "fk_video_shorts_settings_consent_user"),
        sa.Column("consent_text_sha256", sa.String(64), nullable=True),
        sa.Column("consent_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("consent_scope", sa.JSON(), nullable=True),
        sa.Column("budget_ntd_30d", sa.Integer(), nullable=False),
        sa.Column("budget_soft_ntd", sa.Integer(), nullable=False),
        sa.Column("budget_total_ntd", sa.Integer(), nullable=False),
        sa.Column("last_tick_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_tick", sa.JSON(), nullable=True),
        _user("updated_by_user_id", "fk_video_shorts_settings_updated_user"),
        *_timestamps(),
        sa.CheckConstraint("id = 1", name="ck_video_shorts_settings_singleton"),
        sa.CheckConstraint(
            "stock_days BETWEEN 0 AND 30 AND lock_hours BETWEEN 1 AND 72 "
            "AND upload_ahead_days BETWEEN 1 AND 30 AND max_per_day BETWEEN 1 AND 4",
            name="ck_video_shorts_settings_calendar",
        ),
        sa.CheckConstraint(
            "seconds_min BETWEEN 10 AND 180 AND seconds_max BETWEEN 10 AND 180 "
            "AND seconds_min <= seconds_max",
            name="ck_video_shorts_settings_seconds",
        ),
        sa.CheckConstraint(
            "budget_ntd_30d BETWEEN 0 AND 1000000 AND budget_soft_ntd BETWEEN 0 AND 1000000 "
            "AND budget_soft_ntd <= budget_ntd_30d AND budget_total_ntd BETWEEN 0 AND 10000000",
            name="ck_video_shorts_settings_budget",
        ),
    )


def _create_slots() -> None:
    op.create_table(
        SLOTS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("phase", sa.Integer(), nullable=False),
        sa.Column("line", sa.String(8), nullable=True),
        sa.Column("series", sa.String(40), nullable=True),
        sa.Column("topic_slug", sa.String(80), nullable=True),
        sa.Column("project_slug", sa.String(80), nullable=True),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("starts_at", name="uq_video_shorts_slot_starts_at"),
        sa.CheckConstraint(
            "status IN ('open', 'planned', 'assigned', 'locked', 'scheduled', 'published', "
            "'missed', 'skipped')",
            name="ck_video_shorts_slot_status",
        ),
        sa.CheckConstraint(
            "line IS NULL OR line IN ('lab', 'cut', 'drama')", name="ck_video_shorts_slot_line"
        ),
        sa.CheckConstraint("phase BETWEEN 1 AND 99", name="ck_video_shorts_slot_phase"),
    )
    # A Short holds one slot at a time; the slots it missed keep its slug as a record.
    op.create_index(
        SLOT_PROJECT_INDEX,
        SLOTS,
        ["project_slug"],
        unique=True,
        postgresql_where=sa.text(HOLDS_A_SHORT),
    )


def _create_metrics() -> None:
    op.create_table(
        METRICS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("project_slug", sa.String(80), nullable=False),
        sa.Column("youtube_video_id", sa.String(32), nullable=False),
        sa.Column("period", sa.String(4), nullable=False),
        sa.Column("source", sa.String(16), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("range_start", sa.Date(), nullable=True),
        sa.Column("range_end", sa.Date(), nullable=True),
        sa.Column("views", sa.BigInteger(), nullable=True),
        sa.Column("engaged_views", sa.BigInteger(), nullable=True),
        sa.Column("likes", sa.BigInteger(), nullable=True),
        sa.Column("comments", sa.BigInteger(), nullable=True),
        sa.Column("shares", sa.BigInteger(), nullable=True),
        sa.Column("subscribers_gained", sa.BigInteger(), nullable=True),
        sa.Column("avg_view_seconds", sa.Numeric(10, 2), nullable=True),
        sa.Column("avg_view_percent", sa.Numeric(7, 2), nullable=True),
        sa.Column("stayed_percent", sa.Numeric(7, 2), nullable=True),
        sa.Column("raw", sa.JSON(), nullable=False),
        *_timestamps(),
        sa.UniqueConstraint(
            "youtube_video_id", "source", "period", name="uq_video_shorts_metric_snapshot"
        ),
        sa.CheckConstraint(
            "period IN ('d1', 'd3', 'd7', 'now')", name="ck_video_shorts_metric_period"
        ),
        sa.CheckConstraint(
            "source IN ('data_api', 'analytics_api', 'studio_export')",
            name="ck_video_shorts_metric_source",
        ),
    )
    op.create_index("ix_video_shorts_metrics_project_slug", METRICS, ["project_slug"])


def _create_costs() -> None:
    op.create_table(
        COSTS,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("project_slug", sa.String(80), nullable=True),
        sa.Column("category", sa.String(24), nullable=False),
        sa.Column("amount", sa.Numeric(12, 4), nullable=True),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("fx_rate", sa.Numeric(14, 6), nullable=True),
        sa.Column("amount_ntd", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("source", sa.String(8), nullable=False),
        sa.Column("units", sa.JSON(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("dedupe_key", sa.String(160), nullable=True),
        _user("created_by_user_id", "fk_video_shorts_costs_created_user"),
        *_timestamps(),
        sa.UniqueConstraint("dedupe_key", name="uq_video_shorts_cost_dedupe"),
        sa.CheckConstraint(
            "status IN ('confirmed', 'reserved', 'unknown')", name="ck_video_shorts_cost_status"
        ),
        sa.CheckConstraint("source IN ('auto', 'manual')", name="ck_video_shorts_cost_source"),
        # An unknown line has no amount, and any other line has one. The IS NOT NULL is spelled
        # out because a check that evaluates to NULL passes.
        sa.CheckConstraint(
            "(status = 'unknown' AND amount IS NULL AND amount_ntd IS NULL) "
            "OR (status <> 'unknown' AND amount IS NOT NULL AND amount_ntd IS NOT NULL "
            "AND amount >= 0 AND amount_ntd >= 0)",
            name="ck_video_shorts_cost_amount",
        ),
    )
    op.create_index("ix_video_shorts_costs_occurred_at", COSTS, ["occurred_at"])
    op.create_index("ix_video_shorts_costs_project_slug", COSTS, ["project_slug"])


def upgrade() -> None:
    existing = _columns(PROJECTS)
    for name, kind in PROJECT_COLUMNS:
        if name not in existing:
            op.add_column(PROJECTS, sa.Column(name, kind, nullable=True))
    checks = _checks(PROJECTS)
    # The format check is replaced rather than left alone: a fresh database (0001) already
    # has the wide one under this name, an older one has the narrow one from 0097.
    if _offline() or FORMAT_CHECK in checks:
        op.drop_constraint(FORMAT_CHECK, PROJECTS, type_="check")
    op.create_check_constraint(FORMAT_CHECK, PROJECTS, NEW_FORMATS)
    if LINE_CHECK[0] not in checks:
        op.create_check_constraint(LINE_CHECK[0], PROJECTS, LINE_CHECK[1])
    tables = _tables()
    for table, create in (
        (SETTINGS, _create_settings),
        (SLOTS, _create_slots),
        (METRICS, _create_metrics),
        (COSTS, _create_costs),
    ):
        if table not in tables:
            create()


def downgrade() -> None:
    if not _offline() and "shorts_line" in _columns(PROJECTS):
        held = (
            op.get_bind()
            .execute(
                sa.text(
                    f"SELECT count(*) FROM {PROJECTS} "
                    "WHERE format = 'shorts' OR shorts_line IS NOT NULL"
                )
            )
            .scalar()
        )
        if held:
            raise RuntimeError(
                f"{held} videos are Shorts; the narrow format check and the missing columns "
                "cannot hold them"
            )
    tables = _tables()
    for table in (COSTS, METRICS, SLOTS, SETTINGS):
        if _offline() or table in tables:
            op.drop_table(table)
    checks = _checks(PROJECTS)
    if _offline() or LINE_CHECK[0] in checks:
        op.drop_constraint(LINE_CHECK[0], PROJECTS, type_="check")
    if _offline() or FORMAT_CHECK in checks:
        op.drop_constraint(FORMAT_CHECK, PROJECTS, type_="check")
    op.create_check_constraint(FORMAT_CHECK, PROJECTS, OLD_FORMATS)
    existing = _columns(PROJECTS)
    for name, _kind in reversed(PROJECT_COLUMNS):
        if _offline() or name in existing:
            op.drop_column(PROJECTS, name)
