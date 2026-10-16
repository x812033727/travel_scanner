---
id: 2026-10-15-invalidate-story-checks-after-writer-lint
title: Invalidate story checks after writer lint repairs
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-15T16:02:33Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
---

# Invalidate story checks after writer lint repairs

## Why

The deployed story worker can ask the writer to repair chapter lint after a fact checker or listener has already changed that chapter. `fixChapterLint` calls `keepChapter(..., {keepRows: true})` and increments `lint_fixes`, but retains chapter `checked`/`listened` and global verification state. New narration can therefore inherit checks for older text. A01's real listener length holds exposed this path during the switchable-CC pilot; bounded manual repairs instead invalidated checks and reran the genuine stages.

## Definition of done

- [ ] A writer lint repair cannot advance using fact/listener or combined verification evidence for the preceding text.
- [ ] Relevant counters, durable runs, paid artifacts and historical reports remain preserved; unrelated chapters are not needlessly regenerated.
- [ ] Focused regression tests demonstrate a post-check writer edit requires fresh checks and cannot pass the pilot receipt gate using stale evidence.

## Steps

- [ ] Inspect `fixChapterLint`, `keepChapter`, `checkedIsSaved` and global verification/report lifecycle at current main.
- [ ] Invalidate affected downstream checks when the writer's changed chapter is saved, with regression coverage.
- [ ] Review report archival, restart and unchanged-output cases; run the focused story suite and repository checks affected by the fix.

## How to verify

Run `node --test tools/video/automation/story.test.mjs`, plus the affected tools/video checks. Add a case starting from a checked/listened chapter whose new lint repair changes narration and prove the next stage is fresh verification, not media or final approval. Inspect counters before/after and confirm old reports remain recoverable.

## Notes

Observed in live revision `aac8d73fb0e5f2321cf9d929c6ea52e001198b23`, `tools/video/automation/story.mjs` SHA-256 `f9825a7ce9649111d3e49ab33a2846a8be61111dd2cb2df40db3b68b974676f3`, around lines 1148-1158 and 1189-1208. No native writer lint repair was invoked by this session after finding the gap. No implementation changes or deployment are part of filing this follow-up. A01-specific work remains tracked by `2026-09-28-video-story-pilot`.
