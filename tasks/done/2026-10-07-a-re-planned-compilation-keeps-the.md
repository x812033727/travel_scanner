---
id: 2026-10-07-a-re-planned-compilation-keeps-the
title: A re-planned compilation keeps the translations of its previous title and description
status: done
priority: P3
area: tools
owner: claude-opus-5-5-comp-i18n
claimed_at: 2026-10-07T13:21:48Z
created_at: 2026-10-07T10:30:00Z
completed_at: 2026-10-07T15:35:01Z
branch:
depends_on: []
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
  - tools/video/automation/compilation-spoilers.test.mjs
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
    YouTube translated and packaged again on the worker's next round. A re-plan reaches such a
    file all the same: see the review below (`stampLegacyTranslations`).
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
- Review (2026-10-07, two lenses, each finding verified):
  - Fixed, should-fix: a compilation's language batch looped. `i18n-merge` keys a compilation's
    chapters and their hashes by card scene id, so the merged file read as stale, the worker
    translated it again, and the next language round merged it again. Chapter hashes are now
    compared only when they are recorded by episode slug (`compilationTranslationStale`); the
    title, description and tags still are, since i18n-merge records them the same way. The batch
    itself (the lost localized chapter names, the thumbnail hint that points a compilation at
    i18n-merge, and captions that never finish because a compilation's timeline has
    `speech_hash: null`) predates this task and is `2026-10-07-a-compilation-s-language-batch-fights`.
    The same fix keeps the owner's thumbnail words when they follow that hint.
  - Fixed, should-fix: a legacy file merged with captions alone has `source_hashes: { chapters: {} }`
    and read as stale. A file is legacy now when it records no hash of its title, description or
    tags, as `metadataStatus` reads it.
  - Fixed, should-fix: the worker's own re-plan (the zh-TW verifier's word after the cut is joined
    again, a deleted manifest, an owner's reset) did not reach a legacy file, and render's refusal
    covers only the re-plan it advises. `planMetadata` now stamps each legacy translation with the
    hashes of the plan it replaces (`stampLegacyTranslations`) when the text changed, so it reads
    as stale and is translated again; one never planned again still counts as complete.
  - Fixed, nit: a chapter title alone made from earlier text reopened the step but lint and qa said
    nothing (`lintCompilation` keys chapters by card). `lintProject` adds "translations older than
    the zh-TW text: chapter <slug>" from the worker's record. The step's note says "made from
    earlier zh-TW text" and shows when every locale is stale too, not only some.
  - Fixed, nit (tests): the mysteries path and the legacy verifier re-plan are now tests in
    `compilation-spoilers.test.mjs` (added to the scope; it is not bound by the receipt), the flow
    test checks lint against status, and its last assertion says what it pins.
  - Not a defect of this task: a compilation planned again after its package was written keeps
    the old package (the package is bound to final.mp4 alone, and only a compilation with
    mysteries is packaged again). It predates this task: `2026-10-07-a-compilation-whose-public-text-changes`.
  - Mutations of each fix (no stamping, legacy read only when the hashes are absent, card chapters
    compared, no lint warning, the note hidden when all are stale, the title hashed differently,
    a mysteries compilation keeping a stale file) each fail a test.
- Duration re-bind (2026-10-07, independent reviewer `claude-pr-review-comp-i18n`): PASS,
  duration-only, committed as fc0c5497. Non-compilation lint is untouched; a compilation's lint
  gains only a warning; given the document "metadata translated" can only go from done to not done,
  and no other step changed (a differential run over every repository video.json and 3,000 seeded
  compilations). It noted that the new chapter warning appears only when lint has no errors, unlike
  `lintCompilation`'s own `i18n/` warnings; harmless, left as is.
