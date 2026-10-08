---
id: 2026-10-08-mods-clarity-validation-records
title: Repair Mods clarity draft validation records
status: in-progress
priority: P1
area: docs
owner: codex-mods-validation
claimed_at: 2026-10-08T16:51:27Z
created_at: 2026-10-08T16:51:24Z
completed_at:
branch: codex/mods-clarity-20261009
depends_on: []
scope:
  - docs/videos/claude-code-mods-no-sandbox-before-install/revision-review.md
  - tasks/done/2026-10-08-mods-tutorial-clarity.md
  - tasks/open/2026-10-08-mods-tutorial-revision-production.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Repair Mods clarity draft validation records

## Why

PR #1390 CI found host-specific paths in new documentation and stale duration-review bindings for the changed teaching prompts and automated-route reference. These are omissions in the source handoff, separate from the two Windows runtime failures.

## Definition of done

- [x] Repository documentation uses portable path placeholders without weakening the hygiene guard.
- [x] An independent reviewer verifies and binds both changed duration-covered files.
- [x] Relevant local checks pass.
- [ ] Current-head Linux CI results are recorded.

## Steps

- [x] Read failed CI logs and reproduce the two recorded causes.
- [x] Replace five host-specific path references with `<home>`.
- [x] Obtain independent incremental duration review for both changed bindings.
- [x] Verify local hygiene, prompts, receipt tests and all long-form plans.
- [ ] Record Linux CI results for the pushed PR head before closing this task.

## How to verify

Run `node --test tools/repo-hygiene.test.mjs tools/video/long-form/review.test.mjs`, `node tools/video/long-form/cli.mjs check`, and `npm run check:tasks`. Check the new PR head's CI runs after pushing.

## Notes

CI at 6895b1f5b reported only the hygiene guard and stale duration bindings in web-checks. The shared review files also receive an independent one-file Windows-test increment in a separate managed worktree; the same reviewer will handle these sequentially against each branch's verified baseline. No other PR branch is modified. Keep both increments if they later meet on main. No production deployment or media publication is part of this task.

Local verification completed on Windows ARM64 with bundled Node v24.19.0:

- Portable-path repair: `aabb920dbf11c230a4736c5c3d53bf32ea634ca7`; repository hygiene tests passed 3/3 without changing the guard.
- Independent duration receipt: `81184d531f970bd394a39f2bde39df4dd37a2d87`; the reviewer verified all 108 baseline bindings against `c6454463d0eb53e4c8166be0b93a587598c03208`, rebound only the automated-route reference and prompts, and preserved the other 106 bindings and prior increments.
- `tools/video/automation/prompts.test.mjs`: 23/23 passed.
- `tools/video/long-form/review.test.mjs`: 2/2 passed.
- `tools/video/long-form/cli.mjs check`: PASS for all 473 plans, preserving 600/780-second targets, 480-second measured floors, source hashes and covered status.

These are local results, not Linux CI acceptance. PR #1390 remains a draft, and this task stays in progress until the current pushed head's CI outcome is verified. The independent Windows runtime fixes belong to their separate branch and task.
