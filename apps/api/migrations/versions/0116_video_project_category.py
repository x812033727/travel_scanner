"""Give every video a content category for the review page's filters.

Revision ID: 0116_video_project_category
Revises: 0115_video_review_revision

``video_projects.category`` is one of eight codes (app.models.VIDEO_CATEGORIES) or NULL for
a video nobody has filed yet. The pipeline reports it from video.json and only fills an empty
one; the owner changes it on /admin/videos (docs/videos/HANDS-OFF.md §影片分類).

Two rules file the rows that exist: a video that retells a news-automation article (its
``source_guide`` starts with ``ai-news-``) is news, and a video whose slug starts with
``ai-term-`` (the AI terms series) explains a term. Only a NULL category is filled, and
everything else stays NULL for the owner: an article's kind is the site's section, not the
video's type, so nothing else is guessed.
0001 creates the table from the current models, so the column and the constraint are
inspected before they are added, and the backfill runs only when the column was just added.

Application deployment rollback does not downgrade the database; old code never reads the
column, so it is add-only until an explicit downgrade drops it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0116_video_project_category"
down_revision: str | None = "0115_video_review_revision"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
CATEGORY_CHECK = "ck_video_project_category"
# The same list as app.models.VIDEO_CATEGORIES; the migration's test keeps them in step.
CATEGORIES = (
    "ai-terms",
    "ai-news",
    "tutorial",
    "comparison",
    "explainer",
    "story",
    "travel",
    "other",
)
CHECK_TEXT = "category IS NULL OR category IN ({})".format(
    ", ".join(f"'{code}'" for code in CATEGORIES)
)
# (a category, the column whose value starting with the prefix files a video under it), in the
# order applied. Compared with substr() rather than LIKE: no wildcard to escape in offline SQL.
BACKFILL: tuple[tuple[str, str, str], ...] = (
    ("ai-news", "source_guide", "ai-news-"),
    ("ai-terms", "slug", "ai-term-"),
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns() -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(PROJECTS)}


def _checks() -> set[str]:
    if _offline():
        return set()
    inspector = sa.inspect(op.get_bind())
    return {str(check.get("name")) for check in inspector.get_check_constraints(PROJECTS)}


def _backfill() -> None:
    projects = sa.table(
        PROJECTS,
        sa.column("slug", sa.String),
        sa.column("source_guide", sa.String),
        sa.column("category", sa.String),
    )
    for category, column, prefix in BACKFILL:
        statement = (
            projects.update()
            .where(
                projects.c.category.is_(None),
                sa.func.substr(projects.c[column], 1, len(prefix)) == prefix,
            )
            .values(category=category)
        )
        # Rendered with its constants inline, so the offline SQL is runnable as written.
        op.execute(
            str(
                statement.compile(
                    dialect=op.get_context().dialect, compile_kwargs={"literal_binds": True}
                )
            )
        )


def upgrade() -> None:
    added = "category" not in _columns()
    if added:
        op.add_column(PROJECTS, sa.Column("category", sa.String(length=16), nullable=True))
    if _offline() or CATEGORY_CHECK not in _checks():
        op.create_check_constraint(CATEGORY_CHECK, PROJECTS, CHECK_TEXT)
    if added:
        _backfill()


def downgrade() -> None:
    if _offline() or CATEGORY_CHECK in _checks():
        op.drop_constraint(CATEGORY_CHECK, PROJECTS, type_="check")
    if _offline() or "category" in _columns():
        op.drop_column(PROJECTS, "category")
