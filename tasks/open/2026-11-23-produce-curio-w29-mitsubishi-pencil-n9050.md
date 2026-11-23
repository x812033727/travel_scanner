---
id: 2026-11-23-produce-curio-w29-mitsubishi-pencil-n9050
title: Produce curio-w29-mitsubishi-pencil (N9050)
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-23T07:45:47Z
created_at: 2026-11-23T07:45:28Z
completed_at:
branch: antigravity/curio-w29-mitsubishi-pencil
depends_on: []
scope:
  - docs/videos/curio-w29-mitsubishi-pencil
  - docs/videos/lexicon.json
---

# Produce curio-w29-mitsubishi-pencil (N9050)

## Why

Produce the #8 highest-scoring unproduced 奇聞檔案局 (`curio`) episode (`N9050`, score 9.27) covering how Mitsubishi Pencil (`三菱鉛筆`) independently registered trademark `#18865` in 1903 — 11 years before Mitsubishi Goshi — built `uni` / `Hi-uni` / `JETSTREAM` / `KURUTOGA`, and acquired Germany's `LAMY` in 2024.

## Definition of done

- [x] Script, claims, and independent fact-check (`verify-2.md` VERDICT: PASS, 12/12 primary URLs HTTP 200, 1956 redline PASS) locked.
- [x] `lint` 0 errors / 0 warnings, `opening-review` PASSED (`9.0/9.0/9.0`, `problems: []`), 2-reader `narrative` PASSED (`28/28 ALL YES`).
- [x] 55/55 keyframes generated (theatrical-light rich-gouache, `ada-canon-v2.png` locked, zero MiniMax images), 0 border flags, 2x-zoom 4-quadrant independent audit 100% PASS, imported via `keyframes import --provider external --usd 0`.
- [x] 8-locale i18n (`en, ja, ko, es, pt, id, vi, th`) + 9 rendered thumbnails (`heimao-left`, v7 seamless sky) independently audited 8/8 + 9/9 PASS.
- [x] `/admin/videos` `script` + `storyboard` gates pushed, GitHub branch pushed, and Google Drive `W29/` + `W29/製作檔/` verified `differences: 0`.
- [ ] Post-TTS execution (`tts` -> `check-audio` -> `music` -> `clips` -> `assemble` -> `captions` -> 8-locale `dub` -> `qa` -> `review/audience-review.md` -> `package` -> Drive zero-diff -> `review-push --gate final`) after owner confirms Ultra slots restored in `/admin/settings`.

## Steps

- [x] Research 12 official primary sources & write `brief.md`, `claims.md`, `verify-1.md`, `verify-2.md`, `video.json`, `script.md`, and append 10 W29 brand terms to `docs/videos/lexicon.json`.
- [x] Pass `lint`, `opening-review` (3 personas), and `narrative` (2 blind readers).
- [x] Generate, 2x-zoom audit, and import all 55 keyframes (`--provider external --usd 0`).
- [x] Localize 8 languages, render 9 thumbnails, and pass independent 8-locale + 9-thumbnail audit.
- [x] Push `script` & `storyboard` gates, commit & push branch, and complete zero-diff Google Drive pre-TTS backup.
- [ ] Run post-TTS pipeline once owner confirms Ultra slots restored.

## How to verify

```bash
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-w29-mitsubishi-pencil
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Pre-TTS work is 100% complete and zero-diff backed up to Drive (`W29/`: `1MR-xLg-e1WyGVAKPpeXx_8wT4eHo9mGr`, `W29/製作檔/`: `1Dy7BYrYxiW9N7XmnMNECkpoPm5xfo92p`).
- Appended 10 W29 brand terms (`uni`, `Hi-uni`, `JETSTREAM`, `KURUTOGA`, `LAMY`, `safari`, `inside`, `M17`, `uniball`, `ZENTO`) to `docs/videos/lexicon.json`.
- Do NOT run Gemini `tts` on W29 until owner confirms Ultra slots are restored in `/admin/settings` (or explicitly authorizes `SITE` key).

