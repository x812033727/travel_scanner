---
id: 2026-09-28-video-shorts-youtube-auto
title: Video shorts Y1: the site schedules Shorts on YouTube by itself under the owner's standing consent
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-28T03:30:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-api
scope:
  - apps/api/app/video_shorts/publish.py
  - apps/api/app/video_shorts/claim.py
  - apps/api/app/video_shorts/stats.py
  - apps/api/app/video_shorts/tick.py
  - apps/api/app/video_shorts/publish_api.py
  - apps/api/app/video_youtube/client.py
  - apps/api/app/video_youtube/requests.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/app/video_youtube/schemas.py
  - apps/api/tests/test_video_shorts_publish.py
  - apps/api/tests/test_video_shorts_stats.py
  - apps/api/tests/test_video_youtube_sync.py
---

# Video shorts Y1: the site schedules Shorts on YouTube by itself under the owner's standing consent

## Why

站主要 Shorts 全自動，連上架時間都照月曆走。現在送 YouTube 的每一步都要站主按：在「可以上架」卡片選來源、貼網址、選時間、按送出（`app/video_youtube/sync.py` 的 `request_sync` 要一位登入的使用者）。一天一到兩支、連續 90 天，這樣做不下去。

另一方面 YouTube 的開發人員政策要求：自動上傳要有使用者事前、具體、明示的同意；寫入之前要講清楚會做什麼、會怎麼改瀏覽權限；使用者對發布出去的內容有最後決定權。所以「自動」的做法是站主先按一次範圍明確的授權（A1 已經存好），之後網站在這個範圍內替站主送出，每一筆都留紀錄，站主隨時可以改、抽掉、暫停、撤回。

設計全文在 `docs/videos/SHORTS.md`（§上架、§成效與每週報告、§政策與依據）。

## Definition of done

- [ ] `POST /video/automation/shorts/tick`（工具權杖）：在一個請求裡做到期的事並回報各做了幾件——鎖定時段、啟動該送的同步、讀該讀的成效、每天一次驗證授權與已公開的影片還在。同一時間只有一個 `tick` 在跑（Redis 鎖）；記下這次的時間給頂列用。回應不含任何權杖、網址或影片內容。
- [ ] 自動送出：時段已鎖定、Shorts 有核准的上傳包、有影片 id、授權有效、沒有暫停時，伺服器自己建立同步請求（`visibility: scheduled`、`publish_at` 是時段的時間）並啟動 `run_sync`。audit 的操作者是授權的那一位，metadata 帶 `auto: true` 與授權的 id。授權失效、範圍不符（內容線、每天上限、時段）、或已暫停時不送，原因寫在影片上。
- [ ] Shorts 的欄位：只有 zh-TW 的標題與說明（Shorts 設定勾了其他語系才加 `localizations` 與那些語系的字幕）；`categoryId` 依內容線；不送縮圖；沒有章節。已經公開的影片照舊不改。
- [ ] 依檔名認領（`POST /admin/video-shorts/uploads/claim`）：讀連結頻道最近上傳的影片，用 `fileDetails.fileName` 對 `mokaair-short-<slug>.mp4`，讀不到檔名時用標題對檔名的主幹；再核對是私人、從來沒有公開過、長度與我們的成片差不到 1 秒。對到的寫下影片 id。回報每一支：對到、找不到、長度不符、已經公開、重複上傳。
- [ ] 撤回（`POST /admin/video-shorts/recall`）：把已排程、還沒公開的 Shorts 在 YouTube 上取消排程（保持私人），時段回到 `assigned`。
- [ ] 成效快照：用 Data API 讀公開的觀看、喜歡、留言（`videos.list` 的 `statistics`，一次最多 50 支；或 2026-06 新增、有自己配額桶的 `videos.batchGetStats`，實作時讀文件擇一），照 `SHORTS.md` 的三個時間窗寫進 `video_shorts_metrics`；每個時間窗只寫第一筆；`now` 每天更新一次。影片被刪或改成私人時標成已下架。**伺服器不從這些數字算任何分數、排名、平均或達成率**（開發人員政策；例外條款要等稽核接受「Analytics & Reporting」用途）。
- [ ] 稽核通過前，時段到了還沒有影片 id 的 Shorts 回到片庫，時段記成 `missed`。
- [ ] 配額：一天的呼叫量記在 Redis（每個太平洋日），接近 10,000 單位的八成時停止非必要的讀取；被 YouTube 以配額拒絕時當天不再重試。
- [ ] pytest：用假的 YouTube（照 `test_video_youtube_sync.py` 的做法）涵蓋自動送出、各種不送的原因、認領的五種結果、撤回、三個時間窗、配額、`tick` 的互斥。

## Steps

- [ ] 讀 `app/video_youtube/sync.py`、`requests.py`、`client.py` 與 `docs/videos/YOUTUBE-API-AUDIT.md` §五。
- [ ] `client.py` 加讀取用的方法（上傳清單、`videos.list` 帶 `statistics`、`fileDetails`、`contentDetails`）。
- [ ] `requests.py`：Shorts 的 `update_body` 變體（語系、分類、沒有縮圖）。
- [ ] `sync.py`：把「誰發起」抽出來，讓伺服器可以在授權之下建立請求；站主按鈕的路徑不變。
- [ ] `publish.py`、`claim.py`、`stats.py`、`tick.py`；端點都放 `publish_api.py`（A1 已經把這個空的路由檔掛進 `main.py`，後台與工人兩種路由都在這一檔）。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts_publish.py tests/test_video_shorts_stats.py tests/test_video_youtube_sync.py -q
```

對真的頻道的驗證在 `2026-09-28-video-shorts-pilot-launch`：先用一支私人的測試影片。

## Notes

要在真的頻道上實測、然後寫回 `docs/videos/SHORTS.md` 的事（程式先照官方文件寫，兩種結果都要處理）：

1. 站主在 Studio 拖進去、沒有按完精靈的影片（草稿），API 讀不讀得到；上傳清單（`playlistItems.list`）與 `search.list forMine` 哪一個會列出它。`search.list` 自己一桶、每天 100 次，不能拿來輪詢。
2. `fileDetails.fileName` 對 Studio 上傳的 Shorts 有沒有值（文件說只在 `processingDetails.fileAvailability` 是 `available` 時才回）。
3. 取消排程：`videos.update` 送 `status` 而不帶 `publishAt`，排程會不會清掉。
4. YouTube 把我們上傳的 1080×1920、25–55 秒影片歸成 Shorts 了沒有（歸類是自動的，Studio 與 API 都沒有開關；API 的影片資源也沒有任何欄位說它是不是 Shorts）。
5. 沒有通過稽核的專案，對 Studio 上傳的影片呼叫 `captions.insert` 與設 `publishAt` 會不會成功（跟 `2026-09-27-video-youtube-sync-field-test` 同一個問題，結果共用）。官方文件列的條件都符合，但沒有任何一頁明說。

已經查過、不用再測的（2026-09-28 讀官方頁，依據在 `docs/videos/SHORTS.md` §政策與依據）：Shorts 的「相關影片」只能在 Studio 設，API 寫不了；Shorts 不能做標題與縮圖的 A/B 測試；Shorts 的自訂縮圖只能在電腦版 Studio 設。

其他：

- 送 YouTube 的工作只能跑在 API 行程：審核檔案區只掛在那裡，權杖也只在那裡。
- 稽核通過後由網站自己上傳的部分在 `2026-09-28-video-shorts-auto-upload`。
- Analytics API 在 `2026-09-28-video-shorts-analytics`；這張票不加新的 OAuth scope。
- 經授權取得的統計數字可以久存，但每 30 天要確認授權還在、影片沒有被刪（開發人員政策 III.E.4）。
