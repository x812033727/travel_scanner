---
id: 2026-09-09-pr343-account-safety-integration
title: Integrate PR 343 account safety with current main
status: review
priority: P1
area: api
owner: codex-account-safety
claimed_at: 2026-09-09T06:12:27Z
created_at: 2026-09-09T06:12:26Z
completed_at:
branch: codex/pr343-merge-ready-20260909
depends_on: []
scope:
  - apps/api/app/community/accounts.py
  - apps/api/app/community/jobs.py
  - apps/api/tests/test_community_foundation.py
  - docs/community.md
---

# Integrate PR 343 account safety with current main

## Why

PR #343 contains account-token issuance/consumption and erasure locking fixes that
are still absent from main. Its old CI and draft state do not validate integration
with the newer discovery, collections and account-erasure behavior.

## Definition of done

- [x] Preserve User-before-Token locking and stale-state checks without regressing current account cleanup.
- [x] Keep current main's post-place, saved-item and discovery cleanup behavior and private data boundaries.
- [ ] Pass focused account tests and current-head PostgreSQL/full CI before guarded merge.
- [ ] Confirm the authorized merge and post-merge CI; do not activate or deploy services.

## Steps

- [x] Normally merge current main into the original PR head and inspect the final delta.
- [ ] Validate the existing concurrency regressions, refresh draft/PR evidence, and merge only the verified head.

## How to verify

From apps/api: pytest tests/test_community_foundation.py tests/test_discovery_community.py
tests/test_saved_flow.py tests/test_schema.py,
Ruff and mypy. GitHub CI supplies real PostgreSQL row-lock, fresh migration, private
S3 and full-stack coverage. Run the task-board checker and diff checks as well.

## Notes

2026-09-09: The user accepted the proposed #343/#335 integration and merge sequence.
This isolated worktree starts at original #343 head 7fd67ad197a705b769c1862d6828b9d1f98c99ea;
the initial main is a899437aaf2f60c7affe2e944d49d62216537c90. No production connections,
provider calls, registration/community activation, review replays or deployments are
part of this task. Keep the wider community-foundation task open; this narrow task
does not certify the full social/pet product or take ownership of its broad scope.

The main integration has no application/test conflict; only the generated board
needed rebuilding. Main's creator-invitation cleanup, typed post-place cleanup,
collections and discovery cleanup remain intact. Local isolated verification
passed 103 tests with eight PostgreSQL/S3-dependent skips; full API Ruff and mypy
278 files passed. No shared Python environment or lockfile was changed. Real
PostgreSQL serialization and private S3 remain mandatory remote CI checks.

The integrated main still marks the already-merged #374 saved-API task as review.
Its coordinating owner verified a clean source file matching main and explicitly
handed off only test_community_foundation.py in local commit 9841cda1016ea73faec501add2e7984e8232cca6.
Carry that exact metadata delta here without modifying its other scopes/status.
The saved fixtures remain intact. Existing upstream task overlap between discovery
and route-tone tests is preserved rather than modified as unrelated work. The
original foundation task remains open.

Independent read-only review found no blocker: SQLAlchemy's key_share=True with
read=False compiles to FOR NO KEY UPDATE, preserving account serialization without
unnecessary foreign-key insert conflicts. The only jobs.py delta from current main
is populate_existing after locking the User; all newer cleanup paths are retained.
Fifteen focused task-tool tests and diff checks also passed. Current-head CI is
still pending and the draft is not ready to merge until those checks succeed.
