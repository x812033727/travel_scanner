from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from uuid import UUID

from redis import Redis as SyncRedis
from rq import Queue, Retry
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import Settings
from app.db import SessionFactory, engine
from app.hotspots.service import PUBLIC_REVIEW_STATUSES
from app.infra import get_redis
from app.models import RestaurantPlace, RestaurantScanRun, TravelHotspot
from app.restaurants.google import GoogleRestaurantProvider, RestaurantProviderError
from app.restaurants.service import create_scan_run, execute_scan, refresh_restaurant_identity


def enqueue_restaurant_scan(run_id: UUID, settings: Settings) -> str:
    connection = SyncRedis.from_url(settings.redis_url)
    try:
        job = Queue("restaurant-scans", connection=connection).enqueue(
            "app.restaurants.tasks.run_restaurant_scan",
            str(run_id),
            job_timeout=3_600,
            retry=Retry(max=3, interval=[60, 300, 900]),
        )
        return str(job.id)
    finally:
        connection.close()


async def enqueue_next_automatic_scan(
    session: AsyncSession, settings: Settings
) -> dict[str, str | None]:
    if not settings.restaurant_scan_enabled or not settings.google_maps_api_key:
        return {"status": "disabled", "run_id": None, "hotspot_id": None}
    stale_cutoff = datetime.now(UTC) - timedelta(days=settings.restaurant_scan_refresh_days)
    latest_finished = (
        select(func.max(RestaurantScanRun.completed_at))
        .where(
            RestaurantScanRun.hotspot_id == TravelHotspot.id,
            RestaurantScanRun.status.in_(("completed", "partial")),
        )
        .correlate(TravelHotspot)
        .scalar_subquery()
    )
    active_count = (
        select(func.count(RestaurantScanRun.id))
        .where(
            RestaurantScanRun.hotspot_id == TravelHotspot.id,
            RestaurantScanRun.status.in_(("queued", "running")),
        )
        .correlate(TravelHotspot)
        .scalar_subquery()
    )
    latest_attempt = (
        select(func.max(RestaurantScanRun.updated_at))
        .where(RestaurantScanRun.hotspot_id == TravelHotspot.id)
        .correlate(TravelHotspot)
        .scalar_subquery()
    )
    hotspot = await session.scalar(
        select(TravelHotspot)
        .where(
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
            TravelHotspot.latitude.is_not(None),
            TravelHotspot.longitude.is_not(None),
            active_count == 0,
            or_(latest_finished.is_(None), latest_finished < stale_cutoff),
        )
        .order_by(latest_attempt.asc().nullsfirst(), TravelHotspot.updated_at.desc())
        .limit(1)
    )
    if hotspot is None:
        return {"status": "current", "run_id": None, "hotspot_id": None}
    period = datetime.now(UTC).date().toordinal() // settings.restaurant_scan_refresh_days
    run = await create_scan_run(
        session,
        hotspot.id,
        actor_user_id=None,
        idempotency_key=f"automatic:{hotspot.id}:{period}",
    )
    enqueue_restaurant_scan(run.id, settings)
    return {"status": "queued", "run_id": str(run.id), "hotspot_id": str(hotspot.id)}


async def refresh_next_stale_identity(
    session: AsyncSession, settings: Settings
) -> dict[str, str | None]:
    if not settings.google_maps_api_key:
        return {"status": "disabled", "place_id": None}
    cutoff = datetime.now(UTC) - timedelta(days=180)
    place = await session.scalar(
        select(RestaurantPlace)
        .where(
            or_(
                RestaurantPlace.identity_checked_at.is_(None),
                RestaurantPlace.identity_checked_at < cutoff,
            )
        )
        .order_by(RestaurantPlace.identity_checked_at.asc().nullsfirst())
        .limit(1)
    )
    if place is None:
        return {"status": "current", "place_id": None}
    try:
        result = await refresh_restaurant_identity(
            session,
            GoogleRestaurantProvider(get_redis(), settings),
            place,
        )
    except RestaurantProviderError:
        return {"status": "failed", "place_id": place.google_place_id}
    return {"status": result.status, "place_id": place.google_place_id}


async def _mark_failed(run_id: UUID) -> None:
    async with SessionFactory() as session:
        run = await session.get(RestaurantScanRun, run_id)
        if run is None or run.status in {"completed", "partial", "quota_paused"}:
            return
        run.status = "failed"
        run.failure_code = "restaurant_scan_failed"
        run.failure_detail = "Restaurant coverage scan could not be completed"
        run.completed_at = datetime.now(UTC)
        await session.commit()


async def _run(run_id: UUID) -> None:
    async with SessionFactory() as session:
        run = await session.get(RestaurantScanRun, run_id)
        if run is None or run.status not in {"queued", "running", "failed", "quota_paused"}:
            return
        try:
            settings = await load_runtime_settings(session)
            await execute_scan(session, get_redis(), run, settings)
        except Exception:
            await session.rollback()
            await _mark_failed(run_id)
            raise


def run_restaurant_scan(run_id: str) -> None:
    async def run_and_close_resources() -> None:
        try:
            await _run(UUID(run_id))
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close_resources())
