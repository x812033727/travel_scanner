---
id: 2026-09-28-video-story-redo-dropped
title: 放棄的故事可以重做一次
status: done
priority: P3
area: api
owner: claude-opus-5-5-story-redo
claimed_at: 2026-09-30T15:40:28Z
created_at: 2026-09-28T14:30:22Z
completed_at: 2026-09-30T16:02:41Z
branch: claude/story-redo-dropped
depends_on:
  - 2026-09-28-video-story-admin-import-api
  - 2026-09-28-video-story-api-policy-languages
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/stories.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_story_redo.py
---

# 放棄的故事可以重做一次

## Why

站主放棄一支品牌故事的影片時，那一集會變成 `skipped`，名額才會釋放（票 `2026-09-28-video-story-api-policy-languages`，PR #938）。但這一集已經開始過，所以不能恢復（恢復只給從沒開始過的故事，票 `2026-09-28-video-story-admin-import-api`，PR #936），重新匯入同一個代號也只會被當成「已開始，不動」。

結果是：一個故事只要做壞一次、被放棄，就再也做不了。100 個故事都是查核過的企劃，做壞的原因多半是圖片或旁白，不是故事本身；站主應該可以叫它重做。

## Definition of done

- [x] 站主可以對一個被放棄的故事要求重做：它回到 `ready`，下一次輪到時工人從頭做一支新的影片。
- [x] 舊的那支影片與它的紀錄都留著，不會被新的蓋掉；新影片的代號怎麼定（同一個 slug 加序號，或別的做法）寫在 Notes，而且不撞 `video_drama_episodes.slug` 的唯一鍵。
- [x] 重做有次數上限（常數），超過就拒絕並說明，免得同一個故事一直重做一直花錢。
- [x] 每日配額、同時進行數與緩衝照算；有稽核紀錄。
- [x] 還沒被放棄的故事、其他類型的作品，行為不變。

## Steps

- [x] 讀 `start_episode` 怎麼檢查 slug（故事的影片代號必須是匯入時定好的集數 slug），決定新影片的代號規則。
- [x] `series.py` 加重做的函式，`admin_api.py` 加端點，權限照 `/skip` 與 `/restore`。
- [x] 測試：重做一次、超過上限、沒被放棄的故事拒絕、其他類型拒絕。
- [x] 後台頁面的按鈕另開票，或加進票 `2026-09-28-video-story-admin` 的後續：票 `2026-09-28-video-story-admin-redo-button` 已經開好。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story_redo.py tests/test_video_story.py tests/test_video_story_admin.py tests/test_video_series.py tests/test_error_localization.py
```

## Notes

- 這是做伺服器票時回報的（2026-09-28）。在這張票做完之前的權宜做法：把那個故事用新的代號與 slug 加進企劃清單（例如 `A01` 之外另加一筆），重新匯入。
- 工人那一側：工作區是照影片代號開的，新代號就是新的工作區，舊的照清理工作檔的規則處理。

### 做完的紀錄（2026-09-30，claude-opus-5-5-story-redo）

- **認領用了 `--force`**：scope 與四張 `codex-ten-drama` 的 `review` 票（2026-09-28 認領，超過 24 小時；它們的 PR #978 已在 2026-09-29 合併）以及 `claude-fable-5-1-video-languages` 的 `2026-09-27-video-drama-room-withdraw-a-one`（2026-09-27 認領；它分支的 PR #870 已在 2026-09-28 合併）重疊。都是過期、工作已落地的認領，沒有人在改這幾個檔案。
- **端點**：`POST /api/v1/admin/video-automation/series/{slug}/episodes/{number}/redo`，`content.manage`（與 `/skip`、`/restore` 相同），回 `SeriesOut`。函式是 `series.redo_episode`。
- **什麼是「被放棄的故事」**：`status == "skipped"` 而且 `started_at` 有值（放棄影片時 `_skip_abandoned_episode` 留下的樣子），正好是 `/restore` 拒絕（`video_series_episode_was_started`）的那一種。其他情形回 409 `video_series_episode_not_dropped`；沒開始過的略過故事，說明裡提示改用「恢復」。
- **新影片的代號**：計畫的 slug 加 `-redo<n>`，n 從 1 起算（`redo_slug`，例如 `story-rolling-case-redo1`）。計畫的 slug 取這一集第一支影片的請求列的 slug（第一次開始一定用計畫的 slug，`start_episode` 會擋別的），所以第二次重做是 `-redo2`，不會變成 `-redo1-redo1`。計畫 slug 最長 60 字，加上後綴仍在影片代號的 80 字內。重做時先查 `video_drama_episodes.slug`、`video_drama_requests.slug`、`video_projects.slug` 三處，任何一處已有這個代號就 409 `video_series_redo_slug_taken`，不自動換號。集數列的 slug 換成新代號，所以唯一鍵不會撞；舊影片的專案、請求列（`cancelled`）與計畫 slug 都不動。`start_episode` 照舊只接受集數列上的 slug，工人從 `series/next` 拿到的就是新代號，工作區也是新的。
- **上限**：`STORY_REDO_LIMIT = 1`（`series.py`）。已重做次數 = 這一集有 `started_at` 的請求列數 − 1，不需要新欄位也不需要遷移。超過就 409 `video_series_redo_limit`，說明裡寫上限，並建議用新的企劃代號重新匯入（原本的權宜做法）。
- **配額照算**：重做把集數列的 `started_at`、`request_id` 清掉（下一次開始會重寫），舊的那次開始改由請求列算：`_earlier_videos` 是「這部故事作品有 `started_at`、沒有任何一集指向它的請求列」。`story_quota` 的今日支數（新參數 `earlier_starts`）、`_started_this_month` 的本月集數、`_spend` 的作品花費都把它們算進去，所以同一天放棄又重做，今天仍算兩支。重做的故事是一般的 `ready`，照每日支數、同時進行數、上架緩衝排隊；`start_episode` 的鎖內複查也照舊。其他類型的作品不跑這些查詢（`is_story` 擋在前面），行為不變。
- **匯入**：重做後、重新開始前再匯入企劃清單，`plan_rows` 會看到集數列的 slug 與檔案不同；`is_redo_of` 認得 `-redo<n>`，保留重做的 slug，不會把它改回舊影片的代號（那樣會撞到舊影片而整份被拒）。
- **稽核**：`video_series_episode_redone`，metadata 有 `number`、`story`、`redo`、`limit`、`dropped_video`、`video`、`reopened`。放棄的是最後一個開著的故事而作品已經 `finished` 時，重做讓作品回到 `active`（與 `/restore` 相同）。
- 放棄時還停在 `started` 的舊請求列（PR #1023 之前放棄的）在重做時用 `_cancel_started_request` 關掉。
- **給後台按鈕票（`2026-09-28-video-story-admin-redo-button`）**：API 沒有另外回「還能重做幾次」。清單可以用 `status == "skipped"` 且 `started_at` 有值判斷「被放棄」；slug 以 `-redo<n>` 結尾表示已經重做過，在上限 1 之下會被拒，按鈕可以不出現或直接顯示 API 的說明。重做後集數列的 `video` 指新代號（開始前是空的），舊影片不在那一列上，要從 /admin/videos 用舊代號打開。
- 錯誤代碼走 `SeriesRefused`，不是 `AppError`，所以 `tests/test_error_localization.py` 不用加翻譯；scope 沒有擴大，沒有遷移。
