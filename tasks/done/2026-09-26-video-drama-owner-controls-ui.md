---
id: 2026-09-26-video-drama-owner-controls-ui
title: Video drama: production controls on /admin/videos: start an episode, watch progress and spend
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T07:31:27Z
created_at: 2026-09-26T05:12:40Z
completed_at: 2026-09-26T07:35:19Z
branch: claude/video-drama-owner-controls
depends_on:
  - 2026-09-26-video-drama-owner-requests-api
  - 2026-09-26-video-drama-admin-settings-and-gates
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/app/api/video/automation
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video drama: production controls on /admin/videos: start an episode, watch progress and spend

## Why

站主 2026-09-26 補充的要求：漫劇要能在後台**控制與製作**。`/admin/videos` 目前只有審核（選大綱、聽旁白、看成片、確認上架）與設定分頁；站主要能在同一頁發起一支漫劇、看它做到哪一步、花了多少，必要時取消。這張票是後台那一半；伺服器端在 `2026-09-26-video-drama-owner-requests-api`，設定區與 look／storyboard 卡片在 `2026-09-26-video-drama-admin-settings-and-gates`。

## Definition of done

- [x] `/admin/videos` 有「新的漫劇」：故事前提（多行文字）或「改編站上文章」（選 slug）、風格預設、目標長度，送出後出現在「排隊中」清單，可取消。
- [x] 每支影片的卡片顯示格式（投影片／漫劇）、目前步驟（現有 checklist）、媒體花費（美元、片段秒數）、等站主的關卡數。
- [x] 進度不用重新整理就會更新（沿用頁面現有的輪詢或 SWR 方式）。
- [x] 五語文案；`check:i18n`、lint、typecheck、vitest 綠。

## Steps

- [x] 型別與 API 呼叫（`apps/web/app/api/video/automation/*` 若需要新的 BFF 路由）。
- [x] 元件：`NewDramaForm`、排隊清單、卡片上的格式與花費。
- [x] 測試與五語 `admin.json`。

## How to verify

```bash
cd apps/web && npm run lint && npm run typecheck && npm run test:web -- admin-video && git add -A && CI=1 npm run check:i18n
```

## Notes

設計全文在 `docs/videos/DRAMA.md`。五語 `admin.json` 在 `2026-09-25-run-the-site-s-claude-features` 的 scope 裡，這張票要排在它之後。

2026-09-26（claude-fable-5-1-video-drama）：做在 `claude/video-drama-owner-controls`，疊在 #807（同一個 `admin-video-reviews.tsx`）。沒有新的 BFF 路由：後台頁走泛用的 `api("/admin/video-automation/drama-requests")`（#797 的 admin 路由），`apps/web/app/api/video/automation/*` 只有工人用的權杖路由（#798）。列表與專案頁每 60 秒重讀（`REFRESH_MS`）；舊站對 drama-requests 回 404 時清單留空。完成與取消的請求一週後從清單消失，影片本身留在列表。
