---
id: 2026-10-05-manual-renewal-publish-staging-throws-on
title: Manual renewal publish staging throws on a metadata.json whose captions or localizations are missing or mistyped
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T23:54:45Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal-handoff.test.mjs
---

# Manual renewal publish staging throws on a metadata.json whose captions or localizations are missing or mistyped

## Why

The manual hand-off of a renewed final (`tools/video/review/renewal-handoff.mjs`, mode
`manual-import`) stages the publish review itself. Two functions build the package check's
locales straight from `upload/metadata.json` before the check runs:

- `stageManualPublish()`, on the base-only path, passes
  `locales: metadata.captions.map(...)` and
  `descriptionLocales: ["zh-TW", ...Object.keys(metadata.localizations)]` to `checkPackage()`,
  and on every path puts `Object.keys(metadata.localizations)` into the payload's `locales`.
- `bindManualSubmission()`, when the body says `base_only`, does the same two reads.

A metadata.json whose `captions` is not an array (`5`, `{}`) or is absent throws
`TypeError: metadata.captions.map is not a function` (or `reading 'map'`), and one without
`localizations` throws `Cannot convert undefined or null to object`. Those escape as a
`TypeError` instead of the `requireThat` refusal the rest of the hand-off gives, so the operator
gets a stack trace instead of "the package check failed: …".

`package` always writes both fields with the right types, so only a hand-built or hand-edited
imported package can do this; that is why this is P3. Since
`2026-10-05-the-upload-package-check-throws-on`, `checkPackage()` itself reports a mistyped
field by name ("metadata.json captions is not a list; run package again") instead of throwing,
but these two callers read the fields before the check sees them.

## Definition of done

- [ ] `stageManualPublish()` (base-only or not) and `bindManualSubmission()` with a base-only
  body refuse a metadata.json whose `captions` is missing or not a list, or whose
  `localizations` is missing or not an object, with a message naming the field, and never throw
  a `TypeError`.
- [ ] A well-formed manual package stages exactly as before (the existing
  `renewal-handoff.test.mjs` cases pass unchanged).

## Steps

- [ ] Read the locales through a guard: `packageLocales()` from `tools/video/package/check.mjs`
  already returns the default language plus the localizations and ignores a mistyped map; for
  the caption locales, refuse with `requireThat(Array.isArray(metadata.captions), "metadata.json
  captions is not a list; rebuild the package")` (or let `checkPackage()` report it by passing
  `[]` and keeping `report.ok` false).
- [ ] Add `renewal-handoff.test.mjs` cases for `captions: 5` and a missing `localizations` on the
  base-only staging path, expecting a rejection that names the field.

## How to verify

`node --test tools/video/review/renewal-handoff.test.mjs`, then `npm run test:tools`. Neither
file is bound in `docs/videos/long-form/review.json` today; check again with
`node tools/video/long-form/cli.mjs check` before opening the PR.

## Notes

- Found 2026-10-06 while fixing `2026-10-05-the-upload-package-check-throws-on` (read-only: the
  lines are the `locales`/`descriptionLocales` arguments of the `checkPackage()` calls in both
  functions and the payload `locales` of `stageManualPublish()`).
- `stageManualPublish()` is only called from tests and by an operator by hand today; the
  worker and `review-push` reach `bindManualSubmission()` through `bindRenewalSubmission()`
  (`tools/video/review/renewal.mjs`) without `base_only`, so the automated path does not hit it.
- Both files are in the scope of the stale claim `2026-10-01-hand-off-owner-approved-renewed-finals`
  (codex-video-stall-followthrough, claimed 2026-10-04T10:14Z; its branch merged as #1210).
  Claiming this needs `--force` with that evidence, or wait for that ticket to close.
