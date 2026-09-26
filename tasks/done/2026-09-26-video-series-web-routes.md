---
id: 2026-09-26-video-series-web-routes
title: Video series A2: the worker's series routes on the web side
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T20:02:12Z
created_at: 2026-09-26T17:36:23Z
completed_at: 2026-09-26T20:02:51Z
branch: claude/video-series-web-routes
depends_on: []
scope:
  - apps/web/app/api/video/automation/series
---

# Video series A2: the worker's series routes on the web side

## Why

工人用影片工具權杖呼叫作品層的端點（`/video/automation/series/**`），網站的 BFF 只轉權杖不轉 cookie，每條路由要在 `apps/web/app/api/video/automation/series/**` 明列。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [x] `series/next`（GET）、`series/[slug]/docs`（POST，body 上限 1 MiB）、`series/[slug]/episodes/[n]/start|recap|done`（POST）、`series/[slug]/context`（GET）都經 `forwardToSpeech`；slug 與集數先驗證，錯的回 404 `problem()`（英文，check:i18n 的 Han 規則）。
- [x] route.test.ts：無權杖 401、cookie 不轉送、路徑對應。

## Steps

- [x] 路由檔與測試（照 `automation/drama-requests` 的寫法）。

## How to verify

```bash
cd apps/web && npx vitest run app/api/video/automation/series && npm run lint && npm run typecheck
```

2026-09-27（claude-fable-5-1-video-drama）：PR #823。共用的 `guard.ts` 放 `seriesPath`（slug 與集數先驗證）、`isRefusal`、英文的 `problem()`；`context` 的 `?episode=` 也驗證；`docs` 的 body 上限 1 MiB 用 `Content-Length` 與讀完後的長度兩道。route.test.ts 覆蓋無權杖 401、cookie 不轉送、每條路徑的對應與壞 slug／集數的 404。
