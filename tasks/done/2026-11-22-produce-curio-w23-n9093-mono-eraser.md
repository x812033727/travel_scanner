---
id: 2026-11-22-produce-curio-w23-n9093-mono-eraser
title: Produce Curio W23 (N9093 MONO eraser) full episode
status: done
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-22T05:01:53Z
created_at: 2026-11-22T05:00:38Z
completed_at: 2026-11-23T15:31:03Z
branch: antigravity/curio-w23-mono-eraser
depends_on: []
scope:
  - docs/videos/curio-w23-mono-eraser
  - docs/videos/lexicon.json
---

# Produce Curio W23 (N9093 MONO eraser) full episode

## Why

Produce the #1 highest-scoring unproduced single-episode Curio Archive topic on `/admin/videos?tab=pools` (`2026-11-21-curio-1988`): `N9093` (Tombow MONO eraser: 1967 pencil freebie -> 2017 Japan #1 pure-color trademark Reg. No. 5930334 -> 2017 wordless exam edition -> 2024 scallop-shell biomass Good Design edition, score `9.82`, `W-商業與品牌奇聞`).

## Definition of done

- [x] Brief, claims, 9 primary HTTP-200 verified sources, and independent `verify-2.md` fact-check (`14/14 CONFIRMED`, `0 DISCREPANCY`).
- [x] Final `video.json` (63 scenes, 125 lines, 2,356 spoken units, 65% `nobody: true`, 0 cards) passing `lint` (`0 errors, 0 warnings` across all 9 locales), `opening-review` (`PASSED`: `9.2 / 8.7 / 9.1`), and official 14-question storytelling panel (`passed`).
- [x] All 63/63 2K keyframes (6 canonical `ada-canon-v2.png` shots via built-in `generate_image`, 57 via `gemini-3.1-flash-image`, zero MiniMax images, zero trademark striped sleeves, zero text/borders) 2x 4-quadrant independently audited and imported (`--provider external --usd 0`).
- [x] All 8 locales (`en, ja, ko, es, pt, id, vi, th`) translated within MiniMax `× 0.88` budgets, independently audited & fixed, merged (`0/0` lint), and all 9 localized `heimao-left` thumbnails rendered & visually inspected.
- [x] `/admin/videos` `script` and `storyboard` gates pushed (`pending`).
- [x] Complete zero-diff Google Drive backup under `AI/備份/AI劇/奇聞檔案局/W23/` (`1ZUj9glbnDjMQBenEQOuKnVsfWdNkH076`) & `W23/製作檔/` (`1VkVuWl-_u0KIOzMi_z9mg6ZNyZfScrBu`) and branch pushed to GitHub.
- [x] Post-TTS production: `tts` (`zh-TW` `Sulafat`, `4.55 chars/s`) -> `check-audio` -> Lyria `music` -> `clips` -> `assemble` (`final.mp4` sha256 `db8d326bd19c`, `-14 LUFS`) -> `captions` (`0` warnings) -> 8-locale MiniMax `dub` (`en/ja/ko/es/pt/id/vi/th`, all 8 `.m4a` built with music bed) -> `qa` (`9/11`, `0` caption/thumbnail warnings) -> independent `review/audience-review.md` (`8.9/10`, pass) -> `/admin/videos` `audio`, `final`, and `dubs` gates pushed (`pending`) -> Drive zero-diff backup.

## Steps

- [x] Research primary sources (Tombow official press releases, JPO Vol.53, Good Design 2024) and write `brief.md`, `claims.md`, `verify-1.md`, `video.json`, `script.md`.
- [x] Run independent fact-check (`verify-2.md`), opening review panel, and official storytelling panel.
- [x] Generate hero thumbnail (`w23_hero_thumb`) and all 63 keyframes, run 2x 4-quadrant independent audits, redraw until 63/63 PASS, and import.
- [x] Translate, audit, fix, and merge all 8 locales; render and inspect all 9 thumbnails.
- [x] Push `script` and `storyboard` gates to `/admin/videos` and sync zero-diff backup to Google Drive + GitHub.
- [x] Finish `zh-TW` `Sulafat` TTS, Lyria music, assembly, captions, 8-locale MiniMax dubs, independent audience review (`8.9/10`), `/admin/videos` `audio`/`final`/`dubs` submission, and final Drive zero-diff backup.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w23-mono-eraser
node tools/video/cli.mjs opening-review --slug curio-w23-mono-eraser --check
node tools/video/cli.mjs status --slug curio-w23-mono-eraser
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Zero real individuals named or depicted (100% compliant with 1956 redline).
- Strict visual avoidance of Japan Trademark No. 5930334 (equal-proportion blue-white-black striped eraser sleeve) enforced and verified across thumbnail and all 63 keyframes.
- Drive folders: `AI/備份/AI劇/奇聞檔案局/W-商業與品牌奇聞/W23/` (`1ZUj9glbnDjMQBenEQOuKnVsfWdNkH076`, `40/40` `0 differences`), `W23/製作檔` (`1VkVuWl-_u0KIOzMi_z9mg6ZNyZfScrBu`, `upload/` + `captions/` + `review/` + `approvals.json` + `languages.json` `0 differences`).
- 2026-11-23 final packaging & `/admin/videos` update: pulled owner approvals (`audio`, `final`, `dubs`) + 8-locale choice (`en,ja,ko,es,pt,id,vi,th`), regenerated 9-locale captions & `package` (`4/4`, `metadata.json` `88f3638e83d7`), pushed full-tier `publish` (`87788407`, 97 files, `pending`) and 8-locale `languages` (`76fc37f8`, `3969c2925c67`, 34 files, `pending`).
