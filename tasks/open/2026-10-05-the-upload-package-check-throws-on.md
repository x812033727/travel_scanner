---
id: 2026-10-05-the-upload-package-check-throws-on
title: The upload package check throws on a metadata.json whose caption list is not a list
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-video-package-check
claimed_at: 2026-10-05T23:41:09Z
created_at: 2026-10-05T17:09:04Z
completed_at:
branch: claude/video-package-check
depends_on: []
scope:
  - tools/video/package/check.mjs
  - tools/video/package/check.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# The upload package check throws on a metadata.json whose caption list is not a list

## Why

`tools/video/package/check.mjs` reads `upload/metadata.json` and trusts its field types.
`captionsItem()` runs `for (const listed of metadata.captions ?? [])` and `localesOf(metadata.captions ?? [], …)`
spreads it, so a `captions` that is a number or an object (`"captions": 5`) throws
`TypeError: number 5 is not iterable` out of `checkPackage()` and `readPackageReport()`.

`review-push --gate publish` calls `readPackageReport()`, and the worker (`auto`) runs its
sub-commands in process through `tools/video/cli.mjs` `main()`, which turns a `SyntaxError` into
exit 1 but rethrows a `TypeError`. So such a file ends the whole `auto` round in an exception
every round, instead of a failed package report the owner can read. `package` always writes a
list, so only a hand-edited (or truncated-and-patched) metadata.json can do this; that is why
this is P3.

Found while fixing PR #1288 (`2026-10-05-re-package-when-the-language-choice`), where the
worker's own read of the same check (`packageChoiceStale()` in
`tools/video/automation/flow.mjs`) now treats such a file as "unknown" instead of throwing.

## Definition of done

- [x] A metadata.json whose `captions` (or any other list or map the check reads: `dubs`,
  `thumbnail_variants`, `thumbnails`, `localizations`, `skipped_caption_locales`) has the wrong
  type gives a failing package item that names the field, not an exception.
- [x] `review-push --gate publish` on such a package sends that failing report, like any other
  failing package, instead of throwing. (Reworded 2026-10-06: the first wording said "exits
  non-zero", but review-push never does that for a failing package: `publishSubmission` sends the
  report and `reviewPush` returns ok after the POST (`tools/video/review/sync.mjs`), and the site
  declines to approve it on arrival (`publish_package_passed` in
  `apps/api/app/video_automation/judge.py`). Changing that would widen into the receipt-bound
  sync.mjs for every failing package, which is not this ticket.)

## Steps

- [x] In `check.mjs`, read the list fields through a helper that returns `[]` for a non-array
  and adds a problem ("metadata.json captions is not a list; run package again") to the item that
  reads it.
- [x] Add `check.test.mjs` cases for `captions: 5` and `captions: {}`.

## How to verify

`node --test tools/video/package/check.test.mjs`, then `npm run test:tools`. If `check.mjs` is
bound in `docs/videos/long-form/review.json`, `node tools/video/long-form/cli.mjs check` turns
red until an independent reviewer adds an increment; do not edit review.json yourself.

## Notes

- Measured 2026-10-06: with `"captions": 5`, `checkPackage()` throws
  `TypeError: number 5 is not iterable (cannot read property Symbol(Symbol.iterator))`.
- `Object.values`/`Object.keys`/`Object.entries` on the map fields do not throw on numbers or
  strings, but they read a string's characters as entries, so a string there passes or fails
  for the wrong reason; worth checking those too.
- Done 2026-10-06 (claude-opus-5-5-video-package-check). Measured on origin/main a9e4c3851 with
  `checkPackage()` in memory, before the fix: `captions` 5, `{}` and `false` threw (with or
  without a choice); a string `captions` failed as "c is listed but missing; a is listed …";
  `localizations: "en"` gave "no description for 0, 1"; `localizations: 5`, `thumbnails: []`,
  `thumbnail_variants: {}`, `dubs: {}` (with a choice) and `skipped_caption_locales: 5` (with a
  choice) all passed silently; a metadata.json that parses to `5`, `[]`, `"x"` or `true` failed
  with "metadata.json records another final (undefined)" and passed the descriptions item.
- The fix: `listField()`/`mapField()` in `check.mjs` read `captions`, `skipped_caption_locales`
  (captions item), `thumbnails`, `thumbnail_variants`, `dubs`, `language_choice` (files item)
  and `localizations` (descriptions item, and `packageLocales()`, which the publish payload's
  `locales` also uses). A field of another type fails that item with
  "metadata.json <field> is not a list|an object; run package again"; absent or `null` reads as
  empty, as before. A metadata.json that is not an object fails all four items with
  "metadata.json is not an object; run package again". The texts deliberately do not match the
  worker's `CHOICE_PROBLEM` (`flow.mjs`), so a mistyped field is never taken for a stale
  language choice. `language_choice` is not in the first list above, but it is a map the check
  reads, so it got the same guard.
- Scope widened (2026-10-06) to `tools/video/automation/automation.test.mjs` and one doc comment
  in `tools/video/automation/flow.mjs`. The worker test "an upload metadata.json whose fields
  have the wrong types leaves the re-package check unknown" (from #1288) relied on the check
  throwing: a `captions: 5` package written for another choice read as "unknown", so nothing was
  written. Now the check reads the rest of the file, finds "written for another language
  choice", and the worker writes the package again, exactly as it does for a readable file of
  another choice (package rewrites metadata.json from scratch; it never reads the old one). The
  test now covers both halves: the current choice's mistyped package is left alone without
  throwing, and another choice's is written again with a list for `captions`. The
  `packageChoiceStale()` comment said such fields leave the answer unknown; it now says only an
  unparsable or non-object file does. No other line of either file changed.
- Both automation files are bound by the duration receipt; this PR leaves the increment to an
  independent reviewer. Open drafts #1312 and #1301 touch the same two files in other hunks.
- Follow-up filed: `2026-10-05-manual-renewal-publish-staging-throws-on` — `renewal-handoff.mjs`
  reads `metadata.captions.map(...)` and `Object.keys(metadata.localizations)` itself before
  calling the check, on the manual base-only staging path.
