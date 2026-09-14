---
id: 2026-09-14-fix-windows-workflow-pin-test-file
title: Fix Windows workflow pin test file URL resolution
status: done
priority: P2
area: tools
owner: codex-gemini-series
claimed_at: 2026-09-14T07:43:36Z
created_at: 2026-09-14T07:37:16Z
completed_at: 2026-09-14T07:55:08Z
branch:
depends_on:
  - 2026-09-13-pin-actions-and-dependency-updates
scope:
  - tools/workflow-pins.test.mjs
---

# Fix Windows workflow pin test file URL resolution

## Why

`npm run test:tools` fails on Windows in both workflow-pin tests because `new URL(...).pathname` is passed to Node filesystem functions. The drive prefix becomes `C:\\C:\\...` and the non-ASCII workspace name stays percent-encoded, so readdirSync reports ENOENT before any workflow is checked. Discovered during Gemini series validation on Node 24.13.0, 2026-09-14.

## Definition of done

- [x] Workflow-pin tests find the real workflow directory on Windows and continue passing on Linux.

## Steps

- [x] Coordinate with the active upstream task before editing its scope.
- [x] Resolve the file URL with `fileURLToPath` and run the focused suite.

## How to verify

`node --test tools/workflow-pins.test.mjs` and `npm run test:tools` on Windows, plus existing Linux CI.

## Notes

The Gemini release-tool suite passed all eight tests. The separate failure predates the series changes. Subsequently verified PR #472 merged at 2026-09-14T05:15:09Z as 24af149062dd99aad3f4c2bb16cea70f8edf164c (the current checkout base). Archived its stale review ticket. Another worktree still advertises that completed claim, so reclaimed this narrow follow-up with --force using the verified merge evidence. The fix uses Node's fileURLToPath; all 39 tool tests now pass on Windows.

Latest main independently includes the same fileURLToPath correction; retained it during integration. No additional workflow behavior change is needed.
