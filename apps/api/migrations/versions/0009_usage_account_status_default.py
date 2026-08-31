"""Keep legacy usage-account status insertable.

Revision ID: 0009_usage_account_status
Revises: 0008_flight_status_lookups
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009_usage_account_status"
down_revision: str | None = "0008_flight_status_lookups"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("usage_accounts")
    }
    if "status" not in columns:
        op.add_column(
            "usage_accounts",
            sa.Column(
                "status",
                sa.String(length=32),
                server_default="active",
                nullable=False,
            ),
        )
        return
    op.execute("UPDATE usage_accounts SET status = 'active' WHERE status IS NULL")
    op.alter_column(
        "usage_accounts",
        "status",
        existing_type=sa.String(length=32),
        server_default="active",
        nullable=False,
    )


def downgrade() -> None:
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("usage_accounts")
    }
    if "status" in columns:
        op.alter_column(
            "usage_accounts",
            "status",
            existing_type=sa.String(length=32),
            server_default=None,
            nullable=False,
        )
