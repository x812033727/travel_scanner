"""Add supplemental map identity review facts without changing catalog publication.

Revision ID: 0070_map_identity_metadata
Revises: 0069_site_pages
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0070_map_identity_metadata"
down_revision: str | None = "0069_site_pages"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    columns = (
        {column["name"] for column in inspector.get_columns("food_merchants")}
        if inspector
        else set()
    )
    # 0001 creates current metadata when installing into an empty database.
    if "map_identity_metadata" not in columns:
        op.add_column(
            "food_merchants",
            sa.Column("map_identity_metadata", sa.JSON(), nullable=False, server_default="{}"),
        )


def downgrade() -> None:
    op.drop_column("food_merchants", "map_identity_metadata")
