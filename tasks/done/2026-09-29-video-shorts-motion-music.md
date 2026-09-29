---
id: 2026-09-29-video-shorts-motion-music
title: Shorts: per-scene camera motion, transparent card overlay, licensed music bed and the long video's illustrations
status: done
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T10:53:37Z
created_at: 2026-09-29T09:14:25Z
completed_at: 2026-09-29T11:17:09Z
branch: claude/sharp-brown-dh2x95
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
  - tools/video/automation/flow.mjs
  - docs/videos/ILLUSTRATED.md
---

# Shorts: per-scene camera motion, transparent card overlay, licensed music bed and the long video's illustrations

## Why

Shorts（`tools/video/shorts`）每句重畫一張不透明卡片、圖 letterbox 在 820×835、`-tune stillimage` 硬切、沒有配樂與音效；站主要它跟長片一樣生動。字幕條依 `SHORTS.md` L378 保留。

## Definition of done

- [x] `motion.mjs`：1080×1920 運鏡鏈，import `assemble/drama.mjs` 的 `zoompanExpr` 與常數；一場景一段；句子的卡片用 `omitBackground` 截成透明疊層（scrim＋`.content` 半透明底板，幾何不變，`measurePage` 與 qa layout 項照舊）；場景間溶接；純文字場景改成主題底色（含光暈）漂移、文字靜止清晰（比整張卡片漂移不糊字）。
- [x] schema 2 加場景 `camera` 與文件層 `music`／`sfx`（授權檔，Shorts 不生成）；schema 1 位元組不變；`episodeShort` 帶上長片 shot 的 `camera`。
- [x] `build.mjs`：有 `music`／`sfx` 時走 `measureMixArgs`／`mixArgs`，`bed ≤ -24`；`buildId` 加音樂與音效 sha；`profileProblems`／`loudnessProblems` 不變。
- [x] `episode.mjs` 接受任何有 shot 的影片（explainer 漫劇或插圖投影片），16:9 關鍵影格在 9:16 裡裁切平移，不另外生圖。
- [x] `site.mjs` `CHANNEL_VOICE.style` 換說書式（import `automation/register.mjs` 的 `STORY_VOICE_STYLE`）；`qa.mjs` `scriptShape` 加運鏡標記 `c`；`SHORTS.md` 更新。

## Steps

- [x] `motion.mjs`＋測試。
- [x] `core.mjs`、`build.mjs`、`episode.mjs`、`qa.mjs`、`layouts.mjs`、`site.mjs`、`smoke.mjs`（fixture 不動：煙霧測試在工作區複製一份，加合成的圖、配樂與音效組）。
- [x] `SHORTS.md`。

## How to verify

```bash
npm run test:tools
node tools/video/shorts/smoke.mjs --workdir <tmp>
node tools/video/shorts/cli.mjs from-episode --slug <插圖投影片> --workdir <tmp> --speech server
```

## Notes

- 逐句合成＋固定 0.18 秒間隔的節奏不會因 style 改變而消失；改整景合成會動到 phrase↔clip↔caption↔check 的對應，另開票。
- 與 `2026-09-28-video-shorts-worker-drama`（T4）協調：T4 參數化 1920×1080，這裡不等它。

做完學到的：

- ffconcat 的圖片清單最後一張要再列一次才會有自己的 `duration`（`assemble/plan.mjs` `concatList` 早就這樣做）；第一版沒列，每景最後一格是光禿的底色，溶接就從空底色開始，看起來像沒有溶接。`motion.mjs` `cardsList` 現在照做。
- 有圖的場景，面板改成 `height:auto` 貼著文字放在上方，圖在下半可見；原本面板佔滿 1120 高的內容框，圖只剩上下兩條。
- 長片的 `motionMove` 表把「pan left」對到 `pan-right`（是裁切視窗的方向，不是相機的）；Short 的 `camera` 詞以相機命名，`cameraWords()` 只翻長片的敘述成詞，運鏡時再由 `cameraOf()` 對回同一個 zoompan 表達式，兩邊畫面一致。
- 逐句合成加 0.18 秒間隔的節奏（票的 Notes 第一條）沒動；一景一段之後要改整景合成會更容易，但仍是另一張票。
- scope 加了 `automation/flow.mjs`（`saveShorts` 依長片決定系列）與 `ILLUSTRATED.md` 階段表；claim 用 `--force` 蓋過的是過期的 `sothatswhy-shorts-from-episode`（in-progress 超過 24 小時沒動，它改的 `prompts.mjs`／`flow.mjs` 已在 main）。
