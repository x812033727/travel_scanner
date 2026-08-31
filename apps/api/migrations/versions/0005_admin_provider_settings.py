"""Add encrypted provider settings and administrator audit records.

Revision ID: 0005_admin_provider_settings
Revises: 0004_itinerary_route_planner
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0005_admin_provider_settings"
down_revision: str | None = "0004_itinerary_route_planner"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    user_columns = (
        {str(column["name"]) for column in inspector.get_columns("users")}
        if inspector is not None
        else set()
    )
    provider_columns = (
        {str(column["name"]) for column in inspector.get_columns("provider_configs")}
        if inspector is not None
        else set()
    )
    if "is_admin" not in user_columns:
        op.add_column(
            "users",
            sa.Column("is_admin", sa.Boolean(), server_default=sa.false(), nullable=False),
        )

    additions: dict[str, sa.Column[object]] = {
        "secret_config_encrypted": sa.Column("secret_config_encrypted", sa.Text(), nullable=True),
        "updated_by_user_id": sa.Column("updated_by_user_id", sa.Uuid(), nullable=True),
        "last_tested_at": sa.Column("last_tested_at", sa.DateTime(timezone=True), nullable=True),
        "last_test_status": sa.Column("last_test_status", sa.String(32), nullable=True),
        "last_test_message": sa.Column("last_test_message", sa.Text(), nullable=True),
    }
    for name, column in additions.items():
        if name not in provider_columns:
            op.add_column("provider_configs", column)

    if inspector is not None:
        foreign_keys = inspector.get_foreign_keys("provider_configs")
        has_actor_fk = any(
            item.get("constrained_columns") == ["updated_by_user_id"] for item in foreign_keys
        )
        if not has_actor_fk:
            op.create_foreign_key(
                "fk_provider_configs_updated_by_user_id_users",
                "provider_configs",
                "users",
                ["updated_by_user_id"],
                ["id"],
                ondelete="SET NULL",
            )
        indexes = {str(item["name"]) for item in inspector.get_indexes("provider_configs")}
        if "ix_provider_configs_updated_by_user_id" not in indexes:
            op.create_index(
                "ix_provider_configs_updated_by_user_id",
                "provider_configs",
                ["updated_by_user_id"],
            )

    has_audit_table = inspector is not None and inspector.has_table("admin_audit_logs")
    if not has_audit_table:
        op.create_table(
            "admin_audit_logs",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("actor_user_id", sa.Uuid(), nullable=True),
            sa.Column("action", sa.String(64), nullable=False),
            sa.Column("target", sa.String(128), nullable=False),
            sa.Column("metadata_json", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_admin_audit_logs_actor_user_id",
            "admin_audit_logs",
            ["actor_user_id"],
        )
        op.create_index("ix_admin_audit_logs_action", "admin_audit_logs", ["action"])
        op.create_index("ix_admin_audit_logs_target", "admin_audit_logs", ["target"])


def downgrade() -> None:
    op.drop_index("ix_admin_audit_logs_target", table_name="admin_audit_logs")
    op.drop_index("ix_admin_audit_logs_action", table_name="admin_audit_logs")
    op.drop_index("ix_admin_audit_logs_actor_user_id", table_name="admin_audit_logs")
    op.drop_table("admin_audit_logs")
    op.drop_index("ix_provider_configs_updated_by_user_id", table_name="provider_configs")
    op.drop_constraint(
        "fk_provider_configs_updated_by_user_id_users",
        "provider_configs",
        type_="foreignkey",
    )
    for column in (
        "last_test_message",
        "last_test_status",
        "last_tested_at",
        "updated_by_user_id",
        "secret_config_encrypted",
    ):
        op.drop_column("provider_configs", column)
    op.drop_column("users", "is_admin")
