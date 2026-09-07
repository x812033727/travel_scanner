"""Untrusted AI suggestions, never publication or location-verification commands."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

CatalogKind = Literal["hotspot", "food", "merchant"]


class CatalogModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class EvidenceSource(CatalogModel):
    url: str = Field(max_length=2048)
    text: str = Field(default="", max_length=12_000)
    fingerprint: str = Field(default="", max_length=64)
    trusted: bool = False
    fetched: bool = False
    error: str | None = None


class EvidenceCitation(CatalogModel):
    url: str = Field(min_length=1, max_length=2048)
    quote: str = Field(min_length=1, max_length=300)


class ReviewCandidate(CatalogModel):
    candidate_id: str = Field(min_length=1, max_length=100)
    kind: CatalogKind
    name: str = Field(min_length=1, max_length=300)
    local_name: str = Field(default="", max_length=300)
    destination_id: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    sources: list[EvidenceSource] = Field(default_factory=list, max_length=10)


class ReviewAssessment(CatalogModel):
    candidate_id: str = Field(min_length=1, max_length=100)
    decision: Literal["approve", "reject", "needs_review"]
    confidence: float = Field(ge=0, le=1, allow_inf_nan=False)
    reason: str = Field(min_length=1, max_length=2000)
    evidence: list[EvidenceCitation] = Field(default_factory=list, max_length=10)
    corrections: dict[str, Any] = Field(default_factory=dict)


class AssessmentBatch(CatalogModel):
    items: list[ReviewAssessment] = Field(default_factory=list, max_length=20)


class DiscoveryDraft(CatalogModel):
    kind: CatalogKind
    name: str = Field(min_length=1, max_length=255)
    local_name: str = Field(min_length=1, max_length=255)
    destination_id: str = Field(min_length=1, max_length=64)
    slug: str = Field(min_length=1, max_length=128, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    source_urls: list[str] = Field(min_length=1, max_length=5)
    data: dict[str, Any] = Field(default_factory=dict)


class DiscoveryBatch(CatalogModel):
    items: list[DiscoveryDraft] = Field(default_factory=list, max_length=5)
