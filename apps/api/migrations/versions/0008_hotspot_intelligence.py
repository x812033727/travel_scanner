"""Add searchable travel hotspots, signals, and ranking snapshots.

Revision ID: 0008_hotspot_intelligence
Revises: 0007_alert_integrity
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_hotspot_intelligence"
down_revision: str | None = "0007_alert_integrity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    tables = set(sa.inspect(op.get_bind()).get_table_names())
    if "travel_hotspots" not in tables:
        op.create_table(
            "travel_hotspots",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("slug", sa.String(length=128), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("city_code", sa.String(length=8), nullable=False),
            sa.Column("city_name", sa.String(length=100), nullable=False),
            sa.Column("country_code", sa.String(length=2), nullable=False),
            sa.Column("country_name", sa.String(length=100), nullable=False),
            sa.Column("category", sa.String(length=32), nullable=False),
            sa.Column("search_text", sa.Text(), nullable=False),
            sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=True),
            sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=True),
            sa.Column("wikipedia_project", sa.String(length=64), nullable=True),
            sa.Column("wikipedia_title", sa.String(length=255), nullable=True),
            sa.Column("google_place_id", sa.String(length=255), nullable=True),
            sa.Column("source_urls", sa.JSON(), nullable=False),
            sa.Column("metadata_json", sa.JSON(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("slug"),
        )
        for column in (
            "slug",
            "name",
            "city_code",
            "country_code",
            "category",
            "google_place_id",
            "is_active",
        ):
            op.create_index(f"ix_travel_hotspots_{column}", "travel_hotspots", [column])

    if "hotspot_signals" not in tables:
        op.create_table(
            "hotspot_signals",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("hotspot_id", sa.Uuid(), nullable=False),
            sa.Column("source", sa.String(length=64), nullable=False),
            sa.Column("metric", sa.String(length=64), nullable=False),
            sa.Column("value", sa.Numeric(precision=18, scale=4), nullable=False),
            sa.Column("observed_on", sa.Date(), nullable=False),
            sa.Column("window_days", sa.Integer(), nullable=False),
            sa.Column("source_url", sa.Text(), nullable=True),
            sa.Column("is_estimate", sa.Boolean(), nullable=False),
            sa.Column("metadata_json", sa.JSON(), nullable=False),
            sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint(
                "hotspot_id",
                "source",
                "metric",
                "observed_on",
                name="uq_hotspot_signal_observation",
            ),
        )
        for column in ("hotspot_id", "source", "metric", "observed_on"):
            op.create_index(f"ix_hotspot_signals_{column}", "hotspot_signals", [column])

    if "hotspot_rankings" in tables:
        return
    op.create_table(
        "hotspot_rankings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("hotspot_id", sa.Uuid(), nullable=False),
        sa.Column("scope", sa.String(length=16), nullable=False),
        sa.Column("scope_key", sa.String(length=32), nullable=False),
        sa.Column("window_days", sa.Integer(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("score", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("interest_score", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("growth_score", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("quality_score", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("confidence_score", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("observed_on", sa.Date(), nullable=False),
        sa.Column("explanation", sa.JSON(), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "hotspot_id",
            "scope",
            "scope_key",
            "window_days",
            "observed_on",
            name="uq_hotspot_ranking_snapshot",
        ),
    )
    for column in ("hotspot_id", "scope", "scope_key", "observed_on"):
        op.create_index(f"ix_hotspot_rankings_{column}", "hotspot_rankings", [column])


def downgrade() -> None:
    tables = set(sa.inspect(op.get_bind()).get_table_names())
    for table in ("hotspot_rankings", "hotspot_signals", "travel_hotspots"):
        if table in tables:
            op.drop_table(table)
