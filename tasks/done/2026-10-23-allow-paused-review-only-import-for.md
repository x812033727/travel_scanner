---
id: 2026-10-23-allow-paused-review-only-import-for
title: Allow paused review-only import for everyday brand-story C series
status: done
priority: P1
area: api
owner: codex-c-series-integration
claimed_at: 2026-10-23T09:15:55Z
created_at: 2026-10-23T09:15:25Z
completed_at: 2026-10-23T11:12:06Z
branch: codex/everyday-story-review-import-20261023
depends_on: []
scope:
  - apps/api/app/video_automation/stories.py
  - apps/api/tests/test_video_story_import.py
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
---

# Allow paused review-only import for everyday brand-story C series

## Why

The owner asked for twenty C-series plans and eligible approved scripts in the video admin before PR consolidation. The current story importer makes new episodes `ready`; the production story worker could begin paid work. C03 already exists as a VideoProject under the same slug, so a naive import rejects it or risks duplication. This ticket provides a narrowly scoped, paused-series route with exact C03 reconciliation and keeps the older technology C-series validator intact.

## Definition of done

- [x] The exact everyday-reversals C01–C20 plan can validate without changing the 100-story bank's C=tech convention.
- [x] A paused story series can import its twenty plan rows, including the exact existing C03 project, without creating a new request or worker job.
- [x] Other video slug collisions remain rejected; dry-run and repeat apply report stable results.

## Steps

- [x] Limit C+everyday validation to the exact `brand-stories-everyday-reversals` series slug in JavaScript and Python.
- [x] Reconcile C03 only when slug, series and episode number match; preserve the existing project.
- [x] Add focused regression tests for paused import, collisions and idempotence.

## How to verify

`node --test tools/video/story-plans/plan.test.mjs`; `cd apps/api && uv run pytest tests/test_video_story_import.py`; `npm run check:tasks`; `git diff --check`. Before production apply, dry-run the exact reviewed `stories.json`; apply creates the absent series already paused in the same transaction as its planned rows. Read back the paused status and all twenty episode rows.

## Notes

2026-10-23: Production read-only API showed no everyday-reversals story series and one C03 VideoProject (`story-everyday-moleskine-c03`, series slug matches, episode 3, no YouTube ID). The existing importer marks new rows `ready`. This exact batch now creates its series paused and its episodes planned in one transaction; dry-run precedes apply, followed by readback of all rows and no new request. No production mutation has occurred.

Claim override rationale: the overlap reported task `2026-10-18-story-thumbnail-brand` was last claimed October 18, its branch is neither a local worktree nor an open PR, and its implementation landed in main as #1568. This task touches the same validators for a separate series-scoped change; the old task file was left untouched.

2026-10-23 live result: #1778 merged/deployed at `6f9aec8d1606829d81a3acfe926c8d303bb1b0d9`.
The first production dry-run and apply accepted 20 create rows with zero refusals;
database readback found 20 planned episodes, a paused series, and zero new requests.
A second exact-file dry-run and `--apply` both reported `create=0`, `update=0`,
`leave_alone=20`, `refuse=0`, `written=false`, with all C01–C20 unchanged.
