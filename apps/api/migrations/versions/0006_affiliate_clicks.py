"""Add append-only affiliate click tracking.

Revision ID: 0006_affiliate_clicks
Revises: 0005_admin_provider_settings
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0006_affiliate_clicks"
down_revision: str | None = "0005_admin_provider_settings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is None or not inspector.has_table("affiliate_clicks"):
        op.create_table(
            "affiliate_clicks",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("user_id", sa.Uuid(), nullable=False),
            sa.Column("search_id", sa.Uuid(), nullable=True),
            sa.Column("trip_id", sa.Uuid(), nullable=True),
            sa.Column("offer_id", sa.Uuid(), nullable=True),
            sa.Column("partner", sa.String(64), nullable=False),
            sa.Column("module", sa.String(32), nullable=False),
            sa.Column("sub_id", sa.String(64), nullable=False),
            sa.Column("destination_summary", sa.String(128), nullable=False),
            sa.Column("target_host", sa.String(255), nullable=False),
            sa.Column("status", sa.String(32), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
    indexes = (
        set()
        if context.is_offline_mode()
        else {
            str(item["name"])
            for item in sa.inspect(op.get_bind()).get_indexes("affiliate_clicks")
        }
    )
    for column in (
        "user_id",
        "search_id",
        "trip_id",
        "offer_id",
        "partner",
        "module",
        "sub_id",
    ):
        index = f"ix_affiliate_clicks_{column}"
        if index not in indexes:
            op.create_index(index, "affiliate_clicks", [column])
            indexes.add(index)
    if op.get_bind().dialect.name == "postgresql":
        op.execute(
            """
            CREATE OR REPLACE FUNCTION prevent_affiliate_click_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION 'affiliate_clicks is append-only';
            END;
            $$ LANGUAGE plpgsql
            """
        )
        op.execute("DROP TRIGGER IF EXISTS affiliate_clicks_append_only ON affiliate_clicks")
        op.execute(
            """
            CREATE TRIGGER affiliate_clicks_append_only
            BEFORE UPDATE OR DELETE ON affiliate_clicks
            FOR EACH ROW EXECUTE FUNCTION prevent_affiliate_click_mutation()
            """
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS affiliate_clicks_append_only ON affiliate_clicks")
        op.execute("DROP FUNCTION IF EXISTS prevent_affiliate_click_mutation()")
    for column in (
        "sub_id",
        "module",
        "partner",
        "offer_id",
        "trip_id",
        "search_id",
        "user_id",
    ):
        op.drop_index(f"ix_affiliate_clicks_{column}", table_name="affiliate_clicks")
    op.drop_table("affiliate_clicks")
