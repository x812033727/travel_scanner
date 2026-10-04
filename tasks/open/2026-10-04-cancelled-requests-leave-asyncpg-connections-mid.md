---
id: 2026-10-04-cancelled-requests-leave-asyncpg-connections-mid
title: Cancelled requests leave asyncpg connections mid-operation and the next requests on them fail with 500
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-04T19:21:18Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/middleware.py
  - apps/api/app/db.py
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

- [ ] A request cancelled while its session holds a connection cannot hand that connection, still
      mid-operation, to the next request (the connection is invalidated or the cancellation is
      shielded until the session closes).
- [ ] A regression test reproduces the cascade (cancel a request mid-query, then issue requests
      that reuse the pool) and passes after the fix, or the ticket says why a test cannot.
- [ ] Notes record whether production's api log shows the same signature (read-only check).

## Steps

- [ ] Reproduce locally against Postgres (CI's service container or a disposable one): a slow
      query, a client that disconnects, then N quick requests.
- [ ] Compare the options: replace `BaseHTTPMiddleware` with a pure ASGI middleware (it does not
      cancel the endpoint task on disconnect), and/or invalidate the session's connection on
      `CancelledError` in the session dependency. Pick the smallest that makes the test pass.
- [ ] Grep production's api log for `another operation is in progress` (with the owner's consent).

## How to verify

The regression test above, then several green `full-stack-smoke` runs.

## Notes

- Filed by claude-opus-5-5-incomplete-tickets on 2026-10-04 while merging PR #1224, whose own
  change (look reviews keyed by subject, migration 0124) ran cleanly on Postgres in the same job.
- Not yet seen on other runs as far as this session checked; it is not in the CI flake notes.
