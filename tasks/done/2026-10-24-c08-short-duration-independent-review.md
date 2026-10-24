---
id: 2026-10-24-c08-short-duration-independent-review
title: Independently bind C08 short duration review
status: done
priority: P2
area: tools
owner: codex-root-c08-duration-review
claimed_at: 2026-10-24T05:40:46Z
created_at: 2026-10-24T05:40:42Z
completed_at: 2026-10-24T05:42:36Z
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Independently bind C08 short duration review

## Why

PR #1811 changes four duration/lint files for the exact owner-approved C08 short-v8, making the independent 108-file DURATION_ONLY receipt stale. Recheck the final source bytes and update only those four bindings before the PR can pass the guarded video checks.

## Definition of done

- [x] The independent report explains the precise C08-only exception and its measured-body/final-cut limits.
- [x] The 108-file receipt matches all current files and the guarded CLI check passes.

## Steps

- [x] Read the four-file diff independently and rerun focused duration, lint and QA tests.
- [x] Rebind the four reviewed hashes and report hash without changing any other binding.
- [x] Run the guarded CLI and receipt tests; finish the task on the PR branch.

## How to verify

Use the bundled Node runtime: `node --test tools/video/core/duration.test.mjs tools/video/core/lint.test.mjs tools/video/qa/duration.test.mjs tools/video/long-form/review.test.mjs`; `node tools/video/long-form/cli.mjs check`; `npm run check:tasks`; `git diff --check`.

## Notes

At head `fe1838515e8c887bdde03aef57d5e6722daf6e05`, all 74 focused duration/lint/QA tests passed. The pre-rebind CLI reported only the four expected stale paths. The separate open PR #1664 also touches the common receipt and may need a later rebase; it has no active task-board claim for these paths. No paid media, production import or deployment is in scope.

Independent increment and raw SHA bindings now cover exactly four changed files. The guarded CLI and both receipt tests pass; `npm run check:tasks` validates 2,139 task files with pre-existing stale-claim warnings. C08's expanded spoken MoMA remains a measured-duration HOLD: its paper final estimate is about 301.63 seconds against the 300-second cap.
