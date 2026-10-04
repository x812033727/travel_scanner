---
id: 2026-10-04-reject-unselected-locales-in-video-publish
title: Reject unselected locales in video publish packages
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-04T15:43:21Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package/check.mjs
  - tools/video/package/check.test.mjs
---

# Reject unselected locales in video publish packages

## Why

The four upload-package checks can accept leftover files for languages the owner did not choose. An independent private fake-filesystem probe set the current choice to only zh-TW while metadata still contained an English localization/language choice and the package held `description.en.txt` and `captions/en.srt`; all four checks passed. Production packages should carry the current selected parts exactly, so a previous broader package cannot silently become the accepted delivery.

## Definition of done

- [ ] Package metadata, descriptions, captions and dub tracks agree with the current language choice and required narration/channel locales; unexpected locale parts are rejected.
- [ ] Valid mixed part choices and genuinely legacy packages preserve their documented behavior.
- [ ] A package or metadata change during verification cannot reuse a check bound to earlier bytes.

## Steps

- [ ] Reproduce the zh-TW-only package with leftover English parts using fake files, without touching live media.
- [ ] Check both expected missing parts and unexpected extra parts, including metadata language-choice/localization bindings.
- [ ] Add negative and valid part-selection regression fixtures and run focused package tests.

## How to verify

Run `node --test tools/video/package/check.test.mjs` and relevant package tests. A fake zh-TW-only package carrying English parts must fail; the clean zh-TW control and valid mixed metadata/CC/dub choices must pass. No paid or production calls are needed.

## Notes

- Independent source/fake-probe evidence is in the private AI-series continuation directory, `package-extra-locales-private-proof-2030.json`. It reads production pure functions and a private Map, never a real upload package.
- `2026-09-30-youtube-approved-languages-sync` concerns later chosen parts ignored by YouTube synchronization; this ticket covers extra unselected parts accepted before publish delivery.
- Until fixed, the current episode uses a private pre-delivery guard comparing freshly read backend choices, exact package parts and stable metadata SHA. No shared package code or YouTube setting changed.
