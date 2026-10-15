---
id: 2026-10-15-refresh-stale-locale-thumbnail-diagnostics-during
title: Refresh stale locale thumbnail diagnostics during packaging
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-15T11:52:32Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package/cli.mjs
  - tools/video/package/variants.test.mjs
---

# Refresh stale locale thumbnail diagnostics during packaging

## Why

If the frame manifest was made before translation, its thumbnail_locale_gaps can still say a locale has no thumbnail words after that translation is current. Packaging reuses the saved reason and tells the owner to translate again, although the missing step is rendering the optional locale thumbnail.

## Definition of done

- [ ] The packaging note distinguishes missing/stale translation from current translated words whose thumbnail has not been rendered.
- [ ] The default-thumbnail fallback and selected-language behavior stay unchanged.

## Steps

- [ ] Reproduce with current locale thumbnail words and an older frames manifest containing a missing-words reason.
- [ ] Derive the diagnostic from current inputs and add a focused regression test.

## How to verify

Run node --test tools/video/package/variants.test.mjs and npm run check:tasks. The regression should require a render-next diagnostic for current words and retain the translation-next diagnostic when words are actually missing.

## Notes

Observed in H09 on 2026-10-15. EN, JA and KO thumbnail words and source hashes are current, but frames/manifest.json predates translations and lacks thumbnail_locales. package copied the saved missing-words messages. H09 validly uses its approved default thumbnail; the selected components are metadata, captions and dub. This is an unclaimed diagnostic follow-up, not a request to render or change H09 art.
