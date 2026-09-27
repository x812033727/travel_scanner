"""The media generation jobs of the AI drama route (docs/videos/DRAMA.md).

Revision ID: 0096_video_media_jobs
Revises: 0095_video_drama

One row per image, clip or music generation the pipeline asked a vendor for: the request,
where the job stands, the file it produced and what it cost. The API advances a job only when
the tool polls it, so the row has to survive a restart between two polls.

0001 builds a fresh database from the current models, so the table is created only when it is
missing. The downgrade drops it: the files in the media store are a cache and the tool keeps
its own copies.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0096_video_media_jobs"
down_revision: str | None = "0095_video_drama"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_media_jobs"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    if not _offline() and TABLE in sa.inspect(op.get_bind()).get_table_names():
        return
    op.create_table(
        TABLE,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False),
        sa.Column("kind", sa.String(8), nullable=False),
        sa.Column("purpose", sa.String(24), nullable=False),
        sa.Column("shot_id", sa.String(60), nullable=True),
        sa.Column("provider", sa.String(16), nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("request", sa.JSON(), nullable=False),
        sa.Column("request_hash", sa.String(64), nullable=False),
        sa.Column("idempotency_key", sa.String(80), nullable=True),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("vendor_ref", sa.String(512), nullable=True),
        sa.Column("seconds", sa.Integer(), nullable=False),
        sa.Column("file_sha256", sa.String(64), nullable=True),
        sa.Column("file_bytes", sa.BigInteger(), nullable=True),
        sa.Column("content_type", sa.String(32), nullable=True),
        sa.Column("usd_estimate", sa.Numeric(10, 4), nullable=False),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column("polls", sa.Integer(), nullable=False),
        sa.Column(
            "token_id",
            sa.Uuid(),
            sa.ForeignKey(
                "video_tool_tokens.id", name="fk_video_media_jobs_token", ondelete="SET NULL"
            ),
            nullable=True,
        ),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ready_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("slug", "request_hash", name="uq_video_media_job_request"),
        sa.CheckConstraint("kind IN ('image', 'clip', 'music')", name="ck_video_media_job_kind"),
        sa.CheckConstraint(
            "status IN ('queued', 'submitted', 'ready', 'failed', 'expired')",
            name="ck_video_media_job_status",
        ),
    )
    op.create_index("ix_video_media_jobs_slug", TABLE, ["slug"])
    op.create_index("ix_video_media_jobs_created", TABLE, ["created_at"])
    op.create_index("ix_video_media_jobs_status", TABLE, ["status"])


def downgrade() -> None:
    op.drop_table(TABLE)
