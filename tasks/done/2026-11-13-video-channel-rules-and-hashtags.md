---
id: 2026-11-13-video-channel-rules-and-hashtags
title: 補齊頻道審片規則（縮圖禁破梗、多句同景、小問密度、八語系列名、置頂留言）與系列 Hashtag
status: done
priority: P2
area: docs
owner: antigravity-gemini
claimed_at: 2026-11-13T18:15:11Z
created_at: 2026-11-13T18:14:17Z
completed_at: 2026-11-13T18:39:44Z
branch: feat/video-channel-rules-and-hashtags
depends_on: []
scope:
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/youtube-video/references/publish.md
  - docs/videos/explainer-series/README.md
  - docs/videos/lessons/explainer.md
  - docs/videos/lessons/sothatswhy.md
  - docs/videos/so-thats-why/thumbnails.md
  - docs/videos/so-thats-why/refresh-20261101/SPEC.md
  - docs/videos/so-thats-why/refresh-20261101/catalog.json
  - docs/videos/so-thats-why/refresh-20261101/episodes.json
  - docs/videos/so-thats-why/pool/pool.json
  - docs/videos/so-thats-why/pool/manifest.json
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/packaging-refresh-20261111/README.md
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/package/metadata.mjs
  - tools/video/package/metadata.test.mjs
---

# 補齊頻道審片規則（縮圖禁破梗、多句同景、小問密度、八語系列名、置頂留言）與系列 Hashtag

## Why

站主以一般觀眾視角審視 `@Mokaair` 最新六支公開影片（`curio-s42`、`curio-w02`、`story-b01`、`sothatswhy-p18`、`sothatswhy-p23`、`zhong-tian-qu-qi-e016-020`），且目前全部影片皆在 Claude 對話配對影音權杖（本機／雲端 `tools/video/cli.mjs`，不經主機 `settle()`）製作，抓出需要寫入規則與打包工具的缺口：

1. 本機／雲端對話未強制明寫 `"pauses": {"line_ms": 0, "scene_ms": 150}` 與 `"still_motion": "beat"`（S42、B01 退回舊停頓），且分鏡切成「一句一景」（S42 92 句／73 景、B01 137 句／137 景、P23 50 景單句）使 `line_ms: 0` 失效、每句都吃換景停頓。
2. `原來如此事務所` 縮圖規則曾寫「補一句反常識的結論」，導致 P23 縮圖直接寫「鏡子沒翻左右／翻的是前後」把全片答案破梗；W02 右圖選闔上的無字紅皮書無吸睛度；P23 開場寒暄 46 秒才進題、小問感嘆句過密且 `Leda` 語速偏慢。
3. S42、W02、B01 把內部查核算式與「誰過世超過四百年／不畫臉」寫進 `youtube.description`；`SERIES_HASHTAGS` 缺少 `#奇聞檔案局`、`#原來如此事務所`、`#品牌故事`；`packaging-refresh-20261111/README.md` 的八語系列定版譯名表空白；`UPLOAD.md` 缺少系列播放清單與低門檻二選一置頂留言步驟。

## Definition of done

- [x] `SERIES_HASHTAGS` 與 `seriesHashtag()`／`composeDescription()` 支援 `#品牌故事`、`#奇聞檔案局`（`curio-*`）、`#原來如此事務所`（`sothatswhy-*`），保留純 `category: "explainer"` 為無系列 hashtag。
- [x] `UPLOAD.md`（`uploadChecklist`）加入系列播放清單勾選與公開後二選一置頂留言步驟。
- [x] 奇聞、原來如此、共用解說規則與教訓補齊：對話做片必明寫 `pauses`＋`still_motion`、同角色同節拍 2–3 句併一景、小問 `Leda` 快語速範本與 15–20% 台詞上限、開場 20 秒直入提問、縮圖與說明欄禁破梗、禁塞內部查核／入畫備註、八語系列定版譯名表。
- [x] `.claude/skills/` 與 `.agents/skills/` 位元組一致，`npm run test:tools && npm run test:docs-videos && npm run check:tasks` 通過。

## Steps

- [x] 更新 `tools/video/core/metadata.mjs`、`tools/video/package/metadata.mjs` 與對應單元測試。
- [x] 更新 `.agents/skills/curio-episode/SKILL.md`、`.agents/skills/youtube-video/references/publish.md` 並同步 `.claude/skills/`。
- [x] 更新 `docs/videos/packaging-refresh-20261111/README.md`、`docs/videos/so-thats-why/*`、`docs/videos/explainer-series/README.md` 與 `docs/videos/lessons/{explainer,sothatswhy}.md`。
- [x] 執行工具、影片文件與任務看板測試。

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- `tools/video/core/metadata.mjs` 的 `urlKey()` 在 PR #2051 刻意保留 `#L12-L40` 行號錨點以區分同一公有領域長文的不同段落，故不在程式碼移除 `#L...`，改於規則要求 `sources[].title` 寫給一般觀眾看且同一長文只列最關鍵的 1–2 段。
- 本票所有變更檔案皆不在 `tools/video/long-form/review.mjs` 的 `REVIEW_FILES` 內；TTS `voice.tempo` 微加速因觸及 `schema.mjs` 等受保護檔案，獨立拆為下一張票與 PR 並附獨立代理 `DURATION_ONLY` 審查。
