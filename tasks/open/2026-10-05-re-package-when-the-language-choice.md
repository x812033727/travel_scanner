---
id: 2026-10-05-re-package-when-the-language-choice
title: Re-package when the language choice no longer matches the upload package
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T00:30:05Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Re-package when the language choice no longer matches the upload package

## Why

Since `2026-10-04-reject-unselected-locales-in-video-publish`, the upload-package check
(`tools/video/package/check.mjs`) fails a package whose `metadata.json` `language_choice` differs
from the work directory's `languages.json`, or that holds a description, caption file, dub track
or language thumbnail of a locale the current choice does not have ("run package again"). That is
on purpose: a broader package from before must not pass as the current delivery.

The worker does not always write the package again when the choice changes. In
`tools/video/automation/flow.mjs` `languages()`, after `writeLanguages(...)`, a round with nothing
pending returns null (`if (!pending.length && zhNarrated) return null;`, and `channelLocale` is null
once zh-TW is packaged). So when the owner narrows the choice after a package was written (un-ticks
a locale whose parts were already made, or picks 只出繁體中文 for a video whose legacy package holds
translated locales), `upload/` keeps the old parts and the old `language_choice`. A later
`review-push --gate publish` then sends a failing package report, and the 可以上架 card waits on a
re-package nobody runs.

## Definition of done

- [ ] When the current choice differs from the upload package's `language_choice` (or the package holds parts the choice no longer has) and nothing is pending, the worker runs `captions` and `package` again once, so the next publish push carries an exact package.
- [ ] A choice that matches the package does not trigger a re-package (no loop, no new metadata hash every round).
- [ ] A tidied video (final.mp4 gone) is left to `tidiedLanguages` as today.

## Steps

- [ ] In `languages()`, before returning null for "nothing pending", compare `readLanguages(workdir).locales` with `upload/metadata.json`'s `language_choice` the way `check.mjs` does (dub chooses captions, zh-TW left out), or run the package check and look for its "another language choice" / "the language choice does not have" problems.
- [ ] If they differ, run `captions` then `package` (as the only-zh-TW branch does) and return a progress line; block on a failing exit as the other branches do.
- [ ] Add automation tests: a narrowed choice after package re-packages once; a matching choice does nothing.

## How to verify

`node --test tools/video/automation/automation.test.mjs tools/video/package/check.test.mjs`, then
`npm run test:tools`. Both scope files are bound in `docs/videos/long-form/review.json`, so
`node tools/video/long-form/cli.mjs check` turns red until an independent reviewer adds a
DURATION_ONLY increment; do not edit review.json yourself.

## Notes

- Found while doing `2026-10-04-reject-unselected-locales-in-video-publish`; that ticket's scope was only `tools/video/package/check.mjs` and its test.
- The normal order (package and publish push before the owner decides languages) is not affected: the first publish push then runs without `languages.json`, in legacy mode, and a package written after the decision carries the choice it was written for.
