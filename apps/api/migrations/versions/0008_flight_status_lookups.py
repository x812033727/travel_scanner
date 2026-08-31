"""Add minimized flight status lookups.

Revision ID: 0008_flight_status_lookups
Revises: 0007_alert_integrity
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_flight_status_lookups"
down_revision: str | None = "0007_alert_integrity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "flight_status_lookups" in inspector.get_table_names():
        return
    op.create_table(
        "flight_status_lookups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("reservation_id", sa.Uuid(), nullable=True),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("query_json", sa.JSON(), nullable=False),
        sa.Column("result_json", sa.JSON(), nullable=False),
        sa.Column("cache_hit", sa.Boolean(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["reservation_id"], ["usage_reservations.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_flight_status_lookups_user_id", "flight_status_lookups", ["user_id"])
    op.create_index(
        "ix_flight_status_lookups_reservation_id", "flight_status_lookups", ["reservation_id"]
    )
    op.create_index(
        "ix_flight_status_lookups_expires_at", "flight_status_lookups", ["expires_at"]
    )


def downgrade() -> None:
    if "flight_status_lookups" not in sa.inspect(op.get_bind()).get_table_names():
        return
    op.drop_index("ix_flight_status_lookups_expires_at", table_name="flight_status_lookups")
    op.drop_index("ix_flight_status_lookups_reservation_id", table_name="flight_status_lookups")
    op.drop_index("ix_flight_status_lookups_user_id", table_name="flight_status_lookups")
    op.drop_table("flight_status_lookups")
