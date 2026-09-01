"""Add outbound and return flight itinerary anchors.

Revision ID: 0023_flight_anchors
Revises: 0022_food_catalog
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0023_flight_anchors"
down_revision: str | None = "0022_food_catalog"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    checks = (
        {row.get("name") for row in inspector.get_check_constraints("trip_plan_items")}
        if inspector is not None
        else {"ck_trip_plan_item_system_role"}
    )
    with op.batch_alter_table("trip_plan_items") as batch:
        if "ck_trip_plan_item_system_role" in checks:
            batch.drop_constraint("ck_trip_plan_item_system_role", type_="check")
        batch.create_check_constraint(
            "ck_trip_plan_item_system_role",
            "system_role IS NULL OR system_role IN "
            "('outbound_flight', 'hotel_start', 'lunch', 'dinner', "
            "'hotel_end', 'return_flight')",
        )


def downgrade() -> None:
    with op.batch_alter_table("trip_plan_items") as batch:
        batch.drop_constraint("ck_trip_plan_item_system_role", type_="check")
    op.execute(
        sa.text(
            "UPDATE trip_plan_items SET system_role = NULL "
            "WHERE system_role IN ('outbound_flight', 'return_flight')"
        )
    )
    with op.batch_alter_table("trip_plan_items") as batch:
        batch.create_check_constraint(
            "ck_trip_plan_item_system_role",
            "system_role IS NULL OR system_role IN "
            "('hotel_start', 'lunch', 'dinner', 'hotel_end')",
        )
