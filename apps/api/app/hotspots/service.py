from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any

import httpx
from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.destinations.catalog import DESTINATIONS, destination_for_code, destination_for_id
from app.foods.service import seed_food_catalog
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.cities import HOTSPOT_CITIES
from app.hotspots.discovery import WikimediaDiscoveryClient
from app.hotspots.guides import discover_guides
from app.hotspots.maps import build_map_links
from app.hotspots.places import place_summary_payload
from app.hotspots.ranking import RankingInput, score_deep_hotspots, score_hotspots
from app.hotspots.wikimedia import WikimediaPageviewClient
from app.i18n import LOCALES
from app.infra import get_redis
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    FoodMerchant,
    HotspotGuide,
    HotspotLocalization,
    HotspotPlaceProfile,
    HotspotRanking,
    HotspotSignal,
    TravelHotspot,
)
from app.places.google import GoogleTravelService
from app.trips.itinerary import ItineraryHotspot

PUBLIC_REVIEW_STATUSES = ("approved", "auto_approved")


async def refresh_due_map_place_ids(
    session: AsyncSession,
    settings: Settings,
    *,
    client: httpx.AsyncClient | None = None,
    limit: int = 20,
) -> dict[str, int | bool]:
    """Refresh exact Google Place IDs after 12 months without persisting Places coordinates."""

    if not settings.google_maps_api_key:
        return {"configured": False, "checked": 0, "refreshed": 0, "failed": 0}
    cutoff = datetime.now(UTC) - timedelta(days=365)
    hotspots = list(
        (
            await session.scalars(
                select(TravelHotspot)
                .where(
                    TravelHotspot.google_place_id.is_not(None),
                    TravelHotspot.map_match_status == "verified",
                    or_(
                        TravelHotspot.map_verified_at.is_(None),
                        TravelHotspot.map_verified_at <= cutoff,
                    ),
                )
                .order_by(TravelHotspot.map_verified_at.asc().nullsfirst())
                .limit(limit)
            )
        ).all()
    )
    remaining = max(0, limit - len(hotspots))
    merchants = list(
        (
            await session.scalars(
                select(FoodMerchant)
                .where(
                    FoodMerchant.google_place_id.is_not(None),
                    FoodMerchant.map_match_status == "verified",
                    or_(FoodMerchant.verified_at.is_(None), FoodMerchant.verified_at <= cutoff),
                )
                .order_by(FoodMerchant.verified_at.asc().nullsfirst())
                .limit(remaining)
            )
        ).all()
    )
    rows: list[TravelHotspot | FoodMerchant] = [*hotspots, *merchants]
    service = GoogleTravelService(get_redis(), settings, client=client)
    semaphore = asyncio.Semaphore(3)

    async def refresh(
        row: TravelHotspot | FoodMerchant,
    ) -> tuple[TravelHotspot | FoodMerchant, str | None]:
        async with semaphore:
            return row, await service.refresh_place_id(str(row.google_place_id))

    refreshed = 0
    failed = 0
    now = datetime.now(UTC)
    for row, place_id in await asyncio.gather(*(refresh(row) for row in rows)):
        if not place_id:
            failed += 1
            continue
        model = TravelHotspot if isinstance(row, TravelHotspot) else FoodMerchant
        duplicate = await session.scalar(
            select(model.id).where(model.google_place_id == place_id, model.id != row.id)
        )
        if duplicate is not None:
            failed += 1
            continue
        row.google_place_id = place_id
        if isinstance(row, TravelHotspot):
            row.map_verified_at = now
        else:
            row.verified_at = now
        refreshed += 1
    if rows:
        await session.commit()
    return {
        "configured": True,
        "checked": len(rows),
        "refreshed": refreshed,
        "failed": failed,
    }


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
    rows = list((await session.scalars(select(TravelHotspot))).all())
    localization_rows = list((await session.scalars(select(HotspotLocalization))).all())
    localizations = {(item.hotspot_id, item.locale): item for item in localization_rows}
    existing = {item.slug: item for item in rows}
    by_wikidata = {item.wikidata_item_id: item for item in rows if item.wikidata_item_id}
    hotspots: list[TravelHotspot] = []
    for seed in HOTSPOT_SEEDS:
        hotspot = existing.get(seed.slug)
        claimed = by_wikidata.get(seed.wikidata_item_id) if seed.wikidata_item_id else None
        if hotspot is None and claimed is not None:
            # Discovery reaches a place before the curated catalog does and stores it
            # under a generated slug. wikidata_item_id is unique, so inserting a second
            # row for the same item aborts the entire seeding transaction. Adopt the
            # discovered row: it already carries the pageviews collected against it.
            hotspot = claimed
            hotspot.slug = seed.slug
        elif hotspot is not None and claimed is not None and claimed is not hotspot:
            # The seed now points at a different Wikidata item than it used to. Release
            # the id from the row that no longer owns it so the assignment below cannot
            # collide with it.
            claimed.wikidata_item_id = None
            claimed.is_active = False
        if hotspot is None:
            hotspot = TravelHotspot(slug=seed.slug)
        hotspot.name = seed.name
        hotspot.destination_id = seed.destination_id
        hotspot.city_code = seed.city_code
        hotspot.city_name = seed.city_name
        hotspot.country_code = seed.country_code
        hotspot.country_name = seed.country_name
        hotspot.category = seed.category
        hotspot.search_text = seed.search_text
        hotspot.latitude = Decimal(str(seed.latitude))
        hotspot.longitude = Decimal(str(seed.longitude))
        hotspot.coordinate_source_type = (
            "wikidata" if seed.coordinate_source == "wikidata_p625" else "curated"
        )
        hotspot.coordinate_source_url = (
            seed.wikidata_url
            if hotspot.coordinate_source_type == "wikidata"
            else next(iter(seed.source_urls), None) or seed.wikipedia_url or seed.wikidata_url
        )
        hotspot.coordinate_verified_at = hotspot.coordinate_verified_at or datetime.now(UTC)
        hotspot.wikipedia_project = seed.wikipedia_project
        hotspot.wikipedia_title = seed.wikipedia_title
        hotspot.wikidata_item_id = seed.wikidata_item_id
        hotspot.origin = "curated"
        hotspot.review_status = "approved"
        hotspot.review_reason = None
        hotspot.source_urls = [
            url for url in (seed.wikipedia_url, seed.wikidata_url) if url is not None
        ]
        hotspot.metadata_json = {
            "aliases": list(seed.aliases),
            "editorial_relevance": seed.editorial_relevance,
            "pageview_pages": (
                [[seed.wikipedia_project, seed.wikipedia_title]]
                if seed.wikipedia_project and seed.wikipedia_title
                else []
            ),
            "local_name": seed.local_name,
            "depth_reason": seed.depth_reason,
            "access_minutes": seed.access_minutes,
            "recommended_duration_minutes": seed.recommended_duration_minutes,
            "depth_components": seed.depth_components,
            "coordinate_source": seed.coordinate_source,
        }
        hotspot.is_deep_travel = seed.is_deep_travel
        hotspot.depth_kind = seed.depth_kind
        hotspot.depth_score = (
            Decimal(str(seed.depth_score)) if seed.depth_score is not None else None
        )
        if seed.source_urls:
            hotspot.source_urls = list(seed.source_urls)
        hotspot.is_active = True
        hotspot.discovered_at = hotspot.discovered_at or datetime.now(UTC)
        hotspot.last_seen_at = datetime.now(UTC)
        hotspot.reviewed_at = hotspot.reviewed_at or datetime.now(UTC)
        session.add(hotspot)
        await session.flush()
        for locale in LOCALES:
            localization = localizations.get((hotspot.id, locale))
            if localization is None:
                localization = HotspotLocalization(
                    hotspot_id=hotspot.id,
                    locale=locale,
                    name=seed.name,
                    aliases=list(seed.aliases),
                    search_terms=[],
                )
                localizations[(hotspot.id, locale)] = localization
                session.add(localization)
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
            await session.scalars(
                select(TravelHotspot).where(
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
                )
            )
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
            depth_score=float(hotspot.depth_score) if hotspot.depth_score is not None else None,
        )

    await session.execute(delete(HotspotRanking).where(HotspotRanking.observed_on == observed_on))
    scopes: list[tuple[str, str, list[TravelHotspot]]] = [("global", "global", hotspots)]
    by_city: dict[str, list[TravelHotspot]] = defaultdict(list)
    for hotspot in hotspots:
        by_city[hotspot.city_code].append(hotspot)
    scopes.extend(("city", city_code, items) for city_code, items in sorted(by_city.items()))
    by_destination: dict[str, list[TravelHotspot]] = defaultdict(list)
    for hotspot in hotspots:
        by_destination[hotspot.destination_id].append(hotspot)
    scopes.extend(
        ("destination", destination_id, items)
        for destination_id, items in sorted(by_destination.items())
    )
    deep_hotspots = [item for item in hotspots if item.is_deep_travel]
    scopes.append(("deep_global", "global", deep_hotspots))
    deep_by_city: dict[str, list[TravelHotspot]] = defaultdict(list)
    for hotspot in deep_hotspots:
        deep_by_city[hotspot.city_code].append(hotspot)
    scopes.extend(
        ("deep_city", city_code, items) for city_code, items in sorted(deep_by_city.items())
    )
    deep_by_destination: dict[str, list[TravelHotspot]] = defaultdict(list)
    for hotspot in deep_hotspots:
        deep_by_destination[hotspot.destination_id].append(hotspot)
    scopes.extend(
        ("deep_destination", destination_id, items)
        for destination_id, items in sorted(deep_by_destination.items())
    )

    inserted = 0
    for scope, scope_key, scoped_hotspots in scopes:
        by_id = {str(item.id): item for item in scoped_hotspots}
        scoring = score_deep_hotspots if scope.startswith("deep_") else score_hotspots
        for rank, scored in enumerate(
            scoring([ranking_input(item) for item in scoped_hotspots]), start=1
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
                        "formula": (
                            {"depth": 0.80, "interest": 0.15, "confidence": 0.05}
                            if scope.startswith("deep_")
                            else {
                                "interest": 0.45,
                                "growth": 0.25,
                                "quality": 0.20,
                                "confidence": 0.10,
                            }
                        ),
                    },
                )
            )
            inserted += 1
    return inserted


async def discover_hotspots(
    session: AsyncSession,
    settings: Settings,
    *,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    discovery = WikimediaDiscoveryClient(
        settings.hotspot_wikimedia_user_agent,
        settings.hotspot_wikimedia_timeout_seconds,
        client,
    )
    now = datetime.now(UTC)
    added = auto_approved = pending = 0
    errors: list[dict[str, str]] = []
    try:
        for city in HOTSPOT_CITIES:
            try:
                candidates = await discovery.discover_city(
                    city, settings.hotspot_discovery_candidate_limit
                )
                public_count = int(
                    await session.scalar(
                        select(func.count(TravelHotspot.id)).where(
                            TravelHotspot.city_code == city.code,
                            TravelHotspot.is_active.is_(True),
                            TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
                        )
                    )
                    or 0
                )
                for candidate in candidates:
                    hotspot = await session.scalar(
                        select(TravelHotspot).where(TravelHotspot.wikidata_item_id == candidate.qid)
                    )
                    if hotspot is None:
                        hotspot = TravelHotspot(
                            slug=f"wikidata-{candidate.qid.lower()}",
                            wikidata_item_id=candidate.qid,
                            discovered_at=now,
                        )
                        added += 1
                    elif hotspot.origin == "curated" or hotspot.review_status == "approved":
                        hotspot.last_seen_at = now
                        continue
                    if hotspot.review_status in {"rejected", "disabled"}:
                        hotspot.last_seen_at = now
                        continue
                    status, reason = candidate.review_status, candidate.review_reason
                    if status == "auto_approved" and public_count >= city.target_count:
                        status, reason = "pending", "city_quota_reached"
                    elif status == "auto_approved":
                        status, reason = "pending", "map_identity_required"
                    if status == "auto_approved":
                        public_count += 1
                        auto_approved += 1
                    else:
                        pending += 1
                    hotspot.name = candidate.name
                    hotspot.destination_id = city.id
                    hotspot.city_code = city.code
                    hotspot.city_name = city.name
                    hotspot.country_code = city.country_code
                    hotspot.country_name = city.country_name
                    hotspot.category = candidate.category
                    hotspot.search_text = (
                        f"{candidate.name} {candidate.wikipedia_title} {city.name}".casefold()
                    )
                    hotspot.latitude = Decimal(str(candidate.latitude))
                    hotspot.longitude = Decimal(str(candidate.longitude))
                    hotspot.coordinate_source_type = "wikidata"
                    hotspot.coordinate_source_url = next(iter(candidate.source_urls), None)
                    hotspot.coordinate_verified_at = now
                    hotspot.wikipedia_project = candidate.wikipedia_project
                    hotspot.wikipedia_title = candidate.wikipedia_title
                    hotspot.origin = "wikimedia_discovery"
                    hotspot.review_status = status
                    hotspot.review_reason = reason
                    hotspot.discovery_distance_km = Decimal(str(round(candidate.distance_km, 2)))
                    hotspot.last_seen_at = now
                    hotspot.source_urls = list(candidate.source_urls)
                    hotspot.metadata_json = {
                        "wikidata_types": list(candidate.type_ids),
                        "pageview_pages": [list(page) for page in candidate.pageview_pages],
                    }
                    hotspot.is_active = status in PUBLIC_REVIEW_STATUSES
                    session.add(hotspot)
                await session.commit()
            except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
                await session.rollback()
                errors.append({"city_code": city.code, "error": type(exc).__name__})
    finally:
        await discovery.close()
    return {
        "added": added,
        "auto_approved": auto_approved,
        "pending": pending,
        "errors": errors,
    }


async def collect_hotspots(
    session: AsyncSession,
    settings: Settings,
    *,
    observed_on: date | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    target_date = observed_on or date.today()
    hotspots = await seed_catalog(session, target_date)
    await seed_food_catalog(session)
    await session.commit()
    discovery_report: dict[str, Any] = {"skipped": True, "errors": []}
    latest_discovery = await session.scalar(
        select(func.max(TravelHotspot.last_seen_at)).where(
            TravelHotspot.origin == "wikimedia_discovery"
        )
    )
    discovery_due = latest_discovery is None or latest_discovery <= datetime.now(UTC) - timedelta(
        seconds=settings.hotspot_discovery_interval_seconds
    )
    if settings.hotspot_discovery_enabled and discovery_due:
        discovery_report = await discover_hotspots(session, settings, client=client)
        hotspots = list(
            (
                await session.scalars(
                    select(TravelHotspot).where(
                        TravelHotspot.is_active.is_(True),
                        TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
                    )
                )
            ).all()
        )
    collected = 0
    errors: list[dict[str, str]] = []
    if settings.hotspot_wikimedia_enabled:
        wikimedia = WikimediaPageviewClient(
            settings.hotspot_wikimedia_user_agent,
            settings.hotspot_wikimedia_timeout_seconds,
            client,
            settings.hotspot_wikimedia_max_retries,
            settings.hotspot_wikimedia_retry_backoff_seconds,
        )
        semaphore = asyncio.Semaphore(settings.hotspot_discovery_concurrency)
        existing_signal_ids = set(
            (
                await session.scalars(
                    select(HotspotSignal.hotspot_id).where(
                        HotspotSignal.metric == "pageviews_30d",
                        HotspotSignal.observed_on == target_date - timedelta(days=1),
                    )
                )
            ).all()
        )

        async def collect_one(hotspot: TravelHotspot) -> tuple[TravelHotspot, Any] | None:
            if not hotspot.wikipedia_project or not hotspot.wikipedia_title:
                return None
            if hotspot.id in existing_signal_ids:
                return None
            try:
                async with semaphore:
                    window = await wikimedia.pageviews(
                        hotspot.wikipedia_project,
                        hotspot.wikipedia_title,
                        observed_on=target_date - timedelta(days=1),
                    )
                return hotspot, window
            except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
                errors.append({"slug": hotspot.slug, "error": type(exc).__name__})
                return None

        for start in range(0, len(hotspots), 20):
            results = await asyncio.gather(
                *(collect_one(item) for item in hotspots[start : start + 20])
            )
            for result in results:
                if result is None:
                    continue
                hotspot, window = result
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
            await session.commit()
        await session.commit()
    rankings = await refresh_rankings(session, target_date)
    await session.commit()
    map_id_refresh = await refresh_due_map_place_ids(session, settings, client=client)
    guide_report: dict[str, Any] = {"skipped": True, "reason": "disabled_or_unconfigured"}
    if settings.hotspot_guides_enabled and (
        (settings.hotspot_guide_youtube_enabled and settings.hotspot_guide_youtube_api_key)
        or (settings.hotspot_guide_brave_enabled and settings.hotspot_guide_brave_api_key)
    ):
        stale_cutoff = datetime.now(UTC) - timedelta(days=settings.hotspot_guide_refresh_days)
        last_verified = (
            select(func.max(HotspotGuide.last_verified_at))
            .where(HotspotGuide.hotspot_id == TravelHotspot.id)
            .correlate(TravelHotspot)
            .scalar_subquery()
        )
        target = await session.scalar(
            select(TravelHotspot)
            .where(
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
                or_(last_verified.is_(None), last_verified < stale_cutoff),
            )
            .order_by(last_verified.asc().nullsfirst(), TravelHotspot.updated_at.desc())
            .limit(1)
        )
        if target:
            guide_report = {
                "hotspot_id": str(target.id),
                **await discover_guides(
                    session,
                    settings,
                    target,
                    list(LOCALES),
                    client=client,
                    redis=get_redis(),
                    automatic=True,
                ),
            }
        await session.execute(
            delete(HotspotGuide).where(
                HotspotGuide.provider == "youtube",
                HotspotGuide.last_verified_at < datetime.now(UTC) - timedelta(days=30),
            )
        )
        await session.commit()
    return {
        "observed_on": target_date.isoformat(),
        "catalog_count": len(hotspots),
        "discovery": discovery_report,
        "wikimedia_collected": collected,
        "ranking_count": rankings,
        "map_id_refresh": map_id_refresh,
        "guides": guide_report,
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


def _destination_fields(destination_id: str) -> dict[str, Any]:
    profile = destination_for_id(destination_id)
    if profile is None:
        return {
            "destination_role": "primary",
            "parent_destination_id": None,
            "is_cross_city": False,
        }
    return {
        "destination_role": profile.role,
        "parent_destination_id": profile.parent_destination_id,
        "is_cross_city": profile.role == "extension",
    }


async def list_rankings(
    session: AsyncSession,
    *,
    q: str | None = None,
    city_code: str | None = None,
    destination_id: str | None = None,
    country_code: str | None = None,
    category: str | None = None,
    role: str | None = None,
    after_rank: int | None = None,
    limit: int = 20,
    style: str = "all",
    locale: str = "zh-TW",
    places_configured: bool = False,
) -> dict[str, Any]:
    prefix = "deep_" if style == "deep" else ""
    if destination_id:
        scope, scope_key = f"{prefix}destination", destination_id.casefold()
    elif city_code:
        scope, scope_key = f"{prefix}city", city_code.upper()
    else:
        scope, scope_key = f"{prefix}global", "global"
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
            "total": 0,
            "has_more": False,
            "next_cursor": None,
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
            TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
        )
        .order_by(HotspotRanking.rank)
    )
    if q and q.strip():
        term = f"%{q.strip().casefold()}%"
        query = query.where(
            or_(TravelHotspot.search_text.ilike(term), TravelHotspot.name.ilike(term))
        )
    if category:
        query = query.where(TravelHotspot.category == category.casefold())
    if country_code:
        query = query.where(TravelHotspot.country_code == country_code.upper())
    if role:
        role_ids = [item.id for item in DESTINATIONS if item.role == role]
        query = query.where(TravelHotspot.destination_id.in_(role_ids))
    total = int(await session.scalar(select(func.count()).select_from(query.subquery())) or 0)
    if after_rank is not None:
        query = query.where(HotspotRanking.rank > after_rank)
    rows = (await session.execute(query.limit(limit + 1))).all()
    has_more = len(rows) > limit
    rows = rows[:limit]
    hotspot_ids = [hotspot.id for _, hotspot in rows]
    localized_names = {
        row.hotspot_id: row.name
        for row in (
            await session.scalars(
                select(HotspotLocalization).where(
                    HotspotLocalization.hotspot_id.in_(hotspot_ids),
                    HotspotLocalization.locale == locale,
                )
            )
        ).all()
    }
    guide_counts = {
        (hotspot_id, kind): int(count)
        for hotspot_id, kind, count in (
            await session.execute(
                select(
                    HotspotGuide.hotspot_id,
                    HotspotGuide.content_type,
                    func.count(HotspotGuide.id),
                )
                .where(
                    HotspotGuide.hotspot_id.in_(hotspot_ids),
                    HotspotGuide.locale == locale,
                    HotspotGuide.review_status == "approved",
                )
                .group_by(HotspotGuide.hotspot_id, HotspotGuide.content_type)
            )
        ).all()
    }
    place_profiles = {
        profile.hotspot_id: profile
        for profile in (
            await session.scalars(
                select(HotspotPlaceProfile).where(
                    HotspotPlaceProfile.hotspot_id.in_(hotspot_ids)
                )
            )
        ).all()
    }
    items: list[dict[str, Any]] = []
    for ranking, hotspot in rows:
        growth_rate = ranking.explanation.get("growth_rate")
        localized_name = localized_names.get(hotspot.id, hotspot.name)
        local_name = hotspot.metadata_json.get("local_name")
        items.append(
            {
                "id": str(hotspot.id),
                "slug": hotspot.slug,
                "rank": ranking.rank,
                "name": localized_name,
                "destination_id": hotspot.destination_id,
                "city_code": hotspot.city_code,
                "city_name": hotspot.city_name,
                "country_code": hotspot.country_code,
                "country_name": hotspot.country_name,
                "category": hotspot.category,
                "latitude": float(hotspot.latitude) if hotspot.latitude is not None else None,
                "longitude": float(hotspot.longitude) if hotspot.longitude is not None else None,
                "coordinate_source": {
                    "type": hotspot.coordinate_source_type,
                    "url": hotspot.coordinate_source_url,
                    "verified_at": hotspot.coordinate_verified_at.isoformat()
                    if hotspot.coordinate_verified_at is not None
                    else None,
                },
                "map_match_status": hotspot.map_match_status,
                "map_verified_at": hotspot.map_verified_at.isoformat()
                if hotspot.map_verified_at is not None
                else None,
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
                "is_deep_travel": hotspot.is_deep_travel,
                "depth_kind": hotspot.depth_kind,
                "depth_score": float(hotspot.depth_score)
                if hotspot.depth_score is not None
                else None,
                "depth_reason": hotspot.metadata_json.get("depth_reason"),
                "local_name": local_name,
                "access_minutes": hotspot.metadata_json.get("access_minutes"),
                "recommended_duration_minutes": hotspot.metadata_json.get(
                    "recommended_duration_minutes"
                ),
                "guide_counts": {
                    "article": guide_counts.get((hotspot.id, "article"), 0),
                    "video": guide_counts.get((hotspot.id, "video"), 0),
                },
                "map_links": build_map_links(
                    name=localized_name,
                    local_name=local_name,
                    city_name=hotspot.city_name,
                    country_code=hotspot.country_code,
                    latitude=hotspot.latitude,
                    longitude=hotspot.longitude,
                    google_place_id=hotspot.google_place_id,
                    naver_map_url=hotspot.naver_map_url,
                    map_match_status=hotspot.map_match_status,
                ),
                "place_summary": place_summary_payload(
                    hotspot,
                    place_profiles.get(hotspot.id),
                    configured=places_configured,
                ),
                **_destination_fields(hotspot.destination_id),
            }
        )
    return {
        "scope": scope,
        "scope_key": scope_key,
        "observed_on": latest_date.isoformat(),
        "window_days": 30,
        "total": total,
        "has_more": has_more,
        "next_cursor": items[-1]["rank"] if has_more and items else None,
        "items": items,
    }


async def hotspot_facets(session: AsyncSession) -> dict[str, Any]:
    conditions = (
        TravelHotspot.is_active.is_(True),
        TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
    )

    async def grouped(*columns: Any) -> list[Any]:
        return list(
            (
                await session.execute(
                    select(*columns, func.count(TravelHotspot.id).label("count"))
                    .where(*conditions)
                    .group_by(*columns)
                    .order_by(*columns)
                )
            ).all()
        )

    countries = await grouped(TravelHotspot.country_code, TravelHotspot.country_name)
    cities = await grouped(
        TravelHotspot.destination_id,
        TravelHotspot.city_code,
        TravelHotspot.city_name,
        TravelHotspot.country_code,
    )
    categories = await grouped(TravelHotspot.category)
    deep_count = int(
        await session.scalar(
            select(func.count(TravelHotspot.id)).where(
                *conditions, TravelHotspot.is_deep_travel.is_(True)
            )
        )
        or 0
    )
    return {
        "total": sum(int(row.count) for row in countries),
        "countries": [
            {"code": row.country_code, "name": row.country_name, "count": row.count}
            for row in countries
        ],
        "cities": [
            {
                "code": row.city_code,
                "destination_id": row.destination_id,
                "name": row.city_name,
                "country_code": row.country_code,
                "count": row.count,
                **_destination_fields(row.destination_id),
            }
            for row in cities
        ],
        "categories": [{"code": row.category, "count": row.count} for row in categories],
        "styles": [
            {"code": "all", "name": "全部旅遊", "count": sum(int(row.count) for row in countries)},
            {"code": "deep", "name": "深度旅遊", "count": deep_count},
        ],
    }


async def load_planner_hotspots(
    session: AsyncSession,
    *,
    city_code: str | None = None,
    destination_id: str | None = None,
    interests: list[str] | None = None,
    limit: int = 12,
    extension_destination_ids: list[str] | None = None,
    days: int | None = None,
) -> list[ItineraryHotspot]:
    """Load only approved deep-ranking rows for the real itinerary builder."""
    result = await list_rankings(
        session,
        city_code=city_code,
        destination_id=destination_id,
        style="deep",
        limit=min(50, max(1, limit)),
    )
    ranked_items = result["items"]
    primary_id = destination_id
    if primary_id is None and city_code:
        resolved = destination_for_code(city_code)
        primary_id = resolved.id if resolved else None
    extension_limit = 0 if (days or 0) < 4 else (2 if (days or 0) >= 7 else 1)
    for extension_id in (extension_destination_ids or [])[:extension_limit]:
        extension = destination_for_id(extension_id)
        if extension is None or extension.parent_destination_id != primary_id:
            continue
        extension_result = await list_rankings(
            session, destination_id=extension.id, style="deep", limit=1
        )
        ranked_items.extend(extension_result["items"])
    requested = {interest for interest in (interests or []) if interest != "deep_travel"}
    if requested:
        ranked_items = sorted(
            ranked_items,
            key=lambda item: (item["category"] not in requested, item["rank"]),
        )
    rows: list[ItineraryHotspot] = []
    for item in ranked_items:
        required = (
            item["latitude"],
            item["longitude"],
            item["depth_kind"],
            item["depth_score"],
            item["depth_reason"],
            item["access_minutes"],
            item["recommended_duration_minutes"],
        )
        if (
            any(value is None for value in required)
            or item["map_match_status"] != "verified"
            or not item["map_links"]
            or not has_durable_coordinates(
                item["latitude"],
                item["longitude"],
                item["coordinate_source"].get("type"),
                item["coordinate_source"].get("url"),
            )
        ):
            continue
        rows.append(
            ItineraryHotspot(
                hotspot_id=item["id"],
                name=item["name"],
                category=item["category"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                map_links=item["map_links"],
                depth_kind=item["depth_kind"],
                depth_score=item["depth_score"],
                depth_reason=item["depth_reason"],
                access_minutes=item["access_minutes"],
                recommended_duration_minutes=item["recommended_duration_minutes"],
                destination_id=item["destination_id"],
                destination_role=item["destination_role"],
                parent_destination_id=item["parent_destination_id"],
                is_cross_city=item["is_cross_city"],
            )
        )
    return rows
