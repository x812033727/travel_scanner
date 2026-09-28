---
id: 2026-09-28-video-story-admin-import-api
title: 故事企劃清單的後台 API：從頁面匯入、恢復略過的故事
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-28T10:56:09Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-api-series-kind
scope:
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_story_admin.py
---

# 故事企劃清單的後台 API：從頁面匯入、恢復略過的故事

## Why

站主的原則是一切在後台做、不碰命令列（票 `2026-09-28-video-story-admin`）。票 `2026-09-28-video-story-api-series-kind` 做好了匯入本身（`app/video_automation/stories.py` 的 `import_story_rows`），但只接在主機指令 `python -m app.cli video-story-import` 上；後台沒有端點可以貼上 `stories.json` 試跑再寫入。後台票也要能「恢復」一個略過的故事，現在只有 `POST /admin/video-automation/series/{slug}/episodes/{number}/skip`，沒有反方向。後台票的 Steps 寫明：API 本身缺的另開票，就是這張。

改每日支數不用新端點：`PATCH /admin/video-automation/series/{slug}` 已經收 `episodes_per_day`（1–12，null 表示不限）、`image_model`、`look`，只有故事作品收。

## Definition of done

- [ ] `POST /admin/video-automation/series/{slug}/stories/import`：內文是編譯好的 `stories.json` 加 `apply`、`limit`、`episodes_per_day`，回傳 `StoryImportReport.as_dict()` 同樣的欄位；預設試跑；`apply` 要 `content.manage`（建立作品的權限），有問題時不寫入並回 422 帶報告。檔案大小上限寫成常數（100 個故事約 1.3 MB）。
- [ ] 恢復略過的故事：`skipped` 且從沒開始過（`started_at` 是 NULL）的集數回到 `ready`；開始過的拒絕並說明；只限故事作品或也給一般作品，實作時決定並寫進 Notes。
- [ ] 測試照 `tests/test_video_story.py` 的 SQLite 做法，本機就能跑。
- [ ] `ruff`、`mypy app`、`mypy tests`、`pytest` 通過。

## Steps

- [ ] 路由與權限（`require_capability`），沿用 `SeriesRefused` 轉成問題回應的寫法。
- [ ] `series.py` 加恢復集數的函式與稽核紀錄。
- [ ] 測試：試跑不寫、apply 寫入、壞檔 422、沒有權限 403、恢復與拒絕恢復。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story_admin.py tests/test_video_story.py
```

## Notes

- 報告欄位與判斷都在 `stories.py`，端點只做轉接；不要在路由裡再寫一次驗證。
- 經網站轉送時注意 `apps/web` 的 BFF 與 nginx 的請求大小上限（後台票負責轉送路由）。
