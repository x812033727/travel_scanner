---
id: 2026-10-28-package-check-should-flag-language-thumbnails
title: Package check should flag language thumbnails that were never drawn
status: done
priority: P2
area: tools
owner: claude-opus-curio-v2
claimed_at: 2026-10-28T01:15:36Z
created_at: 2026-10-28T01:15:16Z
completed_at: 2026-10-28T01:15:53Z
branch:
depends_on: []
scope:
  - tools/video/package
---

# Package check should flag language thumbnails that were never drawn

## Why

In the curio v2 batch, nine episodes were packaged and approved without their eight language
thumbnails (Studio's 「語言」 page), although every i18n file had the thumbnail words. The hand-run
lanes went `captions -> package` and never ran `render`, so `upload/metadata.json` listed every
locale under `skipped_thumbnail_locales` with "not drawn yet; run render".

## Definition of done

- [x] Someone running `package` by hand can see that a locale's own thumbnail was not drawn.

## Steps

- [x] Read `tools/video/package/cli.mjs`: it already prints
  `note: no <locale> thumbnail of its own, it keeps thumbnail.jpg: <reason>` for every skipped
  locale, before the check lines, and writes the same reasons into `UPLOAD.md` and `metadata.json`.
- [x] Decided not to turn it into a failing check: the worker's `drawLanguageThumbnails` treats a
  thumbnail that cannot be drawn (a missing glyph, words that do not fit, no browser) as a note on
  purpose, so the language batch still goes up.

## How to verify

`node tools/video/cli.mjs package --slug <slug>` on a project whose `frames/manifest.json` has no
`thumbnail_locales` prints one `note: no <locale> thumbnail of its own` line per locale.

## Notes

No code change. The gap was the hand-run lane: it only kept lines matching `submitted|ERROR|passed`
from package's output, so the notes never reached anyone. Anyone driving the stages by hand runs
`render --thumbnails-only` (or a full `render` when `frames/` was cleaned) after `i18n-merge` and
before `package`, and reads package's `note:` lines. Recorded on
`2026-10-25-pr-1844-v2-s09-s11-s14`.
