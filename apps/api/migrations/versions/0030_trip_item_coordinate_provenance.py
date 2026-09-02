"""Add coordinate provenance columns to trip plan items.

Revision ID: 0030_trip_item_coordinates
Revises: 0029_ui_saved_items
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0030_trip_item_coordinates"
down_revision: str | None = "0029_ui_saved_items"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "trip_plan_items"
INDEX = "ix_trip_plan_items_plus_code_global"

COLUMNS: tuple[tuple[str, sa.types.TypeEngine[object]], ...] = (
    ("plus_code_global", sa.String(length=16)),
    ("coordinate_source_type", sa.String(length=32)),
    ("coordinate_source_url", sa.String(length=2048)),
    ("coordinate_verified_at", sa.DateTime(timezone=True)),
)


def _columns() -> set[str]:
    if context.is_offline_mode():
        return set()
    return {col["name"] for col in sa.inspect(op.get_bind()).get_columns(TABLE)}


def _indexes() -> set[str]:
    if context.is_offline_mode():
        return set()
    return {idx["name"] for idx in sa.inspect(op.get_bind()).get_indexes(TABLE)}


def upgrade() -> None:
    existing = _columns()
    for name, type_ in COLUMNS:
        if context.is_offline_mode() or name not in existing:
            op.add_column(TABLE, sa.Column(name, type_, nullable=True))
    if context.is_offline_mode() or INDEX not in _indexes():
        op.create_index(INDEX, TABLE, ["plus_code_global"])


def downgrade() -> None:
    if context.is_offline_mode() or INDEX in _indexes():
        op.drop_index(INDEX, table_name=TABLE)
    existing = _columns()
    for name, _type in reversed(COLUMNS):
        if context.is_offline_mode() or name in existing:
            op.drop_column(TABLE, name)
