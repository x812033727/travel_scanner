"""Every slides video runs at least eight minutes.

Revision ID: 0118_video_min_8_minutes
Revises: 0117_video_shorts_topics

The owner's rule (2026-10-01): every episode runs eight minutes or more, except a drama's. The
slides route takes its length from ``video_automation_settings.target_minutes_min``/``max``, so
both are raised to 8 where they were lower, and the check that allowed 3 is recreated under the
same name to allow 8 to 30. The explainer's floor lives in the schemas and the worker, since its
length is stored per request and per series beside the drama's.

The downgrade only widens the check again; the raised values stay valid under it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0118_video_min_8_minutes"
down_revision: str | None = "0117_video_shorts_topics"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SETTINGS = "video_automation_settings"
MINUTES_CHECK = "ck_video_automation_minutes"
FLOOR = 8
OLD_FLOOR = 3


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _checks() -> set[str]:
    if _offline():
        return set()
    inspector = sa.inspect(op.get_bind())
    return {str(check.get("name")) for check in inspector.get_check_constraints(SETTINGS)}


def check_text(floor: int) -> str:
    return (
        f"target_minutes_min BETWEEN {floor} AND 30 AND target_minutes_max BETWEEN {floor} AND 30 "
        "AND target_minutes_min <= target_minutes_max"
    )


def _replace(floor: int) -> None:
    if _offline() or MINUTES_CHECK in _checks():
        op.drop_constraint(MINUTES_CHECK, SETTINGS, type_="check")
    op.create_check_constraint(MINUTES_CHECK, SETTINGS, check_text(floor))


def upgrade() -> None:
    # Both in one statement: raising either alone can break the old check's min <= max.
    op.execute(
        f"UPDATE {SETTINGS} SET target_minutes_min = GREATEST(target_minutes_min, {FLOOR}), "
        f"target_minutes_max = GREATEST(target_minutes_max, {FLOOR}) "
        f"WHERE target_minutes_min < {FLOOR} OR target_minutes_max < {FLOOR}"
    )
    _replace(FLOOR)


def downgrade() -> None:
    _replace(OLD_FLOOR)
