---
id: 2026-09-28-video-dropped-episode-request
title: 放棄影片後，那一集的漫劇請求列仍是 started
status: done
priority: P3
area: api
owner: claude-fable-5-1-drama-request
claimed_at: 2026-09-30T03:39:59Z
created_at: 2026-09-28T13:07:52Z
completed_at: 2026-09-30T03:56:43Z
branch: claude/drama-request-cancelled-on-abandon
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews.py
---

# 放棄影片後，那一集的漫劇請求列仍是 started

## Why

作品的每一集開始時，伺服器都會建一列 `video_drama_requests`，狀態 `started`（`apps/api/app/video_automation/series.py` 的 `start_episode`；單集漫劇沿用它排隊時的那一列）。影片做完、上架確認核准時，工人回報 `episodes/{n}/done`，那一列才變成 `done`。

站主在 `/admin/videos` 放棄那支影片時，票 `2026-09-28-video-story-api-policy-languages` 已經讓那一集變成 `skipped`（名額釋放），但請求列沒有動：它一直是 `started`，所以後台的漫劇請求清單會一直顯示「製作中」，`GET /video/automation/drama-requests`（工人讀的進行中清單）也一直列著它。品牌故事一天兩支，放棄的故事會一直累積在這裡。

## Definition of done

- [x] 放棄一支屬於作品的影片時，那一集的請求列若還是 `started`，改成 `cancelled`（寫 `cancelled_at`），後台清單不再顯示成製作中。
- [x] 已經 `done` 的請求不動；不屬於作品的舊請求照舊。
- [x] `ruff`、`mypy`、`pytest` 通過。

## Steps

- [x] `video_reviews/admin_service.py` 的 `_skip_abandoned_episode`：一起把 `episode.request_id` 指的請求列改成 `cancelled`。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_reviews.py tests/test_video_story_policy.py
```

## Notes

- 2026-09-28 開票（claude-opus-5-5-video-story-policy）：做「放棄影片時釋放名額」時看到的，那張票的範圍只有集數，沒有動請求列。
- `request_view` 把「`started` 而且影片有 YouTube id」讀成 `done`；放棄的影片沒有 id，所以一直是 `started`。
- 2026-09-30 做完（claude-fable-5-1-drama-request）：`_skip_abandoned_episode` 把那一集改成 skipped 之後，呼叫新的 `_cancel_started_request`：鎖住 `episode.request_id` 指的請求列（順序是作品 → 集數 → 請求，跟 `start_episode` 一樣），還是 `started` 才改成 `cancelled` 並寫 `cancelled_at`、`updated_at`（跟 `cancel_request`、`withdraw_series` 用同一組欄位）。`cancelled` 從 migration 0097 起就在 CHECK 約束與 `REQUEST_STATUSES` 裡，所以沒有新狀態、沒有 migration、沒有新的 `AppError`。
- 已經 `done` 的集數在前面的 `EPISODE_OPEN` 檢查就返回，請求列不讀也不動；集數還開著但請求已是 `done` 的（理論上不會有）也不動。不屬於作品的影片 `_episode_of` 回 None，照舊。
- 稽核紀錄 `video_series_episode_skipped` 的 metadata 沒有加欄位：`tests/test_video_story_policy.py` 整列比對它，加了就得改範圍外的檔案。
- 測試在 `tests/test_video_reviews.py`（mock session，照該檔 `drop_project` 測試的寫法）：放棄作品的影片 → 請求 cancelled、時間等於 `dropped_at`；done 之後放棄 → 不動；教學影片 → 不查請求。`tests/test_video_story_policy.py` 三個真資料庫的放棄測試照樣通過。
- 正式站上已經卡在 `started` 的舊列不會自己變：這支只管之後的放棄。清舊列另開了票 `2026-09-30-video-dropped-request-backfill`。
