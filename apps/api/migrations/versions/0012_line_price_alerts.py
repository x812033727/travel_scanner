"""Add LINE account connections and scheduled price-alert delivery state.

Revision ID: 0012_line_price_alerts
Revises: 0011_auth_session_version
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_line_price_alerts"
down_revision: str | None = "0011_auth_session_version"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    alert_columns = {str(column["name"]) for column in inspector.get_columns("price_alerts")}
    additions = (
        ("provider", sa.String(length=64), True),
        ("monitoring_mode", sa.String(length=24), False),
        ("monitoring_status", sa.String(length=32), False),
        ("monitor_key", sa.JSON(), False),
        ("baseline_price", sa.Numeric(14, 2), True),
        ("last_observed_price", sa.Numeric(14, 2), True),
        ("last_notified_price", sa.Numeric(14, 2), True),
        ("last_checked_at", sa.DateTime(timezone=True), True),
        ("next_check_at", sa.DateTime(timezone=True), True),
        ("armed", sa.Boolean(), False),
        ("consecutive_failures", sa.Integer(), False),
        ("completed_at", sa.DateTime(timezone=True), True),
    )
    defaults = {
        "monitoring_mode": sa.text("'manual_only'"),
        "monitoring_status": sa.text("'manual_only'"),
        "monitor_key": sa.text("'{}'"),
        "armed": sa.true(),
        "consecutive_failures": sa.text("0"),
    }
    for name, column_type, nullable in additions:
        if name in alert_columns:
            continue
        op.add_column(
            "price_alerts",
            sa.Column(name, column_type, nullable=nullable, server_default=defaults.get(name)),
        )
        if not nullable and name in defaults:
            op.alter_column("price_alerts", name, server_default=None)
    for name in ("provider", "monitoring_mode", "monitoring_status", "next_check_at"):
        op.create_index(
            f"ix_price_alerts_{name}",
            "price_alerts",
            [name],
            unique=False,
            if_not_exists=True,
        )

    if "line_connections" not in tables:
        op.create_table(
            "line_connections",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("line_user_id", sa.String(length=64), nullable=False),
            sa.Column("display_name", sa.String(length=255), nullable=False),
            sa.Column("friend_status", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("last_delivery_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("last_delivery_error", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", name="uq_line_connection_user"),
            sa.UniqueConstraint("line_user_id", name="uq_line_connection_line_user"),
        )
        op.create_index("ix_line_connections_user_id", "line_connections", ["user_id"])
        op.create_index(
            "ix_line_connections_line_user_id", "line_connections", ["line_user_id"]
        )
        op.create_index(
            "ix_line_connections_friend_status", "line_connections", ["friend_status"]
        )

    if "price_alert_checks" not in tables:
        op.create_table(
            "price_alert_checks",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("alert_id", sa.Uuid(), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("previous_price", sa.Numeric(14, 2), nullable=True),
            sa.Column("observed_price", sa.Numeric(14, 2), nullable=True),
            sa.Column("currency", sa.String(length=3), nullable=False),
            sa.Column("provider", sa.String(length=64), nullable=True),
            sa.Column("detail", sa.Text(), nullable=True),
            sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["alert_id"], ["price_alerts.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_price_alert_checks_alert_id", "price_alert_checks", ["alert_id"])
        op.create_index("ix_price_alert_checks_status", "price_alert_checks", ["status"])
        op.create_index("ix_price_alert_checks_checked_at", "price_alert_checks", ["checked_at"])

    if "alert_notification_deliveries" not in tables:
        op.create_table(
            "alert_notification_deliveries",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("alert_id", sa.Uuid(), nullable=False),
            sa.Column("line_connection_id", sa.Uuid(), nullable=True),
            sa.Column("dedupe_key", sa.String(length=255), nullable=False),
            sa.Column("event_type", sa.String(length=32), nullable=False),
            sa.Column("observed_price", sa.Numeric(14, 2), nullable=False),
            sa.Column("status", sa.String(length=24), nullable=False),
            sa.Column("attempts", sa.Integer(), nullable=False),
            sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("last_error", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["alert_id"], ["price_alerts.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(
                ["line_connection_id"], ["line_connections.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("dedupe_key", name="uq_alert_notification_dedupe"),
        )
        for name in ("alert_id", "line_connection_id", "dedupe_key", "status"):
            op.create_index(
                f"ix_alert_notification_deliveries_{name}",
                "alert_notification_deliveries",
                [name],
            )


def downgrade() -> None:
    tables = set(sa.inspect(op.get_bind()).get_table_names())
    for table in (
        "alert_notification_deliveries",
        "price_alert_checks",
        "line_connections",
    ):
        if table in tables:
            op.drop_table(table)
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("price_alerts")
    }
    for name in (
        "completed_at",
        "consecutive_failures",
        "armed",
        "next_check_at",
        "last_checked_at",
        "last_observed_price",
        "last_notified_price",
        "baseline_price",
        "monitor_key",
        "monitoring_status",
        "monitoring_mode",
        "provider",
    ):
        if name in columns:
            op.drop_column("price_alerts", name)
