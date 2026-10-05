---
id: 2026-10-05-re-package-when-the-language-choice
title: Re-package when the language choice no longer matches the upload package
status: done
priority: P2
area: tools
owner: claude-opus-5-5-flow-stop-and-repackage
claimed_at: 2026-10-05T12:26:26Z
created_at: 2026-10-05T00:30:05Z
completed_at: 2026-10-05T13:38:50Z
branch: claude/flow-stop-and-repackage
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

- [x] When the current choice differs from the upload package's `language_choice` (or the package holds parts the choice no longer has) and nothing is pending, the worker runs `captions` and `package` again once, so the next publish push carries an exact package.
- [x] A choice that matches the package does not trigger a re-package (no loop, no new metadata hash every round).
- [x] A tidied video (final.mp4 gone) is left to `tidiedLanguages` as today.
- [x] A video past its upload confirmation (status `done`, or on YouTube) is never re-packaged for a changed choice, so a package that can no longer be written never blocks a published video (review fix, 2026-10-06).

## Steps

- [x] In `languages()`, before returning null for "nothing pending", compare `readLanguages(workdir).locales` with `upload/metadata.json`'s `language_choice` the way `check.mjs` does (dub chooses captions, zh-TW left out), or run the package check and look for its "another language choice" / "the language choice does not have" problems.
- [x] If they differ, run `captions` then `package` (as the only-zh-TW branch does) and return a progress line; block on a failing exit as the other branches do.
- [x] Add automation tests: a narrowed choice after package re-packages once; a matching choice does nothing.

## How to verify

`node --test tools/video/automation/automation.test.mjs tools/video/package/check.test.mjs`, then
`npm run test:tools`. Both scope files are bound in `docs/videos/long-form/review.json`, so
`node tools/video/long-form/cli.mjs check` turns red until an independent reviewer adds a
DURATION_ONLY increment; do not edit review.json yourself.

## Notes

- Found while doing `2026-10-04-reject-unselected-locales-in-video-publish`; that ticket's scope was only `tools/video/package/check.mjs` and its test.
- The normal order (package and publish push before the owner decides languages) is not affected: the first publish push then runs without `languages.json`, in legacy mode, and a package written after the decision carries the choice it was written for.
- Done 2026-10-05 (claude-opus-5-5-flow-stop-and-repackage, branch
  `claude/flow-stop-and-repackage`, with 2026-10-05-the-worker-passes-over-a-video and
  2026-10-05-a-narration-retake-a-stop-file in the same two files).
- How: `packageChoiceStale(workdir)` in `flow.mjs` runs the package check's own pure
  `checkPackage()` over `listFiles(upload/)` and metadata.json with the locales
  `packageLocalesWanted()` gives (exported from `tools/video/package/check.mjs`, so the rules are
  that file's, dub-chooses-captions and zh-TW left out included), with the final's hashes left
  out so final.mp4 is never hashed, and reads only the two choice problems ("written for another
  language choice", "the language choice does not have"). `readPackageReport` was not used
  because it hashes final.mp4 every round for every finished video. False without metadata.json
  (the package is written later, with the choice), without a choice, or with a metadata.json that
  cannot be parsed or whose fields have the wrong types (a `captions` that is a number makes
  `checkPackage()` throw a TypeError): the whole read is in one try, and an unknown answer is
  "not stale", so this new read never crashes `auto`.
- In `languages()` both "nothing pending" returns (the zh-TW one and `!channel`) now fall through
  to the existing only-zh-TW branch when the package is stale: thumbnails, `captions`, `package`,
  a block on a failing exit, and the line "upload package written again for the current language
  choice". No batch and no review-push: nothing is in the making. A package that `package` wrote
  passed this same check, so the next round finds it current; the test shows the next round runs
  nothing and metadata.json keeps its bytes. The tidied path is untouched: `tidiedLanguages`
  still returns before, and the tidied test now also narrows the choice after the tidy and sees
  no command run.
- For a video still waiting on its publish confirmation, the rewritten metadata.json has a new
  hash, so the next round's `decision(state, "publish", …)` finds no review for it and pushes
  the publish gate again with the exact package (the existing "on YouTube" step).
- A legacy package (written before the owner decided, `language_choice: null`) that holds only
  zh-TW passes the strict check for 只出繁體中文 and is left alone, so the existing "byte for
  byte as before" test is unchanged; one that holds a translated locale is written again.
- Only before the upload confirmation (review fix, 2026-10-06). The first version also ran for
  videos whose status is `done`; a narrowed choice on a published video then ran `captions` and
  `package` on its own after deploy, and where the package could no longer be written (final.mp4's
  checks older than the script, after the speech hash moved) `package` failed and blocked the done
  video, which the owner's retry returned to done and the next round blocked again. Past the
  confirmation the package already went up with the publish review and nothing pushes the publish
  gate again, so `languages()` now asks `packageChoiceStale()` only when `pastUpload(state)` is
  false. `pastUpload` is the notion `restyle` already used (`state.youtube_video_id` or status
  `done`, which the approved publish review sets), now one helper both read. A stale package on
  such a video is left as it went up, without a log line (it would repeat every round).
- Tests: "a choice narrowed before the upload, …" (`finishedVideo({ confirmed: false })` keeps
  the publish review pending, so the video is still active: it re-packages once, the publish gate
  goes up with the exact package, then the round returns null with no command run); "a choice
  narrowed after the upload confirmation …" (status done, then on YouTube: null every round, no
  command, still done, metadata.json byte for byte); "an upload metadata.json whose fields have
  the wrong types …" (`captions: 5`: null, no command, still active; the same file with the right
  types is written again). Dropping the `pastUpload` guard turns the second red; catching only
  `SyntaxError` turns the third red with the TypeError.
- Not fixed here: `readPackageReport()` in `tools/video/package/check.mjs` throws the same
  TypeError on such a metadata.json, and `auto` runs `review-push` in process. Only a hand-edited
  metadata.json can be like that (`package` writes a list); filed as
  `2026-10-05-the-upload-package-check-throws-on` (P3, scope `check.mjs` and its test).
