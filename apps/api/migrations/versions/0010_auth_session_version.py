"""Add an authentication version for server-side session invalidation.

Revision ID: 0010_auth_session_version
Revises: 0009_usage_account_status
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_auth_session_version"
down_revision: str | None = "0009_usage_account_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {str(column["name"]) for column in sa.inspect(op.get_bind()).get_columns("users")}
    if "auth_version" not in columns:
        op.add_column(
            "users",
            sa.Column("auth_version", sa.Integer(), server_default="1", nullable=False),
        )
        op.alter_column("users", "auth_version", server_default=None)


def downgrade() -> None:
    columns = {str(column["name"]) for column in sa.inspect(op.get_bind()).get_columns("users")}
    if "auth_version" in columns:
        op.drop_column("users", "auth_version")
