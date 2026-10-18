---
id: 2026-10-14-shorts-carry-translated-titles-descriptions-and
title: Shorts carry translated titles, descriptions and captions for the ticked locales
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-14T05:16:43Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts
---

# Shorts carry translated titles, descriptions and captions for the ticked locales

## Why

The Shorts settings have a 語言 choice (`video_shorts_settings.locales`), and SHORTS.md promises
that ticking a locale adds its title, description and CC. Half of that is built: `package.mjs`
records `locales` in `metadata.json`, and `qa.mjs` `captionsItem` then requires
`upload/<locale>.srt` for each ticked locale. Nothing produces those files, and `metadata.json`
has no field for a translated title or description at all, so a ticked locale makes every Short
fail QA (`captions`) and still uploads with zh-TW metadata only. Found 2026-10-14 when the owner
ticked en, ja and ko for the five 奇聞檔案局 recut Shorts; their CC were translated by hand from
the episodes' reviewed i18n files (every Short line is cut from an episode line).

## Definition of done

- [ ] For each ticked locale a Short gets `upload/<locale>.srt` on the zh-TW clock and a
      translated title and description in `metadata.json` (YouTube `localizations`).
- [ ] A cut-line Short (`from-episode`) reuses the episode's reviewed translation of each line,
      trimmed the same way; a lab Short goes through the translator and an independent reviewer.
- [ ] The site's upload/sync sends the localizations and the extra CC.
- [ ] SHORTS.md describes it; tests cover a Short with and without locales.

## Notes

- Related: the long-video translation flow (i18n-sheet → translator → reviewer → i18n-merge).
