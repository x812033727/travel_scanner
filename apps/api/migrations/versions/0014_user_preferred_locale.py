"""Add the user's persisted UI locale.

Revision ID: 0014_user_preferred_locale
Revises: 0013_hotspot_discovery
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014_user_preferred_locale"
down_revision: str | None = "0013_hotspot_discovery"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("users")
    }
    if "preferred_locale" not in columns:
        op.add_column(
            "users",
            sa.Column(
                "preferred_locale",
                sa.String(length=16),
                nullable=False,
                server_default="zh-TW",
            ),
        )


def downgrade() -> None:
    columns = {
        str(column["name"])
        for column in sa.inspect(op.get_bind()).get_columns("users")
    }
    if "preferred_locale" in columns:
        op.drop_column("users", "preferred_locale")
