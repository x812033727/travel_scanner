"""Add fixed meal slots and daily hotel anchors.

Revision ID: 0020_itinerary_system_slots
Revises: 0019_hotspot_destination_id
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0020_itinerary_system_slots"
down_revision: str | None = "0019_hotspot_destination_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    columns = (
        {column["name"] for column in inspector.get_columns("trip_plan_items")}
        if inspector is not None
        else set()
    )
    constraints = (
        {row.get("name") for row in inspector.get_unique_constraints("trip_plan_items")}
        if inspector is not None
        else set()
    )
    checks = (
        {row.get("name") for row in inspector.get_check_constraints("trip_plan_items")}
        if inspector is not None
        else set()
    )
    with op.batch_alter_table("trip_plan_items") as batch:
        if "system_role" not in columns:
            batch.add_column(sa.Column("system_role", sa.String(length=24), nullable=True))
        if "is_skipped" not in columns:
            batch.add_column(
                sa.Column(
                    "is_skipped",
                    sa.Boolean(),
                    nullable=False,
                    server_default=sa.false(),
                )
            )
        if "ck_trip_plan_item_system_role" not in checks:
            batch.create_check_constraint(
                "ck_trip_plan_item_system_role",
                "system_role IS NULL OR system_role IN "
                "('hotel_start', 'lunch', 'dinner', 'hotel_end')",
            )
        if "uq_trip_plan_item_system_role" not in constraints:
            batch.create_unique_constraint(
                "uq_trip_plan_item_system_role",
                ["trip_plan_id", "day_date", "system_role"],
            )


def downgrade() -> None:
    with op.batch_alter_table("trip_plan_items") as batch:
        batch.drop_constraint("uq_trip_plan_item_system_role", type_="unique")
        batch.drop_constraint("ck_trip_plan_item_system_role", type_="check")
        batch.drop_column("is_skipped")
        batch.drop_column("system_role")
