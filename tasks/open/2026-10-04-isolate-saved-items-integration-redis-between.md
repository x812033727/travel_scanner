---
id: 2026-10-04-isolate-saved-items-integration-redis-between
title: Isolate saved-items integration Redis between event loops
status: in-progress
priority: P2
area: api
owner: codex-video-recovery-20261004
claimed_at: 2026-10-04T07:03:32Z
created_at: 2026-10-04T07:01:04Z
completed_at:
branch: codex/video-pipeline-recovery-20261004
depends_on: []
scope:
  - apps/api/tests/test_saved_items_integration.py
---

# Isolate saved-items integration Redis between event loops

## Why

PR #1203 API shard 4 failed its saved-items integration test with a cached Redis
connection attached to a previous module's closed event loop. The same shard had
1351 passing tests and 9 skips; all new video-job and migration PostgreSQL checks
passed in shard 3. The saved-items fixture disposed only its database engine and
did not isolate or close its Redis client. This is a test lifecycle correction,
using the established usage-settings/deployments fixture convention.

## Definition of done

- [x] Saved-items integration begins with fresh asynchronous clients and closes
      both database and Redis clients on the module's own event loop.
- [ ] The real PostgreSQL/Redis API shard passes the previously failing account
      scoping, idempotency and public-only test.

## Steps

- [x] Confirm the CI error and the repository's existing module-isolation pattern.
- [x] Freshly check overlapping worktrees and claim the narrow test path.
- [x] Apply the fixture pattern without changing production Redis behavior.
- [ ] Run Ruff/Mypy and the real-service CI shard.

## How to verify

Run Ruff and Mypy on the test, then CI's API shard 4 with
`RUN_INTEGRATION_TESTS=1` and actual PostgreSQL/Redis services. Offline collection
alone cannot prove the fixture lifecycle.

## Notes

The older illustrated-slides task has a broad overlapping test scope but its
changes already landed as #1172. Both its relevant worktree and the primary
checkout have no edits to this file, and open PR #1202 touches only frontend
monetization paths. The forced claim bypassed that stale broad scope only.
