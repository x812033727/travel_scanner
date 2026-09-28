"""The news queue's own workers (compose service ``news-worker``, profile ``news``).

One candidate is twenty-odd model calls and may run for up to an hour. In the general
worker it would hold the only process that also serves search and trip routing, so the
``news`` queue is deliberately absent from ``app.worker.QUEUE_NAMES``.

The container runs a pool of ``news_worker_processes`` RQ workers (2026-09-28). With one
process, a single candidate at a time was the limit, three to five an hour, and every
source scan waited behind it. The admin's concurrency settings still decide how many
candidates run at once; a worker without a free slot defers its candidate for a minute.
"""

from __future__ import annotations

import asyncio
import logging
import os
from datetime import timedelta
from uuid import UUID

from redis import Redis
from rq import Queue, Worker
from rq.worker_pool import WorkerPool

from app.config import get_settings
from app.db import SessionFactory, engine
from app.news_automation.jobs import enqueue_candidate_once
from app.news_automation.pipeline import recover_stalled_candidates
from app.worker import worker_class

QUEUE_NAME = "news"
logger = logging.getLogger(__name__)


async def recover_interrupted() -> list[UUID]:
    """Fail and re-queue every candidate left in flight by the previous workers.

    This runs once, before the pool starts, and every news worker lives in this one
    container, so no candidate can be running: one still in an in-flight status was cut
    off when the last container stopped. Keep it that way: a second news-worker container
    would have its candidates failed each time this one restarts.
    Every deploy restarts the worker (on 2026-09-24 four did), and waiting for the
    scheduler's 70-minute rule left two such candidates holding both concurrency slots
    while every other candidate deferred once a minute.
    """
    try:
        async with SessionFactory() as session:
            return await recover_stalled_candidates(
                session, older_than=timedelta(0), limit=100
            )
    finally:
        # The worker forks a process per job; no pooled connection may cross the fork.
        await engine.dispose()


def main() -> None:
    for candidate_id in asyncio.run(recover_interrupted()):
        enqueue_candidate_once(candidate_id, "restarted")
        logger.info("news candidate %s re-queued after a worker restart", candidate_id)
    settings = get_settings()
    connection = Redis.from_url(settings.redis_url)
    size = pool_size(settings.news_worker_processes)
    if size == 1:
        # with_scheduler moves Retry(interval=...) and enqueue_in jobs back onto this queue.
        worker_class()([Queue(QUEUE_NAME, connection=connection)], connection=connection).work(
            with_scheduler=True
        )
        return
    # Every pooled worker runs with_scheduler too; RQ's scheduler lock lets one of them do it.
    WorkerPool([QUEUE_NAME], connection=connection, num_workers=size, worker_class=Worker).start()


def pool_size(configured: int, os_name: str = os.name) -> int:
    """Workers to start: the setting, or one where fork is unavailable (Windows dev)."""
    return 1 if os_name == "nt" else configured


if __name__ == "__main__":
    main()
