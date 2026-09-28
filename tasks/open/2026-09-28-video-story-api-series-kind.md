---
id: 2026-09-28-video-story-api-series-kind
title: 作品類型 story：遷移、每日配額、圖片模型覆寫與匯入指令
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-video-story-api
claimed_at: 2026-09-28T09:49:14Z
created_at: 2026-09-28T03:31:12Z
completed_at:
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
  - apps/api/tests/test_migration_0110_video_story_series.py
---

# 作品類型 story：遷移、每日配額、圖片模型覆寫與匯入指令

## Why

品牌故事是漫劇底下的一種作品類型（`docs/videos/STORY.md`）：一部免關卡、全靜態圖的作品，100 個故事是它的 100 集，集數由企劃清單匯入。伺服器現在做不到三件事：

- 作品的 `kind` 只有 `series` 與 `one-off`（PR #870 加的）；`next_job_for` 一定先要設定集、總綱、細綱，故事沒有這些文件。
- 單集長度上限是 8 分鐘（`ck_video_drama_series_numbers`、`SeriesIn`），故事要 12–15 分鐘。
- 沒有每日配額：站主要每天兩支，現在只有同時進行的集數與每月集數兩個上限。

另外，站主選了 Gemini 3.1 Flash Image 給故事用，但圖片模型是全站一個設定；不能為了故事把漫劇的預設 Pro 換掉。

## Definition of done

- [ ] 遷移：`ck_video_drama_series_kind` 接受 `story`；`target_minutes` 放寬到 1–20；`video_drama_series` 新增 `episodes_per_day`（NULL 或 1–12）、`image_model`（NULL 表示照設定）與 `look`（JSON：`{style ≤600, negative ≤400, motion?}`，每個故事共用的畫風；故事沒有設定集，畫風沒有別的地方放；其他類型是 NULL）。升級與降級都有整合測試。
- [ ] 建立 `kind: "story"` 的作品時狀態直接是 `active`；對故事作品送文件會被拒絕。
- [ ] `next_job_for` 的故事分支：不看文件、不等前一集完成；超過每日上限（以 Asia/Taipei 的日期計算已開始的集數）、`series_max_in_flight`、`series_episodes_per_month`，或「上架確認已核准但還沒有 YouTube id」的集數達到 6 時，回傳沒有工作。
- [ ] 匯入：`python -m app.cli video-story-import --series <slug> [--apply]` 從 stdin 讀 `stories.json`，預設試跑並印出會新增、更新、略過的列數；驗證每一列（標題、提問、六段要點、至少 3 個 https 來源、代號與 slug 格式）；同一個 `id` 再匯入只更新還沒開始的列。
- [ ] 工人拿到的集數內容帶 `beats` 全文與作品的 `kind`、`image_model`。
- [ ] `ruff`、`mypy app`、`mypy tests`、`pytest` 通過。

## Steps

- [ ] 確認 PR #870 已合併，遷移接在目前的 head 後面（編號與 revision id 照 skill `backend-conventions`）。
- [ ] 模型、schema、`series.py` 的故事分支與 `import_story_rows`。
- [ ] `story_cli.py` 並在 `app/cli.py` 登記。
- [ ] 測試：每日上限跨台北午夜（15:59Z 與 16:00Z）、匯入重複執行、緩衝滿 6 支、一般作品不受影響。

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
- scope 加了兩個路徑：`apps/api/app/video_automation/stories.py`（企劃清單的驗證與匯入；`series.py` 已經約 1,700 行，匯入與驗證另放一個模組，`story_cli.py` 只剩指令本身）與 `apps/api/tests/test_migration_0110_video_story_series.py`（遷移的整合測試，照 skill `backend-conventions` 一支遷移一個測試檔）。
- 匯入檔的每個故事還可以帶 `caveats`（字串，最多 800 字，可以是空字串，查核者留給撰稿的話：哪個軼事不要講、哪個職稱各來源說法不同）；可以沒有這個鍵。匯入時跟其他欄位一起放進 `beats`，所以 `beats` 的鍵是 `id`、`category`、`region`、`subject`、`question`、`chapters`、`takeaway`、`must_verify`、`sources`、`names`、`cast`、`image_notes`、`sensitivity`、`related_guide`、`thumbnail`、`publish`，以及有的話 `caveats`。其他不認得的欄位仍然是問題。
