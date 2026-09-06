"""Score the pending guide backlog with the configured AI vendor.

Standard discovery (Brave articles, YouTube videos) writes every hit straight to
``pending`` without ever scoring it, so the queue grows faster than anyone reads it.
The AI search path already knows how to judge this exact material — same prompt, same
``AssessmentBatch`` schema, same 60-point relevance bar — it just never ran over rows
that arrived through standard discovery. This module points that assessment at the
backlog and turns each row into approved or rejected, recording the score and the
model's reason on the row so the decision stays auditable in the admin panel.

Candidate titles and summaries are untrusted external text; ``ASSESS_PROMPT`` says so
and the reply is bound to a schema, so a candidate cannot steer the review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal, cast
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.ai_search import (
    ASSESS_PROMPT,
    AIProviderName,
    AssessmentBatch,
    CandidateAssessment,
    _localized_context,
    research_provider,
    summarize_provider_error,
)
from app.i18n import LOCALES, Locale
from app.models import AdminAuditLog, HotspotGuide, TravelHotspot

# ``AssessmentBatch`` accepts 40 items, but a 40-candidate reply runs long enough to hit
# max_output_tokens on a thinking model, and a truncated reply costs the whole batch.
BATCH_SIZE = 20

Decision = Literal["approved", "rejected", "relocated", "skipped"]


@dataclass
class GuideDecision:
    guide_id: UUID
    hotspot_name: str
    title: str
    locale: str
    content_type: str
    decision: Decision
    relevance_score: int | None = None
    quality_score: int | None = None
    reason: str = ""
    detected_locale: str | None = None


@dataclass
class ReviewReport:
    provider: str = ""
    model: str = ""
    decisions: list[GuideDecision] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    applied: bool = False

    def counts(self) -> dict[str, int]:
        tally: dict[str, int] = {}
        for item in self.decisions:
            tally[item.decision] = tally.get(item.decision, 0) + 1
        return tally


def _pending_metadata(guide: HotspotGuide, candidate_id: str) -> dict[str, Any]:
    """The same fields ``_candidate_metadata`` sends, read off a persisted row."""
    return {
        "candidate_id": candidate_id,
        "type": guide.content_type,
        "title": guide.title,
        "creator": guide.creator_name,
        "summary": guide.summary,
        "published_at": guide.published_at.isoformat() if guide.published_at else None,
        "view_count": guide.view_count,
        "provider_locale": guide.locale,
        "provider_language_confidence": float(guide.language_confidence),
    }


def _decide(
    assessment: CandidateAssessment,
    guide: HotspotGuide,
    *,
    min_relevance: int,
    min_quality: int,
    min_language_confidence: float,
) -> tuple[Decision, str]:
    """Approve, relocate then approve, or reject — with the reason an admin will read."""
    mismatch = assessment.detected_locale != guide.locale
    if mismatch and assessment.language_confidence < min_language_confidence:
        return "rejected", (
            f"語言判定不明（標為 {guide.locale}，模型判為 {assessment.detected_locale}，"
            f"信心 {assessment.language_confidence:.2f}）：{assessment.recommendation_reason}"
        )
    if assessment.relevance_score < min_relevance:
        return "rejected", (
            f"相關性 {assessment.relevance_score} 未達 {min_relevance}："
            f"{assessment.recommendation_reason}"
        )
    if assessment.quality_score < min_quality:
        return "rejected", (
            f"品質 {assessment.quality_score} 未達 {min_quality}："
            f"{assessment.recommendation_reason}"
        )
    if mismatch:
        return "relocated", (
            f"改列 {assessment.detected_locale}（原標 {guide.locale}）："
            f"{assessment.recommendation_reason}"
        )
    return "approved", assessment.recommendation_reason


def _apply(
    guide: HotspotGuide,
    assessment: CandidateAssessment,
    decision: Decision,
    reason: str,
    *,
    provider_name: str,
    model: str,
    now: datetime,
) -> None:
    guide.review_status = "rejected" if decision == "rejected" else "approved"
    guide.review_reason = reason[:2000]
    guide.reviewed_at = now
    metadata = dict(guide.metadata_json or {})
    if decision == "relocated":
        metadata["relocated_from_locale"] = guide.locale
        guide.locale = assessment.detected_locale
        guide.language_confidence = Decimal(f"{assessment.language_confidence:.3f}")
    metadata.update(
        {
            "relevance_score": assessment.relevance_score,
            "quality_score": assessment.quality_score,
            "recommendation_reason": assessment.recommendation_reason,
            "detected_locale": assessment.detected_locale,
            "ai_language_confidence": assessment.language_confidence,
            "ai_provider": provider_name,
            "ai_model": model,
            "ai_reviewed_at": now.isoformat(),
            "review_source": "ai_backlog_review",
        }
    )
    # A JSON column only turns dirty on reassignment, never on in-place mutation.
    guide.metadata_json = metadata


async def _pending_groups(
    session: AsyncSession,
    *,
    locales: list[str] | None,
    limit: int | None,
) -> list[tuple[TravelHotspot, Locale, list[HotspotGuide]]]:
    query = (
        select(HotspotGuide, TravelHotspot)
        .join(TravelHotspot, TravelHotspot.id == HotspotGuide.hotspot_id)
        .where(HotspotGuide.review_status == "pending")
        .order_by(HotspotGuide.hotspot_id, HotspotGuide.locale, HotspotGuide.created_at)
    )
    if locales:
        query = query.where(HotspotGuide.locale.in_(locales))
    if limit:
        query = query.limit(limit)
    grouped: dict[tuple[UUID, str], tuple[TravelHotspot, list[HotspotGuide]]] = {}
    for guide, hotspot in (await session.execute(query)).all():
        if guide.locale not in LOCALES:
            continue
        grouped.setdefault((hotspot.id, guide.locale), (hotspot, []))[1].append(guide)
    return [
        (hotspot, cast(Locale, raw_locale), guides)
        for (_, raw_locale), (hotspot, guides) in grouped.items()
    ]


async def review_pending_guides(
    session: AsyncSession,
    settings: Settings,
    *,
    provider_name: AIProviderName | None = None,
    locales: list[str] | None = None,
    limit: int | None = None,
    min_relevance: int = 60,
    min_quality: int = 40,
    min_language_confidence: float = 0.7,
    max_calls: int = 200,
    batch_size: int = BATCH_SIZE,
    apply: bool = False,
    client: httpx.AsyncClient | None = None,
) -> ReviewReport:
    """Assess every pending guide and record approve/reject decisions.

    Nothing is written unless ``apply`` is set, so a dry run costs only the AI calls.
    """
    selected = provider_name or settings.hotspot_guide_ai_default_provider
    provider = research_provider(settings, selected, client)
    report = ReviewReport(provider=provider.name, model=provider.model, applied=apply)
    now = datetime.now(UTC)
    try:
        for hotspot, locale, guides in await _pending_groups(
            session, locales=locales, limit=limit
        ):
            context = await _localized_context(session, hotspot, locale)
            for start in range(0, len(guides), batch_size):
                if report.calls >= max_calls:
                    report.errors.append(f"停在 {max_calls} 次 AI 呼叫上限，其餘維持待審")
                    return report
                batch = guides[start : start + batch_size]
                by_id = {f"c{index}": guide for index, guide in enumerate(batch)}
                try:
                    assessment, usage = await provider.structured(
                        AssessmentBatch,
                        "hotspot_guide_backlog_assessment",
                        ASSESS_PROMPT,
                        {
                            "attraction": context,
                            "requested_locale": locale,
                            "candidates": [
                                _pending_metadata(guide, candidate_id)
                                for candidate_id, guide in by_id.items()
                            ],
                        },
                    )
                except Exception as error:  # noqa: BLE001 - one bad batch must not end the run
                    report.calls += 1
                    report.errors.append(
                        f"{hotspot.name} / {locale}: {summarize_provider_error(error)}"
                    )
                    continue
                report.calls += 1
                report.input_tokens += usage.get("input_tokens", 0)
                report.output_tokens += usage.get("output_tokens", 0)
                scored: set[str] = set()
                for item in assessment.items:
                    guide = by_id.get(item.candidate_id)
                    if guide is None or item.candidate_id in scored:
                        continue
                    scored.add(item.candidate_id)
                    decision, reason = _decide(
                        item,
                        guide,
                        min_relevance=min_relevance,
                        min_quality=min_quality,
                        min_language_confidence=min_language_confidence,
                    )
                    report.decisions.append(
                        GuideDecision(
                            guide_id=guide.id,
                            hotspot_name=hotspot.name,
                            title=guide.title,
                            locale=guide.locale,
                            content_type=guide.content_type,
                            decision=decision,
                            relevance_score=item.relevance_score,
                            quality_score=item.quality_score,
                            reason=reason,
                            detected_locale=item.detected_locale,
                        )
                    )
                    if apply:
                        _apply(
                            guide,
                            item,
                            decision,
                            reason,
                            provider_name=provider.name,
                            model=provider.model,
                            now=now,
                        )
                for candidate_id, guide in by_id.items():
                    if candidate_id in scored:
                        continue
                    # An unscored row stays pending rather than being guessed at.
                    report.decisions.append(
                        GuideDecision(
                            guide_id=guide.id,
                            hotspot_name=hotspot.name,
                            title=guide.title,
                            locale=guide.locale,
                            content_type=guide.content_type,
                            decision="skipped",
                            reason="模型沒有回傳這筆的評分",
                        )
                    )
                if apply:
                    await session.commit()
    finally:
        await provider.close()
    if apply and report.decisions:
        counts = report.counts()
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="hotspot_guides_ai_backlog_reviewed",
                target=f"hotspot-guides:{len(report.decisions)}",
                metadata_json={
                    "provider": report.provider,
                    "model": report.model,
                    "counts": counts,
                    "min_relevance": min_relevance,
                    "min_quality": min_quality,
                    "ai_calls": report.calls,
                },
            )
        )
        await session.commit()
    return report
