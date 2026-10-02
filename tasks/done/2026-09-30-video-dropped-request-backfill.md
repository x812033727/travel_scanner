---
id: 2026-09-30-video-dropped-request-backfill
title: 放棄影片前卡在 started 的漫劇請求列要回填成 cancelled
status: done
priority: P3
area: api
owner: claude-opus-5-5-request-backfill
claimed_at: 2026-10-02T05:57:32Z
created_at: 2026-09-30T03:55:50Z
completed_at: 2026-10-02T06:03:58Z
branch: claude/drama-request-backfill
depends_on: []
scope:
  - apps/api/migrations/versions/0120_video_dropped_request.py
  - apps/api/tests/test_migration_0120_video_dropped_request.py
---

# 放棄影片前卡在 started 的漫劇請求列要回填成 cancelled

## Why

票 `2026-09-28-video-dropped-episode-request` 讓站主在 `/admin/videos` 放棄一支作品的影片時，那一集的 `video_drama_requests` 列從 `started` 改成 `cancelled`。但那只管之後的放棄：在它部署前就被放棄的影片，請求列還停在 `started`，後台的漫劇請求清單照樣顯示「製作中」，`GET /video/automation/drama-requests`（工人讀的進行中清單）也照樣列著它們。

## Definition of done

- [x] 正式站上，`status='started'` 而且 `slug` 對到一支 `dropped_at` 不為空的 `video_projects` 的請求列都變成 `cancelled`，`cancelled_at` 寫成那支影片的 `dropped_at`。（migration 0120，部署時生效）
- [x] 其他請求列（queued、done、影片沒被放棄的 started）一列都不動。

## Steps

- [x] 先在正式站只讀查一次有幾列（`SELECT count(*) FROM video_drama_requests r JOIN video_projects p ON p.slug = r.slug WHERE r.status = 'started' AND p.dropped_at IS NOT NULL`），零列就直接結案。（沒查；改寫成零列或多列都安全的 migration，見 Notes）
- [x] 有的話照 `backend-conventions` skill 寫資料 migration（或一次性的回填指令），加整合測試。

## How to verify

部署後再跑上面那句查詢，結果是 0；後台漫劇請求清單裡那些列顯示已取消。

## Notes

- 2026-09-30 開票（claude-fable-5-1-drama-request）：做 `2026-09-28-video-dropped-episode-request` 時看到的，那張票的範圍只有放棄當下的處理。
- 那些列的集數早就是 `skipped`（`2026-09-28-video-story-api-policy-languages` 起），只差請求列。
- 2026-10-02（claude-opus-5-5-request-backfill）：
  - **正式站的列數沒有讀。** 不先查，直接寫資料 migration `0120_video_dropped_request`：`UPDATE video_drama_requests AS r SET status='cancelled', cancelled_at=p.dropped_at, updated_at=now() FROM video_projects AS p WHERE p.slug=r.slug AND r.status='started' AND p.dropped_at IS NOT NULL`。零列或多列都一樣安全，第二次跑對不到任何列。部署時的檢查就是上面 How to verify 那句查詢（應為 0）。
  - 欄位照放棄當下的 `_cancel_started_request`（`app/video_reviews/admin_service.py`）：它寫 `status`、`cancelled_at`、`updated_at`。這裡 `cancelled_at` 用影片的 `dropped_at`（票的要求，也就是站主真正放棄的時間），`updated_at` 用 `now()`（這列實際被改的時間）。
  - 對應方式照票用 `slug`（請求清單本身就是 `VideoProject.slug == VideoDramaRequest.slug` 外連），不是放棄當下用的 `episode.request_id`。所以也涵蓋沒有 `series_id` 的舊式單次請求；放棄當下的路徑只處理集數，那種舊請求之後被放棄仍會停在 started，但只剩 0107 以前排進的舊請求會走那條路，沒另開票。
  - downgrade 是空的：這裡取消的列和放棄當下取消的列分不出來，改回 started 只會把 bug 放回去。
  - 範圍原本是整個 `apps/api/migrations/versions` 與 `apps/api/tests`，跟二十多張進行中的票重疊、claim 被拒；縮成實際會動的兩個檔。
  - 測試 `tests/test_migration_0120_video_dropped_request.py`：離線 SQL 與 revision 鏈不需資料庫；PostgreSQL 那個用暫存表遮住共用表（只放回填會讀寫的欄位，避開只有 Python 端預設值的 NOT NULL 欄位），種 started+dropped、done+dropped、cancelled+dropped、started+未放棄、started+沒有影片列、queued 六列，斷言只有第一列變 cancelled 且 `cancelled_at = dropped_at`，再跑一次與 downgrade 都不變。本機沒有 PostgreSQL，那個測試 skip，只在 CI（`RUN_INTEGRATION_TESTS=1`）跑。
