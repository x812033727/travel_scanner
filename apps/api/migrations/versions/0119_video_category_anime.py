"""Add anime to the video categories.

Revision ID: 0119_video_category_anime
Revises: 0118_video_min_8_minutes

The owner files anime videos under their own category (docs/videos/HANDS-OFF.md §影片分類),
so ``ck_video_project_category`` takes ``anime`` as well. The check is rebuilt under its name
with every code it took before, as 0117 rebuilt the stage-prompt checks; 0116 keeps its own
list as it ran.

0001 builds a fresh database from the current models, and those do not include the video
tables, so CI runs every branch here. The downgrade unfiles the anime videos (category back
to NULL, "uncategorized") before the narrow check returns; nothing else is touched.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0119_video_category_anime"
down_revision: str | None = "0118_video_min_8_minutes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
CATEGORY_CHECK = "ck_video_project_category"
# The codes 0116 allowed; the migration's test keeps them equal to 0116's list.
OLD_CATEGORIES = (
    "ai-terms",
    "ai-news",
    "tutorial",
    "comparison",
    "explainer",
    "story",
    "drama",
    "long-drama",
    "travel",
    "other",
)
ADDED = "anime"
# The same list as app.models.VIDEO_CATEGORIES; the migration's test keeps them in step.
CATEGORIES = (
    "ai-terms",
    "ai-news",
    "tutorial",
    "comparison",
    "explainer",
    "story",
    "drama",
    "long-drama",
    ADDED,
    "travel",
    "other",
)


def _check_text(categories: Sequence[str]) -> str:
    return "category IS NULL OR category IN ({})".format(
        ", ".join(f"'{code}'" for code in categories)
    )


CHECK_TEXT = _check_text(CATEGORIES)
OLD_CHECK_TEXT = _check_text(OLD_CATEGORIES)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _checks() -> set[str]:
    if _offline():
        return set()
    inspector = sa.inspect(op.get_bind())
    return {str(check.get("name")) for check in inspector.get_check_constraints(PROJECTS)}


def _rebuild(sql: str) -> None:
    if _offline() or CATEGORY_CHECK in _checks():
        op.drop_constraint(CATEGORY_CHECK, PROJECTS, type_="check")
    op.create_check_constraint(CATEGORY_CHECK, PROJECTS, sql)


def upgrade() -> None:
    _rebuild(CHECK_TEXT)


def downgrade() -> None:
    op.execute(sa.text(f"UPDATE {PROJECTS} SET category = NULL WHERE category = '{ADDED}'"))
    _rebuild(OLD_CHECK_TEXT)
