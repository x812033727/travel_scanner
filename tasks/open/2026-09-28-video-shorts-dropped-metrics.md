---
id: 2026-09-28-video-shorts-dropped-metrics
title: 撤掉的已公開 Shorts 在成效表一直顯示等待讀取
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T16:52:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_shorts/overview.py
  - apps/api/app/video_shorts/schemas.py
  - apps/web/components/admin-video-shorts-data.ts
---

# 撤掉的已公開 Shorts 在成效表一直顯示等待讀取

## Why

#935（`717e16280`）修掉了「YouTube 上已刪除的 Short 在成效表顯示『還沒到時間』」的誤導文字，但「撤掉」（dropped）的 Short 還有同樣的問題，這個問題在 #935 之前就存在。

- `stats.read_due`（`apps/api/app/video_shorts/stats.py:113-121`）跳過 `dropped_at` 不為空的影片，所以撤掉的 Short 不會再被讀成效。
- `overview.metrics_view`（`overview.py:253-262`）卻不過濾 `dropped_at`，成效表照樣列出它。
- `ShortMetrics`（API 端 `schemas.py:414-422`、web 端 `admin-video-shorts-data.ts:69-72`）沒有 `dropped_at`，頁面的 `blankReason`（:129）無從分辨，結果「現在」那一格永遠寫「等下一次讀取」。

要走到這個狀態並不容易：影片有 `youtube_video_id` 後，介面就不顯示撤掉鈕（`admin-video-reviews.tsx:336`），其他路徑也各自排除了撤掉的影片。但 `drop_project`（`apps/api/app/video_reviews/admin_service.py:811-826`）不會拒絕已上傳的影片，所以直接 `POST /admin/videos/{slug}/drop`，或詳情頁開著最多 60 秒、同時在另一個分頁認領上傳，就會走到。

2026-09-28 部署 `717e1628` 後的稽核找到的（兩個代理獨立確認）。

## Definition of done

擇一，並寫下理由：
- [ ] `drop_project` 拒絕已有 `youtube_video_id` 的影片（409 並說明要改用撤回），或
- [ ] 成效表不列撤掉的 Short，或列出時寫「已撤掉，不再讀取」。

## Steps

- [ ] 決定做法（前者最小，不必動 web）。
- [ ] 補對應的 API 測試（與 web 測試，如果改了頁面）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts.py -q
npm run test:web
```
