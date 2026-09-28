---
id: 2026-09-28-guard-automatic-shorts-sync-against-changed
title: Guard automatic Shorts sync against changed consent and Studio schedules
status: done
priority: P1
area: api
owner: codex-pr905-schedule-guard
claimed_at: 2026-09-28T10:46:58Z
created_at: 2026-09-28T10:46:43Z
completed_at: 2026-09-28T10:54:37Z
branch: codex/pr905-schedule-guard
depends_on: []
scope:
  - apps/api/app/video_youtube/sync.py
  - apps/api/tests/test_video_shorts_publish.py
---

# Guard automatic Shorts sync against changed consent and Studio schedules

## Why

PR #905 queues automatic Shorts sync with consent only in its audit entry. The later sync can overwrite an independently chosen Studio publish time and can schedule after consent was revoked or publishing paused.

## Definition of done

- [x] Automatic sync preserves a different Studio schedule and stops when its consent changes or publishing pauses; explicit owner requests remain available.

## Steps

- [x] Reproduce queued consent and Studio schedule regressions using the fake YouTube and SQLite.
- [x] Persist automatic provenance and recheck it immediately before scheduling; validate the focused sync suite.

## How to verify

Run pytest tests/test_video_shorts_publish.py tests/test_video_youtube_sync.py with the dedicated checkout on PYTHONPATH, then scoped ruff and task checks.

## Notes

Started from exact #905 head b6d5f0dfe9cf77c6d9dd54892ee34e5022274972. Author implementation task is done; no worktree holds its branch and remote head remained unchanged. Isolated managed worktree, no remote push or deployment. Real YouTube pilot acceptance remains in its existing pilot task.

- Before fix: five new cases fail (Studio time overwritten; queued pause/revocation/expiry/replaced consent ignored), explicit manual update passes. Log: `test-results/regression-before.log`.
- After fix: 96 Shorts publishing and existing YouTube sync tests pass; the mid-read pause regression also passes after its final import adjustment. Logs: `test-results/focused-after.log`, `test-results/mid-read-final.log`.
- Scoped ruff and `git diff --check` pass. Task checker validates 996 tasks (existing stale/overlap warnings only).
- Scoped mypy with `--follow-imports=silent` passes both changed Python files (`test-results/scoped-mypy-resolved.log`). An initial `--follow-imports=skip` attempt erased SQLAlchemy type aliases and was not used as validation; a test import it exposed was corrected before the successful check.
- The settings row lock serializes automatic scheduling with pause/revoke/recall. Local SQLite tests prove behavioral guards, not PostgreSQL lock timing; CI integration and real YouTube pilot remain separate evidence.
