"""Add explainable deep-travel fields to hotspots.

Revision ID: 0015_hotspot_depth_travel
Revises: 0014_user_preferred_locale
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0015_hotspot_depth_travel"
down_revision: str | None = "0014_user_preferred_locale"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    columns = {
        str(column["name"]) for column in sa.inspect(op.get_bind()).get_columns("travel_hotspots")
    }
    if "is_deep_travel" not in columns:
        op.add_column(
            "travel_hotspots",
            sa.Column("is_deep_travel", sa.Boolean(), nullable=False, server_default=sa.false()),
        )
        op.alter_column("travel_hotspots", "is_deep_travel", server_default=None)
    if "depth_kind" not in columns:
        op.add_column("travel_hotspots", sa.Column("depth_kind", sa.String(24), nullable=True))
    if "depth_score" not in columns:
        op.add_column("travel_hotspots", sa.Column("depth_score", sa.Numeric(5, 2), nullable=True))
    indexes = {item["name"] for item in sa.inspect(op.get_bind()).get_indexes("travel_hotspots")}
    if "ix_travel_hotspots_is_deep_travel" not in indexes:
        op.create_index("ix_travel_hotspots_is_deep_travel", "travel_hotspots", ["is_deep_travel"])
    checks = {
        item["name"] for item in sa.inspect(op.get_bind()).get_check_constraints("travel_hotspots")
    }
    if "ck_travel_hotspots_depth_kind" not in checks:
        op.create_check_constraint(
            "ck_travel_hotspots_depth_kind",
            "travel_hotspots",
            "depth_kind IS NULL OR depth_kind IN ('urban_local', 'day_trip')",
        )
    if "ck_travel_hotspots_depth_score" not in checks:
        op.create_check_constraint(
            "ck_travel_hotspots_depth_score",
            "travel_hotspots",
            "depth_score IS NULL OR (depth_score >= 0 AND depth_score <= 100)",
        )


def downgrade() -> None:
    op.drop_constraint("ck_travel_hotspots_depth_score", "travel_hotspots", type_="check")
    op.drop_constraint("ck_travel_hotspots_depth_kind", "travel_hotspots", type_="check")
    op.drop_index("ix_travel_hotspots_is_deep_travel", table_name="travel_hotspots")
    op.drop_column("travel_hotspots", "depth_score")
    op.drop_column("travel_hotspots", "depth_kind")
    op.drop_column("travel_hotspots", "is_deep_travel")
