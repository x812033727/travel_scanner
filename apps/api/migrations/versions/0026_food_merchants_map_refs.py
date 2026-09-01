"""Add reviewed food merchants and named map references.

Revision ID: 0026_food_merchants_map_refs
Revises: 0025_hotspot_place_enrichment
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0026_food_merchants_map_refs"
down_revision: str | None = "0025_hotspot_place_enrichment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    hotspot_columns = {
        column["name"] for column in inspector.get_columns("travel_hotspots")
    }
    if "naver_map_url" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("naver_map_url", sa.String(length=2048), nullable=True),
        )
    if "plus_code_global" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("plus_code_global", sa.String(length=16), nullable=True),
        )
    if "coordinate_source_type" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("coordinate_source_type", sa.String(length=32), nullable=True),
        )
    if "coordinate_source_url" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("coordinate_source_url", sa.String(length=2048), nullable=True),
        )
    if "coordinate_verified_at" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("coordinate_verified_at", sa.DateTime(timezone=True), nullable=True),
        )
    if "map_match_status" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column(
                "map_match_status",
                sa.String(length=24),
                nullable=False,
                server_default="unverified",
            ),
        )
    if "map_verified_at" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("map_verified_at", sa.DateTime(timezone=True), nullable=True),
        )
    if "map_verified_by_user_id" not in hotspot_columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("map_verified_by_user_id", sa.Uuid(), nullable=True),
        )
    op.execute(
        sa.text(
            "UPDATE travel_hotspots SET latitude = NULL, longitude = NULL "
            "WHERE (latitude IS NULL) <> (longitude IS NULL)"
        )
    )
    op.execute(
        sa.text(
            "UPDATE travel_hotspots SET google_place_id = NULL "
            "WHERE google_place_id IS NOT NULL AND btrim(google_place_id) = ''"
        )
    )
    op.execute(
        sa.text(
            "WITH ranked AS ("
            "SELECT id, row_number() OVER "
            "(PARTITION BY google_place_id ORDER BY created_at, id) rn "
            "FROM travel_hotspots WHERE google_place_id IS NOT NULL"
            ") UPDATE travel_hotspots AS hotspot "
            "SET google_place_id = NULL, map_match_status = 'ambiguous' "
            "FROM ranked WHERE hotspot.id = ranked.id AND ranked.rn > 1"
        )
    )
    check_names = {
        constraint["name"]
        for constraint in inspector.get_check_constraints("travel_hotspots")
    }
    if "ck_travel_hotspot_map_match_status" not in check_names:
        op.create_check_constraint(
            "ck_travel_hotspot_map_match_status",
            "travel_hotspots",
            "map_match_status IN ('unverified', 'verified', 'ambiguous', 'disabled')",
        )
    if "ck_travel_hotspot_coordinate_pair" not in check_names:
        op.create_check_constraint(
            "ck_travel_hotspot_coordinate_pair",
            "travel_hotspots",
            "(latitude IS NULL) = (longitude IS NULL)",
        )
    foreign_key_columns = {
        tuple(constraint["constrained_columns"])
        for constraint in inspector.get_foreign_keys("travel_hotspots")
    }
    if ("map_verified_by_user_id",) not in foreign_key_columns:
        op.create_foreign_key(
            "fk_travel_hotspots_map_verified_by_user_id",
            "travel_hotspots",
            "users",
            ["map_verified_by_user_id"],
            ["id"],
            ondelete="SET NULL",
        )
    index_names = {index["name"] for index in inspector.get_indexes("travel_hotspots")}
    for index_name, column in (
        ("ix_travel_hotspots_map_match_status", "map_match_status"),
        ("ix_travel_hotspots_plus_code_global", "plus_code_global"),
        ("ix_travel_hotspots_map_verified_by_user_id", "map_verified_by_user_id"),
    ):
        if index_name not in index_names:
            op.create_index(index_name, "travel_hotspots", [column])
    unique_columns = {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints("travel_hotspots")
    }
    unique_columns.update(
        tuple(index["column_names"])
        for index in inspector.get_indexes("travel_hotspots")
        if index["unique"]
    )
    if ("google_place_id",) not in unique_columns:
        op.create_unique_constraint(
            "uq_travel_hotspots_google_place_id", "travel_hotspots", ["google_place_id"]
        )
    if ("naver_map_url",) not in unique_columns:
        op.create_unique_constraint(
            "uq_travel_hotspots_naver_map_url", "travel_hotspots", ["naver_map_url"]
        )

    # The initial migration creates current metadata on a fresh database. In that
    # path all merchant tables already exist and this revision only needs to stamp.
    if "food_merchants" in tables:
        return

    op.create_table(
        "food_merchants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("destination_id", sa.String(length=64), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("local_name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("plus_code_global", sa.String(length=16), nullable=True),
        sa.Column("coordinate_source_type", sa.String(length=32), nullable=True),
        sa.Column("coordinate_source_url", sa.String(length=2048), nullable=True),
        sa.Column("coordinate_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("google_place_id", sa.String(length=255), nullable=True),
        sa.Column("naver_map_url", sa.String(length=2048), nullable=True),
        sa.Column("map_match_status", sa.String(length=24), nullable=False),
        sa.Column("review_status", sa.String(length=24), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
            name="ck_food_merchant_review_status",
        ),
        sa.CheckConstraint(
            "map_match_status IN ('unverified', 'verified', 'ambiguous', 'disabled')",
            name="ck_food_merchant_map_match_status",
        ),
        sa.CheckConstraint(
            "(latitude IS NULL) = (longitude IS NULL)",
            name="ck_food_merchant_coordinate_pair",
        ),
        sa.ForeignKeyConstraint(["verified_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("google_place_id"),
        sa.UniqueConstraint("naver_map_url"),
    )
    for column in (
        "slug",
        "destination_id",
        "country_code",
        "name",
        "google_place_id",
        "plus_code_global",
        "map_match_status",
        "review_status",
        "is_active",
        "verified_by_user_id",
    ):
        op.create_index(f"ix_food_merchants_{column}", "food_merchants", [column])

    op.create_table(
        "food_merchant_foods",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("merchant_id", sa.Uuid(), nullable=False),
        sa.Column("food_id", sa.Uuid(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["food_id"], ["travel_foods.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["merchant_id"], ["food_merchants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("merchant_id", "food_id", name="uq_food_merchant_food"),
    )
    op.create_index("ix_food_merchant_foods_merchant_id", "food_merchant_foods", ["merchant_id"])
    op.create_index("ix_food_merchant_foods_food_id", "food_merchant_foods", ["food_id"])

    op.create_table(
        "food_merchant_sources",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("merchant_id", sa.Uuid(), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("source_title", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.String(length=2048), nullable=False),
        sa.Column("edition_year", sa.Integer(), nullable=True),
        sa.Column("distinction", sa.String(length=24), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "source_type IN ('official_tourism', 'merchant_official', 'michelin_licensed')",
            name="ck_food_merchant_source_type",
        ),
        sa.CheckConstraint(
            "distinction IS NULL OR distinction IN "
            "('three_star', 'two_star', 'one_star', 'green_star', "
            "'bib_gourmand', 'selected')",
            name="ck_food_merchant_distinction",
        ),
        sa.ForeignKeyConstraint(["merchant_id"], ["food_merchants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "merchant_id", "source_url", "edition_year", name="uq_food_merchant_source"
        ),
    )
    op.create_index(
        "ix_food_merchant_sources_merchant_id", "food_merchant_sources", ["merchant_id"]
    )
    op.create_index(
        "ix_food_merchant_sources_source_type", "food_merchant_sources", ["source_type"]
    )
    op.create_index("ix_food_merchant_sources_is_current", "food_merchant_sources", ["is_current"])


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    for table in ("food_merchant_sources", "food_merchant_foods", "food_merchants"):
        if table in tables:
            op.drop_table(table)

    hotspot_indexes = {
        index["name"]: index for index in inspector.get_indexes("travel_hotspots")
    }
    recreated_google_index = False
    for constraint in inspector.get_unique_constraints("travel_hotspots"):
        if tuple(constraint["column_names"]) in {
            ("google_place_id",),
            ("naver_map_url",),
        } and constraint["name"]:
            op.drop_constraint(constraint["name"], "travel_hotspots", type_="unique")
    for index_name, index in hotspot_indexes.items():
        columns = tuple(index["column_names"])
        if index["unique"] and columns in {("google_place_id",), ("naver_map_url",)}:
            op.drop_index(index_name, table_name="travel_hotspots")
            recreated_google_index = recreated_google_index or columns == ("google_place_id",)
    for index_name in (
        "ix_travel_hotspots_map_verified_by_user_id",
        "ix_travel_hotspots_plus_code_global",
        "ix_travel_hotspots_map_match_status",
    ):
        if index_name in hotspot_indexes:
            op.drop_index(index_name, table_name="travel_hotspots")
    if recreated_google_index:
        op.create_index(
            "ix_travel_hotspots_google_place_id",
            "travel_hotspots",
            ["google_place_id"],
        )

    for constraint in inspector.get_check_constraints("travel_hotspots"):
        if constraint["name"] in {
            "ck_travel_hotspot_coordinate_pair",
            "ck_travel_hotspot_map_match_status",
        }:
            op.drop_constraint(constraint["name"], "travel_hotspots", type_="check")
    for constraint in inspector.get_foreign_keys("travel_hotspots"):
        if tuple(constraint["constrained_columns"]) == ("map_verified_by_user_id",):
            op.drop_constraint(constraint["name"], "travel_hotspots", type_="foreignkey")

    hotspot_columns = {
        column["name"] for column in inspector.get_columns("travel_hotspots")
    }
    for column in (
        "map_verified_by_user_id",
        "map_verified_at",
        "map_match_status",
        "coordinate_verified_at",
        "coordinate_source_url",
        "coordinate_source_type",
        "plus_code_global",
        "naver_map_url",
    ):
        if column in hotspot_columns:
            op.drop_column("travel_hotspots", column)
