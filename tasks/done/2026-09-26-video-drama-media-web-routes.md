---
id: 2026-09-26-video-drama-media-web-routes
title: Video drama: web forward routes for the media API, streaming file downloads
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T05:22:32Z
created_at: 2026-09-26T01:53:25Z
completed_at: 2026-09-26T05:27:56Z
branch: claude/video-drama-media-web-routes
depends_on: []
scope:
  - apps/web/app/api/video/media
---

# Video drama: web forward routes for the media API, streaming file downloads

## Why

nginx 只開放網站；工具走 `https://mokaair.com/api/video/media/*`（主機工人走 `http://web:3000`），由 Next.js 轉送到 API，做法同 `apps/web/app/api/video/speech/forward.ts`。片段是 10–40 MB 的 mp4，下載路由必須串流並支援 Range，不能像語音路由那樣 `arrayBuffer()`。

## Definition of done

- [x] 一個 catch-all `apps/web/app/api/video/media/[...path]/route.ts`（做法同 `reviews/[...path]`，比七個檔案好維護）認得八條路由：`status`、`images`、`clips`、`music`、`judge`、`jobs/<uuid>`、`files/<slug>/<sha256>` 的 PUT 與 GET；只轉 `mkv_` 權杖、不轉 cookie。
- [x] POST 本體上限 256 KiB、逾時 90（送出）／180（judge）秒；`jobs` 240 秒；`files` GET 串流 `upstream.body` 並傳回 `content-type`、`content-length`、`content-range`、`accept-ranges`、`etag`，錯誤答案以 JSON 傳回；PUT 4 MiB 分段（`part`、`parts`、`size` 只收數字）。
- [x] vitest（7 個）、lint、typecheck 綠。

## Steps

- [x] `mediaRoute(path, method)` 決定路由種類、本體上限與逾時；JSON 路由緩衝、上傳送 bytes、下載串流。
- [x] `files` GET 沿用 `admin-video-files` 的串流與 Range 做法，改認權杖。
- [x] 路由測試：路由表、送出（含 Retry-After 傳回）、串流下載、錯誤答案、上傳分段、拒絕的情況、502。

## How to verify

```bash
cd apps/web && npm run lint && npm run typecheck && npm run test:web -- app/api/video/media
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 端點形狀（`JobOut`、`JudgeOut`、分段上傳）以 S2 `2026-09-26-video-drama-media-api` 為準，可平行開發。

- 2026-09-26 做完。給 T2（工具端用戶端）：路徑就是 `${site}/api/video/media/<同 API 的路徑>`；下載要用串流讀（回應可以是 206），輪詢一次最多等 240 秒。`redirect: "manual"`：API 不會轉址，若出現 3xx 就是設定錯了，會以原狀態碼傳回。
