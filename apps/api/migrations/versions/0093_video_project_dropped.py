"""Videos the owner dropped on /admin/videos, and the article each video retells.

Revision ID: 0093_video_project_dropped
Revises: 0092_video_subscription_limit

The first automatic draft (2026-09-25) picked a topic a branch had already scripted, because the
worker only knew its own videos. Now it reads every video on /admin/videos, including the article
each one retells (``source_guide``), and the owner can drop one (``dropped_*``) instead of sending
its outline back, which would have re-planned a new topic under the old slug.

0001 builds a fresh database from the current models, so each column is added only when missing.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0093_video_project_dropped"
down_revision: str | None = "0092_video_subscription_limit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_projects"
NAMES = ("source_guide", "dropped_at", "dropped_note", "dropped_by_user_id")


def _columns() -> list[sa.Column[object]]:
    # Built on each call: a Column belongs to one table, and add_column attaches it to one.
    return [
        sa.Column("source_guide", sa.String(120), nullable=True),
        sa.Column("dropped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dropped_note", sa.Text(), nullable=True),
        sa.Column(
            "dropped_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", name="fk_video_projects_dropped_by", ondelete="SET NULL"),
            nullable=True,
        ),
    ]


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    existing = (
        set()
        if _offline()
        else {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}
    )
    for column in _columns():
        if _offline() or column.name not in existing:
            op.add_column(TABLE, column)


def downgrade() -> None:
    for name in reversed(NAMES):
        op.drop_column(TABLE, name)
