---
id: 2026-11-22-produce-curio-w25-qb-house-n9103
title: Produce curio-w25-qb-house (N9103, #4 pool core)
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-22T08:48:14Z
created_at: 2026-11-22T08:48:13Z
completed_at:
branch: antigravity/curio-w25-qb-house
depends_on: []
scope:
  - docs/videos/curio-w25-qb-house
---

# Produce curio-w25-qb-house (N9103, #4 pool core)

## Why

Produce the #4 highest-scoring unproduced 奇聞檔案局 (`curio-*`) single-episode core from `/admin/videos?tab=pools`: `N9103` (`score = 9.63`, `base = 10`, `demand = 7.75`, QB House 10-minute no-wash haircut business model), completing all pre-TTS production gates and zero-diff Google Drive / GitHub backups while Gemini TTS daily RPD quota is in cooldown.

## Definition of done

- [x] Primary-source research & independent fact-check (`verify-2.md`: `VERDICT: PASS`, 9/9 live URLs, 14/14 claims, 0 real-person/brand-IP violations).
- [x] Script (`v26`, 119 lines / 9.4 min) passes `lint` (`0 errors, 0 warnings` across all 9 locales), `opening-review` (`9.2 / 9.1 / 9.1`, `problems: []`), and 14-question `narrative` panel (`28/28` YES).
- [x] All 60 keyframes pass 2x 4-quadrant independent visual audit (`60/60 = 100% PASS`) and imported via `keyframes import`.
- [x] All 8 locales (`en, ja, ko, es, pt, id, vi, th`) translated, independently audited, fixed, merged, lint-clean, and all 9 `heimao-left` thumbnails rendered and visually verified.
- [x] Pushed `script` and `storyboard` gates to `/admin/videos` (`pending`).
- [x] Committed and pushed branch `antigravity/curio-w25-qb-house` + zero-diff Google Drive backup (`W25/` and `W25/製作檔/`).
- [ ] After Gemini TTS daily quota reset: synthesize `119` `zh-TW` `Sulafat` WAVs + 8-locale MiniMax dubs, assemble, run independent audience review (`review/audience-review.md`), fix any findings, re-pass `qa`, backup to Drive, and push `review-push --gate final`.

## Steps

- [x] Research primary sources, draft `claims.md`, `verify-1.md`, `script.json`, and hero thumbnail (`heimao-left`).
- [x] Run independent fact-check (`verify-2.md` -> `PASS`), 3-persona `opening-review` -> `PASSED`, and 2-reader 14-question `narrative` -> `passed`.
- [x] Generate/redraw and 2x-audit all 60 keyframes -> `60/60 PASS`, import via `keyframes import`.
- [x] Push `script` and `storyboard` to `/admin/videos`.
- [x] Translate all 8 locales, run independent 8-locale audit, apply all fixes, merge, render & inspect all 9 thumbnails.
- [x] Verify `npm run check:tasks && npm run test:docs-videos`, push branch, and verify zero-diff Google Drive backup.
- [ ] Run TTS (`Sulafat` + 8-locale MiniMax), assemble, independent audience review, `qa`, final Drive backup, and `review-push --gate final`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w25-qb-house
node tools/video/cli.mjs opening-review --slug curio-w25-qb-house --check
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Drive folders (under `W-商業與品牌奇聞` `18fdlwsqUSmhNYJD2f8_SWZrBPqiVbNKI`): `W25/` (`1hvrusCImCSsxGWf7lYdysFgHYIyntVcV`), `W25/製作檔/` (`1eEJvfD5qBF_XEj-XZpWlq0qO8vRfMrtg`).
- Full receipts recorded in `docs/videos/curio-w25-qb-house/NOTES.md`.
- 2026-11-23 checkpoint: `script` & `storyboard` approved; `85/119` `Sulafat` WAVs (`q001.wav`–`q085.wav`, measured `4.45 chars/s`) synthesized and zero-diff verified in Drive `W25/製作檔/audio/`; remaining `34` lines paused on upstream Google `gemini-3.8-flash-tts` daily RPD 429 (`00:00 PST` / `08:00 UTC` reset).
