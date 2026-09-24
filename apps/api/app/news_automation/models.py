from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

VERTICALS = ("ai", "tech", "crypto")
SOURCE_FORMATS = ("rss", "atom", "json", "api", "html")
SOURCE_ROLES = ("evidence", "lead_only")
CANDIDATE_STATUSES = (
    "discovered",
    "drafting",
    "verifying",
    "locale_review",
    "jev_review",
    "shadow_review",
    "manual_review",
    # Stopped at the evidence gate before any model call; not an editor's work item.
    "needs_evidence",
    # Stopped before a five-locale article existed: only a new draft or a rejection helps.
    "needs_redraft",
    "published",
    "duplicate",
    "rejected",
    "failed",
)
RUN_STATUSES = ("running", "succeeded", "failed")
ASSESSMENT_TYPES = ("duplicate", "verification", "locale_review", "jev", "human")
ASSESSMENT_VERDICTS = ("pass", "revise", "manual", "publish", "reject", "duplicate")
ASSET_VARIANTS = ("hero", "social", "diagram")
LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")


def utcnow() -> datetime:
    return datetime.now(UTC)


def _choices(column: str, values: tuple[str, ...]) -> str:
    return f"{column} IN ({', '.join(repr(value) for value in values)})"


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class NewsAutomationSettings(Timestamped, Base):
    __tablename__ = "news_automation_settings"
    __table_args__ = (
        CheckConstraint("id = 1", name="ck_news_automation_settings_singleton"),
        CheckConstraint("mode IN ('shadow', 'automatic')", name="ck_news_automation_mode"),
        CheckConstraint(
            "writer_provider IN ('openai','anthropic','minimax','gemini')",
            name="ck_news_writer_provider",
        ),
        CheckConstraint(
            "verifier_provider IN ('openai','anthropic','minimax','gemini')",
            name="ck_news_verifier_provider",
        ),
        CheckConstraint("global_concurrency BETWEEN 1 AND 8", name="ck_news_global_concurrency"),
        CheckConstraint(
            "per_vertical_concurrency BETWEEN 1 AND 4",
            name="ck_news_vertical_concurrency",
        ),
        CheckConstraint("min_shadow_days >= 1", name="ck_news_min_shadow_days"),
        CheckConstraint("min_shadow_candidates >= 1", name="ck_news_min_shadow_candidates"),
        CheckConstraint(
            "min_human_agreement >= 0 AND min_human_agreement <= 1",
            name="ck_news_min_human_agreement",
        ),
        CheckConstraint(
            "jev_act_confidence >= 0 AND jev_act_confidence <= 1",
            name="ck_news_jev_act_confidence",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    mode: Mapped[str] = mapped_column(String(16), default="shadow")
    writer_provider: Mapped[str] = mapped_column(String(16), default="openai")
    writer_model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    verifier_provider: Mapped[str] = mapped_column(String(16), default="openai")
    verifier_model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    global_concurrency: Mapped[int] = mapped_column(Integer, default=2)
    per_vertical_concurrency: Mapped[int] = mapped_column(Integer, default=1)
    min_shadow_days: Mapped[int] = mapped_column(Integer, default=14)
    min_shadow_candidates: Mapped[int] = mapped_column(Integer, default=50)
    min_human_agreement: Mapped[float] = mapped_column(default=0.95)
    jev_act_confidence: Mapped[float] = mapped_column(default=0.9)
    auto_publish_ai: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_publish_tech: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_publish_crypto: Mapped[bool] = mapped_column(Boolean, default=False)
    shadow_started_at_ai: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    shadow_started_at_tech: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    shadow_started_at_crypto: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    prompt_version: Mapped[str] = mapped_column(String(32), default="news-v1")
    policy_version: Mapped[str] = mapped_column(String(32), default="news-policy-v1")
    updated_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class NewsSource(Timestamped, Base):
    __tablename__ = "news_sources"
    __table_args__ = (
        UniqueConstraint("url", name="uq_news_source_url"),
        CheckConstraint(_choices("format", SOURCE_FORMATS), name="ck_news_source_format"),
        CheckConstraint(_choices("role", SOURCE_ROLES), name="ck_news_source_role"),
        CheckConstraint(
            "vertical IN ('ai','tech','crypto','mixed')", name="ck_news_source_vertical"
        ),
        CheckConstraint(
            "scan_interval_minutes BETWEEN 15 AND 1440", name="ck_news_source_interval"
        ),
        Index("ix_news_sources_due", "enabled", "next_scan_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(160))
    url: Mapped[str] = mapped_column(String(2048))
    format: Mapped[str] = mapped_column(String(16))
    role: Mapped[str] = mapped_column(String(16))
    vertical: Mapped[str] = mapped_column(String(16))
    is_first_party: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    scan_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)
    allowed_redirect_hosts_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    config_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    etag: Mapped[str | None] = mapped_column(String(512), nullable=True)
    last_modified: Mapped[str | None] = mapped_column(String(512), nullable=True)
    last_scanned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_scan_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    scan_lock_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_status: Mapped[str] = mapped_column(String(32), default="never")
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class NewsCandidate(Timestamped, Base):
    __tablename__ = "news_candidates"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_news_candidate_idempotency"),
        CheckConstraint(_choices("vertical", VERTICALS), name="ck_news_candidate_vertical"),
        CheckConstraint(_choices("status", CANDIDATE_STATUSES), name="ck_news_candidate_status"),
        CheckConstraint(
            "human_decision IS NULL OR human_decision IN ('publish','reject')",
            name="ck_news_candidate_human_decision",
        ),
        Index("ix_news_candidates_review", "status", "updated_at"),
        Index("ix_news_candidates_vertical_status", "vertical", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    source_id: Mapped[UUID] = mapped_column(
        ForeignKey("news_sources.id", ondelete="RESTRICT"), index=True
    )
    vertical: Mapped[str] = mapped_column(String(16), index=True)
    status: Mapped[str] = mapped_column(String(24), default="discovered", index=True)
    canonical_url: Mapped[str] = mapped_column(String(2048))
    source_title: Mapped[str] = mapped_column(String(500))
    normalized_title: Mapped[str] = mapped_column(String(500), default="")
    source_published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    event_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    evidence_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(64))
    guide_article_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("guide_articles.id", ondelete="SET NULL"), nullable=True, index=True
    )
    draft_bundle_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    claim_ledger_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    lint_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    would_publish: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    human_decision: Mapped[str | None] = mapped_column(String(16), nullable=True)
    human_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    human_major_error: Mapped[bool] = mapped_column(Boolean, default=False)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    processing_started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    prompt_version: Mapped[str] = mapped_column(String(32), default="news-v1")
    policy_version: Mapped[str] = mapped_column(String(32), default="news-policy-v1")


class NewsEvidence(Base):
    __tablename__ = "news_evidence"
    __table_args__ = (
        UniqueConstraint("candidate_id", "url", name="uq_news_evidence_candidate_url"),
        CheckConstraint(_choices("role", SOURCE_ROLES), name="ck_news_evidence_role"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("news_candidates.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(16))
    is_first_party: Mapped[bool] = mapped_column(Boolean, default=False)
    url: Mapped[str] = mapped_column(String(2048))
    title: Mapped[str] = mapped_column(String(500))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    source_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    etag: Mapped[str | None] = mapped_column(String(512), nullable=True)
    last_modified: Mapped[str | None] = mapped_column(String(512), nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64))
    excerpt: Mapped[str] = mapped_column(Text)


class NewsPipelineRun(Base):
    __tablename__ = "news_pipeline_runs"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_news_pipeline_run_idempotency"),
        CheckConstraint(_choices("status", RUN_STATUSES), name="ck_news_pipeline_run_status"),
        Index("ix_news_pipeline_runs_candidate", "candidate_id", "started_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("news_candidates.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(16), default="running")
    attempt: Mapped[int] = mapped_column(Integer, default=1)
    idempotency_key: Mapped[str] = mapped_column(String(160))
    provider: Mapped[str | None] = mapped_column(String(32), nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class NewsAssessment(Base):
    __tablename__ = "news_assessments"
    __table_args__ = (
        CheckConstraint(
            _choices("assessment_type", ASSESSMENT_TYPES), name="ck_news_assessment_type"
        ),
        CheckConstraint(
            _choices("verdict", ASSESSMENT_VERDICTS), name="ck_news_assessment_verdict"
        ),
        CheckConstraint(
            "locale IS NULL OR " + _choices("locale", LOCALES), name="ck_news_assessment_locale"
        ),
        CheckConstraint(
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
            name="ck_news_assessment_confidence",
        ),
        Index("ix_news_assessments_candidate", "candidate_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("news_candidates.id", ondelete="CASCADE"), index=True
    )
    assessment_type: Mapped[str] = mapped_column(String(24))
    locale: Mapped[str | None] = mapped_column(String(16), nullable=True)
    verdict: Mapped[str] = mapped_column(String(16))
    confidence: Mapped[float | None] = mapped_column(nullable=True)
    provider: Mapped[str | None] = mapped_column(String(32), nullable=True)
    model: Mapped[str | None] = mapped_column(String(128), nullable=True)
    reasons_json: Mapped[list[str]] = mapped_column(JSON, default=list)
    details_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    evidence_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    prompt_version: Mapped[str] = mapped_column(String(32))
    created_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class NewsAsset(Base):
    __tablename__ = "news_assets"
    __table_args__ = (
        UniqueConstraint("candidate_id", "variant", "locale", name="uq_news_asset_variant"),
        UniqueConstraint("public_filename", name="uq_news_asset_public_filename"),
        CheckConstraint(_choices("variant", ASSET_VARIANTS), name="ck_news_asset_variant"),
        CheckConstraint(
            "locale IS NULL OR " + _choices("locale", LOCALES), name="ck_news_asset_locale"
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("news_candidates.id", ondelete="CASCADE"), index=True
    )
    variant: Mapped[str] = mapped_column(String(16))
    locale: Mapped[str | None] = mapped_column(String(16), nullable=True)
    storage_key: Mapped[str] = mapped_column(String(512))
    public_filename: Mapped[str] = mapped_column(String(160))
    content_type: Mapped[str] = mapped_column(String(64))
    sha256: Mapped[str] = mapped_column(String(64))
    size: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    # The image itself on a host without object storage (the production host has none);
    # None when it lives in S3 under storage_key. A candidate's seven images are a few
    # hundred kilobytes, and retention clears them with the rest of its unpublished assets.
    content: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
