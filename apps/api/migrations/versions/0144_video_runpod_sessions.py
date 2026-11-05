"""RunPod pods the site starts for video tools (video_runpod_sessions, runpod_access).

Revision ID: 0144_video_runpod_sessions
Revises: 0143_video_daily_briefs

The H3 clip route moves from Colab to RunPod (tasks 2026-10-30-runpod-*). The RunPod key stays
on this server: a video tool asks the site to start and stop a pod, and the site keeps one row
per pod so the monthly cap, the idle stop and the longest run are enforced here, not by the
agent. `runpod_access` says which video tool tokens may ask, like `colab_access` (0142); every
existing token stays without it.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0144_video_runpod_sessions"
down_revision: str | None = "0143_video_daily_briefs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TOKENS = "video_tool_tokens"
COLUMN = "runpod_access"
TABLE = "video_runpod_sessions"
STOP_REASONS = "('manual', 'idle', 'max_hours', 'cap', 'gone', 'failed')"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _create_table() -> None:
    op.create_table(
        TABLE,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "token_id",
            sa.Uuid(),
            sa.ForeignKey("video_tool_tokens.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("pod_id", sa.String(64), nullable=True),
        sa.Column("label", sa.String(80), nullable=False),
        sa.Column("slug", sa.String(120), nullable=True),
        sa.Column("gpu", sa.String(64), nullable=False),
        sa.Column("cloud_type", sa.String(16), nullable=False),
        sa.Column("data_center_id", sa.String(16), nullable=True),
        sa.Column("cost_per_hr", sa.Numeric(8, 4), nullable=True),
        sa.Column("gate_token_hash", sa.String(64), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_heartbeat_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("stopped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("stop_reason", sa.String(16), nullable=True),
        sa.Column("usd", sa.Numeric(10, 4), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            f"stop_reason IS NULL OR stop_reason IN {STOP_REASONS}",
            name="ck_video_runpod_sessions_stop_reason",
        ),
        sa.CheckConstraint(
            "(stopped_at IS NULL) = (stop_reason IS NULL)",
            name="ck_video_runpod_sessions_stopped",
        ),
    )
    op.create_index("ix_video_runpod_sessions_started_at", TABLE, ["started_at"])
    op.create_index("ix_video_runpod_sessions_token_id", TABLE, ["token_id"])


def upgrade() -> None:
    if _offline():
        op.add_column(
            TOKENS, sa.Column(COLUMN, sa.Boolean(), nullable=False, server_default=sa.false())
        )
        _create_table()
        return
    inspector = sa.inspect(op.get_bind())
    if COLUMN not in {column["name"] for column in inspector.get_columns(TOKENS)}:
        op.add_column(
            TOKENS, sa.Column(COLUMN, sa.Boolean(), nullable=False, server_default=sa.false())
        )
    if not inspector.has_table(TABLE):
        _create_table()


def downgrade() -> None:
    if _offline():
        op.drop_table(TABLE)
        op.drop_column(TOKENS, COLUMN)
        return
    inspector = sa.inspect(op.get_bind())
    if inspector.has_table(TABLE):
        op.drop_table(TABLE)
    if COLUMN in {column["name"] for column in inspector.get_columns(TOKENS)}:
        op.drop_column(TOKENS, COLUMN)
