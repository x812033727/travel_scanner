---
id: 2026-10-05-asyncpg-cancel-cascade-production-check
title: Check production's api log for the asyncpg cancellation cascade and watch the regression test in CI
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-05T02:14:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_db_session_cancellation.py
---

# Check production's api log for the asyncpg cancellation cascade and watch the regression test in CI

## Why

Split from `2026-10-04-cancelled-requests-leave-asyncpg-connections-mid`, whose code fix landed
on branch `claude/asyncpg-cancel`. On 2026-10-04 full-stack-smoke (run 37225953048, attempt 1)
answered 93 requests with 500: a reader closing the community event stream
(`/api/v1/community/events`) made Starlette's `StreamingResponse` cancel the stream while its
catch-up session was mid-statement, and connections still mid-operation went back into the pool.
`app.db.SessionFactory` sessions now invalidate their connection, shielded from anyio's
level-triggered cancellation, whenever a cancellation ends them.

Two things the original ticket asked for could not be done from an agent worktree:

1. Whether production ever showed the same signature. Production has the same stream behind
   the same middleware, and a closed tab or a crawler timing out is a client disconnect, so the
   answer says whether readers ever met these 500s. Reading the host's log needs the owner's
   consent and a session on the host.
2. The Postgres half of the regression test. This machine has no PostgreSQL (no Docker; the WSL
   Ubuntu has none installed), so
   `test_a_cancelled_statement_never_reaches_the_next_session_on_postgres` only runs where
   `RUN_INTEGRATION_TESTS=1`, in CI's api-tests shards. Nobody has yet watched it pass there, or
   seen whether it fails without the fix.

## Definition of done

- [ ] Notes record, for the window the api container's log still covers, how many times each of
      these appears in production's api log, and the dates of the first and last:
      `another operation is in progress`, `manually started transaction`,
      `Exception terminating connection`, `non-checked-in connection`. Read-only; nothing restarted.
- [ ] Notes name a CI run (id and shard) where the Postgres test above ran and passed.
- [ ] Notes record three full-stack-smoke runs on main after the fix merged whose service log has
      none of the four strings (or the run ids where one appeared).

## Steps

- [ ] With the owner's consent, grep the api log on the host (command below). Do not restart or
      redeploy anything for it.
- [ ] Find the api-tests shard that ran `tests/test_db_session_cancellation.py` on the fix's pull
      request or on main, and confirm the Postgres test is listed as passed, not skipped.
- [ ] Optional, if a disposable Postgres is at hand: run the Postgres test once with
      `CancellationSafeSession.__aexit__` reduced to `await super().__aexit__(...)` (a local edit,
      not committed) and record whether SQLAlchemy 2.1.3 alone already prevents the cascade (the
      failure was on 2.0.54; see Notes).
- [ ] If the signature shows up in production after the fix deployed, reopen the investigation
      with the log excerpt instead of closing this ticket.

## How to verify

On the host, after the owner agrees (`<SSH>` as in `.agents/skills/prod-host-ops/SKILL.md`):

```bash
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml logs api | grep -c 'another operation is in progress'"
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml logs api | grep -c 'manually started transaction'"
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml logs api | grep -c 'Exception terminating connection'"
<SSH> "cd /root/travel_scanner && docker compose -f docker-compose.prod.yml logs api | grep -c 'non-checked-in connection'"
```

In CI: `gh run view <run-id> --log --job <api-tests job id> | grep test_db_session_cancellation`
prints the file's progress line with seven dots and no `s` (locally, without PostgreSQL, it is
`......s`: the seventh test skipped), and
`gh run view <run-id> --log --job <full-stack-smoke job id> | grep -c 'Exception terminating connection'`
prints 0.

## Notes

- Split from 2026-10-04-cancelled-requests-leave-asyncpg-connections-mid by
  claude-opus-5-5-asyncpg-cancel on 2026-10-05.
- The failing run used SQLAlchemy 2.0.54; main moved to 2.1.3 in #1226 hours later. 2.1 already
  hardens this area: `AsyncSession.__aexit__` runs `close()` to completion in its own task, and
  `_ConnectionRecord._checkin_failed` returns the slot even when a second cancellation interrupts
  its invalidation. It still rolls a cancelled session's connection back and reuses it, which is
  what the fix changes. The SQLite test in the same file shows the difference locally.
- The container log only reaches back to the api container's last start, so an empty grep right
  after a deploy says little; note the container's `StartedAt` next to the counts.
