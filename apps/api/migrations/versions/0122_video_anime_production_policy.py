"""Add a separate, reviewed long-anime production contract.

Revision ID: 0122_video_anime_production
Revises: 0121_video_series_planning

Existing production and locked planning rows retain their values. Policy and runtime
are nullable, additive fields. Raw SQL cannot enable long episodes by category alone.
Downgrade refuses authored production profiles rather than truncating their runtime.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0122_video_anime_production"
down_revision: str | None = "0121_video_series_planning"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_drama_series"
NUMBERS = "ck_video_drama_series_numbers"
LEAD = "ck_video_drama_series_lead"
POLICY = "ck_video_drama_series_anime_policy"
RUNTIME = "ck_video_drama_series_anime_runtime"
OLD_NUMBERS_CHECK = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND (target_minutes BETWEEN 1 AND 20 OR "
    "(planning_only = true AND target_minutes BETWEEN 21 AND 30))"
)
OLD_LEAD_CHECK = (
    "lead IN ('female', 'male', 'dual-male') OR (planning_only = true AND lead = 'ensemble')"
)
NUMBERS_CHECK = (
    "planned_episodes BETWEEN 1 AND 500 AND episodes_per_chapter BETWEEN 1 AND 20 "
    "AND (target_minutes BETWEEN 1 AND 20 OR "
    "((planning_only = true OR (production_policy IS NOT NULL "
    "AND production_policy = 'long-anime-v1')) "
    "AND target_minutes BETWEEN 21 AND 30))"
)
LEAD_CHECK = (
    "lead IN ('female', 'male', 'dual-male') OR "
    "((planning_only = true OR (production_policy IS NOT NULL "
    "AND production_policy = 'long-anime-v1')) AND lead = 'ensemble')"
)
POLICY_CHECK = (
    "(production_policy IS NULL AND runtime_spec IS NULL) OR "
    "(production_policy IS NOT NULL AND production_policy = 'long-anime-v1' "
    "AND planning_only = false AND kind = 'series' AND category IS NOT NULL AND category = 'anime' "
    "AND style_preset = 'anime-2d' AND genre = 'custom' AND lead = 'ensemble' "
    "AND hands_off = false AND compilation = false AND total_minutes IS NULL)"
)
_FIELDS = (
    "body_target_seconds",
    "op_ed_budget_seconds",
    "broadcast_slot_seconds",
    "slot_reserve_seconds",
)
_INTEGERS = " AND ".join(
    f"(runtime_spec ->> '{field}') IS NOT NULL AND "
    f"CAST(runtime_spec -> '{field}' AS TEXT) = "
    f"CAST(CAST(runtime_spec ->> '{field}' AS INTEGER) AS TEXT)"
    for field in _FIELDS
)
_BODY = "CAST(runtime_spec ->> 'body_target_seconds' AS INTEGER)"
_OP_ED = "CAST(runtime_spec ->> 'op_ed_budget_seconds' AS INTEGER)"
_SLOT = "CAST(runtime_spec ->> 'broadcast_slot_seconds' AS INTEGER)"
_RESERVE = "CAST(runtime_spec ->> 'slot_reserve_seconds' AS INTEGER)"
RUNTIME_CHECK = (
    "production_policy IS NULL OR (runtime_spec IS NOT NULL AND "
    f"{_INTEGERS} AND {_BODY} BETWEEN 540 AND 1800 AND {_BODY} % 60 = 0 "
    f"AND {_OP_ED} BETWEEN 0 AND 300 AND {_SLOT} BETWEEN 1 AND 3600 "
    f"AND {_RESERVE} BETWEEN 0 AND 900 AND {_BODY} = target_minutes * 60 "
    f"AND {_SLOT} = {_BODY} + {_OP_ED} + {_RESERVE})"
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
    if "production_policy" not in columns:
        op.add_column(TABLE, sa.Column("production_policy", sa.String(32), nullable=True))
    if "runtime_spec" not in columns:
        op.add_column(TABLE, sa.Column("runtime_spec", sa.JSON(none_as_null=True), nullable=True))
    for name, sql in (
        (NUMBERS, NUMBERS_CHECK),
        (LEAD, LEAD_CHECK),
        (POLICY, POLICY_CHECK),
        (RUNTIME, RUNTIME_CHECK),
    ):
        _rebuild(name, sql)


def downgrade() -> None:
    columns = _columns()
    if _offline():
        op.execute(
            sa.text(
                "DO $$ BEGIN IF EXISTS (SELECT 1 FROM video_drama_series "
                "WHERE production_policy IS NOT NULL) THEN RAISE EXCEPTION "
                "'Long-anime production profiles must be preserved before downgrade'; "
                "END IF; END $$"
            )
        )
    elif "production_policy" in columns and op.get_bind().scalar(
        sa.text(f"SELECT count(*) FROM {TABLE} WHERE production_policy IS NOT NULL")
    ):
        raise RuntimeError("Long-anime production profiles must be preserved before downgrade")
    checks = _checks()
    for name in (RUNTIME, POLICY):
        if _offline() or name in checks:
            op.drop_constraint(name, TABLE, type_="check")
    _rebuild(NUMBERS, OLD_NUMBERS_CHECK)
    _rebuild(LEAD, OLD_LEAD_CHECK)
    for name in ("runtime_spec", "production_policy"):
        if _offline() or name in columns:
            op.drop_column(TABLE, name)
