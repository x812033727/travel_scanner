"""Trip metadata: lifecycle status and cover image.

Revision ID: 0038_trip_metadata
Revises: 0037_user_preferred_currency
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0038_trip_metadata"
down_revision: str | None = "0037_user_preferred_currency"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

STATUS_INDEX = "ix_trip_plans_status"


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {str(column["name"]) for column in inspector.get_columns("trip_plans")}
    if "status" not in columns:
        # Values {planning, ready, travelling, closed} are enforced in
        # Pydantic on purpose — no CHECK, so extending the set is not DDL.
        op.add_column(
            "trip_plans",
            sa.Column("status", sa.String(length=16), nullable=False, server_default="planning"),
        )
    if "cover_image_url" not in columns:
        op.add_column(
            "trip_plans",
            sa.Column("cover_image_url", sa.String(length=1024), nullable=True),
        )
    indexes = {str(index["name"]) for index in inspector.get_indexes("trip_plans")}
    if STATUS_INDEX not in indexes:
        op.create_index(STATUS_INDEX, "trip_plans", ["status"])


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    indexes = {str(index["name"]) for index in inspector.get_indexes("trip_plans")}
    if STATUS_INDEX in indexes:
        op.drop_index(STATUS_INDEX, table_name="trip_plans")
    columns = {str(column["name"]) for column in inspector.get_columns("trip_plans")}
    if "cover_image_url" in columns:
        op.drop_column("trip_plans", "cover_image_url")
    if "status" in columns:
        op.drop_column("trip_plans", "status")
