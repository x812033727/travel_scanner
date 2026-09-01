"""Add multilingual attraction guides and privacy-preserving click totals.

Revision ID: 0018_hotspot_multilingual_guides
Revises: 0017_usage_settings
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context, op

revision: str = "0018_hotspot_multilingual_guides"
down_revision: str | None = "0017_usage_settings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _create_localizations() -> None:
    op.create_table(
        "hotspot_localizations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("hotspot_id", sa.Uuid(), nullable=False),
        sa.Column("locale", sa.String(16), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("aliases", sa.JSON(), nullable=False),
        sa.Column("search_terms", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')", name="ck_hotspot_localization_locale"
        ),
        sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hotspot_id", "locale", name="uq_hotspot_localization_locale"),
    )
    op.create_index("ix_hotspot_localizations_hotspot_id", "hotspot_localizations", ["hotspot_id"])
    op.create_index("ix_hotspot_localizations_locale", "hotspot_localizations", ["locale"])


def _create_guides() -> None:
    op.create_table(
        "hotspot_guides",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("hotspot_id", sa.Uuid(), nullable=False),
        sa.Column("content_type", sa.String(16), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("locale", sa.String(16), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("creator_name", sa.String(255), nullable=False),
        sa.Column("canonical_url", sa.Text(), nullable=False),
        sa.Column("provider_content_id", sa.String(255), nullable=True),
        sa.Column("thumbnail_url", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("view_count", sa.Integer(), nullable=True),
        sa.Column("language_confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("discovery_rank", sa.Integer(), nullable=True),
        sa.Column("review_status", sa.String(24), nullable=False),
        sa.Column("review_reason", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "content_type IN ('article', 'video')", name="ck_hotspot_guide_content_type"
        ),
        sa.CheckConstraint(
            "locale IN ('en', 'ja', 'ko', 'zh-TW', 'zh-CN')", name="ck_hotspot_guide_locale"
        ),
        sa.CheckConstraint(
            "review_status IN ('pending', 'approved', 'rejected', 'disabled')",
            name="ck_hotspot_guide_review_status",
        ),
        sa.ForeignKeyConstraint(["hotspot_id"], ["travel_hotspots.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hotspot_id", "canonical_url", name="uq_hotspot_guide_canonical_url"),
    )
    for column in (
        "hotspot_id",
        "content_type",
        "provider",
        "locale",
        "provider_content_id",
        "review_status",
        "reviewed_by_user_id",
    ):
        op.create_index(f"ix_hotspot_guides_{column}", "hotspot_guides", [column])


def _create_clicks() -> None:
    op.create_table(
        "hotspot_guide_click_daily",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guide_id", sa.Uuid(), nullable=False),
        sa.Column("observed_on", sa.Date(), nullable=False),
        sa.Column("unique_opens", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["guide_id"], ["hotspot_guides.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("guide_id", "observed_on", name="uq_hotspot_guide_click_day"),
    )
    op.create_index(
        "ix_hotspot_guide_click_daily_guide_id", "hotspot_guide_click_daily", ["guide_id"]
    )
    op.create_index(
        "ix_hotspot_guide_click_daily_observed_on", "hotspot_guide_click_daily", ["observed_on"]
    )


def upgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is None or not inspector.has_table("hotspot_localizations"):
        _create_localizations()
    if inspector is None or not inspector.has_table("hotspot_guides"):
        _create_guides()
    if inspector is None or not inspector.has_table("hotspot_guide_click_daily"):
        _create_clicks()


def downgrade() -> None:
    op.drop_table("hotspot_guide_click_daily")
    op.drop_table("hotspot_guides")
    op.drop_table("hotspot_localizations")
