"""Add hotspot discovery and review workflow fields.

Revision ID: 0013_hotspot_discovery
Revises: 0012_line_price_alerts
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0013_hotspot_discovery"
down_revision: str | None = "0012_line_price_alerts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {
        str(column["name"]) for column in sa.inspect(op.get_bind()).get_columns("travel_hotspots")
    }
    additions = (
        ("wikidata_item_id", sa.String(length=32), True, None),
        ("origin", sa.String(length=32), False, "'curated'"),
        ("review_status", sa.String(length=24), False, "'approved'"),
        ("review_reason", sa.Text(), True, None),
        ("discovery_distance_km", sa.Numeric(8, 2), True, None),
        ("discovered_at", sa.DateTime(timezone=True), True, None),
        ("last_seen_at", sa.DateTime(timezone=True), True, None),
        ("reviewed_at", sa.DateTime(timezone=True), True, None),
        ("reviewed_by_user_id", sa.Uuid(), True, None),
    )
    for name, column_type, nullable, default in additions:
        if name not in columns:
            op.add_column(
                "travel_hotspots",
                sa.Column(name, column_type, nullable=nullable, server_default=default),
            )
            if default is not None:
                op.alter_column("travel_hotspots", name, server_default=None)
    constraints = {
        item["name"] for item in sa.inspect(op.get_bind()).get_unique_constraints("travel_hotspots")
    }
    if "uq_travel_hotspots_wikidata_item_id" not in constraints:
        op.create_unique_constraint(
            "uq_travel_hotspots_wikidata_item_id",
            "travel_hotspots",
            ["wikidata_item_id"],
        )
    foreign_keys = {
        item["name"] for item in sa.inspect(op.get_bind()).get_foreign_keys("travel_hotspots")
    }
    if "fk_travel_hotspots_reviewed_by_user_id" not in foreign_keys:
        op.create_foreign_key(
            "fk_travel_hotspots_reviewed_by_user_id",
            "travel_hotspots",
            "users",
            ["reviewed_by_user_id"],
            ["id"],
            ondelete="SET NULL",
        )
    indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("travel_hotspots")}
    for column in (
        "wikidata_item_id",
        "origin",
        "review_status",
        "reviewed_by_user_id",
    ):
        name = f"ix_travel_hotspots_{column}"
        if name not in indexes:
            op.create_index(name, "travel_hotspots", [column])


def downgrade() -> None:
    indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("travel_hotspots")}
    for column in (
        "reviewed_by_user_id",
        "review_status",
        "origin",
        "wikidata_item_id",
    ):
        name = f"ix_travel_hotspots_{column}"
        if name in indexes:
            op.drop_index(name, table_name="travel_hotspots")
    constraints = {
        item["name"] for item in sa.inspect(op.get_bind()).get_unique_constraints("travel_hotspots")
    }
    if "uq_travel_hotspots_wikidata_item_id" in constraints:
        op.drop_constraint("uq_travel_hotspots_wikidata_item_id", "travel_hotspots", type_="unique")
    foreign_keys = {
        item["name"] for item in sa.inspect(op.get_bind()).get_foreign_keys("travel_hotspots")
    }
    if "fk_travel_hotspots_reviewed_by_user_id" in foreign_keys:
        op.drop_constraint(
            "fk_travel_hotspots_reviewed_by_user_id", "travel_hotspots", type_="foreignkey"
        )
    columns = {
        str(column["name"]) for column in sa.inspect(op.get_bind()).get_columns("travel_hotspots")
    }
    for name in (
        "reviewed_by_user_id",
        "reviewed_at",
        "last_seen_at",
        "discovered_at",
        "discovery_distance_km",
        "review_reason",
        "review_status",
        "origin",
        "wikidata_item_id",
    ):
        if name in columns:
            op.drop_column("travel_hotspots", name)
