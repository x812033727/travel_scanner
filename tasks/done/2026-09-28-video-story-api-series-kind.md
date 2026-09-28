---
id: 2026-09-28-video-story-api-series-kind
title: 作品類型 story：遷移、每日配額、圖片模型覆寫與匯入指令
status: done
priority: P1
area: api
owner: claude-opus-5-5-video-story-api
claimed_at: 2026-09-28T09:49:14Z
created_at: 2026-09-28T03:31:12Z
completed_at: 2026-09-28T12:10:58Z
branch: claude/video-story-api-series-kind
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/story_cli.py
  - apps/api/app/video_automation/stories.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/cli.py
  - apps/api/migrations/versions
  - apps/api/tests/test_video_story.py
  - apps/api/tests/test_migration_0111_video_story_series.py
---

# 作品類型 story：遷移、每日配額、圖片模型覆寫與匯入指令

## Why

品牌故事是漫劇底下的一種作品類型（`docs/videos/STORY.md`）：一部免關卡、全靜態圖的作品，100 個故事是它的 100 集，集數由企劃清單匯入。伺服器現在做不到三件事：

- 作品的 `kind` 只有 `series` 與 `one-off`（PR #870 加的）；`next_job_for` 一定先要設定集、總綱、細綱，故事沒有這些文件。
- 單集長度上限是 8 分鐘（`ck_video_drama_series_numbers`、`SeriesIn`），故事要 12–15 分鐘。
- 沒有每日配額：站主要每天兩支，現在只有同時進行的集數與每月集數兩個上限。

另外，站主選了 Gemini 3.1 Flash Image 給故事用，但圖片模型是全站一個設定；不能為了故事把漫劇的預設 Pro 換掉。

## Definition of done

- [x] 遷移：`ck_video_drama_series_kind` 接受 `story`；`target_minutes` 放寬到 1–20；`video_drama_series` 新增 `episodes_per_day`（NULL 或 1–12）、`image_model`（NULL 表示照設定）與 `look`（JSON：`{style ≤600, negative ≤400, motion?}`，每個故事共用的畫風；故事沒有設定集，畫風沒有別的地方放；其他類型是 NULL）。升級與降級都有整合測試。
- [x] 建立 `kind: "story"` 的作品時狀態直接是 `active`；對故事作品送文件會被拒絕。
- [x] `next_job_for` 的故事分支：不看文件、不等前一集完成；超過每日上限（以 Asia/Taipei 的日期計算已開始的集數）、`series_max_in_flight`、`series_episodes_per_month`，或「上架確認已核准但還沒有 YouTube id」的集數達到 6 時，回傳沒有工作。
- [x] 匯入：`python -m app.cli video-story-import --series <slug> [--apply]` 從 stdin 讀 `stories.json`，預設試跑並印出會新增、更新、略過的列數；驗證每一列（標題、提問、六段要點、至少 3 個 https 來源、代號與 slug 格式）；同一個 `id` 再匯入只更新還沒開始的列。
- [x] 工人拿到的集數內容帶 `beats` 全文與作品的 `kind`、`image_model`。
- [x] `ruff`、`mypy app`、`mypy tests`、`pytest` 通過（本機的限制見 Notes 最後一條）。

## Steps

- [x] 確認 PR #870 已合併，遷移接在目前的 head 後面（編號與 revision id 照 skill `backend-conventions`）。
- [x] 模型、schema、`series.py` 的故事分支與 `import_story_rows`（放在新的 `stories.py`）。
- [x] `story_cli.py` 並在 `app/cli.py` 登記。
- [x] 測試：每日上限跨台北午夜（15:59Z 與 16:00Z）、匯入重複執行、緩衝滿 6 支、一般作品不受影響。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story.py tests/test_video_series.py
```

主機上（部署後、站主同意）：匯入先試跑，確認列數，再 `--apply`。

## Notes

- **不要在 PR #870 合併前開工**：`kind` 欄位與遷移 0105–0108 都是它的；撞號的處理見記憶與 skill `backend-conventions`。
- 如果 #870 長期沒合併，退路是用新的 `genre` 值當判別（不同的 CHECK，不依賴 `kind`）；那是較差的判別欄位，採用前先問站主。
- 故事的模型呼叫都帶 `variant`，不算進 `max_drafts_per_month`；這張票要有一個測試證明。
- 圖片模型的覆寫在媒體 API 那一側生效，屬於票 `2026-09-28-video-story-api-policy-languages` 的 scope（`video_media`）；這張票只加欄位並讓它出現在作品的輸出。
- 2026-09-28 認領（claude-opus-5-5-video-story-api）：`claim` 因為 scope 與五張 `review` 狀態的票重疊而拒絕（`video-drama-room-messages-api`、`video-drama-room-one-off-series`、`video-drama-room-withdraw-a-one`、`video-languages-api`、`video-split-settings-api`）。它們都是 PR #870 的票，#870 已在 2026-09-28T06:38Z 合併、分支已刪，內容在 main 上（`git diff` 對這張票的路徑是空的），只是沒人跑 `done`；所以用 `--force` 認領，那五張票沒有動。
- scope 加了兩個路徑：`apps/api/app/video_automation/stories.py`（企劃清單的驗證與匯入；`series.py` 已經約 1,700 行，匯入與驗證另放一個模組，`story_cli.py` 只剩指令本身）與 `apps/api/tests/test_migration_0111_video_story_series.py`（遷移的整合測試，照 skill `backend-conventions` 一支遷移一個測試檔）。
- 匯入檔的每個故事還可以帶 `caveats`（字串，最多 800 字，可以是空字串，查核者留給撰稿的話：哪個軼事不要講、哪個職稱各來源說法不同）；可以沒有這個鍵。匯入時跟其他欄位一起放進 `beats`，所以 `beats` 的鍵是 `id`、`category`、`region`、`subject`、`question`、`chapters`、`takeaway`、`must_verify`、`sources`、`names`、`cast`、`image_notes`、`sensitivity`、`related_guide`、`thumbnail`、`publish`，以及有的話 `caveats`。其他不認得的欄位仍然是問題。
- `must_verify` 的每一條只能有 `claim`（文字）、`sources`（指向 `sources` 的索引），以及三個可選的布林值 `core`（標題靠的那條）、`attributed`（照某人的說法講的軼事）、`reviewer_only`（這條的來源全是工人的讀取器轉不成文字的文件，例如 PDF 或超過 3 MB 的頁面；工人照企劃的話採用，不再自己查）；其他鍵拒絕。匯入時原樣留在 `beats.must_verify`。**給票 `video-story-worker`**：`beats.caveats` 要跟章節要點一起交給撰稿，`reviewer_only: true` 的事實查核時不要去抓來源、當成已查核。
- **遷移編號**：檔名 `0111_video_story_series.py`，revision id `0111_video_story_series`（23 字元）。開 PR #910 時 `down_revision` 是 main 的 head `0108_video_drama_messages`，0109、0110 留給也從 0108 接出 0109 的 #898（`0109_video_shorts`）與 #904（`0109_video_flat_explainer`）。2026-09-28 #898 在 11:47:59Z 合併，草稿 PR #910 在 11:49:04Z 被改成非草稿並合併（不是這個 session 做的），main 因此有兩個 head（`0109_video_shorts` 與 `0111_video_story_series` 都接 0108），`tests/test_schema.py` 與 `alembic upgrade head` 都會失敗。修正在 PR #918（另一個 session 開的；這張票自己的修正 PR #919 內容相同，被當成重複的關掉了）：把 `down_revision` 改成 `0109_video_shorts`，`uv run alembic heads` 只剩 `0111_video_story_series`。#918 另外讓 `start_episode` 在作品列的鎖底下再查一次故事的暫停與配額，站主暫停作品或調低上限之後，先前發出去的 job 開始時會得到 409。**#904 還開著，它排在這支之後：它要接 `0111_video_story_series`，而且編號要大於 0111（例如 0112），才會是唯一、最大號的 head；改成 0110 不論接哪一支都過不了 `tests/test_schema.py`**。兩邊改的 CHECK 不同（#904 改三個 `style_preset` 的，這裡改 `kind` 與 `numbers`），遷移不會互相蓋掉；它合併 main 時 `models.py`、`schemas.py`、`series.py` 的衝突要保留雙方的意圖（它的 `flat-explainer` 畫風與這裡的 `story`）。
- 降級：有 `kind = 'story'` 或 `target_minutes > 8` 的作品時拒絕（RuntimeError，說有幾部、要先怎麼處理），照 skill `backend-conventions` 對縮窄 CHECK 的規矩（0073、0107 也這樣），不默默改站主的資料。brief 要「降級不能因故事列而失敗」：它不會撞 CHECK 出錯，而是在動任何東西之前停下來說明。整合測試 `tests/test_migration_0111_video_story_series.py` 兩個方向都測（本機沒有 PostgreSQL，只在 CI 跑）。另外：`video_drama_series` 不是 0001 用 models 建的（`app.models` 不匯入 `video_automation.models`），是 0099 建、0103／0107 改，所以 CI 的 `alembic upgrade head` 會真的走到加欄位與換 CHECK 的程式。
- 「上架確認已核准、還沒有 YouTube id」怎麼判斷：集數的影片（`video_projects.slug` 等於集數的 `slug`）有一筆 `gate = 'publish'`、`status = 'approved'` 的 `video_reviews`，而且 `youtube_video_id` 與 `dropped_at` 都是 NULL（放棄的影片不會上傳，不算）。這跟「可以上架」清單讀的是同一筆紀錄（`app/video_reviews/admin_service.py` 的 `publish_approved_at`）。常數 `STORY_UPLOAD_BUFFER = 6` 在 `series.py`。
- 每日配額用 `ZoneInfo("Asia/Taipei")` 的日曆日比對 `started_at`（開始後變成 done、skipped 也照算）；每月上限沿用一般作品的算法（UTC 月初起的 `started_at`）；同時進行只算 `started`。
- 不開新故事的原因：`next_job_for` 與後台用同一個純函式 `story_quota`。故事作品的 `SeriesSummary.quota`（`GET /admin/video-automation/series` 與 `/series/{slug}` 帶，工人的 job 不帶）有 `day`、`started_today`、`episodes_per_day`、`in_flight`、`max_in_flight`、`started_this_month`、`episodes_per_month`、`awaiting_upload`、`upload_buffer`、`ready`，以及 `hold`（`not_active`、`per_day`、`in_flight`、`per_month`、`upload_buffer`、`none_ready`）與給站主看的 `hold_detail`。原本沒有任何地方顯示「為什麼不開下一集」，這是第一個；其他類型的 `quota` 是 null、行為不變（有測試）。
- **給票 `video-story-worker`**：`GET /video/automation/series/next` 的故事 job 是 `kind: "episode"`，`job.episode.beats` 是整個故事（含 `caveats`、`publish`），`job.series` 帶 `kind: "story"`、`image_model`、`look`、`target_minutes`、`episodes_per_day`；`context.chapter`、`context.chapter_number` 是 null，`context.episodes` 列出每個故事但不帶 beats（100 份完整企劃約 600 KB，拿掉後約 46 KB；`context.episode` 帶全文）。開始時的影片 slug 必須是集數的 `slug`（匯入時定好的 `story-...`），不同就 409 `video_series_story_slug`；開始時建的請求列 premise 會帶故事的 `question`、長度 13 分鐘。每一次模型呼叫都要帶 `variant`（例如 `story`），才不算進 `max_drafts_per_month`（有測試）。故事作品沒有文件：送文件 422，`actions/*`（排下一篇、開下一集、合集）409。
- **給票 `video-story-admin`**：清單用 `GET /admin/video-automation/series?kind=story`（網站現在的兩個清單是 `?kind=series` 與 `?kind=one-off`，看不到故事作品）；上面的 `quota` 就是「今天開始幾支、每日上限、同時進行、緩衝、原因」。改每日支數、圖片模型、畫風用 `PATCH /admin/video-automation/series/{slug}`（`episodes_per_day` 1–12 或 null、`image_model`、`look`，只有故事作品收；故事作品改不了免關卡、全靜態、合集與每篇集數；`target_minutes` 最多 20，其他類型仍是 8）。從頁面匯入與恢復略過的故事需要新的 API，另開了票 `2026-09-28-video-story-admin-import-api`。
- **給票 `video-story-api-policy-languages`**：`video_drama_series.image_model` 已經有了（NULL 表示照設定分頁），建立或修改時會對媒體目錄檢查（任何廠商、沒退役的圖片模型）；判斷故事作品用 `app.video_automation.series.is_story`。
- 匯入的規則照抄 `tools/video/story-plans/plan.mjs` 的 `storyProblems`、`seriesProblems`、`LIMITS` 與正規表示式（兩邊要一起改），加上編譯檔的 `number`、`publish`、`caveats`、`must_verify` 的鍵，以及整份檔的規則（`schema_version` 是 1、`series.slug` 等於 `--series`、id／slug／標題不重複、number 1..N 不跳號、上架時段不重複）。一個故事有問題就整份拒絕、什麼都不寫，指令 exit 1。檔案的 `series.youtube_category_id` 伺服器沒有欄位，報告只列一句 note。`--episodes-per-day` 只在建立作品時用；作品已存在時匯入不改作品列，只在 `series_differs` 報出哪些欄位不同。
- 2026-09-28 用暫存的真實企劃清單（100 個故事、1.3 MB，還會再改）在記憶體 SQLite 上走過一遍：問題 0；試跑 create 100；`--limit 2 --episodes-per-day 1` 建立作品與 2 集；同樣再跑一次什麼都不變；不帶 `--limit` 補 98 集；再跑一次 leave_alone 100、不寫入。之後 main 上的正式編譯檔 `docs/videos/story-plans/brand-stories-100/stories.json`（100 個故事、1,414,653 bytes，每個都有 `caveats`，8 條事實標了 `reviewer_only`）也照同樣的順序走過：問題 0，試跑會建立作品 `brand-stories` 與 100 集，其餘結果同上。
- 主機上（部署後、站主同意）：`docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-story-import --series brand-stories < stories.json` 先試跑，確認數字，再加 `--apply --limit 2 --episodes-per-day 1` 做試作兩支。
- 本機檢查的限制：這台沒有 PostgreSQL，`RUN_INTEGRATION_TESTS=1` 的測試（含遷移測試）只在 CI 跑；`uv run mypy tests` 在 Windows 會因為既有的 `tests/support/e2e_deploy_agent.py:244`（`socketserver.UnixStreamServer`，與這張票無關）報錯，改用 CI 的平台 `--platform linux` 是綠的。
- CI（PR #910，head `20a5af61`）：`api` 在全新的 PostgreSQL 上跑 `alembic upgrade head` 時真的走了 `0108_video_drama_messages -> 0111_video_story_series`，遷移的整合測試通過，整套 5282 passed、16 skipped；`web`、`containers`、`full-stack-smoke` 也都綠。
