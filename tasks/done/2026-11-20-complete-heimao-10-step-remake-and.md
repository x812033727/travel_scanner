---
id: 2026-11-20-complete-heimao-10-step-remake-and
title: Complete Heimao 10-step remake and full delivery for sothatswhy P25, G653, and G712
status: done
priority: P1
area: docs
owner: antigravity-gemini-3-1-pro
claimed_at: 2026-11-21T09:02:11Z
created_at: 2026-11-20T12:18:14Z
completed_at: 2026-11-21T14:24:56Z
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
- [x] All three episodes have audited rich-gouache keyframes (`85` + `76` + `70` = `231` frames, `0` MiniMax images), Gemini `Sulafat` + `Leda` `zh-TW` narration (`>= 4.4 chars/s`, `check-audio` clean), 9-locale `heimao` full-bleed thumbnails, `assemble` + `captions`, 8-locale MiniMax `dub` (`en,ja,ko,es,pt,id,vi,th`), and `qa` (`11/11` passed).
- [x] Independent post-assembly `review/audience-review.md` passes (`>= 7.5/10` per dimension, `>= 8.0/10` average) for all three episodes with any findings fixed and `qa` re-verified before backup/push.
- [x] Full working directories and `upload/` packages for all three episodes are backed up to Google Drive (`0 differences`) and pushed to `/admin/videos`, and `npm run test:tools && npm run test:docs-videos && npm run check:tasks` pass cleanly.

## Steps

- [x] Restore workdirs and 231 audited rich-gouache keyframes (`85` P25 + `76` G712 + `70` G653) and lock Heimao 10-step scripts (`P25`, `G712`, `G653`) with zero `lint` errors.
- [x] Complete `opening-review` (`G653`), 8-locale `i18n/*.json` sync (`G653`), and blind `narrative` panels (`P25`, `G712`, `G653`).
- [x] Complete `zh-TW` Gemini `tts` + `check-audio` (`P25` `85/85` at `5.10 chars/s`, `G712` `76/76` at `4.66 chars/s`, `G653` `70/70` at `4.54 chars/s`; `0` flagged across all three).
- [x] Run `render`, `assemble`, `captions`, 8-locale MiniMax `dub` (`24/24` `.m4a` tracks across `en,ja,ko,es,pt,id,vi,th` with music bed), and `qa` (`11/11` on all three episodes).
- [x] Run independent post-assembly `audience-review.md` on all three episodes (`G712` `9.12/10`, `P25` `9.23/10`, `G653` `9.18/10`), fix all camera/headroom findings, re-verify `qa` (`11/11`), `package` (`4/4`), sync Google Drive (`0 differences`), push `outline`/`script`/`final`/`publish` to `/admin/videos`, and mark task `done`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug sothatswhy-p25-train-tunnel
node tools/video/cli.mjs lint --slug sothatswhy-g712-printer-ink
node tools/video/cli.mjs lint --slug sothatswhy-g653-honey-crystallization
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- **2026-11-21 Completion Summary (`antigravity-gemini-3-1-pro`, branch `antigravity/sothatswhy-p25-g653-g712`)**:
  1. **`sothatswhy-g712-printer-ink` (100% COMPLETE END-TO-END)**:
     - `zh-TW` Gemini `Sulafat` + `Leda` (`76/76`, `0` flagged, `4.66 chars/s`); **all 8/8 `.m4a` dubs** (`en,ja,ko,es,pt,id,vi,th`) mastered with music bed.
     - `final.mp4` (`sha256: 398669167fa5`, `19567` frames, `-14 LUFS`), `qa` `11/11`, independent `review/audience-review.md` **`9.12/10`** (after fixing 6 wide comparison cameras to `"pull out"`), `package` `4/4` (`metadata.json` sha256 `b61face6559f`).
     - Google Drive backup (`1PI1d5-3xNz-ZxhYmBONibeBGhAC0s8Np` / `1lyP9SkklYSOzsNOQSRmVH_-gChR3EHr_`): **`1786 files, 0 differences`**; `outline`, `script`, `final`, `publish` pushed to `/admin/videos`.
  2. **`sothatswhy-p25-train-tunnel` (100% COMPLETE END-TO-END)**:
     - `zh-TW` Gemini `Sulafat` + `Leda` (`85/85`, `0` flagged, `5.10` / `4.97 chars/s`); **all 8/8 `.m4a` dubs** (`en,ja,ko,es,pt,id,vi,th`) mastered with music bed.
     - `final.mp4` (`sha256: d0ff7a637893`, `18254` frames, `-14 LUFS`), `qa` `11/11`, independent `review/audience-review.md` **`9.23/10`** (after fixing 14 scene cameras to `"pull out"`/`"drift"` and re-verifying all 85 end-frames), `package` `4/4` (`metadata.json` sha256 `a0440a48112c`).
     - Google Drive backup (`1D463NdLjfoKXSxv8Nls1K7gNwefvJiwT` / `1llYIMZ5x9S9xcoa0aAXlx9_9WcpCWBnd`): **`2080 files, 0 differences`**; `outline`, `script`, `final`, `publish` pushed to `/admin/videos`.
  3. **`sothatswhy-g653-honey-crystallization` (100% COMPLETE END-TO-END)**:
     - R45 `video.json` & `script.md` (`V184` boundaries strictly honored, zero medical/antibacterial claims), `narrative.json` `14/14` YES (`cbd588635358db9f`), `opening-review.json` `9.2 / 9.2 / 9.2` (`44c541b3e708...`).
     - `zh-TW` Gemini `Sulafat` + `Leda` (`70/70`, `0` flagged, `4.54` / `4.44 chars/s`); **all 8/8 `.m4a` dubs** (`en,ja,ko,es,pt,id,vi,th`) mastered with music bed & bookend alignment.
     - `final.mp4` (`sha256: 4287e924c834`, `18362` frames, `-14 LUFS`), `qa` `11/11`, independent `review/audience-review.md` **`9.18/10`** (after redrawing `#69` with generous headroom and setting 10 character/wide cameras to `"static camera"`/`"pull out"`), `package` `4/4` (`metadata.json` sha256 `8702534266fb`).
     - Google Drive backup (`1c4tgB6xOEiOoBctYieK9feTDgtyjFQIT` / `1xAfL9Ejlz8zjevh8p5TsGiDHbAiWuEgI`): **`1852 files, 0 differences`**; `outline`, `script`, `final`, `publish` pushed to `/admin/videos`.
