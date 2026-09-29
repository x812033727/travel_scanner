---
id: 2026-09-27-video-drama-room-messages-api
title: Video drama room API: a discussion thread on every series document and every episode's screenplay
status: done
priority: P1
area: api
owner: codex-p1-audit
claimed_at: 2026-09-29T02:11:27Z
created_at: 2026-09-27T06:16:02Z
completed_at: 2026-09-29T02:11:33Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/video_automation/messages.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/migrations
  - apps/api/tests/test_video_drama_messages.py
  - apps/api/tests/test_migration_0108_video_drama_messages.py
  - apps/web/app/api/video/automation/series
---

# Video drama room API: a discussion thread on every series document and every episode's screenplay

## Why

站主對設定集、細綱與劇本只能「退回＋備註」，來回兩次就卡住；站主 2026-09-27 要能「討論劇本」再「製作劇本」。設計在 `docs/videos/DRAMA-FLOW.md` §三：每份文件與每集劇本一條討論串，站主發言，工人下一輪讓模型回覆或出新版本。這張做伺服器端。

## Definition of done

- [x] 遷移（接 head；平行的遷移票見 DRAMA-FLOW.md）：`video_drama_messages`：`id`、`series_id`（FK CASCADE）、`subject`（String(24)，樣式 `^(setting|outline|chapter:\d+|bible|script:\d+)$`）、`author`（`owner`｜`planner`｜`writer`，CHECK）、`body_md`（Text，≤ 8,000）、`refers_to`（String(16)：文件版本號或劇本 sha 前 12 碼）、`answered_at`、`created_at`、`created_by_user_id`；索引 `(series_id, subject, created_at)`。
- [x] 後台：`GET /admin/video-automation/series/{slug}/messages?subject=`（content.read）；`POST …/messages` `{subject, body}`（content.manage；該 subject 的文件已核准、或劇本關卡已核准就 409；audit `video_drama_message_posted`）。
- [x] 工人（VideoTool）：`GET /video/automation/series/messages/next` → 最舊的、`answered_at` 為空的站主訊息，連同文件最新版（或劇本的 slug 與集數）、整條串、`context_view`；`POST …/messages/{id}/answer` `{reply_md, revised?: {body_md, body_json}}` → 存模型回覆（`author` 依 subject）、寫 `answered_at`；`revised` 有東西且 subject 是文件時走 `submit_doc` 出新版本（`review`）；劇本的 `revised` 只存回覆，檔案由工人自己寫。
- [x] `SeriesDocOut` 帶 `unanswered`（等模型回覆的則數）；`SeriesSummary.messages_pending`。
- [x] `AppError` 只在 `admin_api.py`，模組丟自己的例外（後台路徑不需要四語訊息）。
- [x] 測試：發言、已核准拒收、next 的順序、answer 出新版本、劇本的 answer 不出版本。

## Steps

- [x] 遷移與 model。
- [x] `messages.py`、schemas、admin_api。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_drama_messages.py tests/test_video_series.py -q
```

## Notes

- 2026-09-27 做完（claude-fable-5-1-video-languages）。遷移是 `0108_video_drama_messages`（接 one-off 的 0107；併 main 時從 0106 重新編號）。
  - 表照 DoD；`refers_to` 文件存 `v<版本號>`，劇本存 `script` 審核 `content_sha256` 前 12 碼（還沒有劇本審核時是 `null`）。
  - 發言規則（`messages.post_message`）：subject 要是這部作品有的（one-off 只有 `bible` 與 `script:1`；作品有 setting／outline／`chapter:n`（n ≤ 篇數）／`script:n`（n ≤ 集數）），不是就 404 `video_drama_thread_not_found`。文件核准 → 409 `video_drama_doc_approved`；文件還沒有第一版可以先留言（`refers_to` 為 null）。劇本：那一集還沒開始（沒 slug）→ 409 `video_drama_script_not_started`；最新的 `script` 審核已核准 → 409 `video_drama_script_approved`。
  - 工人：`GET /video/automation/series/messages/next` 回最舊、`answered_at` 為空的站主訊息，帶 `thread`、`series`、`target`（`doc`｜`script`）、`doc`（最新版）或 `episode`（帶 slug）、`context`（劇本用那一集、細綱用那篇第一集的脈絡）。`POST …/messages/{id}/answer`：回覆存成 `planner`／`writer` 那一則並寫 `answered_at`；文件有 `revised` 就出新版 `review`，被取代的 `review` 版標成 `rejected`、備註「討論後出了新版本」（`series.DISCUSSION_NOTE`），`_rewrite_job` 算重寫次數時扣掉這些，所以討論不吃 `series_doc_rewrites`；文件在中間被核准就只留回覆、丟掉 `revised`；劇本一律只留回覆。回覆過或不是站主的訊息 → 409 `video_drama_message_answered`。
  - `SeriesDocOut.unanswered`、`SeriesSummary.messages_pending`：`series_view`／`list_series` 各多一個 group by 查詢。
  - 網站的工人轉送：`apps/web/app/api/video/automation/series/messages/next` 與 `messages/[id]/answer` 兩個 route（原本的 series 轉送是逐條列的，不是 catch-all），測試在 `series/route.test.ts`。
- 討論的模型呼叫走既有的 `/video/automation/run`，`variant: "discuss"`，提示詞紀錄 `planner:discuss`、`writer:discuss`；不算每月草稿（同其他 variant）。
- 網站的 BFF 轉送：`api()` 走 `apps/web/app/api/travel/[...path]` 的通用代理，工人的路由看 `apps/web/app/api/video/automation/` 現有的 series 轉送有沒有涵蓋 `series/messages/*`，沒有就加。


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：claude-fable-5-1-video-languages；原分支：未記錄。

- PR #870 merged; all required checks SUCCESS; task DoD/Steps all checked.
- apps/api/app/video_automation/messages.py:323 answer_message; admin_api.py:732 answer_video_series_message; migration 0108_video_drama_messages.py present.
- tools/video/automation/client.mjs:141 calls automation/series/messages/next.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Close open task with merged-PR and CI evidence; preserve history in tasks/done.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
