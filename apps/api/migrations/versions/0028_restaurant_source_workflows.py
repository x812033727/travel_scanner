"""Add restaurant identity, editorial sources and favorites.

Revision ID: 0028_restaurant_sources
Revises: 0027_hotspot_restaurants
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision: str = "0028_restaurant_sources"
down_revision: str | None = "0027_hotspot_restaurants"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _inspector() -> sa.Inspector | None:
    return None if context.is_offline_mode() else sa.inspect(op.get_bind())


def upgrade() -> None:
    inspector = _inspector()
    tables = set(inspector.get_table_names()) if inspector is not None else set()

    if "restaurant_places" in tables:
        columns = {item["name"] for item in inspector.get_columns("restaurant_places")}
        additions = (
            (
                "identity_status",
                sa.Column(
                    "identity_status",
                    sa.String(length=24),
                    nullable=False,
                    server_default="unknown",
                ),
            ),
            ("successor_place_id", sa.Column("successor_place_id", sa.String(255))),
            (
                "identity_checked_at",
                sa.Column("identity_checked_at", sa.DateTime(timezone=True)),
            ),
            ("identity_error_code", sa.Column("identity_error_code", sa.String(64))),
        )
        for name, column in additions:
            if name not in columns:
                op.add_column("restaurant_places", column)
        checks = {
            constraint["name"]
            for constraint in inspector.get_check_constraints("restaurant_places")
        }
        if "ck_restaurant_place_identity_status" not in checks:
            op.create_check_constraint(
                "ck_restaurant_place_identity_status",
                "restaurant_places",
                "identity_status IN ('unknown', 'active', 'moved', 'not_found')",
            )
        indexes = {item["name"] for item in inspector.get_indexes("restaurant_places")}
        for index_name, column in (
            ("ix_restaurant_places_identity_status", "identity_status"),
            ("ix_restaurant_places_identity_checked_at", "identity_checked_at"),
        ):
            if index_name not in indexes:
                op.create_index(index_name, "restaurant_places", [column])

    if "food_merchants" in tables:
        columns = {item["name"] for item in inspector.get_columns("food_merchants")}
        if "official_website_url" not in columns:
            op.add_column(
                "food_merchants",
                sa.Column("official_website_url", sa.String(length=2048)),
            )
        if "official_website_verified_at" not in columns:
            op.add_column(
                "food_merchants",
                sa.Column("official_website_verified_at", sa.DateTime(timezone=True)),
            )

    if "food_merchant_sources" in tables:
        columns = {
            item["name"] for item in inspector.get_columns("food_merchant_sources")
        }
        if "source_scope" not in columns:
            op.add_column(
                "food_merchant_sources",
                sa.Column(
                    "source_scope",
                    sa.String(length=32),
                    nullable=False,
                    server_default="destination_context",
                ),
            )
        if "claims_json" not in columns:
            op.add_column(
                "food_merchant_sources",
                sa.Column(
                    "claims_json",
                    postgresql.JSONB(astext_type=sa.Text()),
                    nullable=False,
                    server_default="[]",
                ),
            )
        checks = {
            constraint["name"]
            for constraint in inspector.get_check_constraints("food_merchant_sources")
        }
        if "ck_food_merchant_source_scope" not in checks:
            op.create_check_constraint(
                "ck_food_merchant_source_scope",
                "food_merchant_sources",
                "source_scope IN ('destination_context', 'merchant_listing', "
                "'merchant_website', 'coordinates')",
            )
        indexes = {
            item["name"] for item in inspector.get_indexes("food_merchant_sources")
        }
        if "ix_food_merchant_sources_source_scope" not in indexes:
            op.create_index(
                "ix_food_merchant_sources_source_scope",
                "food_merchant_sources",
                ["source_scope"],
            )

    if "restaurant_favorites" not in tables:
        op.create_table(
            "restaurant_favorites",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("restaurant_place_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(
                ["restaurant_place_id"], ["restaurant_places.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "user_id", "restaurant_place_id", name="uq_restaurant_favorite"
            ),
        )
        op.create_index("ix_restaurant_favorites_user_id", "restaurant_favorites", ["user_id"])
        op.create_index(
            "ix_restaurant_favorites_restaurant_place_id",
            "restaurant_favorites",
            ["restaurant_place_id"],
        )

    if "restaurant_editorial_profiles" not in tables:
        op.create_table(
            "restaurant_editorial_profiles",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("restaurant_place_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("display_name", sa.String(length=255), nullable=False),
            sa.Column("local_name", sa.String(length=255), nullable=True),
            sa.Column("address", sa.Text(), nullable=True),
            sa.Column("official_website_url", sa.String(length=2048), nullable=True),
            sa.Column("ride_latitude", sa.Numeric(9, 6), nullable=True),
            sa.Column("ride_longitude", sa.Numeric(9, 6), nullable=True),
            sa.Column(
                "review_status", sa.String(length=24), nullable=False, server_default="pending"
            ),
            sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("verified_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
                name="ck_restaurant_editorial_review_status",
            ),
            sa.CheckConstraint(
                "(ride_latitude IS NULL) = (ride_longitude IS NULL)",
                name="ck_restaurant_editorial_coordinate_pair",
            ),
            sa.ForeignKeyConstraint(
                ["restaurant_place_id"], ["restaurant_places.id"], ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["verified_by_user_id"], ["users.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("restaurant_place_id", name="uq_restaurant_editorial_place"),
        )
        for column in (
            "restaurant_place_id",
            "display_name",
            "review_status",
            "verified_by_user_id",
        ):
            op.create_index(
                f"ix_restaurant_editorial_profiles_{column}",
                "restaurant_editorial_profiles",
                [column],
            )

    if "restaurant_editorial_sources" not in tables:
        op.create_table(
            "restaurant_editorial_sources",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("profile_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("source_type", sa.String(length=32), nullable=False),
            sa.Column("source_title", sa.String(length=255), nullable=False),
            sa.Column("source_url", sa.String(length=2048), nullable=False),
            sa.Column(
                "claims_json",
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=False,
                server_default="[]",
            ),
            sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "source_type IN ('merchant_official', 'official_tourism')",
                name="ck_restaurant_editorial_source_type",
            ),
            sa.ForeignKeyConstraint(
                ["profile_id"], ["restaurant_editorial_profiles.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "profile_id", "source_url", name="uq_restaurant_editorial_source_url"
            ),
        )
        op.create_index(
            "ix_restaurant_editorial_sources_profile_id",
            "restaurant_editorial_sources",
            ["profile_id"],
        )
        op.create_index(
            "ix_restaurant_editorial_sources_source_type",
            "restaurant_editorial_sources",
            ["source_type"],
        )


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    for table in (
        "restaurant_editorial_sources",
        "restaurant_editorial_profiles",
        "restaurant_favorites",
    ):
        if table in tables:
            op.drop_table(table)

    if "food_merchant_sources" in tables:
        columns = {
            item["name"] for item in inspector.get_columns("food_merchant_sources")
        }
        if "claims_json" in columns:
            op.drop_column("food_merchant_sources", "claims_json")
        if "source_scope" in columns:
            op.drop_column("food_merchant_sources", "source_scope")
    if "food_merchants" in tables:
        columns = {item["name"] for item in inspector.get_columns("food_merchants")}
        if "official_website_verified_at" in columns:
            op.drop_column("food_merchants", "official_website_verified_at")
        if "official_website_url" in columns:
            op.drop_column("food_merchants", "official_website_url")
    if "restaurant_places" in tables:
        columns = {item["name"] for item in inspector.get_columns("restaurant_places")}
        for column in (
            "identity_error_code",
            "identity_checked_at",
            "successor_place_id",
            "identity_status",
        ):
            if column in columns:
                op.drop_column("restaurant_places", column)
