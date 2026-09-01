"""Add deployment runs and events.

Revision ID: 0024_deployment_center
Revises: 0023_flight_anchors
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision: str = "0024_deployment_center"
down_revision: str | None = "0023_flight_anchors"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ACTIVE = (
    "queued",
    "preflight",
    "building",
    "backing_up",
    "migrating",
    "activating",
    "verifying",
    "rolling_back",
)
STATUSES = ACTIVE + (
    "succeeded",
    "failed",
    "rolled_back",
    "manual_intervention_required",
)


def upgrade() -> None:
    # 0001 still calls the current Base.metadata.create_all. A fresh database
    # therefore already has these tables, while an existing database upgrading
    # from 0023 does not. Inspecting keeps both paths safe and leaves offline SQL
    # generation unchanged.
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    has_runs = inspector is not None and inspector.has_table("deployment_runs")
    has_events = inspector is not None and inspector.has_table("deployment_events")

    if not has_runs:
        op.create_table(
            "deployment_runs",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("requested_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("idempotency_key", sa.String(length=255), nullable=False),
            sa.Column("agent_job_id", sa.String(length=64), nullable=True),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("stage", sa.String(length=32), nullable=False),
            sa.Column("previous_sha", sa.String(length=40), nullable=True),
            sa.Column("target_sha", sa.String(length=40), nullable=False),
            sa.Column("target_commit_subject", sa.String(length=255), nullable=True),
            sa.Column("ci_url", sa.Text(), nullable=True),
            sa.Column("backup_name", sa.String(length=255), nullable=True),
            sa.Column("rollback_status", sa.String(length=32), nullable=True),
            sa.Column("failure_code", sa.String(length=64), nullable=True),
            sa.Column("failure_detail", sa.Text(), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "status IN (" + ", ".join(f"'{status}'" for status in STATUSES) + ")",
                name="ck_deployment_run_status",
            ),
            sa.ForeignKeyConstraint(["requested_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("agent_job_id"),
            sa.UniqueConstraint(
                "requested_by_user_id",
                "idempotency_key",
                name="uq_deployment_request_idempotency",
            ),
        )
        op.create_index(
            "ix_deployment_runs_requested_by_user_id",
            "deployment_runs",
            ["requested_by_user_id"],
        )
        op.create_index("ix_deployment_runs_status", "deployment_runs", ["status"])
        op.create_index("ix_deployment_runs_target_sha", "deployment_runs", ["target_sha"])
        op.create_index(
            "uq_deployment_one_active",
            "deployment_runs",
            [sa.text("(1)")],
            unique=True,
            postgresql_where=sa.text(
                "status IN (" + ", ".join(f"'{status}'" for status in ACTIVE) + ")"
            ),
        )

    if not has_events:
        op.create_table(
            "deployment_events",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("sequence", sa.Integer(), nullable=False),
            sa.Column("stage", sa.String(length=32), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("message", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["run_id"], ["deployment_runs.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("run_id", "sequence", name="uq_deployment_event_sequence"),
        )
        op.create_index("ix_deployment_events_run_id", "deployment_events", ["run_id"])


def downgrade() -> None:
    op.drop_index("ix_deployment_events_run_id", table_name="deployment_events")
    op.drop_table("deployment_events")
    op.drop_index("uq_deployment_one_active", table_name="deployment_runs")
    op.drop_index("ix_deployment_runs_target_sha", table_name="deployment_runs")
    op.drop_index("ix_deployment_runs_status", table_name="deployment_runs")
    op.drop_index("ix_deployment_runs_requested_by_user_id", table_name="deployment_runs")
    op.drop_table("deployment_runs")
