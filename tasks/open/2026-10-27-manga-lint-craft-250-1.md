---
id: 2026-10-27-manga-lint-craft-250-1
title: manga 鏡長估計跟上新節奏：lint／craft 的估計還用 250 字/分＋每鏡 1 秒空白
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-27T06:10:06Z
completed_at:
branch:
depends_on:
  - 2026-10-27-1-3-5-5-5
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/craft.mjs
---

# manga 鏡長估計跟上新節奏：lint／craft 的估計還用 250 字/分＋每鏡 1 秒空白

## Why

票 `2026-10-27-1-3-5-5-5` 讓 manga 等級的漫劇（《系統說我是 BUG》）在 tts 之後的真時間軸改成：同一章的鏡頭之間不加 `SCENE_GAP_MS`、沒寫 pause 的句子 80 ms（`timeline.mjs` `MANGA_PAUSE_MS`，`buildTimeline` 的 `series` 參數），旁白太慢的 take 用 `atempo` 調到 5.5 字/秒（角色 4.5）。撰稿規則也改成一張圖配一到兩句。

但寫稿階段的估計沒跟上：`lint.mjs` 用 `estimateTimeline(doc, cpm)`（沒傳 series.json，所以 manga 判斷不到，每鏡仍加 300＋700 ms）與 250 字/分（4.17 字/秒）估鏡長，`mangaShotLengthProblems` 對 > 4 秒的鏡頭警告、訊息還寫「give the shot one line」。一鏡兩句（例如 8＋8 字）估成約 5.1 秒會被警告，實際只有約 3 秒。`craft.mjs` 的鏡長估計同樣用 `SCENE_GAP_MS`。

## Definition of done

- [ ] lint 對 manga 等級用 series.json 的 tier 估時間軸（`estimateTimeline` 要能帶 `{ series }`，或 lint 自己呼叫 `buildTimeline(doc, estimatedSamples(doc, cpm), { basis: "estimated", series })`），語速用 manga 旁白的目標（約 330 字/分）。
- [ ] `mangaShotLengthProblems` 的訊息改成「一到兩句」。
- [ ] craft 的 manga 鏡長估計不再加 `SCENE_GAP_MS`。
- [ ] 一般漫劇與投影片的估計不變（測試釘住）。

## Notes

- `timeline.mjs`、`craft.mjs`、`lint.mjs` 多半綁在時長收據 `REVIEW_FILES`，改了要另一個名字的獨立審查代理做 DURATION_ONLY 增量。
