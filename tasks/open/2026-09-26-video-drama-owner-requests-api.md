---
id: 2026-09-26-video-drama-owner-requests-api
title: Video drama: the owner starts an episode from /admin/videos and the worker picks it up (API)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-26T05:12:38Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-media-api
scope:
  - apps/api/app/video_automation
  - apps/api/migrations/versions/0097_video_drama_requests.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_migration_0097_video_drama_requests.py
---

# Video drama: the owner starts an episode from /admin/videos and the worker picks it up (API)

## Why

站主 2026-09-26 補充的要求：漫劇最後要**全部接到後台**，讓站主能自己控制與製作，不必碰命令列。現有的自動化只會照排程（`draft_interval_hours`）自己挑題，站主只能在關卡上核准或退回；漫劇要多一條「站主發起」的路：在 `/admin/videos` 按「新的漫劇」、寫下故事前提（或選站上的文章來改編）、選風格與長度，工人下一輪就開始做這一支，而不是等排程。伺服器也要回報每支影片花了多少（媒體生成的美元、片段秒數），後台才能顯示。

## Definition of done

- [ ] 新表 `video_drama_requests`（migration `0097`）：id、`premise`（故事前提或改編的文章 slug）、`source_guide`、`style_preset`、`target_minutes`、`status`（queued／started／done／cancelled）、`slug`（工人開始後填）、建立者與時間；站主可取消 queued 的。
- [ ] `POST /admin/video-automation/drama-requests`（content.manage）建立；`GET` 列出；`DELETE /{id}` 取消 queued 的。
- [ ] 工人的 `GET /video/automation/next`（或 `settings`）回報最舊的 queued request，工人 `POST /video/automation/drama-requests/{id}/start` 認領（寫 slug、status started），做完由 `report` 或 review 的最後關卡標 done。
- [ ] `ProjectSummary`／`ProjectOut` 多 `format`、`media_usd`（`app.video_media.meter.slug_usd`）、`clip_seconds`，後台列表能顯示每支的花費。
- [ ] ruff、mypy、pytest 綠；migration 有整合測試。

## Steps

- [ ] model＋migration＋schemas（`DramaRequestIn/Out`）。
- [ ] admin router 與 tool router 的端點；`list_projects` 加 media 花費。
- [ ] 測試：建立、列出、取消、工人認領、花費欄位。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_drama_requests.py tests/test_video_reviews.py -q
```

## Notes

設計全文在 `docs/videos/DRAMA.md`；工人這一端在 `2026-09-26-video-drama-automation`（`automation/flow.mjs` 的 `advance()` 要先消化 queued request 再做排程草稿），後台畫面在 `2026-09-26-video-drama-owner-controls-ui`。
