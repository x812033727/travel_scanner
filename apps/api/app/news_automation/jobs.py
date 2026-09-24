from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID

from botocore.exceptions import BotoCoreError, ClientError
from pydantic import ValidationError
from redis import Redis as SyncRedis
from rq import Queue, Retry
from sqlalchemy import select

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import get_redis
from app.news_automation.assets import object_storage
from app.news_automation.fetch import RedisHostRateLimiter, SafeNewsFetcher
from app.news_automation.models import NewsAsset, NewsCandidate, NewsEvidence
from app.news_automation.pipeline import process_candidate
from app.news_automation.scanner import scan_source

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


async def _enqueue_candidate_async(candidate_id: UUID) -> None:
    await asyncio.to_thread(enqueue_candidate, candidate_id)


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
                # job already owns or finished the candidate.
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
