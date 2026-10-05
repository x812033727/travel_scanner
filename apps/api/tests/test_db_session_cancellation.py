"""A session ended by a cancellation must not hand its connection back to the pool.

full-stack-smoke failed on 2026-10-04 (run 37225953048, attempt 1) with 93 answers of
500: a client closing the community event stream cancelled the stream's task while its
session was mid-statement, and connections still mid-operation went back into the pool
for the next requests ("another operation is in progress", "cannot use
Connection.transaction() in a manually started transaction").

The first tests stand a probe in for the session's connection work and check what
``app.db.SessionFactory`` sessions do when a cancellation ends them: invalidate, to the
end, even inside a cancel scope that keeps cancelling. One more runs SQLAlchemy's own
invalidation against a SQLite file. The last needs PostgreSQL
(``RUN_INTEGRATION_TESTS=1``, as the CI api-tests shards run it) and drives the real
cascade: cancel a statement in flight, then reuse the pool.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import anyio
import pytest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool, QueuePool
from starlette.types import Message, Scope

from app import db
from app.config import get_settings
from app.middleware import RequestContextMiddleware


class _Probe(db.CancellationSafeSession):
    """An application session whose connection work is recorded instead of done.

    Each step awaits several times, because each await is where a level-triggered
    cancellation would land again and cut the cleanup short.
    """

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[str] = []

    async def _work(self, name: str) -> None:
        self.calls.append(f"{name}:start")
        for _ in range(5):
            await asyncio.sleep(0)
        self.calls.append(f"{name}:end")

    async def invalidate(self) -> None:
        await self._work("invalidate")

    async def close(self) -> None:
        await self._work("close")


INVALIDATED = ["invalidate:start", "invalidate:end"]
CLOSED = ["close:start", "close:end"]


def _checked_out(engine: AsyncEngine) -> int:
    pool = engine.sync_engine.pool
    assert isinstance(pool, QueuePool)
    return pool.checkedout()


def test_the_application_factory_makes_cancellation_safe_sessions() -> None:
    assert issubclass(db.SessionFactory.class_, db.CancellationSafeSession)


async def test_a_cancelled_session_is_invalidated_to_the_end() -> None:
    session = _Probe()
    inside = anyio.Event()

    async def query() -> None:
        async with session:
            inside.set()
            await anyio.sleep(30)  # a statement still in flight

    # The same cancellation a disconnecting client gets: an anyio cancel scope.
    async with anyio.create_task_group() as group:
        group.start_soon(query)
        with anyio.fail_after(5):
            await inside.wait()
        group.cancel_scope.cancel()

    assert session.calls == INVALIDATED


async def test_errors_and_normal_exits_still_close() -> None:
    finished = _Probe()
    async with finished:
        pass

    failed = _Probe()
    with pytest.raises(RuntimeError):
        async with failed:
            raise RuntimeError("handler failed")

    assert finished.calls == CLOSED
    assert failed.calls == CLOSED


async def test_the_request_dependency_invalidates_when_the_request_is_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Probe()
    monkeypatch.setattr(db, "SessionFactory", lambda: session)

    # FastAPI enters a yield dependency as an async context manager and throws the
    # endpoint's exception into it on exit.
    with pytest.raises(asyncio.CancelledError):
        async with asynccontextmanager(db.get_session)() as provided:
            assert provided is session
            raise asyncio.CancelledError

    assert session.calls == INVALIDATED


def _event_stream_app(session: _Probe, inside: anyio.Event) -> FastAPI:
    # The shape of /api/v1/community/events: a stream that opens a session per catch-up,
    # served behind the request-context middleware as in app.main.
    app = FastAPI()
    app.add_middleware(RequestContextMiddleware)

    @app.get("/events")
    async def events() -> StreamingResponse:
        async def stream() -> AsyncIterator[str]:
            async with session:
                inside.set()
                await anyio.sleep(30)  # the catch-up query, still in flight
                yield "data: {}\n\n"

        return StreamingResponse(stream(), media_type="text/event-stream")

    return app


async def test_a_client_closing_the_event_stream_invalidates_the_stream_session() -> None:
    session = _Probe()
    inside = anyio.Event()
    gone = anyio.Event()
    app = _event_stream_app(session, inside)
    scope: Scope = {
        "type": "http",
        # uvicorn's version: below 2.4, StreamingResponse listens for the disconnect
        # itself and cancels the stream when it comes.
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/events",
        "raw_path": b"/events",
        "query_string": b"",
        "root_path": "",
        "headers": [(b"host", b"testserver")],
        "client": ("127.0.0.1", 50000),
        "server": ("testserver", 80),
    }
    requested = False
    sent: list[Message] = []

    async def receive() -> Message:
        nonlocal requested
        if not requested:
            requested = True
            return {"type": "http.request", "body": b"", "more_body": False}
        await gone.wait()
        return {"type": "http.disconnect"}

    async def send(message: Message) -> None:
        sent.append(message)

    async with anyio.create_task_group() as group:
        group.start_soon(app, scope, receive, send)
        with anyio.fail_after(5):
            await inside.wait()
        gone.set()  # the reader closed the tab

    assert sent[0]["type"] == "http.response.start"
    assert session.calls == INVALIDATED


async def test_a_cancelled_session_gives_its_slot_back_with_the_connection_discarded(
    tmp_path: Path,
) -> None:
    # SQLAlchemy's own invalidation, not a probe: one pooled connection, held by a
    # session with a transaction open when its task is cancelled.
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{tmp_path / 'pool.db'}",
        poolclass=AsyncAdaptedQueuePool,
        pool_size=1,
        max_overflow=0,
        pool_timeout=5,
    )
    factory = async_sessionmaker(engine, class_=db.CancellationSafeSession)
    invalidated: list[object] = []
    event.listen(engine.sync_engine, "invalidate", lambda conn, *_: invalidated.append(conn))
    inside = anyio.Event()

    async def held() -> None:
        async with factory() as session:
            await session.execute(text("SELECT 1"))
            inside.set()
            await anyio.sleep(30)

    try:
        async with anyio.create_task_group() as group:
            group.start_soon(held)
            with anyio.fail_after(5):
                await inside.wait()
            group.cancel_scope.cancel()

        assert len(invalidated) == 1
        assert _checked_out(engine) == 0
        with anyio.fail_after(5):
            async with factory() as session:
                assert await session.scalar(text("SELECT 1")) == 1
    finally:
        await engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
async def test_a_cancelled_statement_never_reaches_the_next_session_on_postgres() -> None:
    # One pooled connection, so every session after a cancelled one checks out the same
    # slot: a connection handed back mid-operation, or a slot never handed back, fails
    # the very next query instead of hiding behind four healthy ones.
    engine = create_async_engine(
        get_settings().database_url,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
        pool_timeout=5,
    )
    factory = async_sessionmaker(engine, class_=db.CancellationSafeSession)

    async def reuse_the_pool(times: int) -> set[int]:
        backends: set[int] = set()
        for _ in range(times):
            with anyio.fail_after(10):
                async with factory() as session:
                    assert await session.scalar(text("SELECT 1")) == 1
                    backend = await session.scalar(text("SELECT pg_backend_pid()"))
                    await session.commit()
            assert isinstance(backend, int)
            backends.add(backend)
        return backends

    async def slow_catch_up(cancelled: list[int], running: anyio.Event) -> None:
        async with factory() as session:
            cancelled.append(await session.scalar(text("SELECT pg_backend_pid()")))
            running.set()
            await session.execute(text("SELECT pg_sleep(3)"))

    async def short_request() -> None:
        async with factory() as session:
            await session.execute(text("SELECT pg_sleep(0.005)"))
            await session.execute(text("SELECT 1"))
            await session.commit()

    try:
        # A statement cancelled while the server is still running it.
        for _ in range(3):
            cancelled: list[int] = []
            running = anyio.Event()
            async with anyio.create_task_group() as group:
                group.start_soon(slow_catch_up, cancelled, running)
                with anyio.fail_after(10):
                    await running.wait()
                await anyio.sleep(0.1)  # pg_sleep is on the server by now
                group.cancel_scope.cancel()

            assert cancelled[0] not in await reuse_the_pool(10)
            assert _checked_out(engine) == 0

        # Cancellations landing anywhere, from checkout and its pre-ping through BEGIN
        # and the statements to the commit: one every half millisecond up to 20 ms.
        for step in range(40):
            with anyio.move_on_after(step * 0.0005):
                await short_request()
            await reuse_the_pool(1)
        assert _checked_out(engine) == 0
    finally:
        await engine.dispose()
