from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from uuid import UUID

from redis import Redis
from rq import Queue, Retry

from app.config import get_settings
from app.db import SessionFactory, engine
from app.news_automation.jobs import enqueue_candidate_once, enqueue_source_scan
from app.news_automation.pipeline import orphaned_candidates, recover_stalled_candidates
from app.news_automation.scanner import claim_due_sources

logger = logging.getLogger(__name__)


async def tick() -> int:
    # Claimed sources are queued before anything else can fail: the claim has already
    # moved next_scan_at, so a scan dropped here would be skipped for a whole interval.
    async with SessionFactory() as session:
        source_ids = await claim_due_sources(session)
    for source_id in source_ids:
        await asyncio.to_thread(enqueue_source_scan, source_id)
    rerun: list[tuple[UUID, str]] = []
    try:
        async with SessionFactory() as session:
            recovered = await recover_stalled_candidates(session)
            orphaned = await orphaned_candidates(session)
        rerun = [
            *((candidate_id, "recovered") for candidate_id in recovered),
            *((candidate_id, "orphaned") for candidate_id in orphaned),
        ]
    except Exception:
        logger.exception("news candidate sweep failed; retrying next minute")
    for candidate_id, reason in rerun:
        await asyncio.to_thread(enqueue_candidate_once, candidate_id, reason)
    return len(source_ids)


async def main_async() -> None:
    settings = get_settings()
    connection = Redis.from_url(settings.redis_url)
    queue = Queue("news", connection=connection)
    try:
        while True:
            try:
                await tick()
            except Exception:
                # A database or Redis blip must not stop the hourly schedule; the
                # container restart that would follow also loses nothing but this minute.
                logger.exception("news scheduler tick failed")
            day = datetime.now(UTC).date().isoformat()
            cleanup_id = f"news-retention-{day}"
            if queue.fetch_job(cleanup_id) is None:
                queue.enqueue(
                    "app.news_automation.jobs.run_cleanup",
                    job_id=cleanup_id,
                    job_timeout=900,
                    result_ttl=86_400,
                    failure_ttl=604_800,
                    retry=Retry(max=2, interval=[60, 300]),
                )
            await asyncio.sleep(60)
    finally:
        connection.close()
        await engine.dispose()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
