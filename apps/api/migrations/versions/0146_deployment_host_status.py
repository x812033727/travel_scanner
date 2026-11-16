"""What the host's auto deploy timer last reported (deployment_host_status).

Revision ID: 0146_deployment_host_status
Revises: 0145_video_youtube_reports

docs/ops/admin-redeploy-button-and-daily-autodeploy-plan.md. One row, written by the root
timer on the host (ops/autodeploy) at the end of every tick and read by the admin deployment
page. A new table; nothing existing changes.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0146_deployment_host_status"
down_revision: str | None = "0145_video_youtube_reports"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "deployment_host_status"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _create() -> None:
    op.create_table(
        TABLE,
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reported_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dry_run", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("live_sha", sa.String(40), nullable=True),
        sa.Column("target_sha", sa.String(40), nullable=True),
        sa.Column("target_commit_subject", sa.String(255), nullable=True),
        sa.Column("ci_status", sa.String(64), nullable=True),
        sa.Column("ci_url", sa.Text(), nullable=True),
        sa.Column("paused_reason", sa.Text(), nullable=True),
        sa.Column("state_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.CheckConstraint("id = 1", name="ck_deployment_host_status_single"),
    )


def upgrade() -> None:
    if _offline() or not sa.inspect(op.get_bind()).has_table(TABLE):
        _create()


def downgrade() -> None:
    if _offline() or sa.inspect(op.get_bind()).has_table(TABLE):
        op.drop_table(TABLE)
