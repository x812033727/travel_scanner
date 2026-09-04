from __future__ import annotations

from typing import Any

from app.admin.service import load_runtime_settings
from app.db import SessionFactory
from app.hotspots.guides import backfill_guides_once
from app.hotspots.place_tasks import enqueue_place_enrichment_run
from app.hotspots.places import (
    automatic_refresh_allowed,
    create_system_refresh_run,
    due_refresh_targets,
    purge_expired_place_content,
)
from app.hotspots.service import collect_hotspots
from app.infra import get_redis
from app.restaurants.tasks import enqueue_next_automatic_scan, refresh_next_stale_identity


async def collect_once() -> dict[str, Any]:
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        report = await collect_hotspots(session, settings)
        purged = await purge_expired_place_content(session)
        place_report: dict[str, Any] = {"skipped": True, "reason": "disabled_or_unconfigured"}
        if settings.hotspot_place_enrichment_enabled and settings.google_maps_api_key:
            if await automatic_refresh_allowed(get_redis(), settings):
                targets = await due_refresh_targets(session, settings)
                run = await create_system_refresh_run(session, targets)
                if run is not None and run.status == "queued":
                    enqueue_place_enrichment_run(run.id, [item.id for item in targets])
                    place_report = {
                        "skipped": False,
                        "run_id": str(run.id),
                        "queued": len(targets),
                    }
                elif run is not None:
                    place_report = {"skipped": True, "reason": "already_queued"}
                else:
                    place_report = {"skipped": True, "reason": "nothing_due"}
            else:
                place_report = {"skipped": True, "reason": "usage_threshold_or_unavailable"}
        report["place_enrichment"] = place_report
        report["place_cache_purged"] = purged
        report["restaurant_scan"] = await enqueue_next_automatic_scan(session, settings)
        report["restaurant_place_identity"] = await refresh_next_stale_identity(session, settings)
        report["guide_backfill"] = await backfill_guides_once(session, settings, get_redis())
        return report
