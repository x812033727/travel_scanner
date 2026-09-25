"""Each model call a video stage makes through the server, for the monthly budgets.

Revision ID: 0091_video_ai_runs
Revises: 0090_video_automation_settings

The video worker never holds the site's AI keys: it asks ``/video/automation/run`` to run a
stage with the model the owner chose. Every call leaves a row here with its tokens, so the
month's token budget and draft count are sums over the table, and the settings tab can show
what the pipeline has spent (docs/videos/AUTOMATION.md).

Guarded like 0090, since 0001 builds a fresh database from the current models.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0091_video_ai_runs"
down_revision: str | None = "0090_video_automation_settings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_ai_runs"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def upgrade() -> None:
    if not _offline() and TABLE in sa.inspect(op.get_bind()).get_table_names():
        return
    op.create_table(
        TABLE,
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("stage", sa.String(length=32), nullable=False),
        sa.Column("provider", sa.String(length=16), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=False),
        sa.Column("token_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('ok', 'failed')", name="ck_video_ai_run_status"),
        sa.ForeignKeyConstraint(["token_id"], ["video_tool_tokens.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_video_ai_runs_slug", TABLE, ["slug"])
    op.create_index("ix_video_ai_runs_created", TABLE, ["created_at"])


def downgrade() -> None:
    op.drop_table(TABLE)
