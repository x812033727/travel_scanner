---
id: 2026-10-05-the-upload-package-check-throws-on
title: The upload package check throws on a metadata.json whose caption list is not a list
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T17:09:04Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package/check.mjs
  - tools/video/package/check.test.mjs
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

- [ ] A metadata.json whose `captions` (or any other list or map the check reads: `dubs`,
  `thumbnail_variants`, `thumbnails`, `localizations`, `skipped_caption_locales`) has the wrong
  type gives a failing package item that names the field, not an exception.
- [ ] `review-push --gate publish` on such a package exits non-zero with that report instead of
  throwing.

## Steps

- [ ] In `check.mjs`, read the list fields through a helper that returns `[]` for a non-array
  and adds a problem ("metadata.json captions is not a list; run package again") to the item that
  reads it.
- [ ] Add `check.test.mjs` cases for `captions: 5` and `captions: {}`.

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
