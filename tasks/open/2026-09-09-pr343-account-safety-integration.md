---
id: 2026-09-09-pr343-account-safety-integration
title: Integrate PR 343 account safety with current main
status: in-progress
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

- [ ] Preserve User-before-Token locking and stale-state checks without regressing current account cleanup.
- [ ] Keep current main's post-place, saved-item and discovery cleanup behavior and private data boundaries.
- [ ] Pass focused account tests and current-head PostgreSQL/full CI before guarded merge.
- [ ] Confirm the authorized merge and post-merge CI; do not activate or deploy services.

## Steps

- [ ] Normally merge current main into the original PR head and inspect the final delta.
- [ ] Validate the existing concurrency regressions, refresh draft/PR evidence, and merge only the verified head.

## How to verify

From apps/api: pytest tests/test_community_foundation.py tests/test_discovery_community.py
tests/test_collection_inbox.py tests/test_schema.py (use only existing test files),
Ruff and mypy. GitHub CI supplies real PostgreSQL row-lock, fresh migration, private
S3 and full-stack coverage. Run the task-board checker and diff checks as well.

## Notes

2026-09-09: The user accepted the proposed #343/#335 integration and merge sequence.
This isolated worktree starts at original #343 head 7fd67ad197a705b769c1862d6828b9d1f98c99ea;
the initial main is a899437aaf2f60c7affe2e944d49d62216537c90. No production connections,
provider calls, registration/community activation, review replays or deployments are
part of this task. Keep the wider community-foundation task open; this narrow task
does not certify the full social/pet product or take ownership of its broad scope.
