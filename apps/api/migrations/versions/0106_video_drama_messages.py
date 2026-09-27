"""A discussion thread on every series document and every screenplay (DRAMA-FLOW.md §三).

Revision ID: 0106_video_drama_messages
Revises: 0105_video_one_off_series

``video_drama_messages`` holds the owner's lines about a document (the setting book, the outline, a
chapter's outline, a one-off's story bible) or an episode's screenplay, and the planner's or the
writer's answers: ``subject`` names the thread, ``refers_to`` the version the line was said about,
``answered_at`` is set on the owner's line once the model answered it. The thread is read by
series, subject and time, hence the one index.

0001 builds a fresh database from the current models, so the table is created only when missing.
The downgrade drops it: the messages are the discussion's record, and the documents they led to
stay as versions of their own.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0106_video_drama_messages"
down_revision: str | None = "0105_video_one_off_series"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

MESSAGES = "video_drama_messages"
INDEX = "ix_video_drama_messages_thread"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _tables() -> set[str]:
    return set() if _offline() else set(sa.inspect(op.get_bind()).get_table_names())


def _indexes(table: str) -> set[str]:
    if _offline():
        return set()
    return {str(index.get("name")) for index in sa.inspect(op.get_bind()).get_indexes(table)}


def upgrade() -> None:
    if MESSAGES not in _tables():
        op.create_table(
            MESSAGES,
            sa.Column("id", sa.Uuid(), primary_key=True),
            sa.Column(
                "series_id",
                sa.Uuid(),
                sa.ForeignKey(
                    "video_drama_series.id",
                    name="fk_video_drama_messages_series",
                    ondelete="CASCADE",
                ),
                nullable=False,
            ),
            sa.Column("subject", sa.String(24), nullable=False),
            sa.Column("author", sa.String(12), nullable=False),
            sa.Column("body_md", sa.Text(), nullable=False),
            sa.Column("refers_to", sa.String(16), nullable=True),
            sa.Column("answered_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column(
                "created_by_user_id",
                sa.Uuid(),
                sa.ForeignKey(
                    "users.id", name="fk_video_drama_messages_user", ondelete="SET NULL"
                ),
                nullable=True,
            ),
            sa.CheckConstraint(
                "author IN ('owner', 'planner', 'writer')", name="ck_video_drama_message_author"
            ),
        )
    if INDEX not in _indexes(MESSAGES):
        op.create_index(INDEX, MESSAGES, ["series_id", "subject", "created_at"])


def downgrade() -> None:
    if _offline() or MESSAGES in _tables():
        op.drop_table(MESSAGES)
