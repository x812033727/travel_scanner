---
id: 2026-11-20-push-curio-s13-v2-languages-batch
title: Push curio-s13-v2 languages batch and complete curio-s14 R20 script, 9-language audio, and 2x audit
status: done
priority: P1
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-20T07:38:29Z
created_at: 2026-11-20T07:38:14Z
completed_at: 2026-11-20T13:29:18Z
branch: antigravity/curio-s13-v2-s14-remake
depends_on: []
scope:
  - docs/videos/curio-s13-v2
  - docs/videos/curio-s14
  - docs/videos/lessons/curio.md
  - docs/videos/lessons/explainer.md
  - docs/videos/history-curiosity/look.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# Push curio-s13-v2 languages batch and complete curio-s14 R20 script, 9-language audio, and 2x audit

## Why

1. `curio-s13-v2` ("真田幸村從沒叫過「幸村」？4 封生前書信，簽的都不是這兩個字｜奇聞檔案局") had its renewed `final` (`925ac26e`) and `publish` (`3965ef64`) packages approved on `/admin/videos`, which superseded the older `2026-11-18` `languages` review (`608caf94`). Because `review-push --gate languages` requires `publish` to be approved first on a renewed final, the 8-locale dub/captions/metadata `languages` batch still needs to be submitted so YouTube sync does not fail with `已選取的 en 配音尚未核准，請先完成語言包`, and its updated `docs/videos/curio-s13-v2/` files need to land in git.
2. `curio-s14` (宮本武藏巖流島遲到重製) needed R20 script/i18n completion (`lint` `0/0`, independent `verify-2` fact & i18n check, 2-reader blind panel `14/14`, 3-reader `opening-review` `>= 8.5`), `zh-TW` `Sulafat` narration (`>= 4.4` chars/s) + `check-audio` + `music`, all 8 MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`) + `check-audio`, 9-locale `heimao` thumbnails, 2x quadrant audit of all 71 images, `/admin/videos` `script` + `audio` review-pushes, verified Google Drive backup (`0 differences`), and promotion of lessons/rules discovered along the way. (Because `gemini-3.1-flash-image` hit a ~9h quota cooldown resetting around `2026-11-20T18:25Z` and MiniMax image generation is strictly forbidden by `curio-episode`, the 36 failed keyframe redraws + `assemble` + `audience-review.md` + `final` push are tracked in a dedicated follow-up ticket.)

## Definition of done

- [x] `curio-s13-v2` has its current `docs/videos/curio-s13-v2/` synced from its verified Google Drive backup, `review-push --slug curio-s13-v2 --gate languages` submitted (`f88f9dfc-fcfe-4db7-b713-911ebd36e392`, `sha=fdde9f601ca8`) against approved `final` (`925ac26e`) + `publish` (`3965ef64`) with all 8 MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`), and `review/languages.json` backed up to Google Drive.
- [x] `curio-s14` passes `lint` (`0` errors, `0` warnings), independent `verify-2` fact & i18n audit (`PASS`, `0 issues`), 2-reader blind panel (`14/14`), 3-reader `opening-review` (`9.2` across all 3 personas), `tts` (`4.60` chars/s >= `4.4` chars/s) + `check-audio` (`70/70`, `0 flagged`) + `music`, all 8 MiniMax `dub`s + `check-audio` (`70/70`, `0 flagged` across all 8 locales), 9 `heimao` thumbnails visually verified, 71-shot 2x quadrant visual audit documented in `NOTES.md`, `/admin/videos` `script` + `audio` gates pushed, Google Drive synced (`0 differences`), and follow-up ticket filed for the 36 `generate_image` keyframe redraws + final assembly after quota cooldown.
- [x] Cross-series and Curio-specific lessons & rules recorded in `docs/videos/lessons/explainer.md`, `docs/videos/lessons/curio.md`, `docs/videos/history-curiosity/look.md`, and `.agents`/`.claude` `curio-episode/SKILL.md`.
- [x] `npm run test:tools`, `npm run test:docs-videos`, and `npm run check:tasks` pass cleanly.

## Steps

- [x] Restore `curio-s13-v2` repo docs and package/dub artifacts from Google Drive (`1pOPQLLhXyMuT4XGbIhAhbJf7C1q26ADi`) and run `review-push --slug curio-s13-v2 --gate languages`.
- [x] Iterate `curio-s14` to R20 and pass `lint` (`0/0`), independent `verify-2` fact & i18n check, 2-reader blind panel (`14/14`), and 3-viewer `opening-review` (`9.2` each).
- [x] Synthesize `curio-s14` `zh-TW` `Sulafat` narration (`4.60` chars/s, `09:00`) + `check-audio` (`70/70`) + `music`, and complete all 8 MiniMax `dub`s (`en,ja,ko,es,pt,id,vi,th`) + `check-audio` (`70/70` `0 flagged` each).
- [x] Complete 2x quadrant visual audit of all 71 images (35 PASS kept, 36 FAIL documented with exact redraw specs in `NOTES.md`), render & inspect all 9 `heimao` thumbnails, push `script` + `audio` reviews on `/admin/videos`, sync Google Drive (`0 differences`), update lessons/skills, and file follow-up ticket for keyframe redraws + assembly once `gemini-3.1-flash-image` cooldown resets.

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

Verify `/api/video/reviews/curio-s13-v2` shows pending `languages` review `f88f9dfc-fcfe-4db7-b713-911ebd36e392` bound to `publish` `3965ef64` and `final` `925ac26e`, and `/api/video/reviews/curio-s14` + Google Drive `S14` (`0 differences`) hold the R20 `script` + `audio` + 8 dubs + 2x audit state.

## Notes

- Claimed with `--force` over two month-old stale Oct 19–20 claims (`2026-10-19-curio-s-axis-third-batch-s29`, `2026-10-20-remake-ten-curio-episodes-in-the`, >700h old with no active branches or open PRs).
- Encountered `gemini-3.1-flash-image` quota cooldown (resets ~`2026-11-20T18:25Z`); strictly followed `curio-episode` rule not to fall back to MiniMax image generation, completed 100% of all 9 audio tracks + captions + thumbnails + Drive backup, and filed follow-up ticket for the 36 `generate_image` redraws + final assembly.
