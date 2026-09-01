"""Persist selected itinerary routes and daily routing settings.

Revision ID: 0016_trip_route_segments
Revises: 0015_hotspot_depth_travel
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0016_trip_route_segments"
down_revision: str | None = "0015_hotspot_depth_travel"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "trip_route_day_settings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trip_plan_id", sa.Uuid(), nullable=False),
        sa.Column("day_date", sa.Date(), nullable=False),
        sa.Column("default_travel_mode", sa.String(length=16), nullable=False),
        sa.Column("default_buffer_minutes", sa.Integer(), nullable=False),
        sa.Column("route_preference", sa.String(length=32), nullable=False),
        sa.Column("auto_compute", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "default_buffer_minutes >= 0 AND default_buffer_minutes <= 180",
            name="ck_trip_route_day_buffer",
        ),
        sa.CheckConstraint(
            "default_travel_mode IN ('transit', 'walk', 'drive')",
            name="ck_trip_route_day_mode",
        ),
        sa.ForeignKeyConstraint(["trip_plan_id"], ["trip_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trip_plan_id", "day_date", name="uq_trip_route_day_setting"),
    )
    op.create_index(
        "ix_trip_route_day_settings_trip_plan_id",
        "trip_route_day_settings",
        ["trip_plan_id"],
    )
    op.create_index(
        "ix_trip_route_day_settings_day_date",
        "trip_route_day_settings",
        ["day_date"],
    )

    op.create_table(
        "trip_route_segments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trip_plan_id", sa.Uuid(), nullable=False),
        sa.Column("day_date", sa.Date(), nullable=False),
        sa.Column("from_item_id", sa.Uuid(), nullable=False),
        sa.Column("to_item_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("travel_mode", sa.String(length=16), nullable=False),
        sa.Column("is_override", sa.Boolean(), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("attribution", sa.String(length=255), nullable=False),
        sa.Column("preference", sa.String(length=32), nullable=False),
        sa.Column("schedule_mode", sa.String(length=24), nullable=False),
        sa.Column("requested_departure_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("departure_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("arrival_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ready_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("buffer_minutes", sa.Integer(), nullable=False),
        sa.Column("distance_meters", sa.Integer(), nullable=True),
        sa.Column("fare", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.Column("encoded_polyline", sa.Text(), nullable=True),
        sa.Column("maps_url", sa.Text(), nullable=True),
        sa.Column("steps", sa.JSON(), nullable=False),
        sa.Column("details_available", sa.JSON(), nullable=False),
        sa.Column("warnings", sa.JSON(), nullable=False),
        sa.Column("manual_note", sa.String(length=255), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "buffer_minutes >= 0 AND buffer_minutes <= 180",
            name="ck_trip_route_segment_buffer",
        ),
        sa.CheckConstraint("duration_minutes > 0", name="ck_trip_route_segment_duration"),
        sa.CheckConstraint(
            "travel_mode IN ('transit', 'walk', 'drive')",
            name="ck_trip_route_segment_mode",
        ),
        sa.ForeignKeyConstraint(["from_item_id"], ["trip_plan_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["to_item_id"], ["trip_plan_items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_plan_id"], ["trip_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "trip_plan_id",
            "from_item_id",
            "to_item_id",
            name="uq_trip_route_segment_pair",
        ),
    )
    for column in ("trip_plan_id", "day_date", "from_item_id", "to_item_id"):
        op.create_index(
            f"ix_trip_route_segments_{column}",
            "trip_route_segments",
            [column],
        )


def downgrade() -> None:
    op.drop_table("trip_route_segments")
    op.drop_table("trip_route_day_settings")
