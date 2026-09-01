"""Add policy-aware Google place profiles and enrichment runs.

Revision ID: 0025_hotspot_place_enrichment
Revises: 0024_deployment_center
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0025_hotspot_place_enrichment"
down_revision: str | None = "0024_deployment_center"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _create_profiles() -> None:
    op.create_table(
        "hotspot_place_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("hotspot_id", sa.Uuid(), nullable=False),
        sa.Column("place_id_source", sa.String(16), nullable=False),
        sa.Column("match_status", sa.String(24), nullable=False),
        sa.Column("match_confidence", sa.Numeric(5, 4), nullable=True),
        sa.Column("match_evidence_json", sa.JSON(), nullable=False),
        sa.Column("candidate_place_id", sa.String(255), nullable=True),
        sa.Column("candidate_name", sa.String(255), nullable=True),
        sa.Column("candidate_address", sa.Text(), nullable=True),
        sa.Column("candidate_latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("candidate_longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("manual_official_website_url", sa.Text(), nullable=True),
        sa.Column("manual_official_website_source_url", sa.Text(), nullable=True),
        sa.Column("website_review_status", sa.String(24), nullable=False),
        sa.Column("google_maps_uri", sa.Text(), nullable=True),
        sa.Column("formatted_address", sa.Text(), nullable=True),
        sa.Column("google_latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("google_longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("plus_code_global", sa.String(32), nullable=True),
        sa.Column("plus_code_compound", sa.String(255), nullable=True),
        sa.Column("opening_hours_json", sa.JSON(), nullable=False),
        sa.Column("provider_website_uri", sa.Text(), nullable=True),
        sa.Column("provider_locale", sa.String(16), nullable=True),
        sa.Column("provider_attributions_json", sa.JSON(), nullable=False),
        sa.Column("provider_fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("provider_refresh_after", sa.DateTime(timezone=True), nullable=True),
        sa.Column("provider_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("review_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "match_status IN ('unmatched', 'pending', 'auto_approved', 'approved', "
            "'rejected', 'failed')",
            name="ck_hotspot_place_profile_match_status",
        ),
        sa.CheckConstraint(
            "place_id_source IN ('none', 'legacy', 'automatic', 'manual')",
            name="ck_hotspot_place_profile_place_id_source",
        ),
        sa.CheckConstraint(
            "website_review_status IN ('none', 'pending', 'auto_approved', 'approved', "
            "'rejected')",
            name="ck_hotspot_place_profile_website_review_status",
        ),
        sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hotspot_id"),
    )
    for column in (
        "hotspot_id",
        "match_status",
        "website_review_status",
        "provider_refresh_after",
        "provider_expires_at",
        "reviewed_by_user_id",
    ):
        op.create_index(f"ix_hotspot_place_profiles_{column}", "hotspot_place_profiles", [column])


def _create_runs() -> None:
    op.create_table(
        "hotspot_place_enrichment_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("idempotency_key", sa.String(255), nullable=False),
        sa.Column("mode", sa.String(32), nullable=False),
        sa.Column("scope_json", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("total_count", sa.Integer(), nullable=False),
        sa.Column("processed_count", sa.Integer(), nullable=False),
        sa.Column("published_count", sa.Integer(), nullable=False),
        sa.Column("pending_count", sa.Integer(), nullable=False),
        sa.Column("unmatched_count", sa.Integer(), nullable=False),
        sa.Column("failed_count", sa.Integer(), nullable=False),
        sa.Column("estimated_google_calls", sa.Integer(), nullable=False),
        sa.Column("actual_google_calls", sa.Integer(), nullable=False),
        sa.Column("progress_json", sa.JSON(), nullable=False),
        sa.Column("result_json", sa.JSON(), nullable=False),
        sa.Column("error_json", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'partial', 'completed', 'failed')",
            name="ck_hotspot_place_enrichment_status",
        ),
        sa.CheckConstraint(
            "mode IN ('missing_or_expired', 'force')",
            name="ck_hotspot_place_enrichment_mode",
        ),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "actor_user_id",
            "idempotency_key",
            name="uq_hotspot_place_enrichment_idempotency",
        ),
    )
    for column in ("actor_user_id", "status"):
        op.create_index(
            f"ix_hotspot_place_enrichment_runs_{column}",
            "hotspot_place_enrichment_runs",
            [column],
        )


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is None or not inspector.has_table("hotspot_place_profiles"):
        _create_profiles()
    if inspector is None or not inspector.has_table("hotspot_place_enrichment_runs"):
        _create_runs()
    op.execute(
        sa.text(
            "INSERT INTO hotspot_place_profiles "
            "(id, hotspot_id, place_id_source, match_status, match_evidence_json, "
            "website_review_status, opening_hours_json, provider_attributions_json, "
            "created_at, updated_at) "
            "SELECT gen_random_uuid(), id, 'legacy', 'approved', '{}', 'none', '{}', '[]', "
            "CURRENT_TIMESTAMP, CURRENT_TIMESTAMP FROM travel_hotspots "
            "WHERE google_place_id IS NOT NULL "
            "AND NOT EXISTS (SELECT 1 FROM hotspot_place_profiles p WHERE p.hotspot_id = "
            "travel_hotspots.id)"
        )
    )


def downgrade() -> None:
    op.drop_table("hotspot_place_enrichment_runs")
    op.drop_table("hotspot_place_profiles")
