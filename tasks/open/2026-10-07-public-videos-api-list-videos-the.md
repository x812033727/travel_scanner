---
id: 2026-10-07-public-videos-api-list-videos-the
title: Public videos API: list videos the owner published from Studio
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-07T15:24:57Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/public_api.py
  - apps/api/tests/test_public_videos.py
---

# Public videos API: list videos the owner published from Studio

## Why

頻道 @Mokaair 的 18 支影片都由站主在 YouTube Studio 手動公開，沒有走網站的「送到 YouTube」表單，所以 `video_project.youtube_publish_at` 是空的。`apps/api/app/video_reviews/public_api.py` 的 `_published()` 要求 `youtube_video_id` 與 `youtube_publish_at` 都非空且 ≤ now，結果 2026-10-07 的 mokaair.com/zh-TW/videos 頁寫「這裡還沒有影片」，文章頁的「這篇文章的影片」區塊也是空的：影片→文章 18/18 有連結，文章→影片 0/18。文章讀者是這個頻道最便宜、最對口的第一批觀眾（頻道診斷 `docs/videos/channel-review-20261007/README.md` §1.3 第 1 件、§2.3）。

## Definition of done

- [ ] 站主在 Studio 公開、網站已記下 `youtube_video_id` 的影片，出現在 `/zh-TW/videos` 與對應文章的「這篇文章的影片」區塊；還是私人或未排程的影片仍然不出現。
- [ ] 公開時間有兩個來源都能用：站主在後台卡片填的時間，或（沒有填時）YouTube API 回報的 `publishedAt`／`privacyStatus=public`；`youtube_publish_at` 在未來的影片維持不列出。
- [ ] `apps/api/tests/test_public_videos.py` 覆蓋「有 id、無 publish_at、YouTube 已公開」這一種。

## Steps

- [ ] 讀 `_published()` 與寫入 `youtube_publish_at` 的路徑（`video_youtube/sync.py`、後台「可以上架」卡片），決定是補資料還是放寬條件；放寬時用 YouTube 回報的公開狀態，不要只靠 id 存在。
- [ ] 若採補資料：給工人或後台一個「同步公開時間」動作，從 `videos.list` 的 `status.privacyStatus` 與 `snippet.publishedAt` 回填。
- [ ] 部署後逐篇檢查觀看前四名的來源文章頁（google-vids-free-ai-video-omni-1-1、ai-news-claude-opus-55-20260922、ai-news-google-ai-student-20260820、ai-news-chatgpt-ads-20260925 的實際 slug 以站上為準）有嵌影片。

## How to verify

`cd apps/api && uv run pytest tests/test_public_videos.py`；部署後 `curl -sS https://mokaair.com/api/public/videos?locale=zh-TW`（實際路徑以 `public_router` 為準）回 18 筆，且 `/zh-TW/videos` 頁不再顯示「這裡還沒有影片」。

## Notes

只看了程式碼，沒查正式站資料庫：也可能部分影片連 `youtube_video_id` 都沒寫回（工人在站主貼網址後才寫回 `video.json`）。先在後台看 18 支的卡片狀態再動手。
