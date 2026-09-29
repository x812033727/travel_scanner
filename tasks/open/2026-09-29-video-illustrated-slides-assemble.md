---
id: 2026-09-29-video-illustrated-slides-assemble
title: Illustrated slides: mixed assembly with motion, dissolves, music bed and sound effects
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-29T09:14:22Z
completed_at:
branch:
depends_on:
  - 2026-09-29-video-illustrated-slides-media
scope:
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/assemble/assemble.test.mjs
  - tools/video/assemble/smoke.mjs
  - tools/video/assemble/synthetic.mjs
  - tools/video/assemble/sfx.mjs
  - tools/video/assemble/sfx.test.mjs
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
  - .github/workflows/video-tooling.yml
---

# Illustrated slides: mixed assembly with motion, dissolves, music bed and sound effects

## Why

投影片的合成（`assemble/cli.mjs`）只在 `isDrama` 時走混合版面與配樂（117–118 行）；插圖投影片要用漫劇已有的 `layoutDrama`（卡片＝stills、still shot＝運鏡段）、`dissolveFrom` 溶接、`bedFilter`／`mixFilter` 配樂床，再加卡片漂移與音效軌。站主 2026-09-29 決定：配樂用授權檔（`_music/`）、音效這一輪一起做（`_sfx/`）。

## Definition of done

- [ ] `layoutDrama(doc, timeline, frames, clips, keyframes, { transitionRule, cardMotion })`：第一景與章節卡硬切、其餘 shot 預設 dissolve、`data.transition` 可覆寫；`cardMotion` 時單狀態卡片變 `kind: "motion"`（drift／push-in 交替），多狀態卡片維持 stills；漫劇 fixture 的 layout 與 `motionSegmentKey` golden 不變（卡片來源另加 `MOTION_CARD_VERSION`）。
- [ ] `assemble/sfx.mjs`：`resolveSfx`（`_sfx/<set>/manifest.json`＋sha256）、`sfxPlan`（章節卡→stamp、溶接前 5 格→whoosh、reveal→pop、最小間隔 1.5 秒、每 2 秒最多一個 pop）、`sfxTrackArgs`（adelay＋amix）、`sfxHash`。
- [ ] `assemble/cli.mjs`：`mediaInputs` 一般化；配樂床在有 track 時就混（含 sfx 第三輸入）；`checks.json` 加 `look_hash`、`pictures_hash`、`mix_hash`、`sfx_hash`、`metrics.music_bed_lufs`；運鏡段 PSNR 抽查對任何格式。
- [ ] `package/cli.mjs` `checksCurrent` 比對四個雜湊；純投影片與漫劇不變。
- [ ] `smoke.mjs --fixture illustrated` 通過（合成的 narration、keyframes、`_music/`、`_sfx/`），CI workflow 多一行。
- [ ] 匯出 `overlayGraph`／`overlayInputs` 給 Shorts 用。

## Steps

- [ ] `drama.mjs` 的 layout 選項與 golden 測試。
- [ ] `sfx.mjs`＋測試。
- [ ] `cli.mjs`、`package/cli.mjs`、`synthetic.mjs`、`smoke.mjs`、workflow。

## How to verify

```bash
npm run test:tools
node tools/video/assemble/smoke.mjs --fixture illustrated --workdir <tmp>   # 需 ffmpeg＋Chromium
node tools/video/assemble/smoke.mjs --fixture drama --workdir <tmp>         # 仍綠
```

## Notes

- 卡片 1.25× 放大再裁切會讓密集文字略軟：只給單狀態卡片、`MOTION_DRIFT_ZOOM 0.04`，看聯絡表再放寬。
- 單狀態卡片變運鏡段後會失去 0.3 秒的進場動畫（漂移取代它）；多狀態卡片的整景連續運鏡另開票。
