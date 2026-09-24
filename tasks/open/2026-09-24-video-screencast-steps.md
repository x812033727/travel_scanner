---
id: 2026-09-24-video-screencast-steps
title: 影片產線 T9：Playwright 步驟腳本的螢幕操作教學
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:18Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-pilot-ai-model-choice
scope:
  - tools/video/screencast
---

# 影片產線 T9：Playwright 步驟腳本的螢幕操作教學

## Why

第三期：手把手操作教學。網頁操作用宣告式步驟 JSON（goto、click、fill、wait、capture、mask）讓 Playwright 自動操作並截靜態圖，游標、框選、放大由版型畫，畫面可重現、可快取。不用 Playwright 的 `recordVideo`（VP8、畫質差、變動畫格率、無法跟旁白同步）。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `video.json` 的場景可以是 `screencast` 步驟，render 產生帶游標與框選動畫的影格。
- [ ] 個資與秘密一律用 `mask` 遮掉；登入由站主自己做（持久 profile），代理不輸入帳密。
- [ ] 用一支實際教學跑通。

## Steps

- [ ] 步驟格式與驗證。
- [ ] 截圖、游標與框選動畫版型。
- [ ] 與 assemble 的每場景片段接起來。

## How to verify

```bash
node --test tools/video/screencast/*.test.mjs
```

## Notes
