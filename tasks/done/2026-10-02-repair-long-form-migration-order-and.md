---
id: 2026-10-02-repair-long-form-migration-order-and
title: Repair long-form migration order and review after main merge
status: done
priority: P1
area: tools
owner: codex-longform-continuation
claimed_at: 2026-10-02T00:04:54Z
created_at: 2026-10-02T00:04:40Z
completed_at: 2026-10-02T00:30:35Z
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - apps/api/migrations/versions/0117_video_min_8_minutes.py
  - apps/api/migrations/versions/0118_video_min_8_minutes.py
  - apps/api/tests/test_migration_0117_video_min_8_minutes.py
  - apps/api/tests/test_migration_0118_video_min_8_minutes.py
  - tools/video/long-form/review.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/thumbnail.test.mjs
  - docs/videos/long-form
---

# Repair long-form migration order and review after main merge

## Why

PR #1098 previously passed all eleven checks at 84f2775e. A later main merge produced 7c7a917b after Shorts #1097 landed its own 0117. Both duration and Shorts now point to 0116, causing schema and full-stack migration failures. Fifteen genuinely changed implementation files also invalidate the previous independent duration receipt; the web/tools checks correctly reject it.

## Definition of done

- [x] The duration migration is 0118 after the already-landed Shorts 0117, with one Alembic head and the same eight-minute setting backfill and downgrade behavior.
- [x] All 473 plans and preserved source packages retain their reviewed targets, decisions and hashes; actual-body QA, ten-minute defaults and fixture restrictions coexist with current main.
- [x] A genuine independent incremental review binds all 70 current files; stale or incomplete evidence remains rejected.
- [x] Appropriate local checks pass and the repaired candidate is ready for fresh PR CI; retain no-auto-merge until any separately authorized merge. Final CI acceptance is recorded against the actual pushed SHA in PR #1098.

## Steps

- [x] Preserve the remote merge by fast-forwarding; identify schema/migration and stale-review failures from full job logs.
- [x] Rename only the unmerged duration migration/test to 0118 and attach it to 0117_video_shorts_topics; update exact review-registry paths and parent regression.
- [x] Review all changed bindings independently, install the genuine report and refresh the receipt mechanically.
- [x] Run schema/migration, catalog, duration/worker/production regressions and task validation; preserve submitted peer history for a normal push. Fresh CI verification follows delivery and is recorded in the PR.

## How to verify

In apps/api run `uv run alembic heads`, `uv run pytest tests/test_schema.py tests/test_migration_sql_dialect.py tests/test_migration_0118_video_min_8_minutes.py -q`, ruff and mypy. Run the long-form CLI, duration/planning/review/worker tests, all second-season validators, `npm run test:tools` and `npm run check:tasks`. Inspect api, web, containers and full-stack-smoke on the final pushed SHA; actual PostgreSQL migration/rollback tests run in CI.

## Notes

Initial main was 14970711; remote PR1098 was 7c7a917b with parents 84f2775e and main. The merge message explicitly left independent evidence stale, correctly requiring a new reviewer instead of invented replacement hashes. Shorts #1097 is already merged, so its migration and completed ticket are not changed. The new ticket claim is uncontested and changes stay in its declared narrow scopes. User .codex/environments is preserved. The PR is now non-draft (changed outside this session), and its existing no-auto-merge label is retained. No PR merge, production write, paid media generation or publication occurs in this repair.

While reviewing, remote advanced to d7145a2e, incorporating the peer's same 0118 migration renumbering. Local work is committed and that submitted history is merged without overwriting it; all 70 reviewed working bytes remain unchanged. Main then landed #1100 at a8f0833e. The scope is extended for its existing QA CLI/thumbnail regression integration before any conflict edits; review must preserve the current-body context and both duration rules alongside localized-thumbnail checks. Other upstream files are imported unchanged as main history, not hand-edited or separately claimed.

Final genuine DURATION_ONLY review by review_longform is PASS with report SHA dc6492c76d66fe9d9067703dc211d1aa96488772f4c16c87a5a7601b60a69cc4, all 70 exact current bindings. The reviewer confirms mechanical installation and independently reruns 19 tests plus CLI473. Root checks: sole 0118 head; schema/migration 10 passed/1 PostgreSQL skip; API ruff and mypy 452 app/344 test files; 192 worker/duration/production regressions; all ten season-two validators; 59 thumbnail/integration regressions; complete tools 1,149 passed/2 skipped/0 failed; tasks 1,277 valid. All exits are 0. Main-sync-validation.md records the evidence and remaining-stages.md links the eight existing next-stage tickets without taking another owner's work.

Remote subsequently added 56815409's independent report for the earlier main merge. That commit is retained in merged Git history; the currently installed genuine report also covers the latest thumbnail QA bytes and the explicit parent assertion. Local delivery is complete; the final normal push and fresh CI acceptance are tracked on PR #1098. CI skips locally are not actual PostgreSQL acceptance, and no actual media or publication is asserted.
