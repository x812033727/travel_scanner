"""The owner's requests for a slides video of a chosen site article (docs/videos/AUTOMATION.md).

Revision ID: 0127_video_slides_requests
Revises: 0126_ai_income_topic

``video_slides_requests`` is what the owner files on the tutorials tab of /admin/videos to have
one published lifestyle article made into a slides video next, ahead of the scheduled drafts;
the worker claims the oldest queued row and links it to the video it makes.

A table of its own rather than more rows in ``video_drama_requests``: that table's
``style_preset`` is NOT NULL and its check allows only the drama presets, and a deployed worker
asking for the next drama request would take a slides request and make a drama of it.

This additive table leaves every existing row and caller unchanged, so the previous release runs
against it. 0001 builds a fresh database from the current models, so the table is created only
when it is missing. The downgrade drops it; a request is a note to the worker, not a record the
site needs to keep.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0127_video_slides_requests"
down_revision: str | None = "0126_ai_income_topic"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_slides_requests"
INDEX = "ix_video_slides_requests_status_created"
STATUS_CHECK = "status IN ('queued', 'started', 'done', 'cancelled')"


def upgrade() -> None:
    if not op.get_context().as_sql and TABLE in sa.inspect(op.get_bind()).get_table_names():
        return
    op.create_table(
        TABLE,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("source_guide", sa.String(120), nullable=False),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("slug", sa.String(80), nullable=True),
        sa.Column(
            "created_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", name="fk_video_slides_requests_user", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "started_by_token_id",
            sa.Uuid(),
            sa.ForeignKey(
                "video_tool_tokens.id", name="fk_video_slides_requests_token", ondelete="SET NULL"
            ),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("slug", name="uq_video_slides_requests_slug"),
        sa.CheckConstraint(STATUS_CHECK, name="ck_video_slides_request_status"),
    )
    op.create_index(INDEX, TABLE, ["status", "created_at"])


def downgrade() -> None:
    if not op.get_context().as_sql and TABLE not in sa.inspect(op.get_bind()).get_table_names():
        return
    op.drop_index(INDEX, table_name=TABLE)
    op.drop_table(TABLE)
