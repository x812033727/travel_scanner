---
id: 2026-11-22-produce-curio-w24-n9112-tirol-choco
title: Produce Curio W24 (N9112 Tirol-Choco) full episode
status: done
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-22T07:06:21Z
created_at: 2026-11-22T07:04:26Z
completed_at: 2026-11-23T15:40:17Z
branch:
depends_on: []
scope:
  - docs/videos/curio-w24-tirol-choco
---

# Produce Curio W24 (N9112 Tirol-Choco) full episode

## Why

Produce Curio W24 (`N9112`, Tirol-Choco / 滋露巧克力, `W-商業與品牌奇聞`, score `9.73`, `base = 9.68`, `demand = 10`): how Tirol-Choco went from 10-yen three-piece candy to splitting into 10-yen single cubes (1979) and deliberately doubling in size and price to 20 yen (1993) to fit a convenience-store barcode, scaling to 600M pieces/year.

## Definition of done

- [x] Brief, claims, 9 HTTP-200 verified primary sources, `verify-1.md`, and independent `verify-2.md` (`PASS`, `14/14` confirmed).
- [x] Final `video.json` (62 scenes, 123 lines, 2,355 spoken units, 71% `nobody: true`, 0 cards, `lint` `0/0` across 9 locales), `opening-review` (`PASSED`: `9.2 / 9.0 / 9.2`), and 2-reader blind storytelling panel (`28/28 YES`).
- [x] All 62/62 2K keyframes (5 canonical `ada-canon-v2.png` + 57 `gemini-3.1-flash-image`, zero MiniMax images) 2x 4-quadrant audited and imported (`--provider external --usd 0`), plus 9-locale `heimao-left` thumbnails rendered & verified.
- [x] Full `zh-TW` `Sulafat` TTS (123/123 lines), Lyria music, `final.mp4` (`12f4d106a3c4`), 8-locale MiniMax dubs (`en,ja,ko,es,pt,id,vi,th`), independent `review/audience-review.md`, and `/admin/videos` `script`/`storyboard`/`audio`/`final`/`dubs` approvals.
- [x] 9-locale captions, `package` (`4/4`, `metadata.json` `61b49ade530d`), `/admin/videos` full-tier `publish` (`07669faf`, 96 files, `pending`) and 8-locale `languages` (`19c22563`, `417132107852`, 34 files, `pending`), and verified Google Drive backups under `AI/備份/AI劇/奇聞檔案局/W-商業與品牌奇聞/W24/` (`1TnmyGA4a1vVFSwvHGgO3teidg43yUISt`, `40/40` `0 differences`) and `W24/製作檔/` (`10PHqGhgejPzZIxitTJncfEhc135uIbh5`, `0 differences`).

## Steps

- [x] Author verified script, claims, 8-locale i18n, and pass `lint`, `verify-2`, `opening-review`, and storytelling panel.
- [x] Generate & 2x-audit 62/62 keyframes and 9-locale `heimao-left` thumbnails; synthesize `zh-TW` TTS, Lyria music, 8-locale MiniMax dubs, assemble `final.mp4`, and pass independent audience review.
- [x] Pull owner approvals + 8-locale choice, build 9-locale captions & `package` (`4/4`), push `publish` + `languages` to `/admin/videos`, and sync verified zero-diff backups to Google Drive under `W-商業與品牌奇聞/W24/`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w24-tirol-choco
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Zero living or post-1956 real individuals named or depicted; zero brand text or copyrighted IP mascots in keyframes/thumbnails.
- Drive folders moved to `AI/備份/AI劇/奇聞檔案局/W-商業與品牌奇聞/W24/` (`1TnmyGA4a1vVFSwvHGgO3teidg43yUISt`) and `W24/製作檔/` (`10PHqGhgejPzZIxitTJncfEhc135uIbh5`), verified `0 differences`.
- `/admin/videos`: `script`/`storyboard`/`audio`/`final` (`12f4d106a3c4`)/`dubs` (`2a6549220155`) approved; `publish` (`07669faf`, 96 files) and `languages` (`19c22563`, 34 files) pending owner approval for upload.
