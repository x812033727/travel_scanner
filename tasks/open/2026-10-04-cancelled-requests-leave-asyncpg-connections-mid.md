---
id: 2026-10-04-cancelled-requests-leave-asyncpg-connections-mid
title: Cancelled requests leave asyncpg connections mid-operation and the next requests on them fail with 500
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-asyncpg-cancel
claimed_at: 2026-10-05T01:23:07Z
created_at: 2026-10-04T19:21:18Z
completed_at:
branch: claude/asyncpg-cancel
depends_on: []
scope:
  - apps/api/app/middleware.py
  - apps/api/app/db.py
  - apps/api/tests/test_db_session_cancellation.py
---

# Cancelled requests leave asyncpg connections mid-operation and the next requests on them fail with 500

## Why

On 2026-10-04 the required `full-stack-smoke` check failed on PR #1224 (run 37225953048, attempt 1,
job 111505516455, head 227956d1c) and passed on a rerun of the same SHA with no code change. The
failure was not in the PR's code: the API answered 93 requests with 500 across unrelated
endpoints (`/auth/register`, `/auth/me`, `/community/me`, `/saved-items`, `/guides`, admin
pages), so 20 Playwright journeys failed at their first API call.

The service log shows the chain:

1. `Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection …>>` with
   `asyncio.exceptions.CancelledError: Cancelled via cancel scope … by <Task …
   starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro>`
   (10 times): a request was cancelled while its session was using a connection.
   `RequestContextMiddleware` in `apps/api/app/middleware.py` is a `BaseHTTPMiddleware`.
2. Then `asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is
   in progress` on rollback, and `cannot use Connection.transaction() in a manually started
   transaction` on the next request's first statement: a connection that was still mid-operation
   went back into the pool and was handed out again.

`pool_pre_ping=True` (`apps/api/app/db.py`) does not catch a connection in this state. If the same
thing happens in production, a burst of client disconnects (closed tabs, a crawler timing out)
could turn into a burst of 500s for other readers.

## Definition of done

- [x] A request cancelled while its session holds a connection cannot hand that connection, still
      mid-operation, to the next request (the connection is invalidated or the cancellation is
      shielded until the session closes).
- [x] A regression test reproduces the cascade (cancel a request mid-query, then issue requests
      that reuse the pool) and passes after the fix, or the ticket says why a test cannot.
- [ ] Notes record whether production's api log shows the same signature (read-only check).

## Steps

- [ ] Reproduce locally against Postgres (CI's service container or a disposable one): a slow
      query, a client that disconnects, then N quick requests.
- [x] Compare the options: replace `BaseHTTPMiddleware` with a pure ASGI middleware (it does not
      cancel the endpoint task on disconnect), and/or invalidate the session's connection on
      `CancelledError` in the session dependency. Pick the smallest that makes the test pass.
- [ ] Grep production's api log for `another operation is in progress` (with the owner's consent).

## How to verify

The regression test above, then several green `full-stack-smoke` runs.

## Notes

- Filed by claude-opus-5-5-incomplete-tickets on 2026-10-04 while merging PR #1224, whose own
  change (look reviews keyed by subject, migration 0124) ran cleanly on Postgres in the same job.
- Not yet seen on other runs as far as this session checked; it is not in the CI flake notes.

### 2026-10-05 fix (claude-opus-5-5-asyncpg-cancel, branch claude/asyncpg-cancel)

- **What cancels the request.** Not `BaseHTTPMiddleware`: in Starlette 1.6 it does not cancel the
  endpoint when the client goes away. uvicorn reports ASGI `spec_version` 2.3, and below 2.4
  `StreamingResponse` runs the body in a task group next to a disconnect listener and cancels the
  body when the client disconnects. The cancel comes "by <Task … call_next.<locals>.coro>" only
  because `BaseHTTPMiddleware` runs the endpoint in that task. The one stream that holds a database
  session is `/api/v1/community/events` (`app/community/messaging.py` opens a `SessionFactory()`
  session per catch-up; the search event stream reads Redis only), and Playwright closes it on
  every navigation. All 10 `Exception terminating connection` entries in the job log are SQLAlchemy
  garbage-collecting connections that were never checked back in ("non-checked-in connection"),
  with the termination itself cancelled again.
- **Why cleanup failed.** anyio cancellation is level-triggered: every await in a cancelled task
  raises again, so a session closed inside that task stops at its first await. Measured with the
  new SQLite test: invalidating without a shield leaves the pool slot checked out
  (`checkedout()` stays 1, so a one-connection pool would hang the next request).
- **Options compared.** A pure ASGI `RequestContextMiddleware` would not help: the stream is still
  cancelled by `StreamingResponse` itself. So the middleware is unchanged, and the pinning tests
  the triage asked for before changing it were not needed. The fix is in `app/db.py`:
  `SessionFactory` makes `CancellationSafeSession`s, whose `__aexit__` calls `invalidate()` inside
  `anyio.CancelScope(shield=True)` when the exit is an `asyncio.CancelledError`, and closes as
  before otherwise. That covers `get_session` (FastAPI throws the endpoint's exception into the
  dependency) and every `async with SessionFactory()`, the event stream's included. A cancelled
  session costs one reconnect. `SessionFactory` is annotated `async_sessionmaker[AsyncSession]`
  because the type is invariant: without it `mypy app` reported 9 errors in
  `app/video_youtube/sync.py`.
- **SQLAlchemy version.** The failing run used SQLAlchemy 2.0.54; main moved to 2.1.3 (#1226) the
  same day. 2.1 already runs `AsyncSession.__aexit__`'s `close()` to completion in its own task and
  returns the slot in `_ConnectionRecord._checkin_failed` even when a second cancellation interrupts
  it, but it still rolls a cancelled session's connection back and reuses it. Measured with the new
  tests: with SQLAlchemy's default exit the three cancellation tests fail (`close` instead of
  `invalidate`) and the SQLite test sees no invalidation; without the shield two tests fail
  (`invalidate` stops after its first await) and the SQLite test leaves the slot checked out.
- **Tests** (`apps/api/tests/test_db_session_cancellation.py`): the factory's class; a session
  cancelled inside an anyio scope invalidates to the end; errors and normal exits still close; the
  request dependency invalidates when the request is cancelled; a client closing a
  `StreamingResponse` served behind `RequestContextMiddleware` invalidates the stream's session;
  SQLAlchemy's real invalidation on a one-connection SQLite pool gives the slot back with the
  connection discarded; and a PostgreSQL test (`RUN_INTEGRATION_TESTS=1`) that cancels `pg_sleep`
  mid-statement three times, then reuses a one-connection pool and checks the cancelled backend
  never comes back, plus 40 cancellations from 0 to 20 ms into a short request.
- **Not done here, split into `2026-10-05-asyncpg-cancel-cascade-production-check`:** the
  production log grep (needs the host and the owner's consent; DoD 3 and Step 3), and the Postgres
  reproduction (Step 1). This machine has no PostgreSQL (no Docker, nothing in the WSL Ubuntu), so
  the Postgres test runs only in CI's api-tests shards; nobody has watched it pass yet, nor seen
  whether it fails on 2.1.3 without the fix. Watching full-stack-smoke after the merge went there
  too.
