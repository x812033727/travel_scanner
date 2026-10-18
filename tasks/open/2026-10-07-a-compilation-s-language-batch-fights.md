---
id: 2026-10-07-a-compilation-s-language-batch-fights
title: A compilation's language batch fights the worker's own translations and never finishes
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
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/i18n/cli.mjs
  - tools/video/i18n/i18n.test.mjs
  - tools/video/core/translations.mjs
  - tools/video/core/stages.mjs
  - tools/video/core/state.test.mjs
---

# A compilation's language batch fights the worker's own translations and never finishes

## Why

A compilation's titles, descriptions, tags and chapter titles are the worker's own
(`tools/video/automation/compilation.mjs` `translateMetadata`, chapters keyed by episode slug). The
language panel on /admin/videos is shown for compilations too, and `flow.mjs` `languages()` runs
the owner's ticked parts through `i18n-sheet` and `i18n-merge` like an episode's. Found by the
review of `2026-10-07-a-re-planned-compilation-keeps-the` (2026-10-07), with probes through the
real worker:

- `i18n/cli.mjs` `mergeSheet` keys a compilation's `chapters` and `source_hashes.chapters` by the
  card scene ids (`chapterScenes`), and drops the slug-keyed chapter titles the worker wrote, so
  the localized chapter names are lost (`composeMetadata` falls back to the zh-TW titles).
  `2026-10-07-a-re-planned-compilation-keeps-the` compares chapter hashes only when they are keyed
  by slug, so this no longer reopens "metadata translated" in a loop, but the names are still lost.
- `core/translations.mjs` `thumbnailGap` tells the owner to run `i18n-sheet --parts metadata`
  then `i18n-merge` for a compilation's thumbnail words (UPLOAD.md), which is the path above.
- `core/stages.mjs` `runCaptions` refuses a compilation's timeline ("timeline.json was built for an
  older script; run tts again"): compile writes `speech_hash: null`. So any ticked part of a
  compilation's language batch ends blocked at `captions`, and `ready_to_upload` stays false.

## Definition of done

- [ ] A compilation's language batch leaves the worker's titles, descriptions, tags and chapter
  titles alone, and a ticked caption locale finishes or says plainly why it cannot.
- [ ] Following the thumbnail hint for a compilation keeps its slug-keyed chapter titles.

## Steps

- [ ] In `flow.mjs` `languages()`, skip the metadata part for a compilation (translateMetadata
  owns it), or have `i18n-sheet`/`i18n-merge` key a compilation's chapters by episode slug.
- [ ] Decide what a compilation's captions are (the episodes' captions joined, or none) and make
  `runCaptions` either build them or refuse with a reason the owner can act on.
- [ ] Point `thumbnailGap`'s hint for a compilation at a path that keeps its chapters.

## How to verify

`node --test tools/video/automation/automation.test.mjs tools/video/i18n/i18n.test.mjs
tools/video/automation/compilation.test.mjs`. `flow.mjs` and `automation.test.mjs` are bound by
the duration receipt and need the independent re-bind.

## Notes

- Probes: the compilation review's scratch copies `review-comp/loop-new` (the language batch
  loop on 0f0d1106) and `review-comp/refute-i18n` (the owner following the thumbnail hint).
