from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from redis import Redis as SyncRedis
from rq import Queue, Retry

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.hotspots.places import enrich_hotspot_place
from app.infra import get_redis
from app.models import AdminAuditLog, HotspotPlaceEnrichmentRun, TravelHotspot

CHUNK_SIZE = 25


def enqueue_place_enrichment_run(run_id: UUID, hotspot_ids: list[UUID]) -> list[str]:
    connection = SyncRedis.from_url(get_settings().redis_url)
    queue = Queue("hotspot-places", connection=connection)
    queued: list[str] = []
    for start in range(0, len(hotspot_ids), CHUNK_SIZE):
        job = queue.enqueue(
            "app.hotspots.place_tasks.run_hotspot_place_enrichment_chunk",
            str(run_id),
            [str(item) for item in hotspot_ids[start : start + CHUNK_SIZE]],
            job_timeout=900,
            retry=Retry(max=2, interval=[30, 120]),
        )
        queued.append(job.id)
    return queued


async def _run_chunk(run_id: UUID, hotspot_ids: list[UUID]) -> None:
    async with SessionFactory() as session:
        run = await session.get(HotspotPlaceEnrichmentRun, run_id)
        if run is None or run.status in {"completed", "partial"}:
            return
        settings = await load_runtime_settings(session)
        if not settings.google_maps_api_key or not settings.hotspot_place_enrichment_enabled:
            run.status = "failed"
            run.error_json = [
                {"code": "google_maps_not_configured", "message": "Google Maps 尚未設定"}
            ]
            run.completed_at = datetime.now(UTC)
            await session.commit()
            return
        if run.status == "queued":
            run.status = "running"
            run.started_at = run.started_at or datetime.now(UTC)
            await session.commit()

        processed = set(str(item) for item in (run.result_json or {}).get("processed_ids", []))
        redis = get_redis()
        for hotspot_id in hotspot_ids:
            identifier = str(hotspot_id)
            if identifier in processed:
                continue
            hotspot = await session.get(TravelHotspot, hotspot_id)
            hotspot_name = hotspot.name if hotspot else None
            outcome = "failed"
            calls = 0
            error: dict[str, Any] | None = None
            if hotspot is None:
                error = {"hotspot_id": identifier, "code": "hotspot_not_found"}
            else:
                try:
                    outcome, calls = await enrich_hotspot_place(
                        session, redis, settings, hotspot
                    )
                except Exception as exc:
                    await session.rollback()
                    run = await session.get(HotspotPlaceEnrichmentRun, run_id)
                    if run is None:
                        return
                    error = {
                        "hotspot_id": identifier,
                        "code": "place_enrichment_failed",
                        "type": type(exc).__name__,
                    }
            processed.add(identifier)
            run.processed_count += 1
            run.actual_google_calls += calls
            if outcome == "published":
                run.published_count += 1
            elif outcome == "pending":
                run.pending_count += 1
            elif outcome == "unmatched":
                run.unmatched_count += 1
            else:
                run.failed_count += 1
            errors = list(run.error_json or [])
            if error:
                errors.append(error)
            run.error_json = errors[-100:]
            run.result_json = {"processed_ids": sorted(processed)}
            run.progress_json = {
                "hotspot_id": identifier,
                "hotspot_name": hotspot_name,
            }
            if run.processed_count >= run.total_count:
                run.status = "partial" if run.failed_count else "completed"
                run.completed_at = datetime.now(UTC)
                session.add(
                    AdminAuditLog(
                        actor_user_id=run.actor_user_id,
                        action="hotspot_place_enrichment_completed",
                        target=f"hotspot-place-enrichment:{run.id}",
                        metadata_json={
                            "status": run.status,
                            "processed": run.processed_count,
                            "published": run.published_count,
                            "pending": run.pending_count,
                            "unmatched": run.unmatched_count,
                            "failed": run.failed_count,
                            "google_calls": run.actual_google_calls,
                        },
                    )
                )
            await session.commit()


def run_hotspot_place_enrichment_chunk(run_id: str, hotspot_ids: list[str]) -> None:
    async def run_and_close_resources() -> None:
        try:
            await _run_chunk(UUID(run_id), [UUID(item) for item in hotspot_ids])
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close_resources())
