---
id: 2026-10-05-manual-renewal-publish-staging-throws-on
title: Manual renewal publish staging throws on a metadata.json whose captions or localizations are missing or mistyped
status: done
priority: P3
area: tools
owner: claude-renewal-guard
claimed_at: 2026-10-07T03:10:56Z
created_at: 2026-10-05T23:54:45Z
completed_at: 2026-10-07T03:15:51Z
branch: claude/happy-carson-c1hy91
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

- [x] `stageManualPublish()` (base-only or not) and `bindManualSubmission()` with a base-only
  body refuse a metadata.json whose `captions` is missing or not a list, or whose
  `localizations` is missing or not an object, with a message naming the field, and never throw
  a `TypeError`.
- [x] A well-formed manual package stages exactly as before (the existing
  `renewal-handoff.test.mjs` cases pass unchanged).

## Steps

- [x] Read the locales through a guard: `packageLocales()` from `tools/video/package/check.mjs`
  already returns the default language plus the localizations and ignores a mistyped map; for
  the caption locales, refuse with `requireThat(Array.isArray(metadata.captions), "metadata.json
  captions is not a list; rebuild the package")` (or let `checkPackage()` report it by passing
  `[]` and keeping `report.ok` false).
- [x] Add `renewal-handoff.test.mjs` cases for `captions: 5` and a missing `localizations` on the
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
- 2026-10-07 (claude-renewal-guard): `manualMetadataLocales(metadata)` in
  `renewal-handoff.mjs` refuses through the module's `requireThat` (a `UsageError`) with
  "metadata.json captions is not a list of caption files" / "metadata.json localizations is not an
  object" (and a non-object metadata.json), and returns the caption and description locales.
  `stageManualPublish()` calls it on every path, because its payload names the package's own
  localizations whether base-only or not; `bindManualSubmission()` calls it for a base-only body.
- Finding: after `prepare`, metadata.json is itself one of the receipt's file proofs, so a
  hand-edited one reaching `bindManualSubmission()` is refused first by "manual package attachment
  changed: metadata" (already a refusal, not a TypeError); the guard there matters only for a
  hand-built receipt. `stageManualPublish()` reads the fields before that proof check, which is
  where the TypeError came from.
- Test: captions a number, an object or missing, localizations missing or a list, on the
  base-only and the full staging path: refused naming the field, no submission, nothing staged;
  and through `bindManualSubmission()` with real file proofs: refused, never a TypeError. It fails
  with the guard removed (checked). Existing cases pass unchanged (67 in the file);
  `npm run test:tools` 1988 pass; the duration receipt still passes (neither file is bound).
