"""Add the curated country food catalog.

Revision ID: 0022_food_catalog
Revises: 0021_hotspot_guide_ai_search
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0022_food_catalog"
down_revision: str | None = "0021_hotspot_guide_ai_search"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table("travel_foods"):
        op.create_table(
            "travel_foods",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("slug", sa.String(length=128), nullable=False),
            sa.Column("country_code", sa.String(length=2), nullable=False),
            sa.Column("local_name", sa.String(length=255), nullable=False),
            sa.Column("romanized_name", sa.String(length=255), nullable=False),
            sa.Column("food_kind", sa.String(length=24), nullable=False),
            sa.Column("meal_types", sa.JSON(), nullable=False),
            sa.Column("ingredient_tags", sa.JSON(), nullable=False),
            sa.Column("dietary_notes", sa.JSON(), nullable=False),
            sa.Column("search_text", sa.Text(), nullable=False),
            sa.Column("source_urls", sa.JSON(), nullable=False),
            sa.Column("review_status", sa.String(length=24), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("display_order", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "food_kind IN ('main', 'noodle_soup', 'street_food', 'dessert', 'drink')",
                name="ck_travel_food_kind",
            ),
            sa.CheckConstraint(
                "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
                name="ck_travel_food_review_status",
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("slug"),
        )
        for column in ("slug", "country_code", "food_kind", "review_status", "is_active"):
            op.create_index(f"ix_travel_foods_{column}", "travel_foods", [column])
    if not inspector.has_table("food_localizations"):
        op.create_table(
            "food_localizations",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("food_id", sa.Uuid(), nullable=False),
            sa.Column("locale", sa.String(length=16), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("summary", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')",
                name="ck_food_localization_locale",
            ),
            sa.ForeignKeyConstraint(["food_id"], ["travel_foods.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("food_id", "locale", name="uq_food_localization_locale"),
        )
        op.create_index("ix_food_localizations_food_id", "food_localizations", ["food_id"])
        op.create_index("ix_food_localizations_locale", "food_localizations", ["locale"])
    if not inspector.has_table("food_destinations"):
        op.create_table(
            "food_destinations",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("food_id", sa.Uuid(), nullable=False),
            sa.Column("destination_id", sa.String(length=64), nullable=False),
            sa.Column("display_order", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["food_id"], ["travel_foods.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("food_id", "destination_id", name="uq_food_destination"),
        )
        op.create_index("ix_food_destinations_food_id", "food_destinations", ["food_id"])
        op.create_index(
            "ix_food_destinations_destination_id", "food_destinations", ["destination_id"]
        )
    if not inspector.has_table("food_hotspots"):
        op.create_table(
            "food_hotspots",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("food_id", sa.Uuid(), nullable=False),
            sa.Column("hotspot_id", sa.Uuid(), nullable=False),
            sa.Column("display_order", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["food_id"], ["travel_foods.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("food_id", "hotspot_id", name="uq_food_hotspot"),
        )
        op.create_index("ix_food_hotspots_food_id", "food_hotspots", ["food_id"])
        op.create_index("ix_food_hotspots_hotspot_id", "food_hotspots", ["hotspot_id"])


def downgrade() -> None:
    op.drop_table("food_hotspots")
    op.drop_table("food_destinations")
    op.drop_table("food_localizations")
    op.drop_table("travel_foods")
