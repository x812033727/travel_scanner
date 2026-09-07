"""Persist bounded Gemini catalog review/discovery runs and their immutable snapshots."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0054_catalog_review"
down_revision: str | None = "0053_ui_text_overrides"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    tables = set() if op.get_context().as_sql else set(sa.inspect(op.get_bind()).get_table_names())
    if "catalog_review_runs" not in tables:
        op.create_table(
            "catalog_review_runs",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column(
                "actor_user_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("users.id"),
                nullable=False,
            ),
            sa.Column("idempotency_key", sa.String(128), nullable=False),
            sa.Column("request_hash", sa.String(64), nullable=False),
            sa.Column("request_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("mode", sa.String(24), nullable=False),
            sa.Column("phase", sa.String(32), nullable=False, server_default="review_pending"),
            sa.Column("status", sa.String(24), nullable=False, server_default="queued"),
            sa.Column("model", sa.String(128), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("usage_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("result_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("error_code", sa.String(100), nullable=True),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("lease_token", sa.String(64), nullable=True),
            sa.Column("lease_until", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint(
                "actor_user_id", "idempotency_key", name="uq_catalog_run_idempotency"
            ),
            sa.CheckConstraint(
                "mode IN ('review_pending', 'discover_new')", name="ck_catalog_run_mode"
            ),
            sa.CheckConstraint(
                "status IN ('queued', 'running', 'completed', 'partial', 'failed', 'cancelled')",
                name="ck_catalog_run_status",
            ),
        )
        for field in ("actor_user_id", "status"):
            op.create_index(f"ix_catalog_review_runs_{field}", "catalog_review_runs", [field])
    if "catalog_review_items" not in tables:
        op.create_table(
            "catalog_review_items",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column(
                "run_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("catalog_review_runs.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("kind", sa.String(16), nullable=False),
            sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("phase", sa.String(24), nullable=False, server_default="review_pending"),
            sa.Column("name", sa.String(255), nullable=False),
            sa.Column("destination_id", sa.String(64), nullable=True),
            sa.Column("snapshot_hash", sa.String(64), nullable=False),
            sa.Column("snapshot_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
            sa.Column("assessment_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("evidence_json", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column("gaps_json", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column("decision", sa.String(24), nullable=True),
            sa.Column("reason", sa.Text(), nullable=False, server_default=""),
            sa.Column("applied_action", sa.String(24), nullable=True),
            sa.Column("assessed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("run_id", "kind", "entity_id", name="uq_catalog_review_entity"),
            sa.CheckConstraint(
                "kind IN ('hotspot', 'food', 'merchant')", name="ck_catalog_review_kind"
            ),
            sa.CheckConstraint(
                "status IN ('pending', 'assessed', 'error', 'applied', 'stale')",
                name="ck_catalog_review_item_status",
            ),
        )
        for field in ("run_id", "entity_id", "status"):
            op.create_index(f"ix_catalog_review_items_{field}", "catalog_review_items", [field])


def downgrade() -> None:
    tables = set() if op.get_context().as_sql else set(sa.inspect(op.get_bind()).get_table_names())
    for table in ("catalog_review_items", "catalog_review_runs"):
        if op.get_context().as_sql or table in tables:
            op.drop_table(table)
