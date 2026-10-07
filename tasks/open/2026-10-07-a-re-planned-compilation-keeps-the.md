---
id: 2026-10-07-a-re-planned-compilation-keeps-the
title: A re-planned compilation keeps the translations of its previous title and description
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-comp-i18n
claimed_at: 2026-10-07T13:21:48Z
created_at: 2026-10-07T10:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# A re-planned compilation keeps the translations of its previous title and description

## Why

The worker plans a compilation's public text in "metadata planned"
(`tools/video/automation/compilation.mjs` `planMetadata`: title, description, tags, thumbnail
headline, and sometimes chapter titles), then translates it in "metadata translated"
(`translateMetadata`, one translator call per locale into `docs/videos/<slug>/i18n/<locale>.json`).

When the metadata is planned again, the translations are not. A second plan happens when
`keyframes/manifest.json` is deleted, which render advises when the thumbnail source and its
episode keyframe both changed, or when an owner resets the step. Then:

- `translateMetadata` skips an existing translation that passes `translationProblem` when the
  compilation has no mysteries;
- `core/state.mjs` counts "metadata translated" done whenever `translationComplete` holds, and
  that only checks that the fields are present;
- compilation translations carry no `source_hashes`, so `metadataStatus` reads them as `unknown`
  rather than `stale`, lint warns nothing, and QA's captions item passes.

The review of `2026-10-07-render-tells-a-compilation-to-run` reproduced it. After a re-plan,
`video.json` said 企劃第2版標題 while `i18n/ja.json` still said ja of「企劃第1版標題」, and the
package would ship those localized titles and descriptions for a title that no longer exists.

## Definition of done

- [x] A compilation translation made from an earlier title, description, tags or chapter titles
  is stale. "metadata translated" is not done while any locale is stale, and the worker
  translates it again.

## Steps

- [x] Record the source text's hash in each compilation translation when `translateMetadata`
  writes it, as the episode translations do (`source_hashes`).
- [x] Count a translation whose recorded hash differs from the current source as not complete
  in `core/state.mjs`, and have `translateMetadata` redo it instead of skipping it.
- [x] Tests: a re-plan after "metadata translated" reopens the step and the worker translates
  each locale again; an unchanged plan keeps its translations.

## How to verify

`node --test tools/video/automation/compilation.test.mjs tools/video/core/state.test.mjs`, then
`node tools/video/long-form/cli.mjs check` (`core/state.mjs` and `state.test.mjs` are bound by
the duration receipt and need the independent re-bind).

## Notes

- Found by the review of `2026-10-07-render-tells-a-compilation-to-run` (2026-10-07). That
  task's refusal now tells the owner to delete the compilation's `i18n/*.json` along with the
  manifest, which covers its own path. This task closes the gap for any re-plan.
- 2026-10-07 (claude-opus-5-5-comp-i18n):
  - `core/state.mjs` has `compilationChapters(doc)` (the chapter titles the translator is given,
    by episode slug, else 「第 N 集」; `automation/compilation.mjs` used to build them itself as
    `chaptersOf`) and `compilationSourceHashes(doc)`: the title, description and tags hashed as
    `core/translations.mjs` `sourceHashes` hashes them (tags as one ordered list), and each chapter
    title by episode slug.
  - `translateMetadata` writes those hashes into each translation (`source_hashes`), and keeps an
    existing translation only when `translationComplete(existing, video)` holds.
  - `translationComplete(translation, doc)`: given the document, a translation whose recorded
    hashes differ from the current ones is not complete, so "metadata translated" reopens and the
    worker translates that locale again. The step's note says "missing, incomplete or made from
    an earlier title". Without a document it is the field check it was.
  - Decided: a translation written before the hashes were kept (none recorded) still counts as
    complete. Requiring hashes would have every compilation already translated, packaged or on
    YouTube translated and packaged again on the worker's next round. The cost is that such a
    legacy translation is not caught by a re-plan; render's refusal (render/cli.mjs `replan`)
    still tells the owner to delete `i18n/*.json` with the manifest, which covers that case, so
    it is left as it is.
  - Lint: `lintCompilation` reads the title, description and tags through `metadataStatus`, so a
    stale translation now warns "translations older than the zh-TW text" instead of nothing.
- Tests, each failing on the old code or under a mutant:
  - `compilation.test.mjs`, the worker's whole compilation flow: each translation records the
    text it was made from; a new title and description after "metadata translated" makes the
    worker translate each locale once more with the new title, and nothing is translated again
    after that to the end of the flow.
  - `state.test.mjs`: `translationComplete` with the document for a new title, description, tag
    order, chapter title and 「第 N 集」 number, a legacy translation, and the step's note on disk.
  - Mutations (a stale translation kept, no hashes written, the document ignored, chapters not
    hashed, a legacy translation counted stale, the status not given the document) each fail a
    test.
