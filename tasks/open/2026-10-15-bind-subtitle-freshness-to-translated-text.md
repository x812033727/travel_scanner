---
id: 2026-10-15-bind-subtitle-freshness-to-translated-text
title: Bind subtitle freshness to translated text and dub timing
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-15T11:41:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/stages.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/package/cli.mjs
  - tools/video/dubs/captions-package.test.mjs
---

# Bind subtitle freshness to translated text and dub timing

## Why

A package can reuse subtitles that were generated before a translated sentence or its dub timing changed. captionsCurrent currently checks narration speech_hash, branding_hash and the chosen locale set, but does not compare translated text or the current dub timeline. runCaptions records cue counts/problems/timing without those source bindings. A new current dub can therefore be packaged beside subtitles cut for the previous text or voice timing.

## Definition of done

- [ ] Packaging regenerates a locale's captions when its translated text or dub timeline changes, including the transition from narration timing to dub timing.
- [ ] Unchanged inputs can reuse current captions; older manifests without sufficient bindings safely regenerate.
- [ ] Focused regression tests prove subtitle text and cue times correspond to the current translation and current dub, not just the locale set.

## Steps

- [ ] Inspect captionsCurrent in tools/video/package/cli.mjs and runCaptions in tools/video/core/stages.mjs; choose deterministic content/timing provenance.
- [ ] Add the bindings and compare them before reuse; cover a translated-line change, a new/replaced dub and unchanged-input reuse.

## How to verify

Run node --test tools/video/core/stages.test.mjs tools/video/dubs/captions-package.test.mjs and the affected package tests, then npm run test:tools and npm run check:tasks. The tests should first reproduce the stale-caption reuse, then verify the regenerated SRT text and time ranges.

## Notes

Observed during Curio H09 multilingual delivery on 2026-10-15, branch codex/curio-h09-earhart-20261015. Read-only audit located captionsCurrent at package/cli.mjs:50 and its reuse decision near line188; runCaptions records locale manifest entries near core/stages.mjs:233. H09 explicitly runs captions after all current dubs finish and manually checks each locale's problems and timing before packaging. This ticket is unclaimed; no shared tool implementation was changed in the production task.
