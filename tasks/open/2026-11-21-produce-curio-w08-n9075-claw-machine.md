---
id: 2026-11-21-produce-curio-w08-n9075-claw-machine
title: Produce Curio W08 (N9075 claw machine) full episode
status: in-progress
priority: P1
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-21T12:54:57Z
created_at: 2026-11-21T12:54:56Z
completed_at:
branch: antigravity/curio-w08-claw-machine
depends_on: []
scope:
  - docs/videos/curio-w08-claw-machine
  - docs/videos/lexicon.json
---

# Produce Curio W08 (N9075 claw machine) full episode

## Why

Produce the highest-scoring unproduced 奇聞檔案局 single-episode core from the admin topic pool (`/admin/videos?tab=pools` → 奇聞檔案局 → 單集題, Rank #1 / 1,626, `N9075`, score `9.68`, `W-商業與品牌奇聞`): how claw machines evolved across three anti-gambling legal regimes — US Johnson Act (1951/1962), Japan Sega UFO Catcher + Fueiho 800/1,000 JPY non-retail prize empire (FY2024 417.7B JPY, 68%), and Taiwan MOEA guaranteed-dispense (NT$990 cap) landlord/sub-lessee unmanned shops. Slug is `curio-w08-claw-machine` (W04–W07 are already reserved on `origin/claude/curio-w-batch-2-scripts`).

## Definition of done

- [x] `docs/videos/curio-w08-claw-machine/` passes `lint` (`0 errors, 0 warnings`), independent fact-check (`verify-1.md` + `verify-2.md` `PASS`), 3-persona `opening-review` (`>= 8.5`), and 2-reader blind `narrative` (`14/14`).
- [x] All keyframes + Heimao `heimao-left` subject-named hero thumbnail generated in theatrical-light rich-gouache style (never MiniMax images), audited at 2x 4-quadrant zoom by independent subagents (`100% PASS`), and imported with `--provider external --usd 0`.
- [ ] `zh-TW` Gemini `Sulafat` (`>= 4.4 chars/s`, `0 flagged`), `music`, and 8-locale MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`, `0 flagged`) pass `check-audio`, `render` (all 9 thumbnails inspected), `assemble`, `captions`, and `qa` (`11/11`).
- [ ] Post-assembly independent `review/audience-review.md` (`>= 7.5` each, avg `>= 8.0`, promise-payoff `PASS`) completed and any findings fixed before Google Drive zero-diff backup (`AI/備份/AI劇/奇聞檔案局/W08/製作檔/`) and `/admin/videos` `review-push`.

## Steps

- [x] Author `brief.md`, `claims.md`, `verify-1.md`, `NOTES.md`, `video.json`, and `script.md`; pass `lint` (`0 errors, 0 warnings`).
- [x] Pass independent `verify-2.md`, 3-persona `opening-review`, and 2-reader blind `narrative` (`14/14`); push `script` gate.
- [x] Generate hero thumbnail + all scene keyframes (65% `nobody: true`, `ada-canon-v2.png` for Ada shots), pass 2x 4-quadrant independent visual audit (60/60), and import via `keyframes import --provider external --usd 0`; push `storyboard` gate.
- [x] Complete 8-locale `i18n` (`en,ja,ko,es,pt,id,vi,th`), pass independent 8-locale audit, and `render` + visually verify all 9 locale thumbnails (`lint 0 errors, 0 warnings`).
- [ ] Finish remaining 27 lines (595 chars) of `zh-TW` Gemini `Sulafat` TTS (blocked on 2026-11-21 Google daily RPD 429 on both `flash-tts` and `flash-lite-tts`; 93/119 `flash-tts` takes cached) + `check-audio` + `music`, push `audio` gate; run 8-locale MiniMax `dub` + `check-audio --second-opinion`.
- [ ] Complete `clips` + `assemble --adopt-branding` + dub remix + `captions` + `qa` (`11/11`) + independent `review/audience-review.md` + Drive zero-diff backup + `review-push --gate final` + PR.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w08-claw-machine
node tools/video/cli.mjs opening-review --slug curio-w08-claw-machine --check
node tools/video/cli.mjs qa --slug curio-w08-claw-machine
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Selected from `/admin/videos?tab=pools` (`apps/api/app/video_pools/data/pools.json`, `curio.cores`, Rank #1 / 1,626, `N9075`, `score = 9.68`, `base = 9.62`, `demand = 10`, `produced = false`).
- `W04`–`W07` are taken on remote branch `claude/curio-w-batch-2-scripts`, so this episode uses `curio-w08-claw-machine`.
- All 8 primary sources (`WH12-S016`..`S020`, `S023`..`S025`) verified HTTP 200 via GET (using `archive.org/details/arcade-1-1993-book-scans` and `gcis.nat.gov.tw/elawAp/api/lawAttachment/243`).
- Strict 1956 person redline (only named real person is William D. Bartlett, died 1948) and zero copyrighted IP mascots / zero trademarks / zero text in images.
- 2026-11-21 checkpoint backed up to Google Drive `AI/備份/AI劇/奇聞檔案局/W08/製作檔/` (`1ZpMQOzbu53QCBOQ-0AJPMA0BIM3p0SKc` / `1vrmthZCGtgrtZ5McoqAvTgN-NTHrsKWA`). Resume at `tts --slug curio-w08-claw-machine` once Gemini TTS daily quota resets (Pacific midnight = Taiwan 16:00) or server Gemini API key is updated.


