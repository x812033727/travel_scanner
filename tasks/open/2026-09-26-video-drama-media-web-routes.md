---
id: 2026-09-26-video-drama-media-web-routes
title: Video drama: web forward routes for the media API, streaming file downloads
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-26T01:53:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/api/video/media
---

# Video drama: web forward routes for the media API, streaming file downloads

## Why

nginx 只開放網站；工具走 `https://mokaair.com/api/video/media/*`（主機工人走 `http://web:3000`），由 Next.js 轉送到 API，做法同 `apps/web/app/api/video/speech/forward.ts`。片段是 10–40 MB 的 mp4，下載路由必須串流並支援 Range，不能像語音路由那樣 `arrayBuffer()`。

## Definition of done

- [ ] `apps/web/app/api/video/media/{status,images,clips,music,judge}/route.ts`、`jobs/[id]/route.ts`、`files/[slug]/[sha256]/route.ts` 存在，只轉 `mkv_` 權杖、不轉 cookie。
- [ ] POST 本體上限 256 KiB、逾時 90–180 秒；`jobs` 240 秒；`files` GET 串流 `upstream.body` 並傳回 `content-type`、`content-length`、`content-range`、`accept-ranges`、`etag`；PUT 4 MiB 分段（`part`、`parts`、`size` 只收數字）。
- [ ] vitest、lint、typecheck 綠。

## Steps

- [ ] 用 `forwardToSpeech(request, "media/…", method, maxBody, timeout)` 寫五個 JSON 路由與 `jobs`。
- [ ] `files` GET 照抄 `apps/web/app/api/admin-video-files/[slug]/[sha256]/route.ts` 的串流與 Range，改用權杖；PUT 照抄 `reviews/[...path]` 的分段分支。
- [ ] 路由測試：權杖格式、上限、Range 傳遞、串流不緩衝。

## How to verify

```bash
cd apps/web && npm run lint && npm run typecheck && npm run test:web -- app/api/video/media
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 端點形狀（`JobOut`、`JudgeOut`、分段上傳）以 S2 `2026-09-26-video-drama-media-api` 為準，可平行開發。
