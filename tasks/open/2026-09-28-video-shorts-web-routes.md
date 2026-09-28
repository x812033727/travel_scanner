---
id: 2026-09-28-video-shorts-web-routes
title: Video shorts A2: web routes that forward the worker's Shorts calls
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-28T03:21:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/api/video/automation/shorts
---

# Video shorts A2: web routes that forward the worker's Shorts calls

## Why

nginx 只對外開放網站，不開放 API；工人與本機工具打的每一個 `/video/…` 端點都要有一支對應的 Next 路由把請求連同工具權杖轉給 API（`apps/web/app/api/video/…`）。Shorts 多了幾個工人端點（`docs/videos/SHORTS.md` §端點），沒有這些路由，工人在主機上呼叫會是 404。

## Definition of done

- [ ] `apps/web/app/api/video/automation/shorts/` 底下有這些路由，每支都經 `forwardToSpeech` 轉送、只帶工具權杖、不帶 cookie：
  - `POST tick`
  - `GET next`
  - `POST plan`、`POST topics`、`POST report`
  - `POST [slug]/start`、`POST [slug]/done`
- [ ] 路徑裡的 `slug` 先用 Shorts 的規則檢查（`^[a-z][a-z0-9-]{2,79}$`），不合的回 404，不送到 API。
- [ ] `route.test.ts`：每支路由轉到正確的上游路徑、沒有權杖回 401、壞的 slug 回 404、請求本體超過上限回 413。

## Steps

- [ ] 照 `apps/web/app/api/video/automation/topics/route.ts` 與 `series/guard.ts` 的寫法。
- [ ] 本體上限：`plan`、`topics`、`report` 1 MiB；其餘 64 KiB。
- [ ] 測試照 `apps/web/app/api/video/automation/series/route.test.ts`。

## How to verify

```bash
npm run lint:web && npm run typecheck:web
cd apps/web && npx vitest run app/api/video/automation/shorts
```

## Notes

- 後台頁面打的 `/admin/video-shorts/…` 走通用的 `/api/travel` 代理，不需要新路由；只有二進位或很大的回應才需要（批次下載的 zip 在 `2026-09-28-video-shorts-admin-tab`）。
- 這張票可以跟 A1 同時做：端點的路徑與方法以 `docs/videos/SHORTS.md` §端點 為準。A1 實作時若改了路徑，回來改這裡。
