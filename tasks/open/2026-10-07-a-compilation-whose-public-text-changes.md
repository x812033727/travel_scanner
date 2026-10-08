---
id: 2026-10-07-a-compilation-whose-public-text-changes
title: A compilation whose public text changes after its upload package is written sends the old package
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T14:10:00Z
completed_at:
branch:
depends_on:
  - 2026-10-07-a-re-planned-compilation-keeps-the
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
---

# A compilation whose public text changes after its upload package is written sends the old package

## Why

The "upload package" step is bound to final.mp4 only (`core/state.mjs`). A compilation planned
again after its package was written (an owner's reset, or `keyframes/manifest.json` deleted) keeps
a byte-identical final.mp4 when its cards did not change, so the final approval and the package
stay done, and `upload/metadata.json` and `description.<locale>.txt` keep the old zh-TW title and
the old localizations, though the worker translated the new ones
(`2026-10-07-a-re-planned-compilation-keeps-the`). The only comparison with `composeMetadata` that
packages again (`automation/compilation.mjs` `advanceCompilation`, at "on YouTube") runs only for
a compilation whose series has mysteries. Found by the review of that task (2026-10-07); it
predates it.

## Definition of done

- [ ] Before the publish push, a compilation whose `composeMetadata` or thumbnail differs from what
  `upload/` holds is packaged again, without touching one already past its upload.

## Steps

- [ ] Run `package` again at "on YouTube" (not when the upload is past, as `flow.mjs` `languages`
  guards with `pastUpload`) when the composed metadata or the thumbnail differs, for every
  compilation, not only one with mysteries.
- [ ] A test: plan again after "upload package written" with a new title; the package is written
  again before the publish confirmation.

## How to verify

`node --test tools/video/automation/compilation.test.mjs tools/video/automation/compilation-spoilers.test.mjs`.

## Notes

- Probe: the compilation review's scratch copy `review-comp/pkg-replan`.
- The same final.mp4-only binding affects every video type (an episode whose title is edited
  after its package); this task is the compilation's.
