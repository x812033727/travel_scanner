"""The news queue's own worker (compose service ``news-worker``, profile ``news``).

One candidate is twenty-odd model calls and may run for up to an hour. In the general
worker it would hold the only process that also serves search and trip routing, so the
``news`` queue is deliberately absent from ``app.worker.QUEUE_NAMES``.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from uuid import UUID

from redis import Redis
from rq import Queue

from app.config import get_settings
from app.db import SessionFactory, engine
from app.news_automation.jobs import enqueue_candidate_once
from app.news_automation.pipeline import recover_stalled_candidates
from app.worker import worker_class

QUEUE_NAME = "news"
logger = logging.getLogger(__name__)


async def recover_interrupted() -> list[UUID]:
    """Fail and re-queue every candidate left in flight by the previous worker.

    This is the only news worker, and it has not taken a job yet, so no candidate can be
    running: one still in an in-flight status was cut off when the last worker stopped.
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
    connection = Redis.from_url(get_settings().redis_url)
    # with_scheduler moves Retry(interval=...) and enqueue_in jobs back onto this queue.
    worker_class()([Queue(QUEUE_NAME, connection=connection)], connection=connection).work(
        with_scheduler=True
    )


if __name__ == "__main__":
    main()
