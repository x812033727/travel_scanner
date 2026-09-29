---
id: 2026-09-29-video-shorts-motion-music
title: Shorts: per-scene camera motion, transparent card overlay, licensed music bed and the long video's illustrations
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-29T09:14:25Z
completed_at:
branch:
depends_on:
  - 2026-09-29-video-illustrated-slides-assemble
  - 2026-09-28-sothatswhy-shorts-from-episode
scope:
  - tools/video/shorts/motion.mjs
  - tools/video/shorts/motion.test.mjs
  - tools/video/shorts/build.mjs
  - tools/video/shorts/build.test.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/shorts/episode.mjs
  - tools/video/shorts/episode.test.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/layouts.mjs
  - tools/video/shorts/site.mjs
  - tools/video/shorts/smoke.mjs
  - tools/video/shorts/fixtures
  - docs/videos/SHORTS.md
---

# Shorts: per-scene camera motion, transparent card overlay, licensed music bed and the long video's illustrations

## Why

Shorts（`tools/video/shorts`）每句重畫一張不透明卡片、圖 letterbox 在 820×835、`-tune stillimage` 硬切、沒有配樂與音效；站主要它跟長片一樣生動。字幕條依 `SHORTS.md` L378 保留。

## Definition of done

- [ ] `motion.mjs`：1080×1920 運鏡鏈，import `assemble/drama.mjs` 的 `zoompanExpr` 與常數；一場景一段；句子的卡片用 `omitBackground` 截成透明疊層（scrim＋`.content` 半透明底板，幾何不變，`measurePage` 與 qa layout 項照舊）；場景間溶接；純文字場景用卡片自己漂移。
- [ ] schema 2 加場景 `camera` 與文件層 `music`／`sfx`（授權檔，Shorts 不生成）；schema 1 位元組不變；`episodeShort` 帶上長片 shot 的 `camera`。
- [ ] `build.mjs`：有 `music`／`sfx` 時走 `measureMixArgs`／`mixArgs`，`bed ≤ -24`；`buildId` 加音樂與音效 sha；`profileProblems`／`loudnessProblems` 不變。
- [ ] `episode.mjs` 接受任何有 shot 的影片（explainer 漫劇或插圖投影片），16:9 關鍵影格在 9:16 裡裁切平移，不另外生圖。
- [ ] `site.mjs` `CHANNEL_VOICE.style` 換說書式；`qa.mjs` `scriptShape` 加運鏡標記；`SHORTS.md` 更新。

## Steps

- [ ] `motion.mjs`＋測試。
- [ ] `core.mjs`、`build.mjs`、`episode.mjs`、`qa.mjs`、`layouts.mjs`、`site.mjs`、`smoke.mjs`、fixtures。
- [ ] `SHORTS.md`。

## How to verify

```bash
npm run test:tools
node tools/video/shorts/smoke.mjs --workdir <tmp>
node tools/video/shorts/cli.mjs from-episode --slug <插圖投影片> --workdir <tmp> --speech server
```

## Notes

- 逐句合成＋固定 0.18 秒間隔的節奏不會因 style 改變而消失；改整景合成會動到 phrase↔clip↔caption↔check 的對應，另開票。
- 與 `2026-09-28-video-shorts-worker-drama`（T4）協調：T4 參數化 1920×1080，這裡不等它。
