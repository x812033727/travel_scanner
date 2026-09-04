"""Add the user's persisted display currency.

Revision ID: 0037_user_preferred_currency
Revises: 0036_food_taxonomy
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0037_user_preferred_currency"
down_revision: str | None = "0036_food_taxonomy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("users")
    }
    if "preferred_currency" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "preferred_currency",
                sa.String(length=3),
                nullable=False,
                server_default="TWD",
            ),
        )


def downgrade() -> None:
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("users")
    }
    if "preferred_currency" in columns:
        op.drop_column("users", "preferred_currency")
