"""Store the geographic area a hotspot's coordinates resolve to.

Revision ID: 0035_hotspot_area_code
Revises: 0034_route_alternatives
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0035_hotspot_area_code"
down_revision: str | None = "0034_route_alternatives"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "travel_hotspots"
COLUMN = "area_code"
INDEX = "ix_travel_hotspots_area_code"


def _columns() -> set[str]:
    if context.is_offline_mode():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}


def _indexes() -> set[str]:
    if context.is_offline_mode():
        return set()
    return {
        name
        for index in sa.inspect(op.get_bind()).get_indexes(TABLE)
        if (name := index.get("name"))
    }


def upgrade() -> None:
    if context.is_offline_mode() or COLUMN not in _columns():
        op.add_column(TABLE, sa.Column(COLUMN, sa.String(length=32), nullable=True))
    if context.is_offline_mode() or INDEX not in _indexes():
        op.create_index(INDEX, TABLE, [COLUMN])


def downgrade() -> None:
    if context.is_offline_mode() or INDEX in _indexes():
        op.drop_index(INDEX, table_name=TABLE)
    if context.is_offline_mode() or COLUMN in _columns():
        op.drop_column(TABLE, COLUMN)
