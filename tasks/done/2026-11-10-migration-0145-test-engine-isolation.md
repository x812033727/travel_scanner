---
id: 2026-11-10-migration-0145-test-engine-isolation
title: Isolate migration 0145 test engine across event loops
status: done
priority: P1
area: api
owner: codex-0145-test-isolation
claimed_at: 2026-11-10T13:52:29Z
created_at: 2026-11-10T13:51:48Z
completed_at: 2026-11-10T13:55:07Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/api/tests/test_migration_0145_video_youtube_reports.py
---

# Isolate migration 0145 test engine across event loops

## Why

PR #2061 API shard 3 fails when the first video-review integration test checks out
a PostgreSQL connection tied to a different event loop. The preceding migration
0145 test uses the application's global engine without disposing its pool. Isolate
that test's connection lifecycle; retain all migration and product behavior.

## Definition of done

- [x] The original migration-to-video test sequence reproduces the CI loop error.
- [x] Both migration 0145 tests and the same video test pass after the test-only fix.
- [x] Scoped lint, type checks, task validation and independent root review pass.

## Steps

- [x] Audit scope, current worktrees, remote branches, open PRs and merged history.
- [x] Reproduce the original failure against the isolated local PostgreSQL service.
- [x] Use a test-owned NullPool engine with unconditional disposal.
- [x] Repeat the failing sequence, validate and hand the exact diff to root.

## How to verify

In apps/api with this worktree's own uv sync --frozen environment and the isolated
local test database: python -m pytest tests/test_migration_0145_video_youtube_reports.py
tests/test_video_reviews_integration.py::test_blocked_video_retry_is_one_request_until_worker_acknowledges_it -q.
Run ruff and mypy on the modified test, check:tasks and git diff --check.

## Notes

- The prior scope record 2026-11-02-youtube-reporting-api remains unchanged. Its
  PR #1992 merged on 2026-11-02 at 8fe9233d4561c8259b87eb5370c81be477d3012d.
  Fresh who-is-on-it output finds that 188-hour-old review claim's branch nowhere
  (no active worktree or remote head), and no open PR touches this exact test path.
  This is a narrow follow-up to landed code, not a takeover of unfinished migration
  or product work. The original owner and ticket are preserved.
- Root authorized this one-test fix and owns the combined parent-branch review and
  eventual commit/push. The parallel web route fix has a distinct task and files.
- No production, paid calls, migration-source edit, workflow retry or deployment.
- Initial uv install failed while updating a temporary Windows executable's PE
  resources. The original failure log is retained; installation with a dedicated
  temporary directory succeeded without modifying the lock or other environments.
- Local receipt prefix: ci-fix-0145 under the off-repository news upgrade evidence
  directory. Original CI job 129862638406 and its complete log remain retained.
- Original SHA-256 86ace660bdc86418d1f0b039c602500e6d58f4e775f17b49d597e6dfc5b75a63:
  the two migration tests passed, then the first video test failed at its first
  session.commit(), reproducing the ordering defect without any new news tests.
  Local Windows reports a closed event loop / Proactor transport error; the Linux
  CI trace reports a Future attached to a different loop at the same pool checkout.
  This platform difference is retained in the before log, not presented as identical
  error text. Result: 1 failed, 2 passed in 24.95s.
- Fixed SHA-256 c4359e5a401f16a767cd345f24892b1f7aceab48d289739f4ed9521ad38b1e41:
  the identical three-test sequence passed in 5.56s. Migration statements,
  assertions, transaction boundaries and video product code remain unchanged.
- Own worktree runtime: Python 3.13.15, pytest 9.1.1, SQLAlchemy 2.1.3, asyncpg 0.32.0.
- Scoped Ruff and mypy passed; task validation passed for 2,397 files and
  git diff --check passed. Root independently reviewed the fixed test hash above
  and the same-sequence red-to-green evidence: PASS. Root owns the combined parent
  PR commit/push and subsequent new-head CI; no CI success is claimed for this
  uncommitted fix, and no merge or deployment is included.
