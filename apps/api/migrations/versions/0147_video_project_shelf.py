"""File each video under its show and topic for the review page's catalog.

Revision ID: 0147_video_project_shelf
Revises: 0146_deployment_host_status

The owner, 2026-11-18: 奇聞檔案局 and 原來如此事務所 stand on their own in /admin/videos instead of
inside 觀念解說, findable by their topics, and the dramas are picked one at a time.
``video_projects.series_key`` is the show or drama (``curio``, ``tai-nainai``,
``zhong-tian-qu-qi-r2``…) and ``topic`` an explainer show's category (``H-歷史懸案``). Both are
worked out in Python (app/video_reviews/shelf.py, by the rules Google Drive backup files videos
by), so this migration only adds the columns; ``python -m app.cli video-shelf-backfill --apply``
fills the rows that exist, once, after the deploy. Until it runs the catalog files them under
their category, as before.

0001 creates the table from the current models, so each column and the index are inspected
before they are added. Old code never reads them, so an application rollback keeps working.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0147_video_project_shelf"
down_revision: str | None = "0146_deployment_host_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

PROJECTS = "video_projects"
INDEX = "ix_video_projects_series_key"
COLUMNS: tuple[tuple[str, int], ...] = (("series_key", 40), ("topic", 40))


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns() -> set[str]:
    if _offline():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(PROJECTS)}


def _indexes() -> set[str]:
    if _offline():
        return set()
    return {str(index["name"]) for index in sa.inspect(op.get_bind()).get_indexes(PROJECTS)}


def upgrade() -> None:
    existing = _columns()
    for name, length in COLUMNS:
        if name not in existing:
            op.add_column(PROJECTS, sa.Column(name, sa.String(length=length), nullable=True))
    if INDEX not in _indexes():
        op.create_index(INDEX, PROJECTS, ["series_key"])


def downgrade() -> None:
    if _offline() or INDEX in _indexes():
        op.drop_index(INDEX, table_name=PROJECTS)
    existing = _columns()
    for name, _length in reversed(COLUMNS):
        if _offline() or name in existing:
            op.drop_column(PROJECTS, name)
