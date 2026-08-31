from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx
from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.ranking import RankingInput, score_hotspots
from app.hotspots.wikimedia import WikimediaPageviewClient
from app.models import HotspotRanking, HotspotSignal, TravelHotspot


async def _upsert_signal(
    session: AsyncSession,
    hotspot_id: Any,
    *,
    source: str,
    metric: str,
    value: float,
    observed_on: date,
    source_url: str | None,
    is_estimate: bool,
    metadata: dict[str, Any] | None = None,
) -> None:
    signal = await session.scalar(
        select(HotspotSignal).where(
            HotspotSignal.hotspot_id == hotspot_id,
            HotspotSignal.source == source,
            HotspotSignal.metric == metric,
            HotspotSignal.observed_on == observed_on,
        )
    )
    if signal is None:
        signal = HotspotSignal(
            hotspot_id=hotspot_id,
            source=source,
            metric=metric,
            observed_on=observed_on,
        )
    signal.value = Decimal(str(value))
    signal.window_days = 30
    signal.source_url = source_url
    signal.is_estimate = is_estimate
    signal.metadata_json = metadata or {}
    session.add(signal)


async def seed_catalog(session: AsyncSession, observed_on: date) -> list[TravelHotspot]:
    existing = {item.slug: item for item in (await session.scalars(select(TravelHotspot))).all()}
    hotspots: list[TravelHotspot] = []
    for seed in HOTSPOT_SEEDS:
        hotspot = existing.get(seed.slug)
        if hotspot is None:
            hotspot = TravelHotspot(slug=seed.slug)
        hotspot.name = seed.name
        hotspot.city_code = seed.city_code
        hotspot.city_name = seed.city_name
        hotspot.country_code = seed.country_code
        hotspot.country_name = seed.country_name
        hotspot.category = seed.category
        hotspot.search_text = seed.search_text
        hotspot.latitude = Decimal(str(seed.latitude))
        hotspot.longitude = Decimal(str(seed.longitude))
        hotspot.wikipedia_project = seed.wikipedia_project
        hotspot.wikipedia_title = seed.wikipedia_title
        hotspot.source_urls = [seed.wikipedia_url]
        hotspot.metadata_json = {
            "aliases": list(seed.aliases),
            "editorial_relevance": seed.editorial_relevance,
        }
        hotspot.is_active = True
        session.add(hotspot)
        await session.flush()
        await _upsert_signal(
            session,
            hotspot.id,
            source="curated_catalog",
            metric="editorial_relevance",
            value=seed.editorial_relevance,
            observed_on=observed_on,
            source_url=None,
            is_estimate=True,
            metadata={"purpose": "cold_start_only"},
        )
        hotspots.append(hotspot)
    return hotspots


def _latest_signals(signals: list[HotspotSignal]) -> dict[tuple[Any, str], HotspotSignal]:
    latest: dict[tuple[Any, str], HotspotSignal] = {}
    for signal in signals:
        key = (signal.hotspot_id, signal.metric)
        previous = latest.get(key)
        if previous is None or (signal.observed_on, signal.captured_at) > (
            previous.observed_on,
            previous.captured_at,
        ):
            latest[key] = signal
    return latest


async def refresh_rankings(session: AsyncSession, observed_on: date) -> int:
    hotspots = list(
        (
            await session.scalars(select(TravelHotspot).where(TravelHotspot.is_active.is_(True)))
        ).all()
    )
    signals = list((await session.scalars(select(HotspotSignal))).all())
    latest = _latest_signals(signals)

    def ranking_input(hotspot: TravelHotspot) -> RankingInput:
        editorial = latest.get((hotspot.id, "editorial_relevance"))
        current = latest.get((hotspot.id, "pageviews_30d"))
        previous = latest.get((hotspot.id, "pageviews_previous_30d"))
        return RankingInput(
            hotspot_id=str(hotspot.id),
            editorial_relevance=float(editorial.value) if editorial else 50.0,
            pageviews_current=float(current.value) if current else None,
            pageviews_previous=float(previous.value) if previous else None,
            signal_date=current.observed_on if current else None,
        )

    await session.execute(delete(HotspotRanking).where(HotspotRanking.observed_on == observed_on))
    scopes: list[tuple[str, str, list[TravelHotspot]]] = [("global", "global", hotspots)]
    by_city: dict[str, list[TravelHotspot]] = defaultdict(list)
    for hotspot in hotspots:
        by_city[hotspot.city_code].append(hotspot)
    scopes.extend(("city", city_code, items) for city_code, items in sorted(by_city.items()))

    inserted = 0
    for scope, scope_key, scoped_hotspots in scopes:
        by_id = {str(item.id): item for item in scoped_hotspots}
        for rank, scored in enumerate(
            score_hotspots([ranking_input(item) for item in scoped_hotspots]), start=1
        ):
            hotspot = by_id[scored.hotspot_id]
            signal = latest.get((hotspot.id, "pageviews_30d"))
            session.add(
                HotspotRanking(
                    hotspot_id=hotspot.id,
                    scope=scope,
                    scope_key=scope_key,
                    window_days=30,
                    rank=rank,
                    score=Decimal(str(scored.score)),
                    interest_score=Decimal(str(scored.interest_score)),
                    growth_score=Decimal(str(scored.growth_score)),
                    quality_score=Decimal(str(scored.quality_score)),
                    confidence_score=Decimal(str(scored.confidence_score)),
                    observed_on=observed_on,
                    explanation={
                        "pageviews_30d": scored.pageviews_current,
                        "previous_pageviews_30d": scored.pageviews_previous,
                        "growth_rate": scored.growth_rate,
                        "sources": list(scored.sources),
                        "is_estimate": scored.is_estimate,
                        "signal_date": signal.observed_on.isoformat() if signal else None,
                        "formula": {
                            "interest": 0.45,
                            "growth": 0.25,
                            "quality": 0.20,
                            "confidence": 0.10,
                        },
                    },
                )
            )
            inserted += 1
    return inserted


async def collect_hotspots(
    session: AsyncSession,
    settings: Settings,
    *,
    observed_on: date | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    target_date = observed_on or date.today()
    hotspots = await seed_catalog(session, target_date)
    await session.commit()
    collected = 0
    errors: list[dict[str, str]] = []
    if settings.hotspot_wikimedia_enabled:
        wikimedia = WikimediaPageviewClient(
            settings.hotspot_wikimedia_user_agent,
            settings.hotspot_wikimedia_timeout_seconds,
            client,
        )
        for index, hotspot in enumerate(hotspots, start=1):
            if not hotspot.wikipedia_project or not hotspot.wikipedia_title:
                continue
            try:
                window = await wikimedia.pageviews(
                    hotspot.wikipedia_project,
                    hotspot.wikipedia_title,
                    observed_on=target_date - timedelta(days=1),
                )
                await _upsert_signal(
                    session,
                    hotspot.id,
                    source="wikimedia_pageviews",
                    metric="pageviews_30d",
                    value=window.current,
                    observed_on=window.observed_on,
                    source_url=window.source_url,
                    is_estimate=False,
                )
                await _upsert_signal(
                    session,
                    hotspot.id,
                    source="wikimedia_pageviews",
                    metric="pageviews_previous_30d",
                    value=window.previous,
                    observed_on=window.observed_on,
                    source_url=window.source_url,
                    is_estimate=False,
                )
                collected += 1
            except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
                errors.append({"slug": hotspot.slug, "error": type(exc).__name__})
            if index % 5 == 0:
                await session.commit()
        await session.commit()
    rankings = await refresh_rankings(session, target_date)
    await session.commit()
    return {
        "observed_on": target_date.isoformat(),
        "catalog_count": len(hotspots),
        "wikimedia_collected": collected,
        "ranking_count": rankings,
        "errors": errors,
    }


def _trend_label(growth_rate: float | None) -> str:
    if growth_rate is None:
        return "等待趨勢資料"
    if growth_rate >= 0.15:
        return "近期升溫"
    if growth_rate <= -0.15:
        return "近期降溫"
    return "熱度持平"


async def list_rankings(
    session: AsyncSession,
    *,
    q: str | None = None,
    city_code: str | None = None,
    category: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    scope, scope_key = ("city", city_code.upper()) if city_code else ("global", "global")
    latest_date = await session.scalar(
        select(func.max(HotspotRanking.observed_on)).where(
            HotspotRanking.scope == scope,
            HotspotRanking.scope_key == scope_key,
            HotspotRanking.window_days == 30,
        )
    )
    if latest_date is None:
        return {
            "scope": scope,
            "scope_key": scope_key,
            "observed_on": None,
            "window_days": 30,
            "items": [],
        }
    query = (
        select(HotspotRanking, TravelHotspot)
        .join(TravelHotspot, TravelHotspot.id == HotspotRanking.hotspot_id)
        .where(
            HotspotRanking.scope == scope,
            HotspotRanking.scope_key == scope_key,
            HotspotRanking.observed_on == latest_date,
            TravelHotspot.is_active.is_(True),
        )
        .order_by(HotspotRanking.rank)
        .limit(limit)
    )
    if q and q.strip():
        term = f"%{q.strip().casefold()}%"
        query = query.where(
            or_(TravelHotspot.search_text.ilike(term), TravelHotspot.name.ilike(term))
        )
    if category:
        query = query.where(TravelHotspot.category == category.casefold())
    rows = (await session.execute(query)).all()
    items: list[dict[str, Any]] = []
    for ranking, hotspot in rows:
        growth_rate = ranking.explanation.get("growth_rate")
        items.append(
            {
                "id": str(hotspot.id),
                "slug": hotspot.slug,
                "rank": ranking.rank,
                "name": hotspot.name,
                "city_code": hotspot.city_code,
                "city_name": hotspot.city_name,
                "country_code": hotspot.country_code,
                "country_name": hotspot.country_name,
                "category": hotspot.category,
                "latitude": float(hotspot.latitude) if hotspot.latitude is not None else None,
                "longitude": float(hotspot.longitude) if hotspot.longitude is not None else None,
                "score": float(ranking.score),
                "components": {
                    "interest": float(ranking.interest_score),
                    "growth": float(ranking.growth_score),
                    "quality": float(ranking.quality_score),
                    "confidence": float(ranking.confidence_score),
                },
                "pageviews_30d": ranking.explanation.get("pageviews_30d"),
                "growth_rate": growth_rate,
                "trend_label": _trend_label(growth_rate),
                "sources": ranking.explanation.get("sources", []),
                "source_urls": hotspot.source_urls,
                "signal_date": ranking.explanation.get("signal_date"),
                "is_estimate": bool(ranking.explanation.get("is_estimate", True)),
            }
        )
    return {
        "scope": scope,
        "scope_key": scope_key,
        "observed_on": latest_date.isoformat(),
        "window_days": 30,
        "items": items,
    }
