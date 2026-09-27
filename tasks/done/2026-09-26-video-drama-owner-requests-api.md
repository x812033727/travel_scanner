---
id: 2026-09-26-video-drama-owner-requests-api
title: Video drama: the owner starts an episode from /admin/videos and the worker picks it up (API)
status: done
priority: P1
area: api
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T06:01:55Z
created_at: 2026-09-26T05:12:38Z
completed_at: 2026-09-26T06:09:51Z
branch:
depends_on:
  - 2026-09-26-video-drama-media-api
scope:
  - apps/api/app/video_automation
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_media/meter.py
  - apps/api/app/models.py
  - apps/api/migrations/versions/0097_video_drama_requests.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_migration_0097_video_drama_requests.py
---

# Video drama: the owner starts an episode from /admin/videos and the worker picks it up (API)

## Why

站主 2026-09-26 補充的要求：漫劇最後要**全部接到後台**，讓站主能自己控制與製作，不必碰命令列。現有的自動化只會照排程（`draft_interval_hours`）自己挑題，站主只能在關卡上核准或退回；漫劇要多一條「站主發起」的路：在 `/admin/videos` 按「新的漫劇」、寫下故事前提（或選站上的文章來改編）、選風格與長度，工人下一輪就開始做這一支，而不是等排程。伺服器也要回報每支影片花了多少（媒體生成的美元、片段秒數），後台才能顯示。

## Definition of done

- [x] 新表 `video_drama_requests`（migration `0097`）：id、`premise`、`title`、`source_guide`、`style_preset`、`target_minutes`、`note`、`status`（queued／started／done／cancelled）、`slug`（工人開始後填，唯一）、建立者、認領的權杖與時間；站主可取消 queued 的。同一支 migration 給 `video_projects` 加 `format`（slides／drama，預設 slides）。
- [x] `POST /admin/video-automation/drama-requests`（content.manage；漫劇沒開啟回 409 `video_drama_disabled`）建立；`GET` 列出（最新在前，含影片已上 YouTube 就算 done）；`DELETE /{id}` 取消 queued 的（已開始回 409）。
- [x] 工人：`GET /video/automation/drama-requests`（進行中的，最舊在前，重啟後對得回自己的影片）、`GET .../drama-requests/next`（最舊的 queued 或 null）、`POST .../{id}/start` `{slug}` 認領（FOR UPDATE 鎖；不是 queued 或 slug 已被別的請求用回 409）、`POST .../{id}/done` 標完成；影片上了 YouTube 也會在列表裡顯示為 done。
- [x] `ProjectSummary`／`ProjectOut` 多 `format`、`media_usd`、`clip_seconds`（`app.video_media.meter.spend_by_slug` 一次查全部）；`ProjectIn.format` 可選，舊工具沒送就保留。
- [x] ruff、mypy、pytest 綠；migration 有整合測試（`RUN_INTEGRATION_TESTS=1`）。

## Steps

- [x] model＋migration＋schemas（`DramaRequestIn/Out`）。
- [x] admin router 與 tool router 的端點；`list_projects` 加 media 花費。
- [x] 測試：建立、列出、取消、工人認領、花費欄位。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_drama_requests.py tests/test_video_reviews.py -q
```

## Notes

設計全文在 `docs/videos/DRAMA.md`；工人這一端在 `2026-09-26-video-drama-automation`（`automation/flow.mjs` 的 `advance()` 要先消化 queued request 再做排程草稿），後台畫面在 `2026-09-26-video-drama-owner-controls-ui`。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- 服務邏輯在 `app/video_automation/requests.py`，只丟 `RequestRefused(status, code, detail)`，`admin_api.py` 轉成 `AppError`（套件裡 AppError 只在 router，照 video_media 的規矩）。建立與取消各寫一筆 `AdminAuditLog`（`video_drama_request_created`／`_cancelled`）。
- 給 T8（工人）的合約：每輪先 `GET /video/automation/drama-requests/next`，有就 `POST .../{id}/start {slug}` 再開始做這支（`settle()` 寫 `format: "drama"`、`look.preset = style_preset`、`target_minutes`），`review-push --report-only` 的 `ProjectIn` 要送 `format`；上架後 `POST .../{id}/done`（沒送也沒關係，列表看 `youtube_video_id`）。工人重啟時 `GET .../drama-requests` 對回自己工作區裡的 slug。
- 給 UI 票：`GET /admin/video-automation/drama-requests` 回 `{ requests: [...] }`；表單欄位 premise（必填）、title、source_guide（文章 slug）、style_preset、target_minutes（1–8，預設 3）、note；影片列表的每列多 `format`、`media_usd`、`clip_seconds`。
- 網站的 BFF 轉送：`apps/web/app/api/video/automation` 目前只認固定的幾條路徑，`drama-requests*` 要在 UI／T8 票加進去（不在本票 scope）。
