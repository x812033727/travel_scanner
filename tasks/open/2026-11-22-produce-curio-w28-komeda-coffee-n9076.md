---
id: 2026-11-22-produce-curio-w28-komeda-coffee-n9076
title: Produce curio-w28-komeda-coffee (N9076)
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini-curio
claimed_at: 2026-11-22T17:36:02Z
created_at: 2026-11-22T17:36:01Z
completed_at:
branch: antigravity/curio-w28-komeda-coffee
depends_on: []
scope:
  - docs/videos/curio-w28-komeda-coffee
---

# Produce curio-w28-komeda-coffee (N9076)

## Why

Produce #7 highest-scoring unproduced single-episode Curio Archive topic on `/admin/videos?tab=pools` (`N9076`, score `9.47`, `W-商業與品牌奇聞`): Komeda Coffee's counterintuitive business model — free morning thick toast and unhurried crimson velvet booths yet 16.5%–18.7% operating margin (vs. Doutor Group's 6.4%) and a Tokyo Stock Exchange "Wholesale" (`卸売業`) listing.

## Definition of done

- [x] Brief, claims, 14 primary HTTP-200 verified sources, and independent `verify-2.md` fact-check (`VERDICT: PASS`, 0 DISCREPANCY, 0 NOT FOUND).
- [x] Final `video.json` (v20: 52 scenes, 104 lines, 2,005 spoken units, 0 cards) passing `lint` (`0 errors, 0 warnings` across all 9 locales), `opening-review` (`PASSED`: `9.2 / 9.0 / 9.2`, all `problems: []`), and official 14-question storytelling panel (`passed`, both blind readers `14/14 = 28/28 ALL YES`).
- [x] Hero thumbnail (`w28_hero_thumb`, `$0`) and all 52/52 2K keyframes (5 canonical `ada-canon-v2.png` shots + 9 surgical fixes via built-in `generate_image`, zero MiniMax images, zero text/borders/trademarks) 2x 4-quadrant independently audited (`52/52 PASS`, `Border flags: 0`) and imported (`--provider external --usd 0`).
- [x] All 8 locales (`en, ja, ko, es, pt, id, vi, th`) translated, merged (`0/0` lint across 9 locales), independently audited, and all 9 localized `heimao-left` thumbnails rendered & visually inspected.
- [x] `/admin/videos` `script` and `storyboard` gates pushed (`pending`), GitHub branch pushed, and Google Drive zero-diff backup verified (`W28/` & `W28/製作檔/`).
- [ ] Post-quota-reset (`00:00 PST`): `tts` (`zh-TW` `Sulafat`) -> `check-audio` -> Lyria `music` -> `clips` -> `assemble --adopt-branding` -> `captions` -> 8-locale MiniMax `dub` -> `qa` -> independent `review/audience-review.md` -> `/admin/videos` `audio`/`final`/`dubs` push -> Drive zero-diff backup.

## Steps

- [x] Research 14 primary sources and pass independent fact-check (`verify-2.md` `PASS`).
- [x] Iterate script to v20 passing `lint` (`0/0`), `opening-review` (`9.2 / 9.0 / 9.2`), and 2-reader official narrative panel (`28/28 ALL YES`).
- [x] Generate & 2x-audit all 52/52 keyframes + hero thumbnail, and import via `keyframes import --provider external --usd 0`.
- [x] Translate, merge, audit all 8 locales, render & visually inspect all 9 thumbnails, and push `script` & `storyboard` gates to `/admin/videos`.
- [x] Push `antigravity/curio-w28-komeda-coffee` to GitHub and verify zero-diff Google Drive backup.
- [ ] After Gemini TTS daily quota reset (`00:00 PST`), complete audio, music, assembly, 8-locale dubs, audience review, final gate pushes, and final Drive sync.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-w28-komeda-coffee
node tools/video/cli.mjs opening-review --slug curio-w28-komeda-coffee --check
node tools/video/cli.mjs status --slug curio-w28-komeda-coffee
npm run check:tasks && npm run test:docs-videos
```

## Notes

- Zero real individuals named or depicted (founder Taro Kato 1929–2016 excluded per 1956 redline).
- Drive folders: `W28/` (`14L7D9Vop_AfYsxQyGbJ4aKD2upaBhKE6`), `W28/製作檔/` (`1KnaVUsCuRa_n1VTXgj4K0vGAqqYQsLMS`).
