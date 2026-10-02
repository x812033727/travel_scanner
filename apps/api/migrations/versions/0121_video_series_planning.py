"""Preserve reviewed anime plans without authorizing production.

Revision ID: 0121_video_series_planning
Revises: 0120_video_dropped_request

Existing series remain ordinary rows. Only a planning-only, paused anime may retain
21–30 minutes or an ensemble lead. Its scheduling switches are constrained off.
Application rollback keeps these additive columns. Database downgrade refuses when
authored planning rows exist rather than shortening or deleting an owner's work.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0121_video_series_planning"
down_revision: str | None = "0120_video_dropped_request"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_drama_series"
CATEGORIES = (
    "ai-terms",
    "ai-news",
    "tutorial",
    "comparison",
    "explainer",
    "story",
    "drama",
    "long-drama",
    "anime",
    "travel",
    "other",
)
NUMBERS = "ck_video_drama_series_numbers"
LEAD = "ck_video_drama_series_lead"
CATEGORY = "ck_video_drama_series_category"
PLANNING = "ck_video_drama_series_planning"
OLD_NUMBERS_CHECK = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND target_minutes BETWEEN 1 AND 20"
)
NUMBERS_CHECK = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND (target_minutes BETWEEN 1 AND 20 OR "
    "(planning_only = true AND target_minutes BETWEEN 21 AND 30))"
)
OLD_LEAD_CHECK = "lead IN ('female', 'male', 'dual-male')"
LEAD_CHECK = (
    "lead IN ('female', 'male', 'dual-male') OR (planning_only = true AND lead = 'ensemble')"
)
CATEGORY_CHECK = "category IS NULL OR category IN ({})".format(
    ", ".join(f"'{code}'" for code in CATEGORIES)
)
PLANNING_CHECK = (
    "planning_only = false OR (kind = 'series' AND category IS NOT NULL AND category = 'anime' "
    "AND status = 'paused' AND hands_off = false AND compilation = false AND force_next = false "
    "AND requested_chapter IS NULL)"
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns() -> set[str]:
    if _offline():
        return set()
    return {str(column["name"]) for column in sa.inspect(op.get_bind()).get_columns(TABLE)}


def _checks() -> set[str]:
    if _offline():
        return {NUMBERS, LEAD}
    return {str(check["name"]) for check in sa.inspect(op.get_bind()).get_check_constraints(TABLE)}


def _rebuild(name: str, sql: str) -> None:
    if name in _checks():
        op.drop_constraint(name, TABLE, type_="check")
    op.create_check_constraint(name, TABLE, sql)


def upgrade() -> None:
    columns = _columns()
    if "planning_only" not in columns:
        op.add_column(
            TABLE, sa.Column("planning_only", sa.Boolean(), nullable=False, server_default="false")
        )
    if "category" not in columns:
        op.add_column(TABLE, sa.Column("category", sa.String(24), nullable=True))
    if "planning_spec" not in columns:
        op.add_column(TABLE, sa.Column("planning_spec", sa.JSON(), nullable=True))
    _rebuild(NUMBERS, NUMBERS_CHECK)
    _rebuild(LEAD, LEAD_CHECK)
    _rebuild(CATEGORY, CATEGORY_CHECK)
    _rebuild(PLANNING, PLANNING_CHECK)


def downgrade() -> None:
    columns = _columns()
    if _offline():
        op.execute(
            sa.text(
                "DO $$ BEGIN IF EXISTS (SELECT 1 FROM video_drama_series "
                "WHERE planning_only = true) "
                "THEN RAISE EXCEPTION 'Planning-only anime must be preserved before downgrade'; "
                "END IF; END $$"
            )
        )
    elif "planning_only" in columns and op.get_bind().scalar(
        sa.text(f"SELECT count(*) FROM {TABLE} WHERE planning_only = true")
    ):
        raise RuntimeError("Planning-only anime must be preserved before downgrade")
    checks = _checks()
    for name in (PLANNING, CATEGORY):
        if _offline() or name in checks:
            op.drop_constraint(name, TABLE, type_="check")
    _rebuild(NUMBERS, OLD_NUMBERS_CHECK)
    _rebuild(LEAD, OLD_LEAD_CHECK)
    for name in ("planning_spec", "category", "planning_only"):
        if _offline() or name in columns:
            op.drop_column(TABLE, name)
