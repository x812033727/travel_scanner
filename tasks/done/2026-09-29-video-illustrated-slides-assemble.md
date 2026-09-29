---
id: 2026-09-29-video-illustrated-slides-assemble
title: Illustrated slides: mixed assembly with motion, dissolves, music bed and sound effects
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:29:23Z
created_at: 2026-09-29T09:14:22Z
completed_at: 2026-09-29T09:42:30Z
branch: claude/sharp-brown-dh2x95
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

- [x] `layoutDrama(doc, timeline, frames, clips, keyframes, { transitionRule, cardMotion })`：第一景與章節卡硬切、其餘 shot 預設 dissolve、`data.transition` 可覆寫；`cardMotion` 時單狀態卡片變 `kind: "motion"`（drift／push-in 交替），多狀態卡片維持 stills；漫劇 fixture 的 layout 與 `motionSegmentKey` golden 不變（卡片來源另加 `MOTION_CARD_VERSION`）。
- [x] `assemble/sfx.mjs`：`resolveSfx`（`_sfx/<set>/manifest.json`＋sha256）、`sfxPlan`（章節卡→stamp、溶接前 5 格→whoosh、reveal→pop、最小間隔 1.5 秒、每 2 秒最多一個 pop）、`sfxTrackArgs`（adelay＋amix）、`sfxHash`。
- [x] `assemble/cli.mjs`：`mediaInputs` 一般化；配樂床在有 track 時就混（含 sfx 第三輸入）；`checks.json` 加 `look_hash`、`pictures_hash`、`mix_hash`、`sfx_hash`、`metrics.music_bed_lufs`；運鏡段 PSNR 抽查對任何格式。
- [x] `package/cli.mjs` `checksCurrent` 比對四個雜湊；純投影片與漫劇不變。
- [x] `smoke.mjs --fixture illustrated` 通過（合成的 narration、keyframes、`_music/`、`_sfx/`），CI workflow 多一行。
- [x] 匯出 `overlayGraph`／`overlayInputs` 給 Shorts 用。

## Steps

- [x] `drama.mjs` 的 layout 選項與 golden 測試。
- [x] `sfx.mjs`＋測試。
- [x] `cli.mjs`、`package/cli.mjs`、`synthetic.mjs`、`smoke.mjs`、workflow。

## How to verify

```bash
npm run test:tools
node tools/video/assemble/smoke.mjs --fixture illustrated --workdir <tmp>   # 需 ffmpeg＋Chromium
node tools/video/assemble/smoke.mjs --fixture drama --workdir <tmp>         # 仍綠
```

## Notes

- 卡片 1.25× 放大再裁切會讓密集文字略軟：只給單狀態卡片、`MOTION_DRIFT_ZOOM 0.04`，看聯絡表再放寬。
- 單狀態卡片變運鏡段後會失去 0.3 秒的進場動畫（漂移取代它）；多狀態卡片的整景連續運鏡另開票。

- 2026-09-29：做完。`layoutDrama` 多 `{ transitionRule, cardMotion }`；`illustratedTransition`（第一景與章節卡硬切、其餘溶接、撰稿的 `data.transition` 優先）；單狀態卡片變 `kind: "motion"`、`card: true`，`CARD_MOVES` drift／push-in 輪流，segment key 折進 `MOTION_CARD_VERSION`（漫劇的 key 不變，golden 測試守著）。`sfx.mjs`：manifest 規則、`sfxPlan`（章節卡優先於 whoosh；最小間隔 45 格；pop 每 60 格最多一個；第 0 格不放）、`sfxTrackArgs`。`mixFilter` 第三個輸入是音效；`soundGraph` 統一輸入；沒有音樂只有音效時走 `effectsFilter`。`checks.json` 多 `pictures_hash`（`keyframesHash`）、`mix_hash`、`sfx_hash`、`metrics.sfx`。`smoke.mjs --fixture illustrated` 在本機用 ffmpeg 6.1 跑過：5 個運鏡鏡頭、3 張漂移卡片、6 次溶接、10 個音效、`checks.ok`。
- 觀察：卡片漂移後圖片上沒有章節進度條（插圖本來就沒有）；如果站主想在插圖上也看到章節條，要把 chrome 另外截成透明疊層（後續票）。
