---
id: 2026-10-07-public-videos-api-list-videos-the
title: Public videos API: list videos the owner published from Studio
status: done
priority: P2
area: api
owner: claude-fable
claimed_at: 2026-10-08T00:12:07Z
created_at: 2026-10-07T15:24:57Z
completed_at: 2026-10-08T04:27:42Z
branch: claude/focused-hopper-t3zgz9
depends_on: []
scope:
  - apps/api/app/video_reviews/public_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/cli.py
  - apps/api/tests/test_public_videos.py
  - apps/api/tests/test_video_reviews_youtube.py
---

# Public videos API: list videos the owner published from Studio

## Why

頻道 @Mokaair 的 18 支影片都由站主在 YouTube Studio 手動公開，沒有走網站的「送到 YouTube」表單，所以 `video_project.youtube_publish_at` 是空的。`apps/api/app/video_reviews/public_api.py` 的 `_published()` 要求 `youtube_video_id` 與 `youtube_publish_at` 都非空且 ≤ now，結果 2026-10-07 的 mokaair.com/zh-TW/videos 頁寫「這裡還沒有影片」，文章頁的「這篇文章的影片」區塊也是空的：影片→文章 18/18 有連結，文章→影片 0/18。文章讀者是這個頻道最便宜、最對口的第一批觀眾（頻道診斷 `docs/videos/channel-review-20261007/README.md` §1.3 第 1 件、§2.3）。

## Definition of done

- [x] 站主在 Studio 公開、網站已記下 `youtube_video_id` 的影片，出現在 `/zh-TW/videos` 與對應文章的「這篇文章的影片」區塊；還是私人或未排程的影片仍然不出現。（程式與測試已做；正式站要部署後跑一次回填指令，見 Notes）
- [x] 公開時間有兩個來源都能用：站主在後台卡片填的時間，或（沒有填時）YouTube API 回報的 `publishedAt`／`privacyStatus=public`；`youtube_publish_at` 在未來的影片維持不列出。
- [x] `apps/api/tests/test_public_videos.py` 覆蓋「有 id、無 publish_at、YouTube 已公開」這一種。

## Steps

- [x] 讀 `_published()` 與寫入 `youtube_publish_at` 的路徑（`video_youtube/sync.py`、後台「可以上架」卡片），決定是補資料還是放寬條件；放寬時用 YouTube 回報的公開狀態，不要只靠 id 存在。（決定：補資料，`_published()` 不放寬）
- [x] 若採補資料：給工人或後台一個「同步公開時間」動作，從 `videos.list` 的 `status.privacyStatus` 與 `snippet.publishedAt` 回填。（後台貼網址時自動查；舊片用 CLI `video-youtube-backfill-publish-times`）
- [ ] 部署後逐篇檢查觀看前四名的來源文章頁（google-vids-free-ai-video-omni-1-1、ai-news-claude-opus-55-20260922、ai-news-google-ai-student-20260820、ai-news-chatgpt-ads-20260925 的實際 slug 以站上為準）有嵌影片。

## How to verify

`cd apps/api && uv run pytest tests/test_public_videos.py`；部署後 `curl -sS https://mokaair.com/api/public/videos?locale=zh-TW`（實際路徑以 `public_router` 為準）回 18 筆，且 `/zh-TW/videos` 頁不再顯示「這裡還沒有影片」。

## Notes

只看了程式碼，沒查正式站資料庫：也可能部分影片連 `youtube_video_id` 都沒寫回（工人在站主貼網址後才寫回 `video.json`）。先在後台看 18 支的卡片狀態再動手。

### 2026-10-08 實作（claude-fable，分支 claude/focused-hopper-t3zgz9）

決定：**補資料，不放寬 `_published()`**。公開與否仍以 `youtube_publish_at` 為準，所以私人／未公開的影片絕不會被列出；差別只在這個欄位多了一個來源。

- `admin_service.link_youtube`：站主有填 publish_at 照舊；沒填時用連結的頻道查一次 `videos.list`（`youtube_publication`，1 單位）：`privacyStatus=public` → 記 `snippet.publishedAt`；私人但有 `status.publishAt`（Studio 排程）→ 記排程時間；私人／未公開且沒排程 → 維持 null。沒連結頻道、授權失效、API 失敗、網路斷、影片不在這個頻道或找不到 → 照舊只記 id，貼網址不會失敗；原因寫進 audit `metadata_json.publish_at_reason`（另有 `publish_at_source`：`owner`／`youtube`／null），並放在回傳 `ProjectOut.youtube_publish_note`（新增的可選欄位，只有這條路會填；後台頁面還沒顯示它，見下）。
- 一次性回填：`python -m app.cli video-youtube-backfill-publish-times`（不帶旗標只報告；`--apply` 才寫）。對「有 id、publish_at 為 null、沒放棄」的 project 用 `videos()` 每 50 支一次查 `snippet,status`，每支印 slug／id／publish_at／reason；寫入時每支留一筆 audit `video_youtube_publish_time_backfilled`（actor 為 null）。沒連結頻道時 exit 2 並印 `ERROR video_youtube_not_linked: …`。
- `public_api.py` 只改 docstring；`sync.py`、`client.py`、models、migration 都沒動（不需要新欄位）。
- 測試：`tests/test_video_reviews_youtube.py` 用假 client（`FakeYoutube`，monkeypatch `admin_service._linked_youtube`）覆蓋 public／scheduled／private／unlisted／找不到／別的頻道／沒連結／授權失效／API 拒絕／網路斷、回填 dry-run 與 --apply、50 支一批、CLI 分派；`tests/test_public_videos.py` 加「有 id、無 publish_at、YouTube 已公開」經回填後列出、私人與未公開仍不列、排程的要時間到才列。

部署後要做（站主或下一個接手的人）：
1. `docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-youtube-backfill-publish-times`（先看報告：18 支應該都是 public 且有時間；若有 `reason` 是「不在連結的頻道」，先確認設定分頁連的是 @Mokaair）。
2. 同一行加 `--apply`，再 `curl -sS https://mokaair.com/api/v1/videos` 應回 18 筆，`/zh-TW/videos` 不再顯示「這裡還沒有影片」。
3. 逐篇看觀看前四名的來源文章頁有沒有嵌影片（本票第 3 步，部署後才能做）。

沒做／留給別張票：
- 後台「可以上架」卡片還沒顯示 `youtube_publish_note`（apps/web 不在 scope）；目前只在 audit 與 API 回傳看得到。
- 回填後 `prune_published_previews` 會把這 18 支的 mp4 在一週後從審核區刪掉（原本的規則，之前因為沒有公開時間而沒觸發）——這是既定行為，但站主要知道。
- 沒查正式站資料庫；若某支連 `youtube_video_id` 都沒有，回填不會碰它，要先在後台貼網址（貼的時候就會自動查公開時間）。
