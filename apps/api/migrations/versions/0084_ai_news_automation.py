"""Disabled-by-default hourly multilingual news automation.

Revision ID: 0084_ai_news_automation
Revises: 0083_merchant_platform_source
"""

from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "0084_ai_news_automation"
down_revision: str | None = "0083_merchant_platform_source"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamps() -> list[sa.Column[object]]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    settings_table = op.create_table(
        "news_automation_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("mode", sa.String(16), nullable=False, server_default="shadow"),
        sa.Column("writer_provider", sa.String(16), nullable=False, server_default="openai"),
        sa.Column("writer_model", sa.String(128), nullable=True),
        sa.Column("verifier_provider", sa.String(16), nullable=False, server_default="openai"),
        sa.Column("verifier_model", sa.String(128), nullable=True),
        sa.Column("global_concurrency", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("per_vertical_concurrency", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("min_shadow_days", sa.Integer(), nullable=False, server_default="14"),
        sa.Column("min_shadow_candidates", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("min_human_agreement", sa.Float(), nullable=False, server_default="0.95"),
        sa.Column("jev_act_confidence", sa.Float(), nullable=False, server_default="0.9"),
        sa.Column("auto_publish_ai", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("auto_publish_tech", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("auto_publish_crypto", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("shadow_started_at_ai", sa.DateTime(timezone=True), nullable=False),
        sa.Column("shadow_started_at_tech", sa.DateTime(timezone=True), nullable=False),
        sa.Column("shadow_started_at_crypto", sa.DateTime(timezone=True), nullable=False),
        sa.Column("prompt_version", sa.String(32), nullable=False, server_default="news-v1"),
        sa.Column("policy_version", sa.String(32), nullable=False, server_default="news-policy-v1"),
        sa.Column(
            "updated_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        *timestamps(),
        sa.CheckConstraint("id = 1", name="ck_news_automation_settings_singleton"),
        sa.CheckConstraint("mode IN ('shadow', 'automatic')", name="ck_news_automation_mode"),
        sa.CheckConstraint(
            "writer_provider IN ('openai','anthropic','minimax','gemini')",
            name="ck_news_writer_provider",
        ),
        sa.CheckConstraint(
            "verifier_provider IN ('openai','anthropic','minimax','gemini')",
            name="ck_news_verifier_provider",
        ),
        sa.CheckConstraint("global_concurrency BETWEEN 1 AND 8", name="ck_news_global_concurrency"),
        sa.CheckConstraint(
            "per_vertical_concurrency BETWEEN 1 AND 4", name="ck_news_vertical_concurrency"
        ),
        sa.CheckConstraint("min_shadow_days >= 1", name="ck_news_min_shadow_days"),
        sa.CheckConstraint("min_shadow_candidates >= 1", name="ck_news_min_shadow_candidates"),
        sa.CheckConstraint(
            "min_human_agreement >= 0 AND min_human_agreement <= 1",
            name="ck_news_min_human_agreement",
        ),
        sa.CheckConstraint(
            "jev_act_confidence >= 0 AND jev_act_confidence <= 1",
            name="ck_news_jev_act_confidence",
        ),
    )
    now = datetime.now(UTC)
    op.bulk_insert(
        settings_table,
        [
            {
                "id": 1,
                "enabled": False,
                "mode": "shadow",
                "writer_provider": "openai",
                "writer_model": None,
                "verifier_provider": "openai",
                "verifier_model": None,
                "global_concurrency": 2,
                "per_vertical_concurrency": 1,
                "min_shadow_days": 14,
                "min_shadow_candidates": 50,
                "min_human_agreement": 0.95,
                "jev_act_confidence": 0.9,
                "auto_publish_ai": False,
                "auto_publish_tech": False,
                "auto_publish_crypto": False,
                "shadow_started_at_ai": now,
                "shadow_started_at_tech": now,
                "shadow_started_at_crypto": now,
                "prompt_version": "news-v1",
                "policy_version": "news-policy-v1",
                "updated_by_user_id": None,
                "created_at": now,
                "updated_at": now,
            }
        ],
    )
    op.create_table(
        "news_sources",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("url", sa.String(2048), nullable=False, unique=True),
        sa.Column("format", sa.String(16), nullable=False),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("vertical", sa.String(16), nullable=False),
        sa.Column("is_first_party", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("scan_interval_minutes", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("allowed_redirect_hosts_json", sa.JSON(), nullable=False),
        sa.Column("config_json", sa.JSON(), nullable=False),
        sa.Column("etag", sa.String(512), nullable=True),
        sa.Column("last_modified", sa.String(512), nullable=True),
        sa.Column("last_scanned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_scan_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("scan_lock_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_status", sa.String(32), nullable=False, server_default="never"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("consecutive_failures", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        *timestamps(),
        sa.CheckConstraint(
            "format IN ('rss','atom','json','api','html')", name="ck_news_source_format"
        ),
        sa.CheckConstraint("role IN ('evidence','lead_only')", name="ck_news_source_role"),
        sa.CheckConstraint(
            "vertical IN ('ai','tech','crypto','mixed')", name="ck_news_source_vertical"
        ),
        sa.CheckConstraint(
            "scan_interval_minutes BETWEEN 15 AND 1440", name="ck_news_source_interval"
        ),
    )
    op.create_index("ix_news_sources_enabled", "news_sources", ["enabled"])
    op.create_index("ix_news_sources_due", "news_sources", ["enabled", "next_scan_at"])
    op.create_table(
        "news_candidates",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "source_id",
            sa.Uuid(),
            sa.ForeignKey("news_sources.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("vertical", sa.String(16), nullable=False),
        sa.Column("status", sa.String(24), nullable=False, server_default="discovered"),
        sa.Column("canonical_url", sa.String(2048), nullable=False),
        sa.Column("source_title", sa.String(500), nullable=False),
        sa.Column("normalized_title", sa.String(500), nullable=False),
        sa.Column("source_published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("event_date", sa.Date(), nullable=True),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("evidence_hash", sa.String(64), nullable=True),
        sa.Column("idempotency_key", sa.String(64), nullable=False, unique=True),
        sa.Column(
            "guide_article_id",
            sa.Uuid(),
            sa.ForeignKey("guide_articles.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("draft_bundle_json", sa.JSON(), nullable=False),
        sa.Column("claim_ledger_json", sa.JSON(), nullable=False),
        sa.Column("lint_json", sa.JSON(), nullable=False),
        sa.Column("would_publish", sa.Boolean(), nullable=True),
        sa.Column("human_decision", sa.String(16), nullable=True),
        sa.Column("human_reason", sa.Text(), nullable=True),
        sa.Column("human_major_error", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("processing_started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("prompt_version", sa.String(32), nullable=False),
        sa.Column("policy_version", sa.String(32), nullable=False),
        *timestamps(),
        sa.CheckConstraint("vertical IN ('ai','tech','crypto')", name="ck_news_candidate_vertical"),
        sa.CheckConstraint(
            "status IN ("
            "'discovered','drafting','verifying','locale_review','jev_review',"
            "'shadow_review','manual_review','published','duplicate','rejected','failed'"
            ")",
            name="ck_news_candidate_status",
        ),
        sa.CheckConstraint(
            "human_decision IS NULL OR human_decision IN ('publish','reject')",
            name="ck_news_candidate_human_decision",
        ),
    )
    op.create_index("ix_news_candidates_source_id", "news_candidates", ["source_id"])
    op.create_index("ix_news_candidates_content_hash", "news_candidates", ["content_hash"])
    op.create_index("ix_news_candidates_guide_article_id", "news_candidates", ["guide_article_id"])
    op.create_index("ix_news_candidates_review", "news_candidates", ["status", "updated_at"])
    op.create_index("ix_news_candidates_vertical_status", "news_candidates", ["vertical", "status"])
    op.create_table(
        "news_evidence",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "candidate_id",
            sa.Uuid(),
            sa.ForeignKey("news_candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("is_first_party", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("url", sa.String(2048), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_date", sa.Date(), nullable=True),
        sa.Column("etag", sa.String(512), nullable=True),
        sa.Column("last_modified", sa.String(512), nullable=True),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=False),
        sa.UniqueConstraint("candidate_id", "url", name="uq_news_evidence_candidate_url"),
        sa.CheckConstraint("role IN ('evidence','lead_only')", name="ck_news_evidence_role"),
    )
    op.create_index("ix_news_evidence_candidate_id", "news_evidence", ["candidate_id"])
    op.create_table(
        "news_pipeline_runs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "candidate_id",
            sa.Uuid(),
            sa.ForeignKey("news_candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("stage", sa.String(32), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(160), nullable=False, unique=True),
        sa.Column("provider", sa.String(32), nullable=True),
        sa.Column("model", sa.String(128), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("output_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('running','succeeded','failed')", name="ck_news_pipeline_run_status"
        ),
    )
    op.create_index(
        "ix_news_pipeline_runs_candidate", "news_pipeline_runs", ["candidate_id", "started_at"]
    )
    op.create_table(
        "news_assessments",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "candidate_id",
            sa.Uuid(),
            sa.ForeignKey("news_candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("assessment_type", sa.String(24), nullable=False),
        sa.Column("locale", sa.String(16), nullable=True),
        sa.Column("verdict", sa.String(16), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("provider", sa.String(32), nullable=True),
        sa.Column("model", sa.String(128), nullable=True),
        sa.Column("reasons_json", sa.JSON(), nullable=False),
        sa.Column("details_json", sa.JSON(), nullable=False),
        sa.Column("evidence_hash", sa.String(64), nullable=True),
        sa.Column("prompt_version", sa.String(32), nullable=False),
        sa.Column(
            "created_by_user_id",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "assessment_type IN ('duplicate','verification','locale_review','jev','human')",
            name="ck_news_assessment_type",
        ),
        sa.CheckConstraint(
            "verdict IN ('pass','revise','manual','publish','reject','duplicate')",
            name="ck_news_assessment_verdict",
        ),
        sa.CheckConstraint(
            "locale IS NULL OR locale IN ('en','ja','ko','zh-TW','zh-CN')",
            name="ck_news_assessment_locale",
        ),
        sa.CheckConstraint(
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
            name="ck_news_assessment_confidence",
        ),
    )
    op.create_index(
        "ix_news_assessments_candidate", "news_assessments", ["candidate_id", "created_at"]
    )
    op.create_table(
        "news_assets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "candidate_id",
            sa.Uuid(),
            sa.ForeignKey("news_candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("variant", sa.String(16), nullable=False),
        sa.Column("locale", sa.String(16), nullable=True),
        sa.Column("storage_key", sa.String(512), nullable=False),
        sa.Column("public_filename", sa.String(160), nullable=False, unique=True),
        sa.Column("content_type", sa.String(64), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("candidate_id", "variant", "locale", name="uq_news_asset_variant"),
        sa.CheckConstraint("variant IN ('hero','social','diagram')", name="ck_news_asset_variant"),
        sa.CheckConstraint(
            "locale IS NULL OR locale IN ('en','ja','ko','zh-TW','zh-CN')",
            name="ck_news_asset_locale",
        ),
    )
    op.create_index("ix_news_assets_candidate_id", "news_assets", ["candidate_id"])
    op.create_index("ix_news_assets_is_public", "news_assets", ["is_public"])


def downgrade() -> None:
    op.drop_table("news_assets")
    op.drop_table("news_assessments")
    op.drop_table("news_pipeline_runs")
    op.drop_table("news_evidence")
    op.drop_table("news_candidates")
    op.drop_table("news_sources")
    op.drop_table("news_automation_settings")
