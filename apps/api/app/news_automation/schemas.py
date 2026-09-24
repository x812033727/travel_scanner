from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal, Self
from urllib.parse import urlsplit
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.ai.catalog import ModelStatus, valid_model_id
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.news_automation.provider_schema import ProviderReply

Vertical = Literal["ai", "tech", "crypto"]
SourceVertical = Literal["ai", "tech", "crypto", "mixed"]
SourceFormat = Literal["rss", "atom", "json", "api", "html"]
SourceRole = Literal["evidence", "lead_only"]
CandidateStatus = Literal[
    "discovered",
    "drafting",
    "verifying",
    "locale_review",
    "jev_review",
    "shadow_review",
    "manual_review",
    "needs_evidence",
    "needs_redraft",
    "published",
    "duplicate",
    "rejected",
    "failed",
]
ProviderName = Literal["openai", "anthropic", "minimax", "gemini"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def https_source(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("news sources must be credential-free HTTPS URLs")
    _ = parsed.port
    return value.strip()


def clean_hosts(values: list[str]) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        host = value.strip().casefold().rstrip(".")
        if not host or "/" in host or ":" in host or host.startswith("."):
            raise ValueError("redirect allow-list entries must be host names")
        if host not in cleaned:
            cleaned.append(host)
    return cleaned


class SourceWrite(StrictModel):
    name: str = Field(min_length=1, max_length=160)
    url: str = Field(min_length=1, max_length=2048)
    format: SourceFormat
    role: SourceRole
    vertical: SourceVertical
    is_first_party: bool = False
    enabled: bool = False
    scan_interval_minutes: int = Field(default=60, ge=15, le=1440)
    allowed_redirect_hosts: list[str] = Field(default_factory=list, max_length=20)
    config: dict[str, Any] = Field(default_factory=dict)

    @field_validator("url")
    @classmethod
    def valid_url(cls, value: str) -> str:
        return https_source(value)

    @field_validator("allowed_redirect_hosts")
    @classmethod
    def valid_hosts(cls, values: list[str]) -> list[str]:
        return clean_hosts(values)

    @model_validator(mode="after")
    def first_party_is_evidence(self) -> Self:
        if self.is_first_party and self.role != "evidence":
            raise ValueError("a first-party source must have the evidence role")
        return self


class SourcePatch(StrictModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    url: str | None = Field(default=None, min_length=1, max_length=2048)
    format: SourceFormat | None = None
    role: SourceRole | None = None
    vertical: SourceVertical | None = None
    is_first_party: bool | None = None
    enabled: bool | None = None
    scan_interval_minutes: int | None = Field(default=None, ge=15, le=1440)
    allowed_redirect_hosts: list[str] | None = Field(default=None, max_length=20)
    config: dict[str, Any] | None = None

    @field_validator("url")
    @classmethod
    def valid_url(cls, value: str | None) -> str | None:
        return https_source(value) if value is not None else None

    @field_validator("allowed_redirect_hosts")
    @classmethod
    def valid_hosts(cls, values: list[str] | None) -> list[str] | None:
        return clean_hosts(values) if values is not None else None


class SourceView(SourceWrite):
    id: UUID
    etag: str | None
    last_modified: str | None
    last_scanned_at: datetime | None
    next_scan_at: datetime
    last_status: str
    last_error: str | None
    consecutive_failures: int
    created_at: datetime
    updated_at: datetime


class SettingsWrite(StrictModel):
    enabled: bool
    mode: Literal["shadow", "automatic"] = "shadow"
    writer_provider: ProviderName
    writer_model: str | None = Field(default=None, max_length=128)
    verifier_provider: ProviderName
    verifier_model: str | None = Field(default=None, max_length=128)
    global_concurrency: int = Field(ge=1, le=8)
    per_vertical_concurrency: int = Field(ge=1, le=4)
    min_shadow_days: int = Field(ge=1, le=90)
    min_shadow_candidates: int = Field(ge=1, le=500)
    min_human_agreement: float = Field(ge=0, le=1)
    jev_act_confidence: float = Field(ge=0, le=1)
    auto_publish_ai: bool = False
    auto_publish_tech: bool = False
    auto_publish_crypto: bool = False
    prompt_version: str = Field(min_length=1, max_length=32)
    policy_version: str = Field(min_length=1, max_length=32)

    @field_validator("writer_model", "verifier_model")
    @classmethod
    def model_id(cls, value: str | None) -> str | None:
        # A Gemini model id is interpolated into the request path (security audit R2-25),
        # so a stored id is held to the same pattern as the admin AI settings.
        cleaned = (value or "").strip()
        if not cleaned:
            return None
        if not valid_model_id(cleaned):
            raise ValueError("model ids may contain letters, digits, dot, underscore, colon and -")
        return cleaned

    @model_validator(mode="after")
    def concurrency_order(self) -> Self:
        if self.per_vertical_concurrency > self.global_concurrency:
            raise ValueError("per-vertical concurrency cannot exceed global concurrency")
        return self


class GateView(StrictModel):
    vertical: Vertical
    days: int
    labelled_candidates: int
    agreements: int
    agreement_rate: float
    serious_false_positives: int
    eligible: bool
    reasons: list[str]


class ModelOptionView(StrictModel):
    value: str
    label: str
    description: str | None
    status: ModelStatus


class SettingsView(SettingsWrite):
    gates: dict[Vertical, GateView]
    # The admin model dropdowns: catalog models each vendor's news adapter can drive,
    # and the model an empty choice falls back to.
    model_options: dict[ProviderName, list[ModelOptionView]]
    default_models: dict[ProviderName, str]
    updated_at: datetime


class EvidenceView(StrictModel):
    id: UUID
    role: SourceRole
    is_first_party: bool
    url: str
    title: str
    retrieved_at: datetime
    source_date: date | None
    content_hash: str
    excerpt: str


class AssessmentView(StrictModel):
    id: UUID
    assessment_type: str
    locale: Locale | None
    verdict: str
    confidence: float | None
    provider: str | None
    model: str | None
    reasons: list[str]
    details: dict[str, Any]
    created_at: datetime


class RunView(StrictModel):
    id: UUID
    stage: str
    status: str
    attempt: int
    provider: str | None
    model: str | None
    input_tokens: int
    output_tokens: int
    error_code: str | None
    error_detail: str | None
    metadata: dict[str, Any]
    started_at: datetime
    finished_at: datetime | None


class CandidateSummary(StrictModel):
    id: UUID
    vertical: Vertical
    status: CandidateStatus
    source_title: str
    canonical_url: str
    event_date: date | None
    would_publish: bool | None
    human_decision: Literal["publish", "reject"] | None
    error_code: str | None
    error_detail: str | None
    guide_article_id: UUID | None
    created_at: datetime
    updated_at: datetime


class CandidatePage(StrictModel):
    candidates: list[CandidateSummary]
    total: int
    page: int
    pages: int


class CandidateDetail(CandidateSummary):
    evidence: list[EvidenceView]
    assessments: list[AssessmentView]
    runs: list[RunView]
    documents: dict[Locale, GuideDocument]
    claim_ledger: list[dict[str, Any]]
    lint: dict[str, Any]
    human_reason: str | None
    human_major_error: bool
    # Filled only while the semantic duplicate check is waiting for an editor: the known
    # titles closest to this one, so "not a duplicate" can be answered by eye.
    similar_titles: list[str] = Field(default_factory=list)


class CandidateAction(StrictModel):
    reason: str = Field(min_length=1, max_length=1000)
    major_error: bool = False


class Claim(StrictModel):
    claim: str = Field(min_length=1, max_length=800)
    source_urls: list[str] = Field(min_length=1, max_length=4)


class EditorialDraft(ProviderReply):
    document_fields = ("document",)

    eligible: bool
    exclusion_reason: str = Field(default="", max_length=1000)
    vertical: Vertical
    event_date: date
    slug: str = Field(pattern=r"^(?:ai|tech|crypto)-news-[a-z0-9]+(?:-[a-z0-9]+)*-[0-9]{8}$")
    topics: list[str] = Field(min_length=1, max_length=6)
    claims: list[Claim] = Field(min_length=1, max_length=40)
    document: GuideDocument


class VerificationResult(ProviderReply):
    document_fields = ("corrected_document",)

    verdict: Literal["pass", "revise", "manual"]
    issues: list[str] = Field(default_factory=list, max_length=30)
    corrected_document: GuideDocument | None = None

    @model_validator(mode="after")
    def correction_matches_verdict(self) -> Self:
        if self.verdict == "revise" and self.corrected_document is None:
            raise ValueError("revise requires a corrected document")
        return self


class LocalizedDocument(ProviderReply):
    document_fields = ("document",)

    # One locale per call: four documents in one reply outran the request timeout, and
    # a keyed map has no schema a strict provider accepts.
    document: GuideDocument


class LocaleReviewResult(ProviderReply):
    document_fields = ("corrected_document",)

    verdict: Literal["pass", "revise", "manual"]
    issues: list[str] = Field(default_factory=list, max_length=30)
    corrected_document: GuideDocument | None = None


class Entry(StrictModel):
    title: str = Field(min_length=1, max_length=500)
    url: str = Field(min_length=1, max_length=2048)
    summary: str = Field(default="", max_length=20_000)
    published_at: datetime | None = None


class FetchResult(StrictModel):
    url: str
    status_code: int
    content_type: str
    body: bytes
    etag: str | None = None
    last_modified: str | None = None
    not_modified: bool = False


class StatsView(StrictModel):
    pending_review: int
    failed: int
    published: int
    queue_by_status: dict[str, int]
    pipeline_runs: int = 0
    pipeline_failures: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
