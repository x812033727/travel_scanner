"""Remove Plus Code storage from hotspots, food merchants and trip items.

Revision ID: 0032_remove_plus_codes
Revises: 0031_trip_item_coordinates
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0032_remove_plus_codes"
down_revision: str | None = "0031_trip_item_coordinates"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

COLUMNS: dict[str, tuple[tuple[str, sa.types.TypeEngine[object]], ...]] = {
    "travel_hotspots": (("plus_code_global", sa.String(length=16)),),
    "hotspot_place_profiles": (
        ("plus_code_global", sa.String(length=32)),
        ("plus_code_compound", sa.String(length=255)),
    ),
    "food_merchants": (("plus_code_global", sa.String(length=16)),),
    "trip_plan_items": (("plus_code_global", sa.String(length=16)),),
}

INDEXES: tuple[tuple[str, str], ...] = (
    ("travel_hotspots", "ix_travel_hotspots_plus_code_global"),
    ("food_merchants", "ix_food_merchants_plus_code_global"),
    ("trip_plan_items", "ix_trip_plan_items_plus_code_global"),
)


def _columns(table: str) -> set[str]:
    if context.is_offline_mode():
        return set()
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _indexes(table: str) -> set[str]:
    if context.is_offline_mode():
        return set()
    return {index["name"] for index in sa.inspect(op.get_bind()).get_indexes(table)}


def upgrade() -> None:
    offline = context.is_offline_mode()
    trip_columns = _columns("trip_plan_items")
    if offline or "data" in trip_columns:
        op.execute(
            sa.text(
                "UPDATE trip_plan_items "
                "SET data = (data::jsonb - 'plus_code_global')::json "
                "WHERE data::jsonb ? 'plus_code_global'"
            )
        )

    for table, index in INDEXES:
        if offline or index in _indexes(table):
            op.drop_index(index, table_name=table)

    for table, columns in COLUMNS.items():
        existing = _columns(table)
        for name, _ in columns:
            if offline or name in existing:
                op.drop_column(table, name)


def downgrade() -> None:
    offline = context.is_offline_mode()
    for table, columns in COLUMNS.items():
        existing = _columns(table)
        for name, type_ in columns:
            if offline or name not in existing:
                op.add_column(table, sa.Column(name, type_, nullable=True))

    for table, index in INDEXES:
        if offline or index not in _indexes(table):
            op.create_index(index, table, ["plus_code_global"])
