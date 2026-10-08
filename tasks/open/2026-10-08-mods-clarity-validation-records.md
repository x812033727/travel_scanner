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

- [ ] Repository documentation uses portable path placeholders without weakening the hygiene guard.
- [ ] An independent reviewer verifies and binds both changed duration-covered files.
- [ ] Relevant local checks pass and current-head CI results are recorded.

## Steps

- [x] Read failed CI logs and reproduce the two recorded causes.
- [x] Replace five host-specific path references with `<home>`.
- [ ] Obtain independent incremental duration review, then rerun checks and CI.

## How to verify

Run `node --test tools/repo-hygiene.test.mjs tools/video/long-form/review.test.mjs`, `node tools/video/long-form/cli.mjs check`, and `npm run check:tasks`. Check the new PR head's CI runs after pushing.

## Notes

CI at 6895b1f5b reported only the hygiene guard and stale duration bindings in web-checks. The shared review files also receive an independent one-file Windows-test increment in a separate managed worktree; the same reviewer will handle these sequentially against each branch's verified baseline. No other PR branch is modified. Keep both increments if they later meet on main. No production deployment or media publication is part of this task.
