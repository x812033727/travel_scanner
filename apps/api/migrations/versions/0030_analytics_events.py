"""Add privacy-preserving analytics events and daily rollups.

Revision ID: 0030_analytics_events
Revises: 0029_ui_saved_items
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision: str = "0030_analytics_events"
down_revision: str | None = "0029_ui_saved_items"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _inspector() -> sa.Inspector | None:
    return None if context.is_offline_mode() else sa.inspect(op.get_bind())


def upgrade() -> None:
    inspector = _inspector()
    tables = set(inspector.get_table_names()) if inspector is not None else set()
    if "analytics_events" not in tables:
        op.create_table(
            "analytics_events",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("event_name", sa.String(32), nullable=False),
            sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("normalized_path", sa.String(128), nullable=False),
            sa.Column("locale", sa.String(16), nullable=False),
            sa.Column("session_hash", sa.String(64), nullable=False),
            sa.Column("visitor_day_hash", sa.String(64), nullable=False),
            sa.Column("country_code", sa.String(2)),
            sa.Column("device_type", sa.String(16), nullable=False),
            sa.Column("browser_family", sa.String(32), nullable=False),
            sa.Column("os_family", sa.String(32), nullable=False),
            sa.Column("referrer_type", sa.String(16), nullable=False),
            sa.Column("referrer_host", sa.String(255)),
            sa.Column("utm_source", sa.String(100)),
            sa.Column("utm_medium", sa.String(100)),
            sa.Column("utm_campaign", sa.String(100)),
            sa.Column("is_authenticated", sa.Boolean(), nullable=False),
            sa.Column("is_bot", sa.Boolean(), nullable=False),
            sa.Column("environment", sa.String(16), nullable=False),
            sa.Column("properties_json", postgresql.JSONB(), nullable=False),
            sa.CheckConstraint(
                "event_name IN ('page_view', 'registration_completed', "
                "'search_completed', 'trip_created', 'outbound_click')",
                name="ck_analytics_event_name",
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("event_id", name="uq_analytics_event_id"),
        )
        for column in (
            "event_id",
            "event_name",
            "occurred_at",
            "received_at",
            "normalized_path",
            "locale",
            "session_hash",
            "visitor_day_hash",
            "country_code",
            "device_type",
            "referrer_type",
            "utm_source",
            "is_bot",
            "environment",
        ):
            op.create_index(f"ix_analytics_events_{column}", "analytics_events", [column])

    if "analytics_daily_rollups" not in tables:
        op.create_table(
            "analytics_daily_rollups",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("day", sa.Date(), nullable=False),
            sa.Column("environment", sa.String(16), nullable=False),
            sa.Column("is_bot", sa.Boolean(), nullable=False),
            sa.Column("metric", sa.String(32), nullable=False),
            sa.Column("dimension", sa.String(32), nullable=False),
            sa.Column("dimension_value", sa.String(128), nullable=False),
            sa.Column("value", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("value >= 0", name="ck_analytics_daily_rollup_value"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "day",
                "environment",
                "is_bot",
                "metric",
                "dimension",
                "dimension_value",
                name="uq_analytics_daily_rollup_key",
            ),
        )
        for column in ("day", "environment", "is_bot", "metric", "dimension"):
            op.create_index(
                f"ix_analytics_daily_rollups_{column}",
                "analytics_daily_rollups",
                [column],
            )


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    if "analytics_daily_rollups" in tables:
        op.drop_table("analytics_daily_rollups")
    if "analytics_events" in tables:
        op.drop_table("analytics_events")
