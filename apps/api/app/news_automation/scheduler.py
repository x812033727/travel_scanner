from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from uuid import UUID

from redis import Redis
from rq import Queue, Retry

from app.config import get_settings
from app.db import SessionFactory, engine
from app.news_automation.jobs import enqueue_candidate_once, enqueue_source_scan
from app.news_automation.pipeline import orphaned_candidates, recover_stalled_candidates
from app.news_automation.scanner import claim_due_sources


async def tick() -> int:
    async with SessionFactory() as session:
        source_ids = await claim_due_sources(session)
        recovered = await recover_stalled_candidates(session)
        orphaned = await orphaned_candidates(session)
    for source_id in source_ids:
        await asyncio.to_thread(enqueue_source_scan, source_id)
    rerun: list[tuple[UUID, str]] = [
        *((candidate_id, "recovered") for candidate_id in recovered),
        *((candidate_id, "orphaned") for candidate_id in orphaned),
    ]
    for candidate_id, reason in rerun:
        await asyncio.to_thread(enqueue_candidate_once, candidate_id, reason)
    return len(source_ids)


async def main_async() -> None:
    settings = get_settings()
    connection = Redis.from_url(settings.redis_url)
    queue = Queue("news", connection=connection)
    try:
        while True:
            await tick()
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
