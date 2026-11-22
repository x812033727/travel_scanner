---
id: 2026-11-22-produce-curio-w27-marugame-seimen-n9105
title: Produce curio-w27-marugame-seimen (N9105)
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-22T15:41:04Z
created_at: 2026-11-22T15:40:45Z
completed_at:
branch: antigravity/curio-w27-marugame-seimen
depends_on: []
scope:
  - docs/videos/curio-w27-marugame-seimen
---

# Produce curio-w27-marugame-seimen (N9105)

## Why

Produce the #6 highest-scoring unproduced 奇聞檔案局 single-episode pool topic (`N9105`, 丸龜製麵 Marugame Seimen, score `9.55`, `base = 9.91`, `demand = 7.75`) up to the Gemini TTS gate during daily quota cooldown, with full GitHub branch + `/admin/videos` `script`/`storyboard` gates + zero-diff Google Drive backup.

## Definition of done

- [x] Primary-source research + independent fact-check (`verify-2.md` VERDICT: PASS, 16 sources, 0 living/post-1956 people)
- [x] Final script (`v15`) passes `lint` (`0 errors, 0 warnings` across all 9 locales), `opening-review --check` (`9.1 / 9.0 / 9.2`, all `problems: []`), and 2-reader `narrative` panel (`28/28 ALL YES`)
- [x] 60/60 keyframes (`nobody: true` 39/60 = 65.0%, 5 canonical Ada shots, zero MiniMax images) pass 2x-zoom independent visual audit (`Border flags: 0`) and imported
- [x] 8-locale i18n (`en/ja/ko/th/es/pt/id/vi`) translated, independently audited, fixed, merged, and all 9 rendered `heimao-left` thumbnails visually verified
- [x] `/admin/videos` `script` + `storyboard` gates submitted (`pending`)
- [x] GitHub branch pushed (`antigravity/curio-w27-marugame-seimen`) & zero-diff Google Drive backup verified (`W27/` + `W27/製作檔/`)
- [ ] Post-TTS completion after Gemini TTS daily quota resets (`tts` -> `check-audio` -> `music` -> 8-locale MiniMax `dub` -> `render` -> `clips` -> `assemble` -> `captions` -> `qa` 11/11 -> `review/audience-review.md` fixed & re-`qa`'d -> `package` 4/4 -> Drive backup update -> `review-push --gate final`)

## How to verify

```bash
NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-w27-marugame-seimen
NODE_NO_WARNINGS=1 node tools/video/cli.mjs opening-review --slug curio-w27-marugame-seimen --check
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Google Drive folders under `奇聞檔案局` (`1aJ7QaGpemn_CCbAPtVpk1xjzYcREf-Li`):
  - `W27/`: `1y-spPO-mUWT2yuvyl-xpIHm-qb8aAu5C`
  - `W27/製作檔/`: `1jjlPZ9t3lLCHhKToKPRKIiIzUg8CGEjR`
- Full verification ledger in `docs/videos/curio-w27-marugame-seimen/NOTES.md`.

