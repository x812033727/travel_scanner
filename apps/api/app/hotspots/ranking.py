from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RankingInput:
    hotspot_id: str
    editorial_relevance: float
    pageviews_current: float | None = None
    pageviews_previous: float | None = None
    signal_date: date | None = None
    depth_score: float | None = None


@dataclass(frozen=True)
class RankingScore:
    hotspot_id: str
    score: float
    interest_score: float
    growth_score: float
    quality_score: float
    confidence_score: float
    pageviews_current: int | None
    pageviews_previous: int | None
    growth_rate: float | None
    sources: tuple[str, ...]
    is_estimate: bool


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _interest_scores(items: list[RankingInput]) -> dict[str, float]:
    known = [
        math.log1p(item.pageviews_current) for item in items if item.pageviews_current is not None
    ]
    if not known:
        return {item.hotspot_id: item.editorial_relevance * 0.7 for item in items}
    low, high = min(known), max(known)
    scores: dict[str, float] = {}
    for item in items:
        if item.pageviews_current is None:
            scores[item.hotspot_id] = item.editorial_relevance * 0.45
        elif high == low:
            scores[item.hotspot_id] = 70.0
        else:
            scores[item.hotspot_id] = 25.0 + 75.0 * (
                (math.log1p(item.pageviews_current) - low) / (high - low)
            )
    return scores


def score_hotspots(inputs: list[RankingInput]) -> list[RankingScore]:
    """Score a scope using explainable 30-day interest and growth signals."""
    interest_scores = _interest_scores(inputs)
    results: list[RankingScore] = []
    for item in inputs:
        growth_rate: float | None = None
        growth_score = 50.0
        if item.pageviews_current is not None and item.pageviews_previous is not None:
            denominator = max(1.0, item.pageviews_previous)
            growth_rate = (item.pageviews_current - item.pageviews_previous) / denominator
            growth_score = _clamp(50.0 + _clamp(growth_rate, -1.0, 1.0) * 50.0)
        has_wikimedia = item.pageviews_current is not None
        confidence = 80.0 if has_wikimedia else 35.0
        quality = _clamp(item.editorial_relevance)
        interest = _clamp(interest_scores[item.hotspot_id])
        score = interest * 0.45 + growth_score * 0.25 + quality * 0.20 + confidence * 0.10
        results.append(
            RankingScore(
                hotspot_id=item.hotspot_id,
                score=round(score, 2),
                interest_score=round(interest, 2),
                growth_score=round(growth_score, 2),
                quality_score=round(quality, 2),
                confidence_score=confidence,
                pageviews_current=(
                    round(item.pageviews_current) if item.pageviews_current is not None else None
                ),
                pageviews_previous=(
                    round(item.pageviews_previous) if item.pageviews_previous is not None else None
                ),
                growth_rate=round(growth_rate, 4) if growth_rate is not None else None,
                sources=("curated_catalog", "wikimedia_pageviews")
                if has_wikimedia
                else ("curated_catalog",),
                is_estimate=not has_wikimedia,
            )
        )
    return sorted(results, key=lambda item: (-item.score, item.hotspot_id))


def calculate_depth_value(
    *, locality: float, distinctiveness: float, feasibility: float, evidence: float
) -> float:
    """Apply the editorial deep-value formula without hidden popularity signals."""
    return round(
        _clamp(locality) * 0.35
        + _clamp(distinctiveness) * 0.30
        + _clamp(feasibility) * 0.25
        + _clamp(evidence) * 0.10,
        2,
    )


def score_deep_hotspots(inputs: list[RankingInput]) -> list[RankingScore]:
    interest_scores = _interest_scores(inputs)
    results: list[RankingScore] = []
    for item in inputs:
        depth = _clamp(item.depth_score or 0)
        interest = _clamp(interest_scores[item.hotspot_id])
        confidence = 90.0 if item.pageviews_current is not None else 70.0
        score = depth * 0.80 + interest * 0.15 + confidence * 0.05
        results.append(
            RankingScore(
                hotspot_id=item.hotspot_id,
                score=round(score, 2),
                interest_score=round(interest, 2),
                growth_score=50.0,
                quality_score=round(depth, 2),
                confidence_score=confidence,
                pageviews_current=(
                    round(item.pageviews_current) if item.pageviews_current is not None else None
                ),
                pageviews_previous=(
                    round(item.pageviews_previous) if item.pageviews_previous is not None else None
                ),
                growth_rate=None,
                sources=("curated_catalog", "wikimedia_pageviews")
                if item.pageviews_current is not None
                else ("curated_catalog",),
                is_estimate=item.pageviews_current is None,
            )
        )
    return sorted(results, key=lambda item: (-item.score, item.hotspot_id))
