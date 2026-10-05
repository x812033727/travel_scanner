---
id: 2026-09-27-video-drama-room-withdraw-a-one
title: Video drama room: withdraw a one-off before the worker starts it
status: done
priority: P2
area: api
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T14:06:11Z
created_at: 2026-09-27T13:54:14Z
completed_at: 2026-10-05T00:24:04Z
branch: claude/video-review-manga-workflow-fp1rpz
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/messages
  - apps/api/tests/test_video_series.py
---

# Video drama room: withdraw a one-off before the worker starts it

## Why

2026-09-27 起單集漫劇是一集的作品（`kind = one-off`，`docs/videos/DRAMA-FLOW.md` §二）。以前排隊中的請求可以在「單集漫劇」清單按「撤回」（`DELETE /admin/video-automation/drama-requests/{id}`）；現在表單建的是作品，清單列的是 `?kind=one-off` 的作品，作品在 `setting`（故事聖經還沒核准）時 `PATCH /series/{slug}` 不接受 `status`（409 `video_series_not_planned`），所以站主沒有地方撤回一部還沒開始做的單集。web 那張的審查（2026-09-27）發現這個缺口，先記下來。

## Definition of done

- [x] 作品在 `setting`／`outline`（文件還沒核准、沒有任何一集開始）時可以撤回：`DELETE /admin/video-automation/series/{slug}` 或 `PATCH … {status: "cancelled"}`，把該作品的 `queued` 請求列一起標成 `cancelled`（`video_drama_requests`），audit 一筆；已開始的集一律拒絕。
- [x] 「單集漫劇」清單的卡片與作品頁多一顆「撤回」（content.manage），確認後呼叫；長篇作品同一顆按鈕在文件階段也能用。
- [x] 測試：撤回排隊中的單集、已開始的拒絕；web 的 vitest。

## Notes

- 原本的請求撤回路由留著給遷移前的舊請求。
- 做法（2026-09-27）：`DELETE /admin/video-automation/series/{slug}`（content.manage）→ `series.withdraw_series`。
  條件不是作品狀態，而是「每一集都還在 `planned`／`ready`」：一部單集在故事聖經核准後是 `active`、那一集
  `ready`，worker 還沒接手，也該能撤回；長篇在文件階段沒有任何集，同一條規則也成立。任何一集到
  `queued`／`started`／`done`／`skipped` 就 409 `video_series_started`，請站主到影片清單放棄那支影片。
- 撤回是刪掉作品列：文件、討論、集數靠 `ON DELETE CASCADE` 一起走；請求列保留，`queued` 的先標
  `cancelled`（`cancelled_at`）再刪作品，`series_id` 由 `SET NULL` 清掉，所以舊的請求清單還留得下紀錄。
  audit 動作 `video_series_withdrawn`，metadata 帶種類、當時狀態與被取消的請求 id。
- worker 若正在寫這部的故事聖經，送回時會拿到 404（作品不在了），那一輪就作廢；沒有另外處理。
- web：單集清單卡片在 `setting`，或 `active` 且那一集 `ready`、沒開始也沒完成時有「撤回」；作品頁在每一集都
  `planned`／`ready` 時有，撤回後回到清單。被拒絕時顯示伺服器的理由。
- 整合測試 `test_a_drama_is_withdrawn_before_its_episode_starts_and_not_after` 要 PostgreSQL，本機沒跑，靠 CI。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-fable-5-1-video-languages (since 2026-09-27T14:06:11Z) was stale; the work landed in #870 and every box was already ticked, so the ticket is closed.
