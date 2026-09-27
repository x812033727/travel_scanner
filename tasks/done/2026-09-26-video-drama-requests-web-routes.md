---
id: 2026-09-26-video-drama-requests-web-routes
title: Video drama: forward the worker's drama request calls through the web app
status: done
priority: P2
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T06:13:11Z
created_at: 2026-09-26T06:11:45Z
completed_at: 2026-09-26T06:16:06Z
branch:
depends_on: []
scope:
  - apps/web/app/api/video/automation/drama-requests
---

# Video drama: forward the worker's drama request calls through the web app

## Why

`2026-09-26-video-drama-owner-requests-api`（PR #797）給工人四條端點：`GET /video/automation/drama-requests`、`GET …/next`、`POST …/{id}/start`、`POST …/{id}/done`。主機工人走 `http://web:3000`、站主的電腦走 `https://mokaair.com`，nginx 只開放網站，所以每條都要有 Next.js 的轉送路由（同 `apps/web/app/api/video/automation/{settings,run,topics,videos}`，只轉影片工具權杖、不轉 cookie）。沒有這幾條，T8（`2026-09-26-video-drama-automation`）的工人拿不到站主發起的請求。

## Definition of done

- [x] `GET /api/video/automation/drama-requests`、`GET …/drama-requests/next`、`POST …/drama-requests/<uuid>/start`、`POST …/drama-requests/<uuid>/done` 轉到 API 的同名路徑；id 不是 UUID 回 404；沒有 `mkv_` 權杖回 401；cookie 不轉。
- [x] vitest、lint、typecheck 綠。

## Steps

- [x] 四個 `route.ts`＋一個 `route.test.ts`。

## How to verify

```bash
cd apps/web && npx vitest run app/api/video/automation && npm run lint && npm run typecheck
```

## Notes

從 `2026-09-26-video-drama-owner-controls-ui` 的 scope 拿掉 `apps/web/app/api/video/automation`：後台頁面走 `api("/admin/video-automation/…")` 的一般 admin 代理，不用這條；這條是工人專用。
