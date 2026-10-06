from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID

from botocore.exceptions import BotoCoreError, ClientError
from pydantic import ValidationError
from redis import Redis as SyncRedis
from rq import Queue, Retry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.news_automation import judge
from app.news_automation.assets import object_storage
from app.news_automation.fetch import RedisHostRateLimiter, SafeNewsFetcher
from app.news_automation.models import NewsAsset, NewsCandidate, NewsEvidence
from app.news_automation.pipeline import process_candidate
from app.news_automation.scanner import scan_source

# How long a candidate waiting for a Claude subscription account sleeps between tries, and
# the review judge before it asks about a hold again.
PAUSE_MINUTES = 30
# What a candidate's run returns when the story may now rest in a hold the review judge
# answers. "skipped" is one of them: the run that put it there may have failed to queue the
# judge, or the judge was switched on since, and a later job for the candidate finds it.
JUDGED_RESULTS = frozenset({"manual_review", "needs_redraft", "skipped"})

logger = logging.getLogger(__name__)


def _queue() -> tuple[SyncRedis, Queue]:
    connection = SyncRedis.from_url(get_settings().redis_url)
    return connection, Queue("news", connection=connection)


def enqueue_source_scan(source_id: UUID) -> str:
    connection, queue = _queue()
    try:
        slot = int(datetime.now(UTC).timestamp() // 60)
        job = queue.enqueue(
            "app.news_automation.jobs.run_source_scan",
            str(source_id),
            job_id=f"news-source-{source_id}-{slot}",
            job_timeout=900,
            result_ttl=86_400,
            failure_ttl=604_800,
            # SafeNewsFetcher already performs the policy maximum of three network
            # attempts. The next hourly due scan is the recovery boundary.
        )
        return str(job.id)
    finally:
        connection.close()


def enqueue_candidate(candidate_id: UUID, retry_count: int = 0) -> str:
    connection, queue = _queue()
    try:
        job = queue.enqueue(
            "app.news_automation.jobs.run_candidate",
            str(candidate_id),
            job_id=f"news-candidate-{candidate_id}-{retry_count}",
            job_timeout=3_600,
            result_ttl=86_400,
            failure_ttl=604_800,
            # Two retry attempts is the model-stage ceiling in the product policy.
            retry=Retry(max=2, interval=[60, 300]),
        )
        return str(job.id)
    finally:
        connection.close()


def enqueue_candidate_once(candidate_id: UUID, reason: str) -> str | None:
    """Queue one run per candidate, reason and hour; the scheduler calls this every minute.

    RQ pushes a re-used job id onto the queue a second time instead of refusing it, so an
    existing job is checked first.
    """

    connection, queue = _queue()
    try:
        slot = int(datetime.now(UTC).timestamp() // 3600)
        job_id = f"news-candidate-{candidate_id}-{reason}-{slot}"
        if queue.fetch_job(job_id) is not None:
            return None
        job = queue.enqueue(
            "app.news_automation.jobs.run_candidate",
            str(candidate_id),
            job_id=job_id,
            job_timeout=3_600,
            result_ttl=86_400,
            failure_ttl=604_800,
        )
        return str(job.id)
    finally:
        connection.close()


def enqueue_judge_once(
    candidate_id: UUID, retry_count: int, hold: str, *, tag: str = ""
) -> str | None:
    """Queue the review judge for one hold of a candidate, once.

    A hold is the candidate's ``error_code`` at one ``retry_count``: every rerun raises the
    count, so whatever stops the story next gets a job of its own. ``tag`` asks for the same
    hold again on purpose (the backlog command, a worker restart), because the first job's
    id stays in RQ after it ran or was cut off. No ``Retry``: the judge counts its own
    failed calls, and ``run_judge`` queues the next try when there is to be one.
    """

    connection, queue = _queue()
    try:
        job_id = f"news-judge-{candidate_id}-{retry_count}-{hold}"
        if tag:
            job_id = f"{job_id}-{tag}"
        if queue.fetch_job(job_id) is not None:
            return None
        job = queue.enqueue(
            "app.news_automation.jobs.run_judge",
            str(candidate_id),
            job_id=job_id,
            # One question to the model, and for a finished article the evidence pages
            # fetched again before publication. The limit is the judge's, which says what
            # that may take; a candidate's run has an hour.
            job_timeout=judge.JOB_TIMEOUT_SECONDS,
            result_ttl=86_400,
            failure_ttl=604_800,
        )
        return str(job.id)
    finally:
        connection.close()


async def _enqueue_candidate_async(candidate_id: UUID) -> None:
    await asyncio.to_thread(enqueue_candidate, candidate_id)


async def _offer_to_judge(session: AsyncSession, candidate_id: UUID) -> None:
    """Queue the review judge if the candidate's run left it in a hold the judge answers.

    The run is over and saved, so nothing here may fail the job: RQ would run the candidate
    again for a result it already has. A hold missed here waits in the owner's list like
    any other, and ``backfill_cli --judge-holds`` or ``--judge-redrafts`` sends it later.
    """

    try:
        # Read again: the judge goes by the stored row, not by what this session last held.
        candidate = await session.get(NewsCandidate, candidate_id, populate_existing=True)
        if candidate is None or not await judge.wanted(session, candidate):
            return
        enqueue_judge_once(candidate.id, candidate.retry_count, cast(str, candidate.error_code))
    except Exception:
        logger.exception("news candidate %s could not be queued for the review judge", candidate_id)


async def _close_resources() -> None:
    try:
        await get_redis().aclose()
    finally:
        get_redis.cache_clear()
        await engine.dispose()


def run_source_scan(source_id: str) -> None:
    async def run() -> None:
        try:
            async with SessionFactory() as session:
                fetcher = SafeNewsFetcher(rate_limiter=RedisHostRateLimiter(get_redis()))
                try:
                    await scan_source(
                        session,
                        UUID(source_id),
                        _enqueue_candidate_async,
                        fetcher=fetcher,
                    )
                finally:
                    await fetcher.close()
        finally:
            await _close_resources()

    asyncio.run(run())


def run_candidate(candidate_id: str) -> None:
    async def run() -> None:
        try:
            async with SessionFactory() as session:
                # Model keys and ids live in the admin AI settings (provider_configs) as
                # well as the environment; the hotspot AI tasks read them the same way.
                environment = await load_runtime_settings(session)
                try:
                    result = await process_candidate(
                        session, get_redis(), environment, UUID(candidate_id)
                    )
                except (ValidationError, ValueError) as error:
                    # A model reply that failed validation after its repair round (or came
                    # back incomplete) fails the same way on a rerun, and RQ's retry would
                    # rerun every stage. The candidate is already marked failed with the
                    # reason, and an editor can run it again from /admin/news.
                    logger.warning(
                        "news candidate %s failed without retry: %s",
                        candidate_id,
                        type(error).__name__,
                    )
                    return
                # Only a full concurrency slot comes back in a minute. "disabled" waits for
                # the orphan sweep once the switch is on again; "skipped" means another
                # job already owns or finished the candidate. "jev_paused" needs no job
                # either: the orphan sweep runs it once the UTC day's Jev budget resets.
                if result == "paused":
                    # Every subscription account is full: try again once a window has had
                    # time to move, instead of spending MiniMax on it.
                    connection, queue = _queue()
                    try:
                        paused_slot = int(datetime.now(UTC).timestamp() // 1800)
                        queue.enqueue_in(
                            timedelta(minutes=PAUSE_MINUTES),
                            "app.news_automation.jobs.run_candidate",
                            candidate_id,
                            job_id=f"news-candidate-{candidate_id}-paused-{paused_slot}",
                            job_timeout=3_600,
                        )
                    finally:
                        connection.close()
                if result == "deferred":
                    connection, queue = _queue()
                    try:
                        deferred_slot = int(datetime.now(UTC).timestamp() // 60)
                        queue.enqueue_in(
                            timedelta(minutes=1),
                            "app.news_automation.jobs.run_candidate",
                            candidate_id,
                            job_id=(f"news-candidate-{candidate_id}-deferred-{deferred_slot}"),
                            job_timeout=3_600,
                        )
                    finally:
                        connection.close()
                if result in JUDGED_RESULTS:
                    await _offer_to_judge(session, UUID(candidate_id))
        finally:
            await _close_resources()

    asyncio.run(run())


def run_judge(candidate_id: str) -> None:
    """Put one candidate's hold to the review judge and queue what its answer calls for."""

    async def run() -> None:
        try:
            async with SessionFactory() as session:
                # The judge's vendor key and model ids are admin AI settings too.
                environment = await load_runtime_settings(session)
                outcome = await judge.judge_candidate(
                    session, get_redis(), environment, UUID(candidate_id)
                )
            if outcome.action == "requeue":
                # The verdict sent the story back to the pipeline: an approved draft goes on
                # to translation and publication; a rewrite, or a story the judge found not
                # to be a duplicate, runs again.
                enqueue_candidate(UUID(candidate_id), retry_count=outcome.retry_count or 0)
            if outcome.action == "retry_later":
                # No verdict yet: every subscription account is full, or the call failed and
                # the judge has not given up on it. The same hold is asked again later.
                connection, queue = _queue()
                try:
                    later_slot = int(datetime.now(UTC).timestamp() // 1800)
                    queue.enqueue_in(
                        timedelta(minutes=PAUSE_MINUTES),
                        "app.news_automation.jobs.run_judge",
                        candidate_id,
                        job_id=(
                            f"news-judge-{candidate_id}-{outcome.retry_count}"
                            f"-{outcome.hold}-later-{later_slot}"
                        ),
                        job_timeout=judge.JOB_TIMEOUT_SECONDS,
                    )
                finally:
                    connection.close()
        finally:
            await _close_resources()

    asyncio.run(run())


async def cleanup_retention() -> dict[str, int]:
    cutoff = datetime.now(UTC) - timedelta(days=90)
    deleted_assets = 0
    cleared_excerpts = 0
    async with SessionFactory() as session:
        assets = list(
            await session.scalars(
                select(NewsAsset)
                .join(NewsCandidate, NewsCandidate.id == NewsAsset.candidate_id)
                .where(
                    NewsAsset.is_public.is_(False),
                    NewsAsset.deleted_at.is_(None),
                    NewsAsset.created_at < cutoff,
                    NewsCandidate.status != "published",
                )
            )
        )
        # Built only when an asset actually lives in S3: on a host without object
        # storage the old unconditional client failed this job every day.
        client = None
        for asset in assets:
            if asset.content is not None:
                asset.content = None
            else:
                client = client or object_storage()
                if client is None:
                    continue
                try:
                    await asyncio.to_thread(
                        client.delete_object,
                        Bucket=get_settings().community_s3_bucket,
                        Key=asset.storage_key,
                    )
                except (BotoCoreError, ClientError):
                    continue
            asset.deleted_at = datetime.now(UTC)
            deleted_assets += 1
        evidence = await session.scalars(
            select(NewsEvidence).where(
                NewsEvidence.retrieved_at < cutoff,
                NewsEvidence.excerpt != "[retention-expired]",
            )
        )
        for row in evidence:
            row.excerpt = "[retention-expired]"
            cleared_excerpts += 1
        await session.commit()
    return {"deleted_assets": deleted_assets, "cleared_excerpts": cleared_excerpts}


def run_cleanup() -> None:
    async def run() -> None:
        try:
            await cleanup_retention()
        finally:
            await _close_resources()

    asyncio.run(run())
