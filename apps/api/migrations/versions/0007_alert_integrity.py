"""Add alert ownership lookup and duplicate protection.

Revision ID: 0007_alert_integrity
Revises: 0006_affiliate_clicks
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_alert_integrity"
down_revision: str | None = "0006_affiliate_clicks"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _columns(table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _indexes(table: str) -> set[str]:
    return {index["name"] for index in sa.inspect(op.get_bind()).get_indexes(table)}


def _constraints(table: str) -> set[str]:
    return {
        constraint["name"]
        for constraint in sa.inspect(op.get_bind()).get_unique_constraints(table)
        if constraint.get("name")
    }


def upgrade() -> None:
    uuid_pattern = (
        "^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
        "[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )
    for table in ("flight_offers", "hotel_offers"):
        if "public_offer_id" not in _columns(table):
            op.add_column(table, sa.Column("public_offer_id", sa.Uuid(), nullable=True))
        index_name = f"ix_{table}_public_offer_id"
        if index_name not in _indexes(table):
            op.create_index(index_name, table, ["public_offer_id"])
        op.execute(
            sa.text(
                f"""
                UPDATE {table}
                SET public_offer_id = CAST(data ->> 'id' AS UUID)
                WHERE public_offer_id IS NULL
                  AND data ->> 'id' ~* '{uuid_pattern}'
                """
            )
        )

    if "uq_price_alert_user_resource" not in _constraints("price_alerts"):
        op.execute(
            sa.text(
                """
                DELETE FROM price_alerts
                WHERE id IN (
                    SELECT id FROM (
                        SELECT id,
                               row_number() OVER (
                                   PARTITION BY user_id, resource_type, resource_id
                                   ORDER BY created_at DESC, id DESC
                               ) AS duplicate_position
                        FROM price_alerts
                    ) duplicates
                    WHERE duplicate_position > 1
                )
                """
            )
        )
        op.create_unique_constraint(
            "uq_price_alert_user_resource",
            "price_alerts",
            ["user_id", "resource_type", "resource_id"],
        )


def downgrade() -> None:
    if "uq_price_alert_user_resource" in _constraints("price_alerts"):
        op.drop_constraint("uq_price_alert_user_resource", "price_alerts", type_="unique")
    for table in ("hotel_offers", "flight_offers"):
        index_name = f"ix_{table}_public_offer_id"
        if index_name in _indexes(table):
            op.drop_index(index_name, table_name=table)
        if "public_offer_id" in _columns(table):
            op.drop_column(table, "public_offer_id")
