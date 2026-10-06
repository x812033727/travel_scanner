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
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID

from redis import Redis
from rq import Queue, Worker
from rq.worker_pool import WorkerPool

from app.config import get_settings
from app.db import SessionFactory, engine
from app.news_automation import judge
from app.news_automation.jobs import enqueue_candidate_once, enqueue_judge_once
from app.news_automation.models import NewsCandidate
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


async def recover_interrupted_judging() -> list[tuple[UUID, int, str]]:
    """Fail the review judge's runs left ``running`` and return the holds to ask it again.

    A judge job cut off by a restart leaves its run running and its hold unanswered. The
    candidate rests in ``manual_review`` or ``needs_redraft``, which ``recover_interrupted``
    does not look at, and no sweep queues the judge: without this the story would wait in
    the owner's list as if the judge had never been asked. Each item is what
    ``enqueue_judge_once`` takes: the candidate, its retry count and the hold. Where the
    judge would not answer now (a person acted meanwhile, a switch is off) the run is failed
    all the same and the hold is left out. Like ``recover_interrupted`` this runs before the
    pool starts, when no judge job can be running.
    """
    try:
        async with SessionFactory() as session:
            interrupted = await judge.fail_interrupted_runs(session)
            await session.commit()
            again: list[tuple[UUID, int, str]] = []
            for candidate_id in interrupted:
                candidate = await session.get(NewsCandidate, candidate_id)
                if candidate is not None and await judge.wanted(session, candidate):
                    again.append(
                        (candidate.id, candidate.retry_count, cast(str, candidate.error_code))
                    )
            return again
    finally:
        await engine.dispose()


def main() -> None:
    for candidate_id in asyncio.run(recover_interrupted()):
        enqueue_candidate_once(candidate_id, "restarted")
        logger.info("news candidate %s re-queued after a worker restart", candidate_id)
    # The cut-off job's id is still in RQ, so the hold would count as queued already; the
    # start time makes this a job of its own.
    restart = f"restarted-{int(datetime.now(UTC).timestamp())}"
    for candidate_id, retry_count, hold in asyncio.run(recover_interrupted_judging()):
        enqueue_judge_once(candidate_id, retry_count, hold, tag=restart)
        logger.info("news candidate %s goes back to the review judge after a restart", candidate_id)
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
