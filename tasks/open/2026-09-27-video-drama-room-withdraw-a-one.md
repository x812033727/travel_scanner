---
id: 2026-09-27-video-drama-room-withdraw-a-one
title: Video drama room: withdraw a one-off before the worker starts it
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T14:06:11Z
created_at: 2026-09-27T13:54:14Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/web/components/admin-video-series.tsx
---

# Video drama room: withdraw a one-off before the worker starts it

## Why

2026-09-27 起單集漫劇是一集的作品（`kind = one-off`，`docs/videos/DRAMA-FLOW.md` §二）。以前排隊中的請求可以在「單集漫劇」清單按「撤回」（`DELETE /admin/video-automation/drama-requests/{id}`）；現在表單建的是作品，清單列的是 `?kind=one-off` 的作品，作品在 `setting`（故事聖經還沒核准）時 `PATCH /series/{slug}` 不接受 `status`（409 `video_series_not_planned`），所以站主沒有地方撤回一部還沒開始做的單集。web 那張的審查（2026-09-27）發現這個缺口，先記下來。

## Definition of done

- [ ] 作品在 `setting`／`outline`（文件還沒核准、沒有任何一集開始）時可以撤回：`DELETE /admin/video-automation/series/{slug}` 或 `PATCH … {status: "cancelled"}`，把該作品的 `queued` 請求列一起標成 `cancelled`（`video_drama_requests`），audit 一筆；已開始的集一律拒絕。
- [ ] 「單集漫劇」清單的卡片與作品頁多一顆「撤回」（content.manage），確認後呼叫；長篇作品同一顆按鈕在文件階段也能用。
- [ ] 測試：撤回排隊中的單集、已開始的拒絕；web 的 vitest。

## Notes

- 原本的請求撤回路由留著給遷移前的舊請求。
