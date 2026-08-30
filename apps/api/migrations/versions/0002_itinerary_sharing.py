"""Add editable itinerary and secret trip sharing.

Revision ID: 0002_itinerary_sharing
Revises: 0001_initial
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0002_itinerary_sharing"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 0001 uses Base.metadata.create_all. On a fresh install it therefore sees
    # the current model, while an existing database still needs these columns.
    # Inspecting keeps both upgrade paths idempotent until 0001 can be frozen.
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

    if "version" not in plan_columns:
        op.add_column(
            "trip_plans",
            sa.Column("version", sa.Integer(), server_default=sa.text("1"), nullable=False),
        )
    additions = {
        "day_date": sa.Column("day_date", sa.Date(), nullable=True),
        "position": sa.Column(
            "position", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        "title": sa.Column("title", sa.String(255), nullable=True),
        "location_name": sa.Column("location_name", sa.String(255), nullable=True),
        "start_time": sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        "end_time": sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        "latitude": sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
        "longitude": sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
        "locked": sa.Column(
            "locked", sa.Boolean(), server_default=sa.false(), nullable=False
        ),
        "is_estimated": sa.Column(
            "is_estimated", sa.Boolean(), server_default=sa.false(), nullable=False
        ),
    }
    for name, column in additions.items():
        if name not in item_columns:
            op.add_column("trip_plan_items", column)

    has_share_table = inspector is not None and inspector.has_table("trip_shares")
    if not has_share_table:
        op.create_table(
            "trip_shares",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("trip_plan_id", sa.Uuid(), nullable=False),
            sa.Column("token_hash", sa.String(64), nullable=False),
            sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["trip_plan_id"], ["trip_plans.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("token_hash"),
            sa.UniqueConstraint("trip_plan_id", name="uq_trip_share_trip"),
        )
        op.create_index("ix_trip_shares_trip_plan_id", "trip_shares", ["trip_plan_id"])
        op.create_index("ix_trip_shares_token_hash", "trip_shares", ["token_hash"])


def downgrade() -> None:
    op.drop_index("ix_trip_shares_token_hash", table_name="trip_shares")
    op.drop_index("ix_trip_shares_trip_plan_id", table_name="trip_shares")
    op.drop_table("trip_shares")
    for column in (
        "is_estimated",
        "locked",
        "longitude",
        "latitude",
        "end_time",
        "start_time",
        "location_name",
        "title",
        "position",
        "day_date",
    ):
        op.drop_column("trip_plan_items", column)
    op.drop_column("trip_plans", "version")
