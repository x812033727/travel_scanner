---
id: 2026-11-21-produce-curio-w08-n9075-claw-machine
title: Produce Curio W08 (N9075 claw machine) full episode
status: done
priority: P1
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-21T12:54:57Z
created_at: 2026-11-21T12:54:56Z
completed_at: 2026-11-23T15:40:30Z
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
- [x] `zh-TW` Gemini `Sulafat` (`4.85 chars/s`, all 13 ASR flags directly verified clean by audio inspection), Lyria `music`, and 8-locale MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`, all 8 `.m4a` built with music bed), `render` (all 9 thumbnails `0` warnings), `assemble` (`final.mp4` sha256 `7f8b9f45e5e5`, `-14 LUFS`), `captions` (`0` warnings), and `qa` (`9/11`, pending owner `narration` approval + site-wide travel stance score `0.36`, `advice 0.05`, `sponsored 0.04`).
- [x] Post-assembly independent `review/audience-review.md` (`9.1/10`, `Would watch to end: Yes`, zero audiovisual defects; `brief.md` stance rephrased positively) completed before Google Drive zero-diff backup (`AI/備份/AI劇/奇聞檔案局/W08/` & `W08/製作檔/`) and `/admin/videos` `review-push` (`audio`, `final`, `dubs` submitted).

## Steps

- [x] Author `brief.md`, `claims.md`, `verify-1.md`, `NOTES.md`, `video.json`, and `script.md`; pass `lint` (`0 errors, 0 warnings`).
- [x] Pass independent `verify-2.md`, 3-persona `opening-review`, and 2-reader blind `narrative` (`14/14`); push `script` gate.
- [x] Generate hero thumbnail + all scene keyframes (65% `nobody: true`, `ada-canon-v2.png` for Ada shots), pass 2x 4-quadrant independent visual audit (60/60), and import via `keyframes import --provider external --usd 0`; push `storyboard` gate.
- [x] Complete 8-locale `i18n` (`en,ja,ko,es,pt,id,vi,th`), pass independent 8-locale audit, and `render` + visually verify all 9 locale thumbnails (`lint 0 errors, 0 warnings`).
- [x] Finish all 119/119 lines of `zh-TW` Gemini `Sulafat` TTS (`4.85 chars/s`) + `check-audio` + Lyria `music`, push `audio` gate; build all 8/8 MiniMax dubs (`en/ja/ko/es/pt/id/vi/th`) with music bed.
- [x] Complete `clips` + `assemble --adopt-branding` + `captions` + `qa` + independent `review/audience-review.md` (`9.1/10`) + `/admin/videos` `final`/`dubs` submission + Drive zero-diff backup.

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
- 2026-11-23 final packaging & `/admin/videos` update: pulled owner approvals (`audio`, `final` `7f8b9f45e5e5`, `dubs` `fde840a74e2f`) + 8-locale choice (`en,ja,ko,es,pt,id,vi,th`), regenerated 9-locale captions & `package` (`4/4`, `metadata.json` `f72fa242ffcb`), pushed full-tier `publish` (`717c16de`, 94 files, `pending`) and 8-locale `languages` (`fcb272aa`, `cad806c138a4`, 34 files, `pending`).
- Drive folders moved to `AI/備份/AI劇/奇聞檔案局/W-商業與品牌奇聞/W08/` (`1ZpMQOzbu53QCBOQ-0AJPMA0BIM3p0SKc`, `40/40` `0 differences`) and `W08/製作檔/` (`1vrmthZCGtgrtZ5McoqAvTgN-NTHrsKWA`, `upload/` + `captions/` + `review/` + `approvals.json` + `languages.json` `0 differences`).
