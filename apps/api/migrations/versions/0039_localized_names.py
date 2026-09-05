"""Five-locale plus original names on trip items and food merchants.

Revision ID: 0039_localized_names
Revises: 0038_trip_metadata
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0039_localized_names"
down_revision: str | None = "0038_trip_metadata"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (table, column): a JSON map of site-locale labels plus the original-script
# text. Trip items nest one map per field ({"title": {...}, "location_name":
# {...}}); merchants hold one flat map. Existing rows start empty and keep
# showing their stored single-language text until they are re-saved.
COLUMNS: tuple[tuple[str, str], ...] = (
    ("trip_plan_items", "names_json"),
    ("food_merchants", "names_json"),
)


def _columns(table: str) -> set[str]:
    if context.is_offline_mode():
        return set()
    inspector = sa.inspect(op.get_bind())
    return {str(column["name"]) for column in inspector.get_columns(table)}


def upgrade() -> None:
    for table, column in COLUMNS:
        if context.is_offline_mode() or column not in _columns(table):
            op.add_column(
                table,
                sa.Column(column, sa.JSON(), nullable=False, server_default="{}"),
            )


def downgrade() -> None:
    for table, column in COLUMNS:
        if context.is_offline_mode() or column in _columns(table):
            op.drop_column(table, column)
