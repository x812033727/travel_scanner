---
id: 2026-09-14-workflow-pin-tests-use-file-url
title: Workflow pin tests use file URL paths on Windows
status: done
priority: P2
area: tools
owner: codex-ai-terms
claimed_at: 2026-09-14T06:21:12Z
created_at: 2026-09-14T06:19:41Z
completed_at: 2026-09-14T06:22:44Z
branch:
depends_on: []
scope:
  - tools/workflow-pins.test.mjs
---

# Workflow pin tests use file URL paths on Windows

## Why

The workflow-pin tests used a file URL pathname as a native path. On Windows this
produced `C:\\C:\\...travel_scan%E3%84%90`, so all three pin checks failed before reading workflows.

## Definition of done

- [x] All workflow-pin checks run successfully from the Windows checkout with a non-ASCII directory name.

## Steps

- [x] Decode the file URL using Node's fileURLToPath.
- [x] Run the full tools test suite: 39 passed.

## How to verify

`npm run test:tools` on Windows: 39 passed, 0 failed.

## Notes

The prior Actions pinning task had already merged in PR #472 and exact-main CI
34808942136 was green. Its stale review state was closed before claiming this scope.
The same two-line fix was initially checked before the failed claim was noticed;
it was reverted, the stale task was verified and closed, then this task was claimed
and the fix reapplied. No --force or unreviewed task takeover was used.
