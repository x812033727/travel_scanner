---
id: 2026-11-20-complete-heimao-10-step-remake-and
title: Complete Heimao 10-step remake and full delivery for sothatswhy P25, G653, and G712
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-11-20T12:18:14Z
completed_at:
branch: antigravity/sothatswhy-p25-g653-g712
depends_on: []
scope:
  - docs/videos/sothatswhy-p25-train-tunnel
  - docs/videos/sothatswhy-g653-honey-crystallization
  - docs/videos/sothatswhy-g712-printer-ink
---

# Complete Heimao 10-step remake and full delivery for sothatswhy P25, G653, and G712

## Why

Following the 2026-11-19 / 2026-11-20 `原來如此事務所` rule updates (no intro at `0:00`, single opening question with no question menu, opening-15s thumbnail echo, Heimao 10-step dialogue structure with relaxed 4 rules, Heimao title formula, strict 3-persona first-300s `opening-review`, theatrical rich-gouache keyframes with 45%–65% `nobody: true` mechanism shots, and post-assembly independent audience review), three active `sothatswhy-*` episodes need complete end-to-end remake/production, 8-locale MiniMax dubs, QA (`11/11`), Google Drive `todrive` backup (`0 differences`), and `/admin/videos` review push:

1. `sothatswhy-p25-train-tunnel` (85 scenes, 200-Series / 500-Series / N700S / Taiwan 700T & N700ST tunnel micro-pressure wave)
2. `sothatswhy-g712-printer-ink` (76 scenes, printer hardware vs ink cartridge lock-in, patents, firmware & CISS)
3. `sothatswhy-g653-honey-crystallization` (70 scenes, pure honey crystallization, sugar-syrup two-layer separation, heating HMF/FTIR & seeded creamed honey)

## Definition of done

- [x] All three episodes (`sothatswhy-p25-train-tunnel`, `sothatswhy-g712-printer-ink`, `sothatswhy-g653-honey-crystallization`) pass `lint` with `0` errors and `0` narrative/title/i18n warnings, independent fact-checks (`verify-*.md`), blind 14-question storytelling `narrative` panel, and strict 3-persona `opening-review` (`score >= 8.5`, `would_stay_300: true`, `problems: []`).
- [ ] All three episodes have audited rich-gouache keyframes (`85` + `76` + `70` = `231` frames, `0` MiniMax images), Gemini `Sulafat` + `Leda` `zh-TW` narration (`>= 4.4 chars/s`, `check-audio` clean), 9-locale `heimao` full-bleed thumbnails, `assemble` + `captions`, 8-locale MiniMax `dub` (`en,ja,ko,es,pt,id,vi,th`), and `qa` (`11/11` passed).
- [ ] Independent post-assembly `review/audience-review.md` passes (`>= 7.5/10` per dimension, `>= 8.0/10` average) for all three episodes with any findings fixed and `qa` re-verified before backup/push.
- [ ] Full working directories and `upload/` packages for all three episodes are backed up to Google Drive (`0 differences`) and pushed to `/admin/videos`, and `npm run test:tools && npm run test:docs-videos && npm run check:tasks` pass cleanly.

## Steps

- [x] Restore workdirs and 231 audited rich-gouache keyframes (`85` P25 + `76` G712 + `70` G653) and lock Heimao 10-step scripts (`P25`, `G712`, `G653`) with zero `lint` errors.
- [x] Complete `opening-review` (`G653`), 8-locale `i18n/*.json` sync (`G653`), and blind `narrative` panels (`P25`, `G712`, `G653`).
- [ ] Complete `zh-TW` Gemini `tts` + `check-audio` (`P25`, `G712`, `G653`) — `G712` 100% complete (`76/76` passed, `0` flagged, `4.66 chars/s`); `P25` & `G653` paused on Google AI Ultra Gemini TTS daily quota (RPD).
- [ ] Run `render`, `assemble`, `captions`, 8-locale MiniMax `dub`, and `qa` (`11/11`) for all three episodes — `G712` `render` + `assemble` + 9-locale `captions` + 7 MiniMax dubs (`en,ja,ko,es,pt,id,th`) + `qa` (`11/11`) complete; `P25` & `G653` 9-locale `heimao` thumbnails rendered.
- [ ] Run independent post-assembly `audience-review.md` on all three episodes, fix any issues, package, sync Google Drive (`0 differences`), push to `/admin/videos`, and mark task `done` — `G712` complete (`9.12/10`, packaged, backed up at `0 differences`, pushed); `P25` & `G653` pre-TTS workdirs backed up at `0 differences` and `outline`/`script` pushed.

## How to verify

```bash
node tools/video/cli.mjs lint --slug sothatswhy-p25-train-tunnel
node tools/video/cli.mjs lint --slug sothatswhy-g712-printer-ink
node tools/video/cli.mjs lint --slug sothatswhy-g653-honey-crystallization
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- **2026-11-20 Handoff Summary (`antigravity`, branch `antigravity/sothatswhy-p25-g653-g712`)**:
  1. **`sothatswhy-g712-printer-ink` (COMPLETE & PACKAGED — `final.mp4` sha256 `398669167fa5`, `qa` `11/11`, `audience-review.md` `9.12/10`)**:
     - `zh-TW` Gemini `Sulafat` (`tempo: 1.08`) + `Leda` (`tempo: 1.12`): `76/76` lines passed dual-transcriber `check-audio` (`0` flagged) at `4.66 chars/s`.
     - Independent post-assembly `audience-review.md` caught 6 wide side-by-side comparison shots (`#04, #31, #56, #58, #65, #67`) cropped by `pan left`/`pan right` (`panZoom: 1.2`); all 6 were switched to `"pull out"` (and `#66` to `"drift"`), re-assembled, visually verified via `build/last-*.png`, and re-passed `qa` `11/11` + `package` `4/4` (`metadata.json` sha256 `87ca600be807`).
     - 7 of 8 MiniMax dub tracks (`en, ja, ko, es, pt, id, th`) are mastered with music bed in `dubs/*.m4a` and `upload/dubs/`; only `vi` (`DUB_MINIMAX_VOICES.vi` has 1 voice, so `kid`'s 19 lines fall back to Gemini `Leda`) waits on Gemini TTS RPD reset.
     - Google Drive backup (`1PI1d5-3xNz-ZxhYmBONibeBGhAC0s8Np` / `sothatswhy-g712-printer-ink` `1lyP9SkklYSOzsNOQSRmVH_-gChR3EHr_`): **`1699 files, 0 differences`**.
     - Copy-paste follow-up commands are in `docs/videos/sothatswhy-g712-printer-ink/NOTES.md`.
  2. **`sothatswhy-p25-train-tunnel` (PRE-TTS 100% COMPLETE + 80/85 CACHED WAVS, WAITING ON GEMINI TTS RPD RESET)**:
     - `lint` `0` errors / `0` narrative-title-i18n warnings, `verify-1..4.md` PASS, blind `narrative.json` `14/14` YES, `opening-review.json` `9.2 / 9.2 / 9.2` (`712d95759390...`), 85 audited rich-gouache keyframes + 9-locale `heimao` thumbnails complete, `outline` & `script` pushed to `/admin/videos`.
     - Google Drive backup (`1D463NdLjfoKXSxv8Nls1K7gNwefvJiwT` / `sothatswhy-p25-train-tunnel` `1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd`): **`401 files, 0 differences`**.
     - Copy-paste resume commands after Gemini TTS RPD reset are in `docs/videos/sothatswhy-p25-train-tunnel/NOTES.md`.
  3. **`sothatswhy-g653-honey-crystallization` (PRE-TTS 100% COMPLETE, WAITING ON GEMINI TTS RPD RESET)**:
     - R44 `video.json` & `script.md` (`2f064afd571b...`), `lint` `0` errors / `0` narrative-title-i18n warnings across all 8 locales, `verify-1.md` PASS (`V184` boundaries strictly honored), blind `narrative.json` `14/14` YES, `opening-review.json` `9.2 / 9.2 / 9.2` (`872109256fe3...`), 70 audited rich-gouache keyframes + 9-locale `heimao` thumbnails complete, `outline` & `script` pushed to `/admin/videos`.
     - Google Drive backup (`1c4tgB6xOEiOoBctYieK9feTDgtyjFQIT` / `sothatswhy-g653-honey-crystallization` `1xAfL9Ejlz8zjevh8p5TsGiDHbAiWuEgI`): **`202 files, 0 differences`**.
     - Copy-paste resume commands after Gemini TTS RPD reset are in `docs/videos/sothatswhy-g653-honey-crystallization/NOTES.md`.
  4. **Note on Open PR `#2154` (`docs/sothatswhy-g653-honey-crystallization`)**:
     - `#2154` contains the pre-Heimao 2026-11-18 v1 draft of `G653` alongside already-relevant `tools/video/*` changes; this branch (`antigravity/sothatswhy-p25-g653-g712`) holds the 2026-11-20 Heimao 10-step R44 remake of `docs/videos/sothatswhy-g653-honey-crystallization/` without touching `tools/video/*`.
