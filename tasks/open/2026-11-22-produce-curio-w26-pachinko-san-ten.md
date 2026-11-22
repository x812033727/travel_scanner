---
id: 2026-11-22-produce-curio-w26-pachinko-san-ten
title: Produce curio-w26-pachinko-san-ten (N9117, #5 pool core)
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-22T13:01:48Z
created_at: 2026-11-22T13:01:17Z
completed_at:
branch: antigravity/curio-w26-pachinko-san-ten
depends_on: []
scope:
  - docs/videos/curio-w26-pachinko-san-ten
---

# Produce curio-w26-pachinko-san-ten (N9117, #5 pool core)

## Why

Produce the #5 highest-scoring unproduced 奇聞檔案局 (`curio-*`) single-episode core from `/admin/videos?tab=pools`: `N9117` (`score = 9.63`, `base = 10`, `demand = 7.75`, Japanese Pachinko Three-Shop System `三店方式`), completing all pre-TTS production gates and zero-diff Google Drive / GitHub backups while Gemini TTS daily RPD quota is in cooldown.

## Definition of done

- [x] Primary-source research & independent fact-check (`verify-2.md`: `VERDICT: PASS`, 17 live primary/official URLs, 0 1956 real-person or brand/IP violations).
- [x] Script passes `lint` (`0 errors, 0 warnings` across all 9 locales), `opening-review` (3 fresh personas >= 8.5, `problems: []` — `9.0 / 9.1 / 9.2`), and official 14-question `narrative` panel (2 readers = `28/28` YES).
- [x] All 60 keyframes pass 2x 4-quadrant independent visual audit (`60/60 = 100% PASS` across 4 rounds) and imported via `keyframes import`.
- [x] All 8 locales (`en, ja, ko, es, pt, id, vi, th`) translated, independently audited (`OVERALL: PASS`), fixed, merged, lint-clean (`0 errors, 0 warnings`), and all 9 `heimao-left` thumbnails rendered and visually verified.
- [x] Pushed `script` and `storyboard` gates to `/admin/videos` (`pending`).
- [x] Committed and pushed branch `antigravity/curio-w26-pachinko-san-ten` + zero-diff Google Drive backup (`W26/` and `W26/製作檔/`).
- [ ] After Gemini TTS daily quota reset: synthesize `zh-TW` `Sulafat` WAVs (120 lines) + 8-locale MiniMax dubs, assemble, independent audience review (`review/audience-review.md`), fix findings, re-pass `qa`, backup to Drive, and push `review-push --gate final`.

## Steps

- [x] Research primary sources, create `brief.md`, `claims.md`, `verify-1.md`, `NOTES.md`, and `heimao-left` hero thumbnail (`w26_hero_thumb_v4`).
- [x] Complete independent fact-check (`verify-2.md` -> `PASS`), 3-persona `opening-review` -> `passed`, and 2-reader 14-question `narrative` -> `passed`.
- [x] Generate/redraw and 2x-audit all 60 keyframes -> `60/60 PASS`, import via `keyframes import`.
- [x] Push `script` and `storyboard` to `/admin/videos`.
- [x] Translate all 8 locales, run independent 8-locale audit, apply all fixes, merge, render & inspect all 9 thumbnails.
- [x] Verify `npm run check:tasks && npm run test:docs-videos`, push branch, and verify zero-diff Google Drive backup.
- [ ] Run TTS (`Sulafat` + 8-locale MiniMax), assemble, independent audience review, `qa`, final Drive backup, and `review-push --gate final`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w26-pachinko-san-ten
node tools/video/cli.mjs opening-review --slug curio-w26-pachinko-san-ten --check
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Drive folders: `W26/` (`1plG2y3AzQVyT_wUGeRMrsj7hn3LFil99`), `W26/製作檔/` (`1V4zX383A52GINtXu53notKpQBXVqWIv-`).
- Registered in `scratch/sync_drive_episode.mjs` and `scratch/verify_drive_zero_diff.mjs`.
- Pre-TTS 100% complete on 2026-11-22; awaiting Gemini TTS daily quota reset (queued behind W08 -> W24 -> W23 -> W25).
