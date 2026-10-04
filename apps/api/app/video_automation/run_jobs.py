"""Durable video writing operations, on their own RQ worker.

The database owns dispatch and results; Redis only schedules work. Only queued rows may
dispatch. Losing a dispatched process leaves an uncertain receipt, never an automatic
model retry. A caller may reconnect with its persisted request key or poll its receipt.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
from datetime import UTC, timedelta
from typing import Any, cast
from uuid import UUID, uuid4

from redis import Redis
from redis.exceptions import RedisError
from rq import Queue
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import SessionFactory, engine
from app.infra import enforce_named_rate_limit, get_redis
from app.models import VideoToolToken
from app.video_automation import settings as service
from app.video_automation.ai import NO_MODEL_CALL_ERRORS, prepare_stage, run_stage
from app.video_automation.errors import StageFailed
from app.video_automation.models import VideoStageJob, utcnow
from app.video_automation.schemas import StageJobIn, StageJobOut, StageRunIn, StageRunOut

QUEUE_NAME = "video-ai"
JOB_TIMEOUT_SECONDS = 1_200
INTERRUPTED_AFTER_SECONDS = JOB_TIMEOUT_SECONDS + 60
RUNS_PER_HOUR = 120
TERMINAL_STATUSES = {"succeeded", "failed", "uncertain"}


def _hash(value: object) -> str:
    try:
        canonical = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        )
    except (TypeError, ValueError) as error:
        raise StageFailed(
            422, "video_ai_job_input_invalid", "工作輸入必須是有限的 JSON 值"
        ) from error
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def request_hash(request: StageRunIn) -> str:
    # Pydantic's JSON mode silently turns NaN into null. Reject it before conversion so
    # two different inputs cannot acquire the same receipt identity.
    return _hash(request.model_dump())


def _view(job: VideoStageJob) -> StageJobOut:
    return StageJobOut(
        id=job.id,
        request_key=job.request_key,
        request_hash=job.request_hash,
        input_hash=job.input_hash,
        provider=cast(Any, job.provider),
        model=job.model,
        status=cast(Any, job.status),
        result=StageRunOut.model_validate(job.result_json) if job.result_json is not None else None,
        error_code=job.error_code,
        error_detail=job.error_detail,
        error_status=job.error_status,
        retry_after=job.retry_after,
    )


def _schedule(job_id: UUID, *, queued: bool) -> str | None:
    """Inspect or enqueue a non-dispatched operation, under a Redis scheduling lock."""
    connection = Redis.from_url(get_settings().redis_url, socket_timeout=5)
    try:
        queue = Queue(QUEUE_NAME, connection=connection)
        rq_id = f"video-stage-{job_id}"
        with connection.lock(f"video-stage-schedule:{job_id}", timeout=15, blocking_timeout=2):
            existing = queue.fetch_job(rq_id)
            if existing is not None:
                status = existing.get_status(refresh=True)
                return status.value if status is not None else None
            if queued:
                queue.enqueue(
                    "app.video_automation.run_jobs.run_job",
                    str(job_id),
                    job_id=rq_id,
                    job_timeout=JOB_TIMEOUT_SECONDS,
                    result_ttl=86_400,
                    failure_ttl=604_800,
                    # No RQ Retry: an interrupted upstream call may already have run.
                )
                return "queued"
            return None
    finally:
        connection.close()


async def _reconcile(session: AsyncSession, job: VideoStageJob) -> StageJobOut:
    if job.status in TERMINAL_STATUSES:
        return _view(job)
    try:
        state = await asyncio.to_thread(_schedule, job.id, queued=job.status == "queued")
    except RedisError as error:
        raise StageFailed(
            503,
            "video_ai_job_queue_unavailable",
            "影片工作佇列暫時無法連線，請繼續查詢同一份工作",
            "30",
        ) from error
    started = job.started_at
    if started is not None and started.tzinfo is None:
        started = started.replace(tzinfo=UTC)
    expired = started is not None and utcnow() > started + timedelta(
        seconds=INTERRUPTED_AFTER_SECONDS
    )
    if state in {"failed", "stopped", "canceled", "finished"} or (
        job.status == "running" and (state is None or expired)
    ):
        status = "uncertain" if job.dispatched_at is not None else "failed"
        code = (
            "video_ai_job_uncertain"
            if job.dispatched_at is not None
            else "video_ai_job_interrupted_before_dispatch"
        )
        detail = (
            "模型請求已送出但沒有保存結果，請由站主核對；不會自動重跑"
            if job.dispatched_at is not None
            else "工作在送出模型請求前中斷，沒有執行模型"
        )
        # The worker can finish while Redis is being inspected. Do not overwrite a
        # concurrently committed exact result with a stale interruption verdict.
        await session.execute(
            update(VideoStageJob)
            .where(
                VideoStageJob.id == job.id,
                VideoStageJob.status == job.status,
                VideoStageJob.result_json.is_(None),
                VideoStageJob.dispatched_at.is_(None)
                if job.dispatched_at is None
                else VideoStageJob.dispatched_at == job.dispatched_at,
            )
            .values(
                status=status,
                error_code=code,
                error_detail=detail,
                error_status=409,
                completed_at=utcnow(),
            )
        )
        await session.commit()
        await session.refresh(job)
    return _view(job)


async def submit_job(session: AsyncSession, request: StageJobIn, token_id: UUID) -> StageJobOut:
    body = request.run_request()
    source_hash = request_hash(body)

    async def existing() -> VideoStageJob | None:
        with session.no_autoflush:
            found = await session.scalar(
                select(VideoStageJob).where(
                    VideoStageJob.token_id == token_id,
                    VideoStageJob.request_key == request.request_key,
                )
            )
        if found is not None and found.request_hash != source_hash:
            raise StageFailed(
                409, "video_ai_job_input_changed", "相同工作識別碼不能套用到不同的影片或輸入"
            )
        return found

    found = await existing()
    if found is not None:
        # A retained result is accessible even after the model or budget changes.
        return await _reconcile(session, found)
    # Serialize new submits per credential, including concurrent submits of one key.
    # The unique constraint remains the database boundary if a caller ignores this lock.
    with session.no_autoflush:
        token = await session.scalar(
            select(VideoToolToken).where(VideoToolToken.id == token_id).with_for_update()
        )
    if token is None or token.revoked_at is not None:
        raise StageFailed(401, "video_tool_token_invalid", "影片工具權杖無效或已撤銷")
    found = await existing()
    if found is not None:
        await session.commit()
        return await _reconcile(session, found)
    await enforce_named_rate_limit(
        "video_ai_run", str(token_id), limit=RUNS_PER_HOUR, window_seconds=3600
    )
    row = await service.settings_row(session)
    runtime = await load_runtime_settings(session)
    provider, model, _, _ = await prepare_stage(session, runtime, row, body)
    await service.remember_prompt(session, body)
    job = VideoStageJob(
        id=uuid4(),
        token_id=token_id,
        request_key=request.request_key,
        request_hash=source_hash,
        input_hash=_hash(
            {"request": body.model_dump(mode="json"), "provider": provider, "model": model}
        ),
        request_json=body.model_dump(mode="json"),
        provider=provider,
        model=model,
        status="queued",
        created_at=utcnow(),
    )
    session.add(job)
    # Commit before enqueue: a disconnected POST leaves a safe queued receipt that the
    # same request key can recover and enqueue without a second model operation.
    await session.commit()
    return await _reconcile(session, job)


async def poll_job(
    session: AsyncSession, job_id: UUID, token_id: UUID, input_hash: str
) -> StageJobOut:
    with session.no_autoflush:
        job = await session.scalar(
            select(VideoStageJob).where(
                VideoStageJob.id == job_id, VideoStageJob.token_id == token_id
            )
        )
    if job is None:
        raise StageFailed(404, "video_ai_job_not_found", "找不到這個權杖的影片工作")
    if job.input_hash != input_hash:
        raise StageFailed(409, "video_ai_job_input_changed", "工作輸入雜湊不符，不能採用這份結果")
    return await _reconcile(session, job)


async def _mark_error(job_id: UUID, error: Exception) -> None:
    async with SessionFactory() as session:
        job = await session.get(VideoStageJob, job_id)
        if job is None or job.status != "running":
            return
        known = error if isinstance(error, StageFailed) else None
        no_call = job.dispatched_at is None or (
            known is not None and known.code in NO_MODEL_CALL_ERRORS
        )
        job.status = "failed" if no_call else "uncertain"
        job.error_code = (
            known.code
            if known is not None
            else "video_ai_job_interrupted_before_dispatch"
            if no_call
            else "video_ai_job_uncertain"
        )
        job.error_detail = (
            known.detail
            if known is not None
            else "工作在送出模型請求前中斷，沒有執行模型"
            if no_call
            else "模型工作中斷，無法確定模型執行結果；不會自動重跑"
        )
        job.error_status = known.status if known is not None else 409
        job.retry_after = known.retry_after if known is not None else None
        job.completed_at = utcnow()
        await session.commit()


async def _run(job_id: UUID) -> None:
    try:
        async with SessionFactory() as session:
            claimed = await session.scalar(
                update(VideoStageJob)
                .where(VideoStageJob.id == job_id, VideoStageJob.status == "queued")
                .values(status="running", started_at=utcnow())
                .returning(VideoStageJob.id)
            )
            await session.commit()
            if claimed is None:
                return
            job = await session.get(VideoStageJob, job_id)
            assert job is not None
            token = await session.get(VideoToolToken, job.token_id) if job.token_id else None
            if token is None or token.revoked_at is not None:
                raise StageFailed(401, "video_tool_token_invalid", "影片工具權杖無效或已撤銷")
            row = await service.settings_row(session)
            runtime = await load_runtime_settings(session)
            await run_stage(
                session,
                runtime,
                row,
                StageRunIn.model_validate(job.request_json),
                token.id,
                job=job,
            )
    except Exception as error:
        # Unexpected failures are kept as uncertain; RQ is never given a retry policy.
        await _mark_error(job_id, error)
        raise


def run_job(job_id: str) -> None:
    async def run_and_close() -> None:
        try:
            await _run(UUID(job_id))
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close())


def main() -> None:
    from app.worker import configure_logging, worker_class

    configure_logging()
    asyncio.run(recover_pending())
    connection = Redis.from_url(get_settings().redis_url)
    try:
        worker_class()([Queue(QUEUE_NAME, connection=connection)], connection=connection).work()
    finally:
        connection.close()


async def recover_pending() -> int:
    """Close the database-commit/Redis-enqueue gap after a worker restart.

    Only queued rows are scheduled. A running or uncertain row is never redispatched,
    even if its Redis job disappeared while the host was down.
    """
    try:
        async with SessionFactory() as session:
            ids = list(
                await session.scalars(
                    select(VideoStageJob.id).where(VideoStageJob.status == "queued")
                )
            )
        for job_id in ids:
            await asyncio.to_thread(_schedule, job_id, queued=True)
        return len(ids)
    finally:
        # No pooled database connection may cross RQ's fork boundary.
        await engine.dispose()


if __name__ == "__main__":
    main()
