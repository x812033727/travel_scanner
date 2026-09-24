---
id: 2026-09-24-video-speaking-rate
title: 影片長度估計改用聲音的實際語速，不固定每分鐘 250 字
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-24T06:13:09Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core
---

# 影片長度估計改用聲音的實際語速，不固定每分鐘 250 字

## Why

影片工具在合成之前，用「每分鐘 250 個唸出來的字」估計長度（`tools/video/core/timeline.mjs` 的 `DEFAULT_CPM`）。lint 靠這個估計檢查章節至少 10 秒、全片 8–12 分鐘；企劃與撰稿代理也照它控制字數。

2026-09-24 第一次真合成，量到的語速比這個快：同一段 101 字的樣稿，Ava 原速 19.9 秒，約每分鐘 300 字；+5% 約每分鐘 320 字；原生 zh-TW 聲音在 250–320 之間。照 250 估計的話，一支實際 10 分鐘的片會被估成 12 分鐘以上，lint 會警告「太長」，代理也會把稿子寫得太短。

## Definition of done

- [ ] `video.json` 能寫出這個聲音的語速（例如 `voice.cpm`），或由試聽結果推出；沒寫的時候維持 250。
- [ ] `lint`、`estimateTimeline` 與企劃、撰稿提示都用同一個值。
- [ ] `docs/videos/README.md` 的聲音表記下頻道聲音的實測語速。

## Steps

- [ ] 在 schema 加欄位並驗證範圍（例如 150–450）。
- [ ] `estimatedSamples`／`estimateTimeline` 讀它。
- [ ] 測試：同一份稿子在 250 與 320 的估計長度不同，章節檢查跟著變。

## How to verify

```bash
node --test tools/video/core/timeline.test.mjs tools/video/core/lint.test.mjs
```

## Notes

- 語速量法：`audition` 產生的 WAV，時長除以唸出來的字數。`spokenUnits`（英文字母算 2）跟估計用的是同一種單位。
- 試作票 `2026-09-24-video-pilot-ai-model-choice` 在等頻道聲音定案；定案後再量一次。
