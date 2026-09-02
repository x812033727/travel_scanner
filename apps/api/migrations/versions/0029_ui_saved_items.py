"""Add account-synced hotspot and food favorites.

Revision ID: 0029_ui_saved_items
Revises: 0028_restaurant_sources
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision: str = "0029_ui_saved_items"
down_revision: str | None = "0028_restaurant_sources"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _tables() -> set[str]:
    if context.is_offline_mode():
        return set()
    return set(sa.inspect(op.get_bind()).get_table_names())


def _favorite_table(name: str, target_table: str, target_column: str, unique_name: str) -> None:
    op.create_table(
        name,
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(target_column, postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint([target_column], [f"{target_table}.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", target_column, name=unique_name),
    )
    op.create_index(f"ix_{name}_user_id", name, ["user_id"])
    op.create_index(f"ix_{name}_{target_column}", name, [target_column])


def upgrade() -> None:
    tables = _tables()
    if "hotspot_favorites" not in tables:
        _favorite_table(
            "hotspot_favorites", "travel_hotspots", "hotspot_id", "uq_hotspot_favorite"
        )
    if "food_favorites" not in tables:
        _favorite_table("food_favorites", "travel_foods", "food_id", "uq_food_favorite")


def downgrade() -> None:
    tables = _tables()
    if context.is_offline_mode() or "food_favorites" in tables:
        op.drop_table("food_favorites")
    if context.is_offline_mode() or "hotspot_favorites" in tables:
        op.drop_table("hotspot_favorites")
