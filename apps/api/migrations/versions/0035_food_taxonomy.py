"""Add food areas, categories, merchant taxonomy links and merchant favorites.

Revision ID: 0035_food_taxonomy
Revises: 0034_route_alternatives
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision: str = "0035_food_taxonomy"
down_revision: str | None = "0034_route_alternatives"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

MERCHANTS = "food_merchants"


def _inspector() -> sa.Inspector | None:
    if context.is_offline_mode():
        return None
    return sa.inspect(op.get_bind())


def _tables() -> set[str]:
    inspector = _inspector()
    return set(inspector.get_table_names()) if inspector else set()


def _columns(table: str) -> set[str]:
    inspector = _inspector()
    return {column["name"] for column in inspector.get_columns(table)} if inspector else set()


def _constraints(table: str) -> set[str]:
    inspector = _inspector()
    if inspector is None:
        return set()
    names: set[str] = set()
    for item in inspector.get_foreign_keys(table):
        names.add(str(item.get("name")))
    for item in inspector.get_indexes(table):
        names.add(str(item.get("name")))
    for item in inspector.get_check_constraints(table):
        names.add(str(item.get("name")))
    return names


def _timestamps() -> list[sa.Column[object]]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    tables = _tables()
    if "food_categories" not in tables:
        op.create_table(
            "food_categories",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("slug", sa.String(length=128), nullable=False),
            sa.Column("names_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("display_order", sa.Integer(), nullable=False, server_default="100"),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="admin"),
            *_timestamps(),
            sa.CheckConstraint("source IN ('seed', 'admin')", name="ck_food_category_source"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("slug"),
        )
        op.create_index("ix_food_categories_slug", "food_categories", ["slug"])
        op.create_index("ix_food_categories_is_active", "food_categories", ["is_active"])
    if "food_areas" not in tables:
        op.create_table(
            "food_areas",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("slug", sa.String(length=128), nullable=False),
            sa.Column("destination_id", sa.String(length=64), nullable=False),
            sa.Column("country_code", sa.String(length=2), nullable=False),
            sa.Column("names_json", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("match_terms_json", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
            sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
            sa.Column("display_order", sa.Integer(), nullable=False, server_default="100"),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="admin"),
            *_timestamps(),
            sa.CheckConstraint(
                "(latitude IS NULL) = (longitude IS NULL)", name="ck_food_area_coordinate_pair"
            ),
            sa.CheckConstraint("source IN ('seed', 'admin')", name="ck_food_area_source"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("slug"),
        )
        op.create_index("ix_food_areas_slug", "food_areas", ["slug"])
        op.create_index("ix_food_areas_destination_id", "food_areas", ["destination_id"])
        op.create_index("ix_food_areas_country_code", "food_areas", ["country_code"])
        op.create_index("ix_food_areas_is_active", "food_areas", ["is_active"])
        op.create_index(
            "ix_food_areas_destination_active", "food_areas", ["destination_id", "is_active"]
        )
    if "food_merchant_categories" not in tables:
        op.create_table(
            "food_merchant_categories",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("merchant_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("display_order", sa.Integer(), nullable=False, server_default="100"),
            sa.Column("source", sa.String(length=16), nullable=False, server_default="admin"),
            sa.ForeignKeyConstraint(["merchant_id"], [f"{MERCHANTS}.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["category_id"], ["food_categories.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("merchant_id", "category_id", name="uq_food_merchant_category"),
        )
        op.create_index(
            "ix_food_merchant_categories_merchant_id", "food_merchant_categories", ["merchant_id"]
        )
        op.create_index(
            "ix_food_merchant_categories_category_id", "food_merchant_categories", ["category_id"]
        )
    if "food_merchant_favorites" not in tables:
        op.create_table(
            "food_merchant_favorites",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("merchant_id", postgresql.UUID(as_uuid=True), nullable=False),
            *_timestamps(),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["merchant_id"], [f"{MERCHANTS}.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "merchant_id", name="uq_food_merchant_favorite"),
        )
        op.create_index(
            "ix_food_merchant_favorites_user_id", "food_merchant_favorites", ["user_id"]
        )
        op.create_index(
            "ix_food_merchant_favorites_merchant_id", "food_merchant_favorites", ["merchant_id"]
        )

    columns = _columns(MERCHANTS)
    constraints = _constraints(MERCHANTS)
    if context.is_offline_mode() or "area_id" not in columns:
        op.add_column(MERCHANTS, sa.Column("area_id", postgresql.UUID(as_uuid=True), nullable=True))
    if context.is_offline_mode() or "area_source" not in columns:
        op.add_column(MERCHANTS, sa.Column("area_source", sa.String(length=16), nullable=True))
    if context.is_offline_mode() or "fk_food_merchants_area_id" not in constraints:
        op.create_foreign_key(
            "fk_food_merchants_area_id",
            MERCHANTS,
            "food_areas",
            ["area_id"],
            ["id"],
            ondelete="SET NULL",
        )
    if context.is_offline_mode() or "ix_food_merchants_area_id" not in constraints:
        op.create_index("ix_food_merchants_area_id", MERCHANTS, ["area_id"])
    if context.is_offline_mode() or "ck_food_merchant_area_source" not in constraints:
        op.create_check_constraint(
            "ck_food_merchant_area_source",
            MERCHANTS,
            "area_source IS NULL OR area_source IN ('seed', 'admin')",
        )


def downgrade() -> None:
    columns = _columns(MERCHANTS)
    constraints = _constraints(MERCHANTS)
    if context.is_offline_mode() or "ck_food_merchant_area_source" in constraints:
        op.drop_constraint("ck_food_merchant_area_source", MERCHANTS, type_="check")
    if context.is_offline_mode() or "ix_food_merchants_area_id" in constraints:
        op.drop_index("ix_food_merchants_area_id", table_name=MERCHANTS)
    if context.is_offline_mode() or "fk_food_merchants_area_id" in constraints:
        op.drop_constraint("fk_food_merchants_area_id", MERCHANTS, type_="foreignkey")
    if context.is_offline_mode() or "area_source" in columns:
        op.drop_column(MERCHANTS, "area_source")
    if context.is_offline_mode() or "area_id" in columns:
        op.drop_column(MERCHANTS, "area_id")
    tables = _tables()
    for table in (
        "food_merchant_favorites",
        "food_merchant_categories",
        "food_areas",
        "food_categories",
    ):
        if context.is_offline_mode() or table in tables:
            op.drop_table(table)
