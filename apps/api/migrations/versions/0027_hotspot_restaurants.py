"""Add hotspot restaurant discovery identities and scan progress.

Revision ID: 0027_hotspot_restaurants
Revises: 0026_food_merchants_map_refs
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.dialects import postgresql

revision: str = "0027_hotspot_restaurants"
down_revision: str | None = "0026_food_merchants_map_refs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _inspector() -> sa.Inspector | None:
    return None if context.is_offline_mode() else sa.inspect(op.get_bind())


def upgrade() -> None:
    # 0001 creates current Base.metadata on a fresh database. Guard every table
    # so both fresh installs and upgrades from 0024 are valid.
    inspector = _inspector()
    existing = set(inspector.get_table_names()) if inspector is not None else set()

    if "restaurant_places" not in existing:
        op.create_table(
            "restaurant_places",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("google_place_id", sa.String(length=255), nullable=False),
            sa.Column("generated_maps_url", sa.String(length=2048), nullable=False),
            sa.Column("is_suppressed", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("suppression_reason", sa.Text(), nullable=True),
            sa.Column("suppressed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("suppressed_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["suppressed_by_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("google_place_id"),
        )
        op.create_index(
            "ix_restaurant_places_google_place_id", "restaurant_places", ["google_place_id"]
        )
        op.create_index(
            "ix_restaurant_places_is_suppressed", "restaurant_places", ["is_suppressed"]
        )
        op.create_index(
            "ix_restaurant_places_suppressed_by_user_id",
            "restaurant_places",
            ["suppressed_by_user_id"],
        )

    if "restaurant_scan_runs" not in existing:
        op.create_table(
            "restaurant_scan_runs",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("hotspot_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("idempotency_key", sa.String(length=255), nullable=False),
            sa.Column("status", sa.String(length=24), nullable=False, server_default="queued"),
            sa.Column("radius_meters", sa.Integer(), nullable=False, server_default="10000"),
            sa.Column("cells_total", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("cells_completed", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("candidate_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("aggregate_calls", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("details_calls", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("failure_code", sa.String(length=64), nullable=True),
            sa.Column("failure_detail", sa.Text(), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "metadata_json",
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=False,
                server_default="{}",
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "status IN ('queued', 'running', 'partial', 'completed', 'failed', 'quota_paused')",
                name="ck_restaurant_scan_status",
            ),
            sa.CheckConstraint("radius_meters IN (5000, 10000)", name="ck_restaurant_scan_radius"),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("idempotency_key"),
        )
        op.create_index(
            "ix_restaurant_scan_runs_hotspot_id", "restaurant_scan_runs", ["hotspot_id"]
        )
        op.create_index(
            "ix_restaurant_scan_runs_actor_user_id", "restaurant_scan_runs", ["actor_user_id"]
        )
        op.create_index("ix_restaurant_scan_runs_status", "restaurant_scan_runs", ["status"])

    if "restaurant_scan_cells" not in existing:
        op.create_table(
            "restaurant_scan_cells",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("parent_cell_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column("status", sa.String(length=24), nullable=False, server_default="queued"),
            sa.Column("center_latitude", sa.Numeric(9, 6), nullable=False),
            sa.Column("center_longitude", sa.Numeric(9, 6), nullable=False),
            sa.Column("radius_meters", sa.Integer(), nullable=False),
            sa.Column("depth", sa.Integer(), nullable=False, server_default="0"),
            sa.Column(
                "provider_place_ids",
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=False,
                server_default="[]",
            ),
            sa.Column("details_cursor", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("error_code", sa.String(length=64), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "status IN ('queued', 'running', 'split', 'completed', 'partial', 'failed')",
                name="ck_restaurant_scan_cell_status",
            ),
            sa.ForeignKeyConstraint(["run_id"], ["restaurant_scan_runs.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(
                ["parent_cell_id"], ["restaurant_scan_cells.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "run_id",
                "center_latitude",
                "center_longitude",
                "radius_meters",
                "depth",
                name="uq_restaurant_scan_cell_geometry",
            ),
        )
        op.create_index("ix_restaurant_scan_cells_run_id", "restaurant_scan_cells", ["run_id"])
        op.create_index(
            "ix_restaurant_scan_cells_parent_cell_id", "restaurant_scan_cells", ["parent_cell_id"]
        )
        op.create_index("ix_restaurant_scan_cells_status", "restaurant_scan_cells", ["status"])

    if "hotspot_restaurant_candidates" not in existing:
        op.create_table(
            "hotspot_restaurant_candidates",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("hotspot_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("restaurant_place_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("scan_run_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column(
                "discovery_radius_meters", sa.Integer(), nullable=False, server_default="10000"
            ),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(
                ["restaurant_place_id"], ["restaurant_places.id"], ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["scan_run_id"], ["restaurant_scan_runs.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "hotspot_id", "restaurant_place_id", name="uq_hotspot_restaurant_candidate"
            ),
        )
        op.create_index(
            "ix_hotspot_restaurant_candidates_hotspot_id",
            "hotspot_restaurant_candidates",
            ["hotspot_id"],
        )
        op.create_index(
            "ix_hotspot_restaurant_candidates_restaurant_place_id",
            "hotspot_restaurant_candidates",
            ["restaurant_place_id"],
        )
        op.create_index(
            "ix_hotspot_restaurant_candidates_scan_run_id",
            "hotspot_restaurant_candidates",
            ["scan_run_id"],
        )

def downgrade() -> None:
    op.drop_index(
        "ix_hotspot_restaurant_candidates_scan_run_id", table_name="hotspot_restaurant_candidates"
    )
    op.drop_index(
        "ix_hotspot_restaurant_candidates_restaurant_place_id",
        table_name="hotspot_restaurant_candidates",
    )
    op.drop_index(
        "ix_hotspot_restaurant_candidates_hotspot_id", table_name="hotspot_restaurant_candidates"
    )
    op.drop_table("hotspot_restaurant_candidates")
    op.drop_index("ix_restaurant_scan_cells_status", table_name="restaurant_scan_cells")
    op.drop_index("ix_restaurant_scan_cells_parent_cell_id", table_name="restaurant_scan_cells")
    op.drop_index("ix_restaurant_scan_cells_run_id", table_name="restaurant_scan_cells")
    op.drop_table("restaurant_scan_cells")
    op.drop_index("ix_restaurant_scan_runs_status", table_name="restaurant_scan_runs")
    op.drop_index("ix_restaurant_scan_runs_actor_user_id", table_name="restaurant_scan_runs")
    op.drop_index("ix_restaurant_scan_runs_hotspot_id", table_name="restaurant_scan_runs")
    op.drop_table("restaurant_scan_runs")
    op.drop_index("ix_restaurant_places_suppressed_by_user_id", table_name="restaurant_places")
    op.drop_index("ix_restaurant_places_is_suppressed", table_name="restaurant_places")
    op.drop_index("ix_restaurant_places_google_place_id", table_name="restaurant_places")
    op.drop_table("restaurant_places")
