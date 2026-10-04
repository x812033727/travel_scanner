"""Real transactions for durable replies, duplicate dispatch and disconnected callers."""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import nullcontext
from datetime import timedelta
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from fakeredis import FakeRedis
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis import Redis
from redis.exceptions import RedisError
from rq import Queue
from sqlalchemy import Table, delete, event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.db import SessionFactory, engine, get_session
from app.models import VideoProject, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api, ai, run_jobs
from app.video_automation import settings as automation_settings
from app.video_automation.errors import StageFailed
from app.video_automation.models import VideoAiRun, VideoAutomationSettings, VideoStageJob, utcnow
from app.video_automation.schemas import StageJobIn, StageRunOut, UsageView
from app.video_speech.admin_api import video_tool

EXACT = '\n{"title":"同一份撰稿", "segments": []}\n'


def usage() -> UsageView:
    return UsageView(tokens=0, token_budget=1000, drafts=0, draft_budget=8, calls=0, failed_calls=0)


def request(**changes: Any) -> StageJobIn:
    return StageJobIn.model_validate(
        {
            "request_key": str(uuid4()),
            "stage": "writer",
            "slug": "durable-writer",
            "instructions": "Write the approved brief.",
            "payload": {"brief": "source", "round": 1},
            **changes,
        }
    )


@pytest_asyncio.fixture
async def store(tmp_path, monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[Any]:
    local = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'stages.sqlite'}")
    async with local.begin() as connection:
        for table in (
            VideoToolToken.__table__,
            VideoProject.__table__,
            VideoAiRun.__table__,
            VideoStageJob.__table__,
        ):
            await connection.run_sync(cast(Table, table).create)
    factory = async_sessionmaker(local, expire_on_commit=False)
    monkeypatch.setattr(run_jobs, "SessionFactory", factory)
    monkeypatch.setattr(
        run_jobs, "_schedule", lambda _id, *, queued: "queued" if queued else "started"
    )
    monkeypatch.setattr(run_jobs, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(run_jobs, "load_runtime_settings", AsyncMock(return_value=Settings()))
    monkeypatch.setattr(
        automation_settings,
        "settings_row",
        AsyncMock(return_value=VideoAutomationSettings(enabled=True)),
    )
    monkeypatch.setattr(automation_settings, "remember_prompt", AsyncMock())
    prepared = AsyncMock(return_value=("anthropic", "writer-v1", usage(), False))
    monkeypatch.setattr(run_jobs, "prepare_stage", prepared)
    monkeypatch.setattr(ai, "prepare_stage", prepared)
    monkeypatch.setattr(
        ai, "_on_api_key", AsyncMock(return_value=(EXACT, "writer-v1", {"output_tokens": 7}))
    )
    try:
        yield factory
    finally:
        await local.dispose()


async def credential(store: Any) -> VideoToolToken:
    async with store() as session:
        token = VideoToolToken(
            id=uuid4(), name="test", token_hash=uuid4().hex, token_prefix="mkv_test"
        )
        session.add(token)
        await session.commit()
        return token


@pytest.mark.asyncio
async def test_disconnected_submit_recovers_same_receipt_without_quota_or_model_checks(
    store: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    token = await credential(store)
    body = request()
    # The receipt commits before Redis; an HTTP interruption at enqueue is recoverable.
    monkeypatch.setattr(
        run_jobs,
        "_schedule",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("disconnect")),
    )
    async with store() as session:
        with pytest.raises(RuntimeError, match="disconnect"):
            await run_jobs.submit_job(session, body, token.id)
    monkeypatch.setattr(run_jobs, "_schedule", lambda *_args, **_kwargs: "queued")
    monkeypatch.setattr(run_jobs, "prepare_stage", AsyncMock(side_effect=AssertionError("quota")))
    monkeypatch.setattr(
        run_jobs, "load_runtime_settings", AsyncMock(side_effect=AssertionError("settings"))
    )
    monkeypatch.setattr(
        run_jobs, "enforce_named_rate_limit", AsyncMock(side_effect=AssertionError("rate"))
    )
    async with store() as session:
        receipt = await run_jobs.submit_job(session, body, token.id)
        rows = list(await session.scalars(select(VideoStageJob)))
    assert receipt.status == "queued" and len(rows) == 1 and rows[0].id == receipt.id
    monkeypatch.setattr(run_jobs, "load_runtime_settings", AsyncMock(return_value=Settings()))
    await run_jobs._run(receipt.id)
    monkeypatch.setattr(
        run_jobs, "load_runtime_settings", AsyncMock(side_effect=AssertionError("settings"))
    )
    async with store() as session:
        completed = await run_jobs.submit_job(session, body, token.id)
    assert completed.status == "succeeded" and completed.result and completed.result.text == EXACT


@pytest.mark.asyncio
async def test_long_writer_continues_after_caller_disconnect_and_duplicate_rq_job(
    store: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    entered, finish = asyncio.Event(), asyncio.Event()
    calls = 0

    async def long_writer(*_args: object, **kwargs: object) -> tuple[str, str, dict[str, int]]:
        nonlocal calls
        assert kwargs["timeout_seconds"] == 960.0
        calls += 1
        entered.set()
        await finish.wait()
        return EXACT, "writer-v1", {"output_tokens": 7}

    monkeypatch.setattr(ai, "_on_api_key", long_writer)
    monkeypatch.setattr(ai, "time", SimpleNamespace(monotonic=iter([0.0, 642.0]).__next__))
    running = asyncio.create_task(run_jobs._run(receipt.id))
    await entered.wait()
    # An ordinary HTTP deadline only ends the caller's wait; the RQ execution persists.
    async with store() as session:
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(asyncio.shield(running), timeout=0.001)
        poll = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert poll.status == "running" and poll.result is None
    await run_jobs._run(receipt.id)
    assert calls == 1
    finish.set()
    await running
    async with store() as session:
        poll = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
        records = list(await session.scalars(select(VideoAiRun)))
    assert calls == 1 and poll.result and poll.result.text == EXACT
    assert len(records) == 1 and records[0].output_tokens == 7
    assert records[0].duration_ms == 642_000, "completion exceeds the ordinary 295-second relay"
    assert poll.result.usage.calls == 1


@pytest.mark.asyncio
async def test_exact_reply_and_usage_share_the_completion_commit(store: Any) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    witnessed = []

    def before_commit(session: Any) -> None:
        runs = [row for row in session.new if isinstance(row, VideoAiRun)]
        if runs:
            jobs = [row for row in session.dirty if isinstance(row, VideoStageJob)]
            witnessed.append((len(runs), jobs[0].status, jobs[0].result_json["text"]))

    event.listen(AsyncSession.sync_session_class, "before_commit", before_commit)
    try:
        await run_jobs._run(receipt.id)
    finally:
        event.remove(AsyncSession.sync_session_class, "before_commit", before_commit)
    assert witnessed == [(1, "succeeded", EXACT)]


@pytest.mark.asyncio
@pytest.mark.parametrize("failure_kind", ["network", "invalid", "unexpected"])
async def test_failure_after_dispatch_is_uncertain_and_cannot_retry(
    store: Any, monkeypatch, failure_kind: str
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    error = {
        "unexpected": RuntimeError("crash"),
        "network": StageFailed(502, "video_ai_upstream_unreachable", "connection lost"),
        "invalid": StageFailed(502, "video_ai_output_invalid", "invalid reply"),
    }[failure_kind]
    upstream = AsyncMock(side_effect=error)
    monkeypatch.setattr(ai, "_on_api_key", upstream)
    with pytest.raises(type(error)):
        await run_jobs._run(receipt.id)
    async with store() as session:
        result = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert result.status == "uncertain" and result.result is None
    await run_jobs._run(receipt.id)
    assert upstream.await_count == 1


@pytest.mark.asyncio
async def test_late_exact_reply_can_resolve_uncertain_without_stale_error_fields(
    store: Any, monkeypatch
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    entered, finish = asyncio.Event(), asyncio.Event()

    async def upstream(*_args: object, **_kwargs: object) -> tuple[str, str, dict[str, int]]:
        entered.set()
        await finish.wait()
        return EXACT, "writer-v1", {"output_tokens": 7}

    monkeypatch.setattr(ai, "_on_api_key", upstream)
    running = asyncio.create_task(run_jobs._run(receipt.id))
    await entered.wait()
    monkeypatch.setattr(run_jobs, "_schedule", lambda *_args, **_kwargs: None)
    async with store() as session:
        result = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert result.status == "uncertain" and result.error_code
    finish.set()
    await running
    async with store() as session:
        result = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert result.status == "succeeded" and result.result and result.result.text == EXACT
    assert (
        result.error_code
        is result.error_detail
        is result.error_status
        is result.retry_after
        is None
    )


@pytest.mark.asyncio
async def test_refusal_before_dispatch_is_definite_failed_and_does_not_call_model(
    store: Any, monkeypatch
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    monkeypatch.setattr(
        ai,
        "prepare_stage",
        AsyncMock(side_effect=StageFailed(429, "video_ai_budget_exhausted", "budget")),
    )
    with pytest.raises(StageFailed):
        await run_jobs._run(receipt.id)
    async with store() as session:
        result = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
        row = await session.get(VideoStageJob, receipt.id)
    assert result.status == "failed" and result.error_status == 429
    assert row.dispatched_at is None
    assert ai._on_api_key.await_count == 0  # type: ignore[attr-defined]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "stop", ["dropped", "disabled", "stop_file", "video_stop_file", "drama_disabled"]
)
async def test_owner_stop_while_queued_prevents_model_dispatch(
    store: Any, monkeypatch, stop: str, tmp_path
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(
            session, request(format="drama" if stop == "drama_disabled" else "slides"), token.id
        )
        if stop == "dropped":
            session.add(
                VideoProject(
                    slug="durable-writer", title="Stopped", stage="script", dropped_at=utcnow()
                )
            )
            await session.commit()
    if stop == "disabled":
        monkeypatch.setattr(
            automation_settings,
            "settings_row",
            AsyncMock(return_value=VideoAutomationSettings(enabled=False)),
        )
    if stop == "drama_disabled":
        monkeypatch.setattr(
            automation_settings,
            "settings_row",
            AsyncMock(return_value=VideoAutomationSettings(enabled=True, drama_enabled=False)),
        )
    if stop == "stop_file":
        stop_file = tmp_path / "STOP"
        stop_file.write_text("owner paused", encoding="utf-8")
        monkeypatch.setenv("VIDEO_STAGE_STOP_FILE", str(stop_file))
    if stop == "video_stop_file":
        video_stop = tmp_path / "durable-writer" / "STOP"
        video_stop.parent.mkdir()
        video_stop.write_text("owner paused this video", encoding="utf-8")
        monkeypatch.setenv("VIDEO_STAGE_STOP_FILE", str(tmp_path / "STOP"))
    with pytest.raises(StageFailed):
        await run_jobs._run(receipt.id)
    async with store() as session:
        result = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
        row = await session.get(VideoStageJob, receipt.id)
    assert result.status == "failed"
    assert (
        result.error_code
        == {
            "dropped": "video_ai_project_dropped",
            "disabled": "video_ai_automation_disabled",
            "stop_file": "video_ai_worker_stopped",
            "video_stop_file": "video_ai_worker_stopped",
            "drama_disabled": "video_ai_drama_disabled",
        }[stop]
    )
    assert row.dispatched_at is None
    assert ai._on_api_key.await_count == 0  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_queue_outage_preserves_receipt_and_running_dispatch(store: Any, monkeypatch) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
        row = await session.get(VideoStageJob, receipt.id)
        row.status, row.started_at, row.dispatched_at = "running", utcnow(), utcnow()
        await session.commit()
    monkeypatch.setattr(
        run_jobs, "_schedule", lambda *_args, **_kwargs: (_ for _ in ()).throw(RedisError("outage"))
    )
    async with store() as session:
        with pytest.raises(StageFailed) as outage:
            await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
        row = await session.get(VideoStageJob, receipt.id)
        assert row.status == "running"
    assert outage.value.status == 503 and outage.value.code == "video_ai_job_queue_unavailable"


@pytest.mark.asyncio
async def test_startup_schedules_only_proven_queued_operations(store: Any, monkeypatch) -> None:
    token = await credential(store)
    ids = []
    async with store() as session:
        for status in ("queued", "running", "uncertain"):
            receipt = await run_jobs.submit_job(session, request(), token.id)
            ids.append(receipt.id)
            row = await session.get(VideoStageJob, receipt.id)
            row.status = status
            if status != "queued":
                row.dispatched_at = utcnow()
            await session.commit()
    scheduled = []
    monkeypatch.setattr(
        run_jobs, "_schedule", lambda job_id, *, queued: scheduled.append((job_id, queued))
    )
    cleanup = AsyncMock()
    monkeypatch.setattr(run_jobs, "engine", SimpleNamespace(dispose=cleanup))
    assert await run_jobs.recover_pending() == 1
    assert scheduled == [(ids[0], True)]
    cleanup.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "changed",
    [
        {"slug": "other-video"},
        {"payload": {"brief": "stale"}},
        {"instructions": "Changed"},
        {"max_output_tokens": 2000},
        {"format": "drama"},
    ],
)
async def test_reused_key_cannot_adopt_other_video_or_stale_inputs(
    store: Any, changed: dict[str, Any]
) -> None:
    token = await credential(store)
    body = request()
    async with store() as session:
        receipt = await run_jobs.submit_job(session, body, token.id)
    await run_jobs._run(receipt.id)
    async with store() as session:
        with pytest.raises(StageFailed, match="不同的影片"):
            await run_jobs.submit_job(
                session, request(**{**body.model_dump(), **changed}), token.id
            )


@pytest.mark.asyncio
async def test_poll_requires_original_token_and_input_hash(store: Any) -> None:
    token, other = await credential(store), await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    async with store() as session:
        with pytest.raises(StageFailed) as unauthorized:
            await run_jobs.poll_job(session, receipt.id, other.id, receipt.input_hash)
    assert unauthorized.value.status == 404
    async with store() as session:
        with pytest.raises(StageFailed) as stale:
            await run_jobs.poll_job(session, receipt.id, token.id, "0" * 64)
    assert stale.value.code == "video_ai_job_input_changed"


@pytest.mark.asyncio
@pytest.mark.parametrize("state", [None, "failed", "stopped", "finished"])
async def test_lost_dispatched_job_becomes_uncertain_and_never_reexecutes(
    store: Any, monkeypatch: pytest.MonkeyPatch, state: str | None
) -> None:
    token = await credential(store)
    body = request()
    async with store() as session:
        receipt = await run_jobs.submit_job(session, body, token.id)
        row = await session.get(VideoStageJob, receipt.id)
        row.status, row.started_at, row.dispatched_at = "running", utcnow(), utcnow()
        await session.commit()
    monkeypatch.setattr(run_jobs, "_schedule", lambda *_args, **_kwargs: state)
    async with store() as session:
        uncertain = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert uncertain.status == "uncertain" and uncertain.result is None
    await run_jobs._run(receipt.id)
    assert ai._on_api_key.await_count == 0  # type: ignore[attr-defined]
    async with store() as session:
        same = await run_jobs.submit_job(session, body, token.id)
    assert same.id == receipt.id and same.status == "uncertain"


@pytest.mark.asyncio
async def test_poll_does_not_overwrite_concurrent_completed_result(store: Any, monkeypatch) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
        row = await session.get(VideoStageJob, receipt.id)
        row.status, row.started_at, row.dispatched_at = "running", utcnow(), utcnow()
        await session.commit()
    entered, finish = asyncio.Event(), asyncio.Event()

    async def inspection(*_args: object, **_kwargs: object) -> str:
        entered.set()
        await finish.wait()
        return "finished"

    monkeypatch.setattr(asyncio, "to_thread", inspection)
    async with store() as polling:
        pending = asyncio.create_task(
            run_jobs.poll_job(polling, receipt.id, token.id, receipt.input_hash)
        )
        await entered.wait()
        async with store() as writing:
            row = await writing.get(VideoStageJob, receipt.id)
            row.status = "succeeded"
            row.result_json = StageRunOut(
                text=EXACT,
                provider="anthropic",
                model="writer-v1",
                input_tokens=0,
                output_tokens=7,
                usage=usage(),
            ).model_dump(mode="json")
            await writing.commit()
        finish.set()
        completed = await pending
    assert completed.status == "succeeded" and completed.result and completed.result.text == EXACT


@pytest.mark.asyncio
async def test_poll_cannot_classify_new_dispatch_as_a_no_call_failure(
    store: Any, monkeypatch
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
        row = await session.get(VideoStageJob, receipt.id)
        row.status, row.started_at = "running", utcnow()
        await session.commit()
    entered, finish = asyncio.Event(), asyncio.Event()

    async def inspection(*_args: object, **_kwargs: object) -> str:
        entered.set()
        await finish.wait()
        return "failed"

    monkeypatch.setattr(asyncio, "to_thread", inspection)
    async with store() as polling:
        pending = asyncio.create_task(
            run_jobs.poll_job(polling, receipt.id, token.id, receipt.input_hash)
        )
        await entered.wait()
        async with store() as writing:
            row = await writing.get(VideoStageJob, receipt.id)
            row.dispatched_at = utcnow()
            await writing.commit()
        finish.set()
        result = await pending
        assert result.status == "running"
        uncertain = await run_jobs.poll_job(polling, receipt.id, token.id, receipt.input_hash)
        assert uncertain.status == "uncertain"


@pytest.mark.asyncio
async def test_interrupt_before_dispatch_closes_dispatch_atomically(
    store: Any, monkeypatch
) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
    entered, finish = asyncio.Event(), asyncio.Event()

    async def preflight(*_args: object, **_kwargs: object) -> tuple[str, str, UsageView, bool]:
        entered.set()
        await finish.wait()
        return "anthropic", "writer-v1", usage(), False

    monkeypatch.setattr(ai, "prepare_stage", preflight)
    running = asyncio.create_task(run_jobs._run(receipt.id))
    await entered.wait()
    monkeypatch.setattr(run_jobs, "_schedule", lambda *_args, **_kwargs: None)
    async with store() as session:
        failed = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert failed.status == "failed"
    finish.set()
    with pytest.raises(StageFailed) as closed:
        await running
    assert closed.value.code == "video_ai_job_dispatch_closed"
    assert ai._on_api_key.await_count == 0  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_expired_started_job_does_not_wait_forever(store: Any, monkeypatch) -> None:
    token = await credential(store)
    async with store() as session:
        receipt = await run_jobs.submit_job(session, request(), token.id)
        row = await session.get(VideoStageJob, receipt.id)
        row.status = "running"
        row.started_at = utcnow() - timedelta(seconds=run_jobs.INTERRUPTED_AFTER_SECONDS + 1)
        row.dispatched_at = row.started_at
        await session.commit()
    async with store() as session:
        result = await run_jobs.poll_job(session, receipt.id, token.id, receipt.input_hash)
    assert result.status == "uncertain"


@pytest.mark.asyncio
async def test_transport_routes_require_token_and_preserve_exact_reply(store: Any) -> None:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")

    async def session() -> AsyncIterator[AsyncSession]:
        async with store() as current:
            yield current

    app.dependency_overrides[get_session] = session
    body = request()
    token = await credential(store)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        denied = await client.post(
            "/api/v1/video/automation/run/jobs", json=body.model_dump(mode="json")
        )
        assert denied.status_code == 401
        app.dependency_overrides[video_tool] = lambda: token
        submitted = await client.post(
            "/api/v1/video/automation/run/jobs", json=body.model_dump(mode="json")
        )
        receipt = submitted.json()
        assert submitted.status_code == 200 and receipt["status"] == "queued"
        await run_jobs._run(UUID(receipt["id"]))
        answer = await client.get(
            f"/api/v1/video/automation/run/jobs/{receipt['id']}",
            params={"input_hash": receipt["input_hash"]},
        )
    assert answer.status_code == 200 and answer.json()["result"]["text"] == EXACT


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def postgres_engine() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio(loop_scope="module")
async def test_concurrent_submits_share_one_receipt_on_postgresql(
    monkeypatch, postgres_engine
) -> None:
    token = await credential(SessionFactory)
    body = request()
    monkeypatch.setattr(run_jobs, "_schedule", lambda *_args, **_kwargs: "queued")
    monkeypatch.setattr(run_jobs, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(run_jobs, "load_runtime_settings", AsyncMock(return_value=Settings()))
    monkeypatch.setattr(automation_settings, "remember_prompt", AsyncMock())
    monkeypatch.setattr(
        run_jobs,
        "prepare_stage",
        AsyncMock(return_value=("anthropic", "writer-v1", usage(), False)),
    )

    async def submit() -> Any:
        async with SessionFactory() as session:
            return await run_jobs.submit_job(session, body, token.id)

    try:
        one, two = await asyncio.gather(submit(), submit())
        assert one.id == two.id
    finally:
        async with SessionFactory() as session:
            await session.execute(delete(VideoStageJob).where(VideoStageJob.token_id == token.id))
            await session.execute(delete(VideoToolToken).where(VideoToolToken.id == token.id))
            await session.commit()


def test_hash_is_order_independent_and_includes_entire_source() -> None:
    one = request(payload={"b": 2, "a": {"z": "中文", "x": 1}}).run_request()
    two = request(payload={"a": {"x": 1, "z": "中文"}, "b": 2}).run_request()
    assert run_jobs.request_hash(one) == run_jobs.request_hash(two)
    assert run_jobs.request_hash(one) != run_jobs.request_hash(
        one.model_copy(update={"slug": "other"})
    )
    with pytest.raises(StageFailed, match="JSON"):
        run_jobs.request_hash(request(payload={"bad": float("nan")}).run_request())


def test_rq_scheduler_retains_one_job_and_has_no_automatic_retry(monkeypatch) -> None:
    connection = FakeRedis()
    # fakeredis without Lua cannot run Redis' lock release script. Scheduling itself
    # still uses the real RQ queue and job format; replace only the local lock boundary.
    monkeypatch.setattr(connection, "lock", lambda *_args, **_kwargs: nullcontext())
    monkeypatch.setattr(Redis, "from_url", lambda *_args, **_kwargs: connection)
    job_id = uuid4()
    assert run_jobs._schedule(job_id, queued=True) == "queued"
    assert run_jobs._schedule(job_id, queued=True) == "queued"
    queue = Queue(run_jobs.QUEUE_NAME, connection=connection)
    assert queue.count == 1
    job = queue.fetch_job(f"video-stage-{job_id}")
    assert job and job.func_name == "app.video_automation.run_jobs.run_job"
    assert job.timeout == 1200 and not job.retries_left
    assert run_jobs._schedule(uuid4(), queued=False) is None
