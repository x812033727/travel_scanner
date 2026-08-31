"""Add itinerary route-planner fields.

Revision ID: 0004_itinerary_route_planner
Revises: 0003_usage_packs
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0004_itinerary_route_planner"
down_revision: str | None = "0003_usage_packs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    plan_columns = (
        {column["name"] for column in inspector.get_columns("trip_plans")}
        if inspector is not None
        else set()
    )
    item_columns = (
        {column["name"] for column in inspector.get_columns("trip_plan_items")}
        if inspector is not None
        else set()
    )
    plan_additions = {
        "destination_name": sa.Column("destination_name", sa.String(255), nullable=True),
        "destination_place_id": sa.Column("destination_place_id", sa.String(255), nullable=True),
        "start_date": sa.Column("start_date", sa.Date(), nullable=True),
        "end_date": sa.Column("end_date", sa.Date(), nullable=True),
        "timezone": sa.Column("timezone", sa.String(64), server_default="UTC", nullable=False),
        "route_preference": sa.Column(
            "route_preference", sa.String(32), server_default="FEWER_TRANSFERS", nullable=False
        ),
    }
    item_additions = {
        "provider_place_id": sa.Column("provider_place_id", sa.String(255), nullable=True),
        "location_source": sa.Column("location_source", sa.String(32), nullable=True),
        "duration_minutes": sa.Column("duration_minutes", sa.Integer(), nullable=True),
        "notes": sa.Column("notes", sa.Text(), nullable=True),
        "fixed_time": sa.Column(
            "fixed_time", sa.Boolean(), server_default=sa.false(), nullable=False
        ),
    }
    for name, column in plan_additions.items():
        if name not in plan_columns:
            op.add_column("trip_plans", column)
    for name, column in item_additions.items():
        if name not in item_columns:
            op.add_column("trip_plan_items", column)


def downgrade() -> None:
    for column in (
        "fixed_time",
        "notes",
        "duration_minutes",
        "location_source",
        "provider_place_id",
    ):
        op.drop_column("trip_plan_items", column)
    for column in (
        "route_preference",
        "timezone",
        "end_date",
        "start_date",
        "destination_place_id",
        "destination_name",
    ):
        op.drop_column("trip_plans", column)
