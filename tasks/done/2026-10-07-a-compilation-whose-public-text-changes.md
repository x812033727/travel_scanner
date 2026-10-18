---
id: 2026-10-07-a-compilation-whose-public-text-changes
title: A compilation whose public text changes after its upload package is written sends the old package
status: done
priority: P3
area: tools
owner: claude-opus-5-5-compilation-package
claimed_at: 2026-10-18T10:31:32Z
created_at: 2026-10-07T14:10:00Z
completed_at: 2026-10-18T10:37:45Z
branch:
depends_on:
  - 2026-10-07-a-re-planned-compilation-keeps-the
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
  - tools/video/automation/compilation-spoilers.test.mjs
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

- [x] Before the publish push, a compilation whose `composeMetadata` or thumbnail differs from what
  `upload/` holds is packaged again, without touching one already past its upload.

## Steps

- [x] Run `package` again at "on YouTube" (not when the upload is past, as `flow.mjs` `languages`
  guards with `pastUpload`) when the composed metadata or the thumbnail differs, for every
  compilation, not only one with mysteries.
- [x] A test: plan again after "upload package written" with a new title; the package is written
  again before the publish confirmation.

## How to verify

`node --test tools/video/automation/compilation.test.mjs tools/video/automation/compilation-spoilers.test.mjs`.

## Notes

- Probe: the compilation review's scratch copy `review-comp/pkg-replan`.
- The same final.mp4-only binding affects every video type (an episode whose title is edited
  after its package); this task is the compilation's.

### 2026-10-17 done (claude-opus-5-5-compilation-package)

- `repackageStale` in `compilation.mjs` is the old mysteries-only comparison, moved into a
  function and extended to the thumbnail: upload/ is packaged again when its title, description,
  tags, localizations, chapters or default language differ from what `composeMetadata` gives
  now, or when the rendered `thumbnail.jpg` differs from upload/'s copy.
- It now runs at "on YouTube" for every compilation. A compilation with mysteries also keeps
  the old check when nothing is left (`next` null). Without mysteries, a video past its upload
  is left alone, as the ticket asked.
- Tests (`compilation-spoilers.test.mjs`): a compilation without mysteries planned again with a
  new title, then given a new thumbnail, is packaged again each time; at "upload package" and
  past its upload it is not. The end-to-end test's fake `package` now writes the composed fields,
  as the real one does, so a current package goes straight on to the publish push.
- Not done here: the same final.mp4-only binding for other video types (Notes).
