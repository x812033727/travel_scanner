---
id: 2026-10-15-h09-en-localization
title: Localize Curio H09 English metadata and captions
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h09-en
claimed_at: 2026-10-15T08:18:22Z
created_at: 2026-10-15T08:17:12Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/i18n/en.json
---

# Localize Curio H09 English metadata and captions

## Why

The owner selected English metadata, captions, and dubbing for the approved H09 film. The English words must track the approved Chinese script, its uncertainty boundaries, and the timed narration before an English dub or caption file is made.

## Definition of done

- [x] Current English title, description, tags, thumbnail words, 8 chapter names, and all 100 line captions are merged into `docs/videos/curio-h09/i18n/en.json`.
- [x] An independent bilingual reviewer checks the merged English against the Chinese source and the 100 dub budgets; its fixes are merged.

## Steps

- [x] Claim the narrow English localization scope and fill `en.todo.json` for `metadata,captions`.
- [x] Self-check every line against the Chinese source, including the 157/337 line, Gardner/Nikumaroro distinction, the 2018 sample comparison, and the separate 2024 and Taraia targets.
- [x] Merge the 100 lines and metadata after the Chinese description's publication wording was corrected.
- [x] Hand the merged result to an independent reviewer and incorporate its corrections.

## How to verify

With `VIDEO_WORKDIR` set to the media root containing `curio-h09`:

- `node tools/video/cli.mjs i18n-sheet --slug curio-h09 --locale en --parts metadata,captions` should report 0 of 100 lines, 0 of 8 chapters, and no stale metadata field.
- `node tools/video/cli.mjs i18n-merge --slug curio-h09 --locale en` should exit 0 with 100 lines written and no problem rows.
- Check each `en.todo.json` line length against its `max_chars`; `node tools/video/cli.mjs lint --slug curio-h09` and `npm run check:tasks` should exit 0.

## Notes

Translator owner: `codex-gpt6-curio-h09-en`. The first merge wrote 100 lines and 8 chapters with no line over `max_chars`; English title is `Where Did Amelia Earhart Go? The Last Radio Line and an Island`. The translated title and tags omit an invented English channel name per `caption-translate.md`. The thumbnail keeps the headline's two lines and `**` emphasis.

After the Chinese `video.json` description changed its stale promise to recheck and update the description before publication, `i18n-sheet` reported only the English description stale. I updated that one worksheet field and merged again. No external translator, paid API, TTS, or audio QA was called. The independent review is still pending; leave this task in progress until that review is applied.

The local `lint` pass had 0 errors and 4 warnings: two existing story-hook warnings, one long shot, and a Japanese title warning outside this English scope. `npm run check:tasks` passed with unrelated existing stale-claim and overlapping-scope warnings.

All 100 lines fit their hard dub `max_chars` values. Thirty-two lines exceed the translator prompt's softer "about 80 characters" reading target; the independent reviewer should focus on whether caption cue splitting keeps these readable without losing historical qualifiers.

Independent bilingual review by the Japanese localization agent found four English corrections, all applied and remerged: `h0hg5g67` and `h12n9upy` now refer to one bottle; `h0xw6uto` says Earhart may have reached the island without implying her aircraft landed there; the description calls it the Nikumaroro Island hypothesis. Fresh `i18n-sheet` after that merge reported 0 of 100 lines, 0 of 8 chapters, and no stale metadata; no line exceeds its hard dub budget. The resulting `en.json` SHA-256 is `86EF18CE651E47B6B41A9756DAD21A862642631064B2DE87D093C2FA0027E7E1`. Keep this task in progress until the coordinator closes the combined H09 language work.
