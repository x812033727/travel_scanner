---
id: 2026-10-02-repair-long-form-migration-order-and
title: Repair long-form migration order and review after main merge
status: in-progress
priority: P1
area: tools
owner: codex-longform-continuation
claimed_at: 2026-10-02T00:04:54Z
created_at: 2026-10-02T00:04:40Z
completed_at:
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - apps/api/migrations/versions/0117_video_min_8_minutes.py
  - apps/api/migrations/versions/0118_video_min_8_minutes.py
  - apps/api/tests/test_migration_0117_video_min_8_minutes.py
  - apps/api/tests/test_migration_0118_video_min_8_minutes.py
  - tools/video/long-form/review.mjs
  - docs/videos/long-form
---

# Repair long-form migration order and review after main merge

## Why

PR #1098 previously passed all eleven checks at 84f2775e. A later main merge produced 7c7a917b after Shorts #1097 landed its own 0117. Both duration and Shorts now point to 0116, causing schema and full-stack migration failures. Fifteen genuinely changed implementation files also invalidate the previous independent duration receipt; the web/tools checks correctly reject it.

## Definition of done

- [ ] The duration migration is 0118 after the already-landed Shorts 0117, with one Alembic head and the same eight-minute setting backfill and downgrade behavior.
- [ ] All 473 plans and preserved source packages retain their reviewed targets, decisions and hashes; actual-body QA, ten-minute defaults and fixture restrictions coexist with current main.
- [ ] A genuine independent incremental review binds all 70 current files; stale or incomplete evidence remains rejected.
- [ ] Appropriate local checks pass and the repaired PR head receives fresh CI; retain no-auto-merge until any separately authorized merge.

## Steps

- [x] Preserve the remote merge by fast-forwarding; identify schema/migration and stale-review failures from full job logs.
- [x] Rename only the unmerged duration migration/test to 0118 and attach it to 0117_video_shorts_topics; update exact review-registry paths and parent regression.
- [ ] Review all changed bindings independently, install the genuine report and refresh the receipt mechanically.
- [ ] Run schema/migration, catalog, duration/worker/production regressions and task validation; push without overwriting another author's update and inspect the final CI results.

## How to verify

In apps/api run `uv run alembic heads`, `uv run pytest tests/test_schema.py tests/test_migration_sql_dialect.py tests/test_migration_0118_video_min_8_minutes.py -q`, ruff and mypy. Run the long-form CLI, duration/planning/review/worker tests, all second-season validators, `npm run test:tools` and `npm run check:tasks`. Inspect api, web, containers and full-stack-smoke on the final pushed SHA; actual PostgreSQL migration/rollback tests run in CI.

## Notes

Main is 14970711; remote PR1098 is 7c7a917b with parents 84f2775e and main. The merge message explicitly leaves independent evidence stale, correctly requiring a new reviewer instead of invented replacement hashes. Shorts #1097 is already merged, so its migration and completed ticket are not changed. The new ticket claim is uncontested; changes stay in its six narrow scopes. User .codex/environments is preserved. The PR is now non-draft (changed outside this session), and its existing no-auto-merge label is retained. No merge, production write, paid media generation or publication occurs in this repair.
