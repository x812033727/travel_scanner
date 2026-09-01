"""Add reviewed food merchants and named map references.

Revision ID: 0024_food_merchants_and_map_refs
Revises: 0023_flight_anchors
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0024_food_merchants_and_map_refs"
down_revision: str | None = "0023_flight_anchors"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "travel_hotspots", sa.Column("naver_map_url", sa.String(length=2048), nullable=True)
    )
    op.add_column(
        "travel_hotspots", sa.Column("plus_code_global", sa.String(length=16), nullable=True)
    )
    op.add_column(
        "travel_hotspots", sa.Column("coordinate_source_type", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "travel_hotspots", sa.Column("coordinate_source_url", sa.String(length=2048), nullable=True)
    )
    op.add_column(
        "travel_hotspots",
        sa.Column("coordinate_verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "travel_hotspots",
        sa.Column(
            "map_match_status",
            sa.String(length=24),
            nullable=False,
            server_default="unverified",
        ),
    )
    op.add_column(
        "travel_hotspots",
        sa.Column("map_verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column("travel_hotspots", sa.Column("map_verified_by_user_id", sa.Uuid(), nullable=True))
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
    op.create_check_constraint(
        "ck_travel_hotspot_map_match_status",
        "travel_hotspots",
        "map_match_status IN ('unverified', 'verified', 'ambiguous', 'disabled')",
    )
    op.create_check_constraint(
        "ck_travel_hotspot_coordinate_pair",
        "travel_hotspots",
        "(latitude IS NULL) = (longitude IS NULL)",
    )
    op.create_foreign_key(
        "fk_travel_hotspots_map_verified_by_user_id",
        "travel_hotspots",
        "users",
        ["map_verified_by_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_travel_hotspots_map_match_status", "travel_hotspots", ["map_match_status"])
    op.create_index("ix_travel_hotspots_plus_code_global", "travel_hotspots", ["plus_code_global"])
    op.create_index(
        "ix_travel_hotspots_map_verified_by_user_id",
        "travel_hotspots",
        ["map_verified_by_user_id"],
    )
    op.create_unique_constraint(
        "uq_travel_hotspots_google_place_id", "travel_hotspots", ["google_place_id"]
    )
    op.create_unique_constraint(
        "uq_travel_hotspots_naver_map_url", "travel_hotspots", ["naver_map_url"]
    )

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
    op.drop_table("food_merchant_sources")
    op.drop_table("food_merchant_foods")
    op.drop_table("food_merchants")
    op.drop_index("ix_travel_hotspots_map_verified_by_user_id", table_name="travel_hotspots")
    op.drop_index("ix_travel_hotspots_plus_code_global", table_name="travel_hotspots")
    op.drop_index("ix_travel_hotspots_map_match_status", table_name="travel_hotspots")
    op.drop_constraint("uq_travel_hotspots_naver_map_url", "travel_hotspots", type_="unique")
    op.drop_constraint("uq_travel_hotspots_google_place_id", "travel_hotspots", type_="unique")
    op.drop_constraint(
        "ck_travel_hotspot_coordinate_pair", "travel_hotspots", type_="check"
    )
    op.drop_constraint(
        "ck_travel_hotspot_map_match_status", "travel_hotspots", type_="check"
    )
    op.drop_constraint(
        "fk_travel_hotspots_map_verified_by_user_id", "travel_hotspots", type_="foreignkey"
    )
    op.drop_column("travel_hotspots", "map_verified_by_user_id")
    op.drop_column("travel_hotspots", "map_verified_at")
    op.drop_column("travel_hotspots", "map_match_status")
    op.drop_column("travel_hotspots", "coordinate_verified_at")
    op.drop_column("travel_hotspots", "coordinate_source_url")
    op.drop_column("travel_hotspots", "coordinate_source_type")
    op.drop_column("travel_hotspots", "plus_code_global")
    op.drop_column("travel_hotspots", "naver_map_url")
