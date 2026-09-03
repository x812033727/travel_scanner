"""Persist the selected provider route alternative.

Revision ID: 0034_route_alternatives
Revises: 0033_social_login
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0034_route_alternatives"
down_revision: str | None = "0033_social_login"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "trip_route_segments"
COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object]], ...] = (
    ("provider_route_key", sa.String(length=64)),
    ("route_option_rank", sa.Integer()),
)


def _columns() -> set[str]:
    if context.is_offline_mode():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}


def upgrade() -> None:
    existing = _columns()
    for name, type_ in COLUMNS:
        if context.is_offline_mode() or name not in existing:
            op.add_column(TABLE, sa.Column(name, type_, nullable=True))


def downgrade() -> None:
    existing = _columns()
    for name, _type in reversed(COLUMNS):
        if context.is_offline_mode() or name in existing:
            op.drop_column(TABLE, name)
