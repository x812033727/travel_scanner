---
id: 2026-10-04-reject-unselected-locales-in-video-publish
title: Reject unselected locales in video publish packages
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-publish-unselected-locales
claimed_at: 2026-10-05T00:14:05Z
created_at: 2026-10-04T15:43:21Z
completed_at:
branch: claude/publish-unselected-locales
depends_on: []
scope:
  - tools/video/package/check.mjs
  - tools/video/package/check.test.mjs
---

# Reject unselected locales in video publish packages

## Why

The four upload-package checks can accept leftover files for languages the owner did not choose. An independent private fake-filesystem probe set the current choice to only zh-TW while metadata still contained an English localization/language choice and the package held `description.en.txt` and `captions/en.srt`; all four checks passed. Production packages should carry the current selected parts exactly, so a previous broader package cannot silently become the accepted delivery.

## Definition of done

- [x] Package metadata, descriptions, captions and dub tracks agree with the current language choice and required narration/channel locales; unexpected locale parts are rejected.
- [x] Valid mixed part choices and genuinely legacy packages preserve their documented behavior.
- [x] A package or metadata change during verification cannot reuse a check bound to earlier bytes.

## Steps

- [x] Reproduce the zh-TW-only package with leftover English parts using fake files, without touching live media.
- [x] Check both expected missing parts and unexpected extra parts, including metadata language-choice/localization bindings.
- [x] Add negative and valid part-selection regression fixtures and run focused package tests.

## How to verify

Run `node --test tools/video/package/check.test.mjs` and relevant package tests. A fake zh-TW-only package carrying English parts must fail; the clean zh-TW control and valid mixed metadata/CC/dub choices must pass. No paid or production calls are needed.

## Notes

- Independent source/fake-probe evidence is in the private AI-series continuation directory, `package-extra-locales-private-proof-2030.json`. It reads production pure functions and a private Map, never a real upload package.
- `2026-09-30-youtube-approved-languages-sync` concerns later chosen parts ignored by YouTube synchronization; this ticket covers extra unselected parts accepted before publish delivery.
- Until fixed, the current episode uses a private pre-delivery guard comparing freshly read backend choices, exact package parts and stable metadata SHA. No shared package code or YouTube setting changed.
- 2026-10-05 (claude-opus-5-5-publish-unselected-locales): fixed in `tools/video/package/check.mjs` only. `checkPackage` takes the owner's choice (`languages`, as `readLanguages` returns it); `readPackageReport` passes it from `packageLocalesWanted`. With a choice, `descriptions` fails a `description.<l>.txt`, `localizations.<l>` or `default_language` outside the narration + zh-TW + chosen-metadata locales; `captions` fails a `captions/<l>.srt` there or listed outside the caption locales; `files` fails a `metadata.json` whose `language_choice` ticks other parts than `languages.json` (compared the way `readLanguages` reads it: a dub chooses its captions, zh-TW left out, a missing field reads as nothing chosen), a dub track (`dubs/<l>.<ext>` or `metadata.dubs[]`) outside the chosen dubs minus the narration, a listed track that is missing or a track not listed, and a `thumbnails/<l>.jpg` outside the locales any part was chosen for (package's `youtubeLocales`). A chosen dub may be absent (in the making, given up in `skipped_dub_locales`, or a compilation's). The item ids stay the four the server reads (`PACKAGE_ITEM_IDS`).
- Without a choice (no `languages.json`) nothing extra is refused, and `checkPackage` called with explicit `locales`/`descriptionLocales` but no `languages` (the renewed hand-off in `tools/video/review/renewal-handoff.mjs`, out of scope and held by the codex claim) keeps today's rule. This matches docs/videos/LANGUAGES.md step 3 (`upload/` holds only zh-TW and the ticked parts), so no doc changed.
- Bytes binding: `readPackageReport` used to parse `metadata.json` with `readJson`, await the final's hash, then hash `metadata.json` again, so a rewrite in between bound the new hash to a check of the old content (and the server's `publish_package_passed` only compares that hash). It now reads `metadata.json` once, hashes and parses those same bytes, and at the end re-lists `upload/` (size and mtime of every file), re-hashes `metadata.json` and re-reads the choice; any difference fails the `files` item ("changed while the package was being checked; check it again"). Tested by writing during the first await (the final's hash).
- Mutation check: with `languages`/`unchanged` forced off in `checkPackage`, the four new tests fail and the eight old ones pass.
- Follow-up filed: `2026-10-05-re-package-when-the-language-choice` — the worker's `languages()` does not re-run `package` when the choice narrows and nothing is pending, so a later publish push would now carry a failing report instead of a broader package.
