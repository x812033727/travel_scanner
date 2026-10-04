---
id: 2026-10-04-a-cancelled-request-poisons-the-asyncpg
title: A cancelled request poisons the asyncpg pool and turns the rest of full-stack-smoke into 500s
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-04T19:21:21Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/middleware.py
  - apps/api/app/db.py
---

# A cancelled request poisons the asyncpg pool and turns the rest of full-stack-smoke into 500s

## Why

`full-stack-smoke` failed on PR #1224 (head 227956d1, run 37225953048 attempt 1, job
111505516455) and passed unchanged on attempt 2. #1224 only touched video reviews, and
main's own runs were green. The failure was in the shared API process, not the PR:

1. During `e2e/community.spec.ts` a request was cancelled inside Starlette's
   `BaseHTTPMiddleware.call_next` (`asyncio.exceptions.CancelledError: Cancelled via cancel
   scope ... BaseHTTPMiddleware.__call__.<locals>.call_next`). Our only such middleware is
   `RequestContextMiddleware` in `apps/api/app/middleware.py`.
2. SQLAlchemy then logged `Exception terminating connection` and "The garbage collector is
   trying to clean up non-checked-in connection", i.e. the cancelled request's connection was
   never returned cleanly.
3. From then on 93 requests answered 500, starting with `GET /api/v1/auth/me`, with
   `asyncpg InterfaceError: cannot perform operation: another operation is in progress` once
   and `cannot use Connection.transaction() in a manually started transaction` 92 times.
4. Every later browser step failed: community (12 failed, `POST /auth/register: Internal
   Server Error`), admin domains (2 failed) and the admin operations matrix (6 failed,
   `"Internal S"... is not valid JSON`).

So one cancelled request can leave a pooled connection inside an open transaction, and every
request that later checks it out fails. In production the same thing would surface as a burst
of unrelated 500s until the API restarts.

## Definition of done

- [ ] A request cancelled mid-query (client disconnect, SSE stream closed, cancel scope) never
      returns a connection to the pool with a transaction still open, and later requests on the
      same pool succeed.
- [ ] A regression test reproduces the poisoning on PostgreSQL (`RUN_INTEGRATION_TESTS=1`) and
      fails against the current code.

## Steps

- [ ] Reproduce: cancel a request inside `RequestContextMiddleware` while its session holds an
      asyncpg connection in a transaction, then issue another request on the same pool.
- [ ] Decide the fix. Candidates: replace `BaseHTTPMiddleware` with a pure ASGI middleware (the
      Starlette docs recommend this, since `call_next` runs the endpoint in a separate task and
      cancels it); shield session close/rollback from cancellation in `db.py`; or enable
      `pool_pre_ping` / a reset-on-return that rolls back.
- [ ] Add the PostgreSQL regression test and run the full-stack-smoke community and admin specs
      repeatedly.

## How to verify

```bash
cd apps/api && RUN_INTEGRATION_TESTS=1 uv run pytest -k <new test>
# then several CI full-stack-smoke runs with no "manually started transaction" in the API log
```

## Notes

- Evidence: the attempt-1 job log of run 37225953048 (job 111505516455). Grep it for
  `manually started transaction`, `another operation is in progress` and
  `non-checked-in connection`.
- Not in `.agents/skills/dev-and-ci/references/ci-triage.md` yet. Add it there as a known flake
  once the cause is confirmed. Until it is fixed, one re-run is the right response when these
  errors appear on a PR that does not touch the API session or middleware.
