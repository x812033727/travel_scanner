"""Add auditable AI-assisted hotspot guide search runs.

Revision ID: 0021_hotspot_guide_ai_search
Revises: 0020_itinerary_system_slots
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0021_hotspot_guide_ai_search"
down_revision: str | None = "0020_itinerary_system_slots"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _create_table() -> None:
    op.create_table(
        "hotspot_guide_ai_search_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("hotspot_id", sa.Uuid(), nullable=False),
        sa.Column("idempotency_key", sa.String(255), nullable=False),
        sa.Column("requested_locales", sa.JSON(), nullable=False),
        sa.Column("content_types", sa.JSON(), nullable=False),
        sa.Column("provider", sa.String(16), nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("depth", sa.String(16), nullable=False),
        sa.Column("only_missing", sa.Boolean(), nullable=False),
        sa.Column("custom_instructions", sa.String(500), nullable=True),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("progress_json", sa.JSON(), nullable=False),
        sa.Column("query_plan_json", sa.JSON(), nullable=False),
        sa.Column("usage_json", sa.JSON(), nullable=False),
        sa.Column("result_json", sa.JSON(), nullable=False),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("queue_job_id", sa.String(128), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "provider IN ('minimax', 'openai', 'anthropic')",
            name="ck_hotspot_guide_ai_search_provider",
        ),
        sa.CheckConstraint(
            "depth IN ('economy', 'balanced', 'deep')",
            name="ck_hotspot_guide_ai_search_depth",
        ),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'partial', 'completed', 'failed')",
            name="ck_hotspot_guide_ai_search_status",
        ),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "actor_user_id",
            "idempotency_key",
            name="uq_hotspot_guide_ai_search_idempotency",
        ),
    )
    for column in ("actor_user_id", "hotspot_id", "provider", "status"):
        op.create_index(
            f"ix_hotspot_guide_ai_search_runs_{column}",
            "hotspot_guide_ai_search_runs",
            [column],
        )


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is None or not inspector.has_table("hotspot_guide_ai_search_runs"):
        _create_table()


def downgrade() -> None:
    op.drop_table("hotspot_guide_ai_search_runs")
