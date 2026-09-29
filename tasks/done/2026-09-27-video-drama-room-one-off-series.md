---
id: 2026-09-27-video-drama-room-one-off-series
title: Video drama room: a one-off episode is a one-episode series with a single story bible document
status: done
priority: P1
area: api
owner: codex-p1-audit
claimed_at: 2026-09-29T02:11:33Z
created_at: 2026-09-27T06:16:01Z
completed_at: 2026-09-29T02:11:37Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/api/migrations
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_migration_0107_video_one_off_series.py
---

# Video drama room: a one-off episode is a one-episode series with a single story bible document

## Why

單集漫劇（`video_drama_requests`）與作品的一集走不同的路：單集用「選大綱」卡片、沒有劇本關卡、退回兩次就卡住；作品有文件、有劇本關卡。站主 2026-09-27 要「整個順一下漫劇的製作流程」。設計在 `docs/videos/DRAMA-FLOW.md` §二：單集就是一集的作品，文件只有一份「故事聖經」，之後跟作品的一集完全一樣。

## Definition of done

- [x] 遷移（接 main 的 head；跟 `video-split-settings-api`、`video-drama-room-messages-api`、`video-languages-api` 平行，後落地改號）：`video_drama_series.kind`（`series`｜`one-off`，預設 `series`，CHECK）；`ck_video_drama_series_numbers` 重建，`episodes_per_chapter` 放寬到 ≥ 1；`ck_video_drama_doc_kind` 加 `bible`；把 `status = 'queued'` 的請求各建成一部 `one-off` 作品（slug `one-off-<請求 id 前 8 碼>`，title、premise、style_preset、target_minutes、note 搬過去；請求列補 `series_id`、`episode_number = 1`）。已 `started` 的請求不動，走完舊路。
- [x] `SeriesIn.kind`；`kind == "one-off"` 時 `planned_episodes = 1`、`episodes_per_chapter = 1`、沒有 aspects 與 tone 也可以。`POST /admin/video-automation/drama-requests` 改成建立 one-off 作品並回它（表單不變；`DramaRequestOut` 帶 `series_slug`）。
- [x] `next_job_for`：one-off 的文件鏈只有 `bible`（企劃 variant `bible`）；`bible` 核准 → 第 1 集 `ready` → 依 `series_auto_continue` 開始。`doc_problem` 的 `bible` 形狀：`characters`（同 `setting`）、`acts`、`outline`（單一）、`music`、`not_doing`、`lexicon`。
- [x] `context_view` 與 `start_episode` 對 one-off 把 `bible` 當 `setting` 回；`GET /admin/video-automation/series?kind=`；`SeriesSummary.kind`。
- [x] 測試：建 one-off、bible 核准開集、遷移轉換排隊中的請求、started 的不動。

## Steps

- [x] 遷移與 model。
- [x] series.py、requests.py、schemas、admin_api。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_series.py tests/test_video_drama_requests.py -q
```

## Notes

- 2026-09-27 做完（claude-fable-5-1-video-languages）。遷移是 `0107_video_one_off_series`（併 main 時從 0105 重新編號，接在 `0106_video_locales` 之後；分支自己的 T8 遷移 0104 隨 YouTube 那段一起 revert，main 的 T8 是 `0102_video_youtube_sync`；`messages-api` 那張的遷移要接 0105）。
  - `video_drama_series.kind`（`series`｜`one-off`，CHECK `ck_video_drama_series_kind`）；`ck_video_drama_series_numbers` 與 `ck_video_drama_doc_kind` 每次都重建（PostgreSQL 會把 BETWEEN 存成兩個比較，比對文字不可靠，照 0099 對 gate check 的做法）。
  - 轉換：`status = 'queued'` 且沒有 `series_id` 的請求各建一部 `one-off` 作品，**作品的 id 就用請求的 id**（三段 SQL 都以它為鍵，重跑找不到東西），slug `one-off-<id 前 8 碼>`，title 沒有就取 premise 前 200 字；同時建第 1 集（planned）；請求列補 `series_id`、`episode_number = 1`，狀態仍是 `queued`。已 `started` 的不動。
  - 請求列就是那一集的運送列：`start_episode` 找到同 series、同集數、`queued` 的請求就沿用（改 started、填 slug），沒有才新建；所以「單集漫劇」清單裡那筆請求會從排隊→製作中→完成，不會多一筆。`next_request`（舊路，工人的 `drama-requests/next`）只回沒有 `series_id` 的排隊請求，episode 的請求一律走 `series/next`。
  - `POST /admin/video-automation/drama-requests` 呼叫 `series.create_one_off`：建作品＋第 1 集＋請求列，回 `DramaRequestOut`（多 `series_slug`、`episode_number`）。`requests.create_request` 刪掉。`SeriesIn.kind = "one-off"` 從作品表單建也可以（數字一律壓成 1、`open_ended = False`；`series` 的 `episodes_per_chapter` 仍要 ≥ 4，改成 model validator）。
  - `doc_problem` 的 `bible`：`characters`（同 setting）、`acts` 非空 list、`outline` 是物件；one-off 只收 `bible`，series 不收 `bible`。核准 bible → 第 1 集 `ready`，`title`／`logline`／`beats` 取自 `outline`（沒有就用作品名與前提），作品直接 `active`。
  - `context_view`：one-off 的 `setting` 回核准的 bible（`kind` 是 `bible`，工人讀 `body_json.characters`、`body_md` 不用改），`chapter` 為 None、`chapter_range = (1, 1)`。`next_job_for` 對 one-off 不排任何 chapter 工作；`act("plan-next-chapter")` 對 one-off 回「每一篇都已經規劃過了」；`patch_series` 拒改 one-off 的集數（`video_series_one_off_fixed`）。
  - `GET /admin/video-automation/series?kind=`；`SeriesSummary.kind`。
  - 舊工人碰到 `bible` 工作會在 `documentProblem` 拒收後 later 一次，不會壞；worker 票接手。
- 工人端的對應（`draftEpisode` 也給 one-off、拿掉單集的選大綱）在 `2026-09-27-video-drama-room-worker`。
- 單集的頁面在 `2026-09-27-video-drama-room-web`：「單集漫劇」清單改列 `kind = one-off` 的作品。


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：claude-fable-5-1-video-languages；原分支：未記錄。

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/api/app/video_automation/series.py:984 creates one-off series; models.py:450 includes one-off; migration 0107_video_one_off_series.py present.
- Current schemas.py:621 validates one-off form and series.py:1277 handles approved bible.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Close stale review task.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
