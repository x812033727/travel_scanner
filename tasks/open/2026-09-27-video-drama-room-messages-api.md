---
id: 2026-09-27-video-drama-room-messages-api
title: Video drama room API: a discussion thread on every series document and every episode's screenplay
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-27T06:16:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/messages.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/migrations
  - apps/api/tests/test_video_drama_messages.py
  - apps/api/tests/test_migration_0104_video_drama_messages.py
---

# Video drama room API: a discussion thread on every series document and every episode's screenplay

## Why

站主對設定集、細綱與劇本只能「退回＋備註」，來回兩次就卡住；站主 2026-09-27 要能「討論劇本」再「製作劇本」。設計在 `docs/videos/DRAMA-FLOW.md` §三：每份文件與每集劇本一條討論串，站主發言，工人下一輪讓模型回覆或出新版本。這張做伺服器端。

## Definition of done

- [ ] 遷移（接 head；平行的遷移票見 DRAMA-FLOW.md）：`video_drama_messages`：`id`、`series_id`（FK CASCADE）、`subject`（String(24)，樣式 `^(setting|outline|chapter:\d+|bible|script:\d+)$`）、`author`（`owner`｜`planner`｜`writer`，CHECK）、`body_md`（Text，≤ 8,000）、`refers_to`（String(16)：文件版本號或劇本 sha 前 12 碼）、`answered_at`、`created_at`、`created_by_user_id`；索引 `(series_id, subject, created_at)`。
- [ ] 後台：`GET /admin/video-automation/series/{slug}/messages?subject=`（content.read）；`POST …/messages` `{subject, body}`（content.manage；該 subject 的文件已核准、或劇本關卡已核准就 409；audit `video_drama_message_posted`）。
- [ ] 工人（VideoTool）：`GET /video/automation/series/messages/next` → 最舊的、`answered_at` 為空的站主訊息，連同文件最新版（或劇本的 slug 與集數）、整條串、`context_view`；`POST …/messages/{id}/answer` `{reply_md, revised?: {body_md, body_json}}` → 存模型回覆（`author` 依 subject）、寫 `answered_at`；`revised` 有東西且 subject 是文件時走 `submit_doc` 出新版本（`review`）；劇本的 `revised` 只存回覆，檔案由工人自己寫。
- [ ] `SeriesDocOut` 帶 `unanswered`（等模型回覆的則數）；`SeriesSummary.messages_pending`。
- [ ] `AppError` 只在 `admin_api.py`，模組丟自己的例外（後台路徑不需要四語訊息）。
- [ ] 測試：發言、已核准拒收、next 的順序、answer 出新版本、劇本的 answer 不出版本。

## Steps

- [ ] 遷移與 model。
- [ ] `messages.py`、schemas、admin_api。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_drama_messages.py tests/test_video_series.py -q
```

## Notes

- 討論的模型呼叫走既有的 `/video/automation/run`，`variant: "discuss"`，提示詞紀錄 `planner:discuss`、`writer:discuss`；不算每月草稿（同其他 variant）。
- 網站的 BFF 轉送：`api()` 走 `apps/web/app/api/travel/[...path]` 的通用代理，工人的路由看 `apps/web/app/api/video/automation/` 現有的 series 轉送有沒有涵蓋 `series/messages/*`，沒有就加。
