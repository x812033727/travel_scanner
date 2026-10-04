"""Retain source-bound video stage operations and exact replies across HTTP timeouts.

Revision ID: 0123_video_stage_jobs
Revises: 0122_video_anime_production

This additive table leaves synchronous callers and existing usage rows unchanged. Only
queued operations may dispatch; interrupted dispatched jobs cannot be automatically retried.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0123_video_stage_jobs"
down_revision: str | None = "0122_video_anime_production"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_stage_jobs"
STATUS_CHECK = "status IN ('queued', 'running', 'succeeded', 'failed', 'uncertain')"
RESULT_CHECK = "(status = 'succeeded') = (result_json IS NOT NULL)"


def upgrade() -> None:
    if not op.get_context().as_sql and TABLE in sa.inspect(op.get_bind()).get_table_names():
        return
    op.create_table(
        TABLE,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "token_id",
            sa.Uuid(),
            sa.ForeignKey("video_tool_tokens.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("request_key", sa.Uuid(), nullable=False),
        sa.Column("request_hash", sa.String(64), nullable=False),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column("request_json", sa.JSON(), nullable=False),
        sa.Column("provider", sa.String(16), nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("result_json", sa.JSON(none_as_null=True), nullable=True),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column("error_status", sa.Integer(), nullable=True),
        sa.Column("retry_after", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("token_id", "request_key", name="uq_video_stage_job_request"),
        sa.CheckConstraint(STATUS_CHECK, name="ck_video_stage_job_status"),
        sa.CheckConstraint(RESULT_CHECK, name="ck_video_stage_job_result"),
    )
    op.create_index("ix_video_stage_jobs_status_created", TABLE, ["status", "created_at"])


def downgrade() -> None:
    if not op.get_context().as_sql and TABLE not in sa.inspect(op.get_bind()).get_table_names():
        return
    op.drop_index("ix_video_stage_jobs_status_created", table_name=TABLE)
    op.drop_table(TABLE)
