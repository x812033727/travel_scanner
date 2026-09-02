from __future__ import annotations

import asyncio
import json
import math
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal
from urllib.parse import urlencode
from uuid import UUID

import httpx
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.hotspots.service import PUBLIC_REVIEW_STATUSES
from app.i18n import Locale
from app.models import (
    HotspotRestaurantCandidate,
    RestaurantEditorialProfile,
    RestaurantFavorite,
    RestaurantPlace,
    RestaurantScanCell,
    RestaurantScanRun,
    TravelHotspot,
)
from app.problems import AppError
from app.restaurants.editorial import editorial_by_google_place_id
from app.restaurants.google import (
    GoogleRestaurantProvider,
    RestaurantIdentityResult,
    RestaurantProviderError,
    RestaurantQuotaExceeded,
    RestaurantSnapshot,
)

RestaurantSort = Literal["recommended", "rating", "reviews", "distance"]
MIN_RATING = 3.8
MIN_REVIEW_COUNT = 1_000
RECOMMENDATION_PRIOR = 4.0
MAX_AGGREGATE_PLACES = 100
RESTAURANT_LOCATION_CACHE_PREFIX = "restaurant-location:v1"


def build_place_maps_url(place_id: str) -> str:
    """Build the free cross-platform Maps URL without calling a Google API."""
    query = urlencode(
        {
            "api": "1",
            "query": place_id,
            "query_place_id": place_id,
        }
    )
    return f"https://www.google.com/maps/search/?{query}"


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6_371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    value = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return radius_km * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def recommendation_score(rating: float, review_count: int) -> float:
    weight = review_count / (review_count + MIN_REVIEW_COUNT)
    return weight * rating + (1 - weight) * RECOMMENDATION_PRIOR


def _sort_items(items: list[dict[str, Any]], sort: RestaurantSort) -> list[dict[str, Any]]:
    def key(item: dict[str, Any]) -> tuple[float, ...]:
        if sort == "rating":
            return (-item["rating"], -item["review_count"], item["distance_km"])
        if sort == "reviews":
            return (-item["review_count"], -item["rating"], item["distance_km"])
        if sort == "distance":
            return (item["distance_km"], -item["recommendation_score"])
        return (
            -item["recommendation_score"],
            -item["review_count"],
            item["distance_km"],
        )

    return sorted(items, key=key)


def _serialize_snapshot(
    snapshot: RestaurantSnapshot,
    hotspot: TravelHotspot,
    *,
    observed_at: datetime,
) -> dict[str, Any] | None:
    if not snapshot.qualified or snapshot.latitude is None or snapshot.longitude is None:
        return None
    if hotspot.latitude is None or hotspot.longitude is None:
        return None
    distance = haversine_km(
        float(hotspot.latitude),
        float(hotspot.longitude),
        snapshot.latitude,
        snapshot.longitude,
    )
    assert snapshot.rating is not None
    assert snapshot.review_count is not None
    return {
        "place_id": snapshot.place_id,
        "name": snapshot.name,
        "address": snapshot.address,
        "latitude": snapshot.latitude,
        "longitude": snapshot.longitude,
        "distance_km": round(distance, 2),
        "rating": snapshot.rating,
        "review_count": snapshot.review_count,
        "recommendation_score": round(
            recommendation_score(snapshot.rating, snapshot.review_count), 4
        ),
        "opening_hours": list(snapshot.opening_hours),
        "open_now": snapshot.open_now,
        "official_website_url": snapshot.official_website_url,
        "google_maps_url": snapshot.google_maps_url or build_place_maps_url(snapshot.place_id),
        "primary_type": snapshot.primary_type,
        "business_status": snapshot.business_status,
        "observed_at": observed_at.isoformat(),
        "attribution": "Google Maps",
    }


async def cache_restaurant_location(
    redis: Redis,
    snapshot: RestaurantSnapshot,
    settings: Settings,
    observed_at: datetime,
) -> None:
    """Cache only lat/lng in Redis, where expiry is enforced by the key TTL."""
    if snapshot.latitude is None or snapshot.longitude is None:
        return
    payload = json.dumps(
        {
            "latitude": snapshot.latitude,
            "longitude": snapshot.longitude,
            "fetched_at": observed_at.isoformat(),
        },
        separators=(",", ":"),
    )
    try:
        await redis.set(
            f"{RESTAURANT_LOCATION_CACHE_PREFIX}:{snapshot.place_id}",
            payload,
            ex=settings.restaurant_location_cache_days * 86_400,
        )
    except RedisError:
        # The location cache is optional; a cache outage must not hide live data.
        return


async def save_restaurant_identity(
    session: AsyncSession,
    hotspot_id: UUID,
    place_id: str,
    *,
    run_id: UUID | None,
    radius_meters: int,
) -> RestaurantPlace:
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    generated_maps_url = build_place_maps_url(place_id)
    if place is None:
        place = RestaurantPlace(
            google_place_id=place_id,
            generated_maps_url=generated_maps_url,
        )
        session.add(place)
        await session.flush()
    elif place.generated_maps_url != generated_maps_url:
        place.generated_maps_url = generated_maps_url
    place.identity_status = "active"
    place.identity_checked_at = datetime.now(UTC)
    place.identity_error_code = None
    candidate = await session.scalar(
        select(HotspotRestaurantCandidate).where(
            HotspotRestaurantCandidate.hotspot_id == hotspot_id,
            HotspotRestaurantCandidate.restaurant_place_id == place.id,
        )
    )
    if candidate is None:
        candidate = HotspotRestaurantCandidate(
            hotspot_id=hotspot_id,
            restaurant_place_id=place.id,
            scan_run_id=run_id,
            discovery_radius_meters=radius_meters,
        )
    else:
        candidate.scan_run_id = run_id or candidate.scan_run_id
        candidate.discovery_radius_meters = max(candidate.discovery_radius_meters, radius_meters)
    session.add(candidate)
    return place


async def _hotspot(session: AsyncSession, hotspot_id: UUID) -> TravelHotspot:
    hotspot = await session.get(TravelHotspot, hotspot_id)
    if (
        hotspot is None
        or not hotspot.is_active
        or hotspot.review_status not in PUBLIC_REVIEW_STATUSES
    ):
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    if hotspot.latitude is None or hotspot.longitude is None:
        raise AppError(422, "hotspot_coordinates_missing", "景點尚未設定座標")
    return hotspot


async def _coverage_status(session: AsyncSession, hotspot_id: UUID) -> dict[str, Any]:
    run = await session.scalar(
        select(RestaurantScanRun)
        .where(RestaurantScanRun.hotspot_id == hotspot_id)
        .order_by(RestaurantScanRun.created_at.desc())
        .limit(1)
    )
    candidate_count = int(
        await session.scalar(
            select(func.count())
            .select_from(HotspotRestaurantCandidate)
            .join(
                RestaurantPlace,
                RestaurantPlace.id == HotspotRestaurantCandidate.restaurant_place_id,
            )
            .where(
                HotspotRestaurantCandidate.hotspot_id == hotspot_id,
                RestaurantPlace.is_suppressed.is_(False),
                RestaurantPlace.identity_status.not_in(("moved", "not_found")),
            )
        )
        or 0
    )
    if run is None:
        return {
            "status": "not_started",
            "run_id": None,
            "cells_completed": 0,
            "cells_total": 0,
            "candidate_count": candidate_count,
        }
    return {
        "status": run.status,
        "run_id": str(run.id),
        "cells_completed": run.cells_completed,
        "cells_total": run.cells_total,
        "candidate_count": candidate_count,
        "updated_at": run.updated_at.isoformat(),
    }


async def search_restaurants(
    session: AsyncSession,
    redis: Redis,
    settings: Settings,
    hotspot_id: UUID,
    *,
    locale: Locale,
    radius_km: Literal[5, 10],
    sort: RestaurantSort,
    cursor: int | None,
    limit: int,
    exclude_place_ids: list[str],
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    hotspot = await _hotspot(session, hotspot_id)
    provider = GoogleRestaurantProvider(redis, settings, locale=locale, client=client)
    observed_at = datetime.now(UTC)
    radius_meters = radius_km * 1_000
    assert hotspot.latitude is not None and hotspot.longitude is not None
    snapshots: list[RestaurantSnapshot] = []
    next_cursor: int | None = None
    source = "nearby"
    if cursor is None:
        snapshots = await provider.nearby(
            float(hotspot.latitude),
            float(hotspot.longitude),
            radius_meters,
            limit=limit,
        )
        next_cursor = 0
    else:
        source = "coverage"
        query = (
            select(RestaurantPlace)
            .join(
                HotspotRestaurantCandidate,
                HotspotRestaurantCandidate.restaurant_place_id == RestaurantPlace.id,
            )
            .where(
                HotspotRestaurantCandidate.hotspot_id == hotspot_id,
                RestaurantPlace.is_suppressed.is_(False),
                RestaurantPlace.identity_status.not_in(("moved", "not_found")),
            )
        )
        if exclude_place_ids:
            query = query.where(RestaurantPlace.google_place_id.not_in(exclude_place_ids))
        query = query.order_by(RestaurantPlace.google_place_id).offset(cursor).limit(limit)
        rows = list((await session.execute(query)).scalars())
        results = await asyncio.gather(
            *(provider.details(row.google_place_id) for row in rows),
            return_exceptions=True,
        )
        removed_count = 0
        for row, result in zip(rows, results, strict=True):
            if isinstance(result, RestaurantSnapshot) and result.qualified:
                snapshots.append(result)
            elif isinstance(result, RestaurantSnapshot):
                removed_count += 1
                await session.execute(
                    delete(HotspotRestaurantCandidate).where(
                        HotspotRestaurantCandidate.hotspot_id == hotspot_id,
                        HotspotRestaurantCandidate.restaurant_place_id == row.id,
                    )
                )
        if any(isinstance(result, RestaurantQuotaExceeded) for result in results):
            raise RestaurantQuotaExceeded("place_details_restaurant")
        next_cursor = cursor + len(rows) - removed_count if len(rows) == limit else None

    items: list[dict[str, Any]] = []
    for snapshot in snapshots:
        if not snapshot.qualified:
            continue
        await save_restaurant_identity(
            session,
            hotspot.id,
            snapshot.place_id,
            run_id=None,
            radius_meters=10_000,
        )
        await cache_restaurant_location(redis, snapshot, settings, observed_at)
        item = _serialize_snapshot(snapshot, hotspot, observed_at=observed_at)
        if item is not None and item["distance_km"] <= radius_km:
            items.append(item)
    editorial = await editorial_by_google_place_id(
        session, [str(item["place_id"]) for item in items]
    )
    for item in items:
        item["editorial"] = editorial.get(str(item["place_id"]))
    await session.commit()
    coverage = await _coverage_status(session, hotspot_id)
    if not coverage["candidate_count"]:
        next_cursor = None
    return {
        "hotspot_id": str(hotspot.id),
        "hotspot_name": hotspot.name,
        "radius_km": radius_km,
        "sort": sort,
        "filters": {"min_rating": MIN_RATING, "min_review_count": MIN_REVIEW_COUNT},
        "items": _sort_items(items, sort),
        "next_cursor": next_cursor,
        "source": source,
        "coverage": coverage,
        "observed_at": observed_at.isoformat(),
        "attribution": "Google Maps",
        "persistence": {
            "place_id": "durable",
            "generated_maps_url": "durable",
            "location_cache_ttl_days": settings.restaurant_location_cache_days,
            "other_google_fields": "live_only",
        },
    }


async def ensure_restaurant_place(
    session: AsyncSession,
    place_id: str,
) -> RestaurantPlace:
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    if place is None:
        place = RestaurantPlace(
            google_place_id=place_id,
            generated_maps_url=build_place_maps_url(place_id),
        )
        session.add(place)
        await session.flush()
    return place


async def refresh_restaurant_identity(
    session: AsyncSession,
    provider: GoogleRestaurantProvider,
    place: RestaurantPlace,
) -> RestaurantIdentityResult:
    now = datetime.now(UTC)
    try:
        result = await provider.refresh_identity(place.google_place_id)
    except RestaurantProviderError:
        place.identity_error_code = "place_id_refresh_failed"
        place.identity_checked_at = now
        await session.commit()
        raise
    place.identity_status = result.status
    place.identity_checked_at = now
    place.identity_error_code = None
    place.successor_place_id = result.moved_place_id
    if result.moved_place_id:
        successor = await ensure_restaurant_place(session, result.moved_place_id)
        successor.identity_status = "active"
        successor.identity_checked_at = now
        old_candidates = list(
            (
                await session.scalars(
                    select(HotspotRestaurantCandidate).where(
                        HotspotRestaurantCandidate.restaurant_place_id == place.id
                    )
                )
            ).all()
        )
        for candidate in old_candidates:
            duplicate = await session.scalar(
                select(HotspotRestaurantCandidate).where(
                    HotspotRestaurantCandidate.hotspot_id == candidate.hotspot_id,
                    HotspotRestaurantCandidate.restaurant_place_id == successor.id,
                )
            )
            if duplicate is None:
                candidate.restaurant_place_id = successor.id
            else:
                await session.delete(candidate)
        old_favorites = list(
            (
                await session.scalars(
                    select(RestaurantFavorite).where(
                        RestaurantFavorite.restaurant_place_id == place.id
                    )
                )
            ).all()
        )
        for favorite in old_favorites:
            duplicate = await session.scalar(
                select(RestaurantFavorite).where(
                    RestaurantFavorite.user_id == favorite.user_id,
                    RestaurantFavorite.restaurant_place_id == successor.id,
                )
            )
            if duplicate is None:
                favorite.restaurant_place_id = successor.id
            else:
                await session.delete(favorite)
        old_profile = await session.scalar(
            select(RestaurantEditorialProfile).where(
                RestaurantEditorialProfile.restaurant_place_id == place.id
            )
        )
        successor_profile = await session.scalar(
            select(RestaurantEditorialProfile).where(
                RestaurantEditorialProfile.restaurant_place_id == successor.id
            )
        )
        if old_profile is not None and successor_profile is None:
            old_profile.restaurant_place_id = successor.id
    await session.commit()
    return result


def split_circle(
    latitude: float, longitude: float, radius_meters: int
) -> tuple[tuple[float, float, int], ...]:
    """Cover a circle with one central and six overlapping half-radius circles."""
    child_radius = max(50, round(radius_meters / 2))
    center_distance = radius_meters * math.sqrt(3) / 2
    latitude_scale = 111_320.0
    longitude_scale = max(1.0, latitude_scale * math.cos(math.radians(latitude)))
    children: list[tuple[float, float, int]] = [(latitude, longitude, child_radius)]
    for angle in range(0, 360, 60):
        radians = math.radians(angle)
        child_latitude = latitude + math.sin(radians) * center_distance / latitude_scale
        child_longitude = longitude + math.cos(radians) * center_distance / longitude_scale
        child_longitude = ((child_longitude + 180) % 360) - 180
        children.append((child_latitude, child_longitude, child_radius))
    return tuple(children)


async def create_scan_run(
    session: AsyncSession,
    hotspot_id: UUID,
    *,
    actor_user_id: UUID | None,
    idempotency_key: str,
) -> RestaurantScanRun:
    existing = await session.scalar(
        select(RestaurantScanRun).where(RestaurantScanRun.idempotency_key == idempotency_key)
    )
    if existing is not None:
        return existing
    hotspot = await _hotspot(session, hotspot_id)
    run = RestaurantScanRun(
        hotspot_id=hotspot.id,
        actor_user_id=actor_user_id,
        idempotency_key=idempotency_key,
        radius_meters=10_000,
        status="queued",
    )
    session.add(run)
    await session.flush()
    session.add(
        RestaurantScanCell(
            run_id=run.id,
            center_latitude=hotspot.latitude,
            center_longitude=hotspot.longitude,
            radius_meters=10_000,
            depth=0,
            status="queued",
        )
    )
    await session.commit()
    return run


async def execute_scan(
    session: AsyncSession,
    redis: Redis,
    run: RestaurantScanRun,
    settings: Settings,
    *,
    client: httpx.AsyncClient | None = None,
) -> None:
    provider = GoogleRestaurantProvider(redis, settings, client=client)
    hotspot = await _hotspot(session, run.hotspot_id)
    run.status = "running"
    run.started_at = run.started_at or datetime.now(UTC)
    run.completed_at = None
    run.failure_code = None
    run.failure_detail = None
    await session.commit()
    partial = False
    batch_calls = 0
    while True:
        cell = await session.scalar(
            select(RestaurantScanCell)
            .where(
                RestaurantScanCell.run_id == run.id,
                RestaurantScanCell.status == "queued",
            )
            .order_by(RestaurantScanCell.depth, RestaurantScanCell.created_at)
            .limit(1)
        )
        if cell is None:
            break
        if batch_calls >= settings.restaurant_scan_batch_call_limit:
            run.status = "quota_paused"
            run.failure_code = "restaurant_scan_batch_limit"
            run.completed_at = datetime.now(UTC)
            await session.commit()
            return
        cell.status = "running"
        await session.commit()
        try:
            if cell.provider_place_ids and cell.details_cursor < len(cell.provider_place_ids):
                place_id = cell.provider_place_ids[cell.details_cursor]
                snapshot = await provider.details(place_id)
                run.details_calls += 1
                batch_calls += 1
                cell.details_cursor += 1
                if snapshot is not None and snapshot.qualified:
                    observed_at = datetime.now(UTC)
                    item = _serialize_snapshot(snapshot, hotspot, observed_at=observed_at)
                    if item is not None and item["distance_km"] <= run.radius_meters / 1_000:
                        await save_restaurant_identity(
                            session,
                            run.hotspot_id,
                            place_id,
                            run_id=run.id,
                            radius_meters=run.radius_meters,
                        )
                        await cache_restaurant_location(redis, snapshot, settings, observed_at)
                if cell.details_cursor >= len(cell.provider_place_ids):
                    cell.status = "completed"
                    run.cells_completed += 1
                else:
                    cell.status = "queued"
                await session.commit()
                continue

            result = await provider.aggregate(
                float(cell.center_latitude),
                float(cell.center_longitude),
                cell.radius_meters,
            )
            run.aggregate_calls += 1
            batch_calls += 1
            if result.count > MAX_AGGREGATE_PLACES:
                if cell.depth >= settings.restaurant_scan_max_depth or cell.radius_meters <= 50:
                    cell.status = "partial"
                    run.cells_completed += 1
                    partial = True
                else:
                    for latitude, longitude, radius in split_circle(
                        float(cell.center_latitude),
                        float(cell.center_longitude),
                        cell.radius_meters,
                    ):
                        session.add(
                            RestaurantScanCell(
                                run_id=run.id,
                                parent_cell_id=cell.id,
                                status="queued",
                                center_latitude=Decimal(str(round(latitude, 6))),
                                center_longitude=Decimal(str(round(longitude, 6))),
                                radius_meters=radius,
                                depth=cell.depth + 1,
                            )
                        )
                    cell.status = "split"
                    run.cells_total += 7
            else:
                cell.provider_place_ids = list(result.place_ids)
                cell.details_cursor = 0
                if cell.provider_place_ids:
                    cell.status = "queued"
                else:
                    cell.status = "completed"
                    run.cells_completed += 1
            await session.commit()
        except RestaurantQuotaExceeded:
            cell.status = "queued"
            run.status = "quota_paused"
            run.failure_code = RestaurantQuotaExceeded.code
            run.completed_at = datetime.now(UTC)
            await session.commit()
            return
        except RestaurantProviderError as exc:
            cell.status = "failed"
            cell.error_code = exc.code
            run.status = "partial" if run.cells_completed else "failed"
            run.failure_code = exc.code
            run.failure_detail = str(exc)
            run.completed_at = datetime.now(UTC)
            await session.commit()
            return
    run.candidate_count = int(
        await session.scalar(
            select(func.count())
            .select_from(HotspotRestaurantCandidate)
            .where(HotspotRestaurantCandidate.hotspot_id == run.hotspot_id)
        )
        or 0
    )
    run.status = "partial" if partial else "completed"
    run.completed_at = datetime.now(UTC)
    run.metadata_json = {
        "min_rating": MIN_RATING,
        "min_review_count": MIN_REVIEW_COUNT,
        "qualification_filters_applied_live": True,
        "persisted_provider_fields": ["place_id"],
        "location_cache_ttl_days": settings.restaurant_location_cache_days,
        "coverage_algorithm": "adaptive_seven_circle",
    }
    await session.commit()
