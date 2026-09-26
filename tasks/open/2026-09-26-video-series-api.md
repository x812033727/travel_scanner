---
id: 2026-09-26-video-series-api
title: Video series A1: series, documents and episodes on the server, the script gate and the auto-continue rule
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-26T17:36:21Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-settings
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/requests.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/models.py
  - apps/api/migrations/versions
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_reviews.py
---

# Video series A1: series, documents and episodes on the server, the script gate and the auto-continue rule

## Why

一部約 100 集、分篇章的長篇漫劇要有作品層：作品、可核准的文件（設定集、總綱、篇章細綱）、集數表，以及「上一集上架才做下一集」的規則。現在的 `VideoDramaRequest` 一個前提一集、`next_request` 只看 `created_at`、沒有劇本關卡、列表沒有篩選。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [ ] 表 `video_drama_series`、`video_drama_docs`（一表三種、有版本與退回備註）、`video_drama_episodes`；`video_drama_requests` 加 `series_id`、`episode_number`；`video_projects` 加 `series_slug`、`episode_number`；migration「不存在才建」，編號接當時的 head（hands-off 的 `0099` 若已合併就是 `0100`）。
- [ ] 關卡 `script`：`Gate`、`ck_video_review_gate` 重建（同 0095），downgrade 有 script 審核時拒絕；`CHOICE_GATES` 不變。
- [ ] `next_request` 先作品集數（依 `(series, number)`，該作品沒有 `started` 的集）再單集請求；`GET /video/automation/series/next` 依「作品 active、篇章細綱已核准、前一集 done 或 skipped、進行中 < `series_max_in_flight`」給下一件工作（setting／outline／chapter／episode）。
- [ ] 後台端點：作品列表與詳情、建立與 PATCH、文件 decision 與站主自改、集數 PUT、actions（plan-next-chapter、start-next、skip）；工人端點：next、docs、episodes start／recap／done、context。`AppError` 只在 `admin_api.py`。
- [ ] `GET /admin/videos?format=&series=` 篩選（上限 200 改成依條件查）。
- [ ] `video_stage_prompts` 加 `variant`、`StageRunIn.variant`；`GET /admin/video-automation/prompts` 依 variant 分開。
- [ ] 設定：`series_max_in_flight`、`series_script_gate`、`series_auto_continue`、`series_chapter_ahead`、`series_doc_rewrites`、`series_episodes_per_month`；作品集數與作品層文件不算 `max_drafts_per_month`。
- [ ] pytest：文件版本與退回、順序與接續規則、篩選、關卡、設定。

## Steps

- [ ] models、migration、schemas。
- [ ] `series.py`（作品、文件、集數、next 的規則）、`requests.py`、`settings.py`、`admin_api.py`、`video_reviews` 的篩選與關卡。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_series.py tests/test_video_automation_settings.py tests/test_video_reviews.py -q
```

## Notes

依賴 `2026-09-26-video-hands-off-settings` 只為了 migration 編號與 `admin-video-settings` 的欄位；它若沒人動，這張票先拿 0099 並在票裡註明。
