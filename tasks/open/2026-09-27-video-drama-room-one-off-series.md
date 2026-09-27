---
id: 2026-09-27-video-drama-room-one-off-series
title: Video drama room: a one-off episode is a one-episode series with a single story bible document
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-27T06:16:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/api/migrations
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_migration_0103_video_one_off_series.py
---

# Video drama room: a one-off episode is a one-episode series with a single story bible document

## Why

單集漫劇（`video_drama_requests`）與作品的一集走不同的路：單集用「選大綱」卡片、沒有劇本關卡、退回兩次就卡住；作品有文件、有劇本關卡。站主 2026-09-27 要「整個順一下漫劇的製作流程」。設計在 `docs/videos/DRAMA-FLOW.md` §二：單集就是一集的作品，文件只有一份「故事聖經」，之後跟作品的一集完全一樣。

## Definition of done

- [ ] 遷移（接 main 的 head；跟 `video-split-settings-api`、`video-drama-room-messages-api`、`video-languages-api` 平行，後落地改號）：`video_drama_series.kind`（`series`｜`one-off`，預設 `series`，CHECK）；`ck_video_drama_series_numbers` 重建，`episodes_per_chapter` 放寬到 ≥ 1；`ck_video_drama_doc_kind` 加 `bible`；把 `status = 'queued'` 的請求各建成一部 `one-off` 作品（slug `one-off-<請求 id 前 8 碼>`，title、premise、style_preset、target_minutes、note 搬過去；請求列補 `series_id`、`episode_number = 1`）。已 `started` 的請求不動，走完舊路。
- [ ] `SeriesIn.kind`；`kind == "one-off"` 時 `planned_episodes = 1`、`episodes_per_chapter = 1`、沒有 aspects 與 tone 也可以。`POST /admin/video-automation/drama-requests` 改成建立 one-off 作品並回它（表單不變；`DramaRequestOut` 帶 `series_slug`）。
- [ ] `next_job_for`：one-off 的文件鏈只有 `bible`（企劃 variant `bible`）；`bible` 核准 → 第 1 集 `ready` → 依 `series_auto_continue` 開始。`doc_problem` 的 `bible` 形狀：`characters`（同 `setting`）、`acts`、`outline`（單一）、`music`、`not_doing`、`lexicon`。
- [ ] `context_view` 與 `start_episode` 對 one-off 把 `bible` 當 `setting` 回；`GET /admin/video-automation/series?kind=`；`SeriesSummary.kind`。
- [ ] 測試：建 one-off、bible 核准開集、遷移轉換排隊中的請求、started 的不動。

## Steps

- [ ] 遷移與 model。
- [ ] series.py、requests.py、schemas、admin_api。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_series.py tests/test_video_drama_requests.py -q
```

## Notes

- 工人端的對應（`draftEpisode` 也給 one-off、拿掉單集的選大綱）在 `2026-09-27-video-drama-room-worker`。
- 單集的頁面在 `2026-09-27-video-drama-room-web`：「單集漫劇」清單改列 `kind = one-off` 的作品。
