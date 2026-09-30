---
id: 2026-09-30-video-dropped-request-backfill
title: 放棄影片前卡在 started 的漫劇請求列要回填成 cancelled
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-30T03:55:50Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/migrations/versions
  - apps/api/tests
---

# 放棄影片前卡在 started 的漫劇請求列要回填成 cancelled

## Why

票 `2026-09-28-video-dropped-episode-request` 讓站主在 `/admin/videos` 放棄一支作品的影片時，那一集的 `video_drama_requests` 列從 `started` 改成 `cancelled`。但那只管之後的放棄：在它部署前就被放棄的影片，請求列還停在 `started`，後台的漫劇請求清單照樣顯示「製作中」，`GET /video/automation/drama-requests`（工人讀的進行中清單）也照樣列著它們。

## Definition of done

- [ ] 正式站上，`status='started'` 而且 `slug` 對到一支 `dropped_at` 不為空的 `video_projects` 的請求列都變成 `cancelled`，`cancelled_at` 寫成那支影片的 `dropped_at`。
- [ ] 其他請求列（queued、done、影片沒被放棄的 started）一列都不動。

## Steps

- [ ] 先在正式站只讀查一次有幾列（`SELECT count(*) FROM video_drama_requests r JOIN video_projects p ON p.slug = r.slug WHERE r.status = 'started' AND p.dropped_at IS NOT NULL`），零列就直接結案。
- [ ] 有的話照 `backend-conventions` skill 寫資料 migration（或一次性的回填指令），加整合測試。

## How to verify

部署後再跑上面那句查詢，結果是 0；後台漫劇請求清單裡那些列顯示已取消。

## Notes

- 2026-09-30 開票（claude-fable-5-1-drama-request）：做 `2026-09-28-video-dropped-episode-request` 時看到的，那張票的範圍只有放棄當下的處理。
- 那些列的集數早就是 `skipped`（`2026-09-28-video-story-api-policy-languages` 起），只差請求列。
