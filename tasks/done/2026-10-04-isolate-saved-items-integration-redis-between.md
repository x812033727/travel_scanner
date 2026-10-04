---
id: 2026-10-04-isolate-saved-items-integration-redis-between
title: Isolate saved-items integration Redis between event loops
status: done
priority: P2
area: api
owner: codex-video-recovery-20261004
claimed_at: 2026-10-04T07:03:32Z
created_at: 2026-10-04T07:01:04Z
completed_at: 2026-10-04T07:16:38Z
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
- [x] The real PostgreSQL/Redis API shard passes the previously failing account
      scoping, idempotency and public-only test.

## Steps

- [x] Confirm the CI error and the repository's existing module-isolation pattern.
- [x] Freshly check overlapping worktrees and claim the narrow test path.
- [x] Apply the fixture pattern without changing production Redis behavior.
- [x] Run Ruff/Mypy and the real-service CI shard.

## How to verify

Run Ruff and Mypy on the test, then CI's API shard 4 with
`RUN_INTEGRATION_TESTS=1` and actual PostgreSQL/Redis services. Offline collection
alone cannot prove the fixture lifecycle.

## Notes

The older illustrated-slides task has a broad overlapping test scope but its
changes already landed as #1172. Both its relevant worktree and the primary
checkout have no edits to this file, and open PR #1202 touches only frontend
monetization paths. The forced claim bypassed that stale broad scope only.

## PR handoff (2026-10-04)

Implementation and independent review are included in draft PR #1203. This task
records completed source work and validation, not a production deployment or a
recovered/published video. All four API shards passed 6695 tests with 22 skips;
API Ruff/Mypy, Web checks and all three Web unit shards passed on source head
dc2a4b194. The complete tools suite passed 1536 tests with 2 skips. Real PostgreSQL/Redis shard 4 passed 1352 tests
with 9 skips, including the saved-items lifecycle regression. Final aggregate CI
results are recorded in the PR. Existing media switches, caps, owner approvals
and disabled uploader were not changed.

Local API broad run: 6070 passed, 442 skipped; 28 Windows-only failures were
rechecked with UTF-8 mode. The relevant collection then passed 173 tests with
1 skip and only the unavailable Windows symlink privilege case remaining.
That test-platform gap is tracked separately as
2026-10-04-python-anime-planning-symlink-windows.
