---
id: 2026-09-28-malformed-episode-shorts-isolation
title: Keep malformed episode Shorts from blocking long videos
status: done
priority: P1
area: tools
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T10:14:12Z
created_at: 2026-09-28T10:13:48Z
completed_at: 2026-09-28T10:21:53Z
branch: codex/pr904-explainer-review
depends_on: []
scope:
  - tools/video/shorts/core.mjs
  - tools/video/shorts/episode.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/automation/automation.test.mjs
---

# Keep malformed episode Shorts from blocking long videos

## Why

PR #904 makes Shorts optional, but malformed model output such as `scenes: {}`
or `evidence: [null]` throws inside validation. That exception escapes the
worker's `saveShorts` call and interrupts the long video instead of adding a note.

## Definition of done

- [x] Malformed JSON collections and rows yield validation findings without throwing.
- [x] An invalid optional draft leaves the long video active and existing scripts intact.
- [x] Scoped tools tests and task checks pass; the repair is prepared for PR #904.

## Steps

- [x] Reproduce the crash with validator and worker regression cases.
- [x] Validate collection/row shapes before iteration and preserve rejection rules.
- [x] Run focused and affected tools checks, then finish this maintenance task.

## How to verify

Run Node tests for `tools/video/shorts/*.test.mjs` and
`tools/video/automation/automation.test.mjs`, then `npm run test:tools` and
`npm run check:tasks`. Record before/after results below.

## Notes

Claimed with `--force` under the owner's standing instruction to repair and merge
all PRs. This narrow review fix overlaps the author's Shorts implementation,
which is committed in ready PR #904; its remaining checklist item is a separate
real ffmpeg pilot, not implementation changes. No other local worktree uses the
author's branch, and its remote head was still `b9a01994` on inspection.
The author-owned pilot/implementation tasks are preserved. Recheck the remote
head before any normal fast-forward push; never force-push or replace new work.

Both new regression cases failed before the fix with `TypeError` from `validate`
through `episodeShortsProblems` and `Automation.saveShorts`. Afterward all 67
affected Shorts/automation tests passed. The full Windows tools run, serialized
with `--test-concurrency=1`, passed 531 tests with zero failures and one existing
platform skip. Task validation passed for 1,034 files; `git diff --check` passed.
Existing valid campaign/episode fixtures and evidence-binding checks remain intact.

Remote delivery waits for the existing PR run to finish and the current three-PR
update batch to advance. No paid narration, real-model acceptance, pilot rendering,
deployment or publication was performed by this fix.
