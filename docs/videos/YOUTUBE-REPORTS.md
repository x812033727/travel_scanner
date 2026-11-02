# 頻道報表：YouTube Reporting API

站台每天把頻道的 YouTube Reporting API 報表下載回來保存，配對過影片工具權杖（`mkv_`）的 AI
session 從站台讀這些數字，分析哪支影片、哪種題材、哪種標題縮圖表現好，回頭改進下一批。AI 不碰
Google 的授權，也不需要任何 Google 憑證。

- 程式：`apps/api/app/video_youtube/reporting.py`（Google 的呼叫）、`reports.py`（同步與讀取）、
  `admin_reports_api.py`（路由）、`models.py`（三張表，migration 0145）。
- 網站轉送：`apps/web/app/api/video/youtube-reports`（只轉送影片工具權杖，不轉 cookie）。
- 後台：`/admin/videos` 設定分頁的 YouTube 卡片多一段「頻道報表」。
- 工具：`node tools/video/youtube-reports/cli.mjs`（`overview`、`sync`、`rows`、`videos`、`traffic`、`export`）。
  `videos` 與 `traffic` 在 AI 那一端把原始列加總成每支影片的成效與流量來源，輸出時標明是自行計算；
  `codes.mjs` 把流量來源、播放位置、裝置、作業系統的數字代碼對成名稱（2026-11-02 讀的維度頁）。
- AI 的做法：skill `youtube-channel-reports`（`.agents/skills/youtube-channel-reports/SKILL.md`）。

## Reporting API 是什麼（2026-11-02 讀的官方文件）

YouTube Analytics 有兩半：Analytics API 是即時查詢，Reporting API 是批次報表。後者的運作：

1. 頻道為每一種報表類型建一個 job（`POST https://youtubereporting.googleapis.com/v1/jobs`，
   body 是 `reportTypeId` 與 `name`；已經有就回 409）。
2. YouTube 之後每天為每個 job 產生一份 CSV，涵蓋一個太平洋時間的日（00:00–24:00 PT），
   通常晚 48–72 小時。建 job 時還會補上建立前 30 天的資料，一兩天內陸續出現。
3. `GET /v1/jobs/{id}/reports?createdAfter=…` 列出報表，每份有 `startTime`、`endTime`、
   `createTime` 與 `downloadUrl`；帶同一個 bearer token GET `downloadUrl` 拿 CSV（`Accept-Encoding:
   gzip` 時用 gzip 傳）。第一列是欄位名，之後可能多出新欄位，要照欄位名讀。
4. **每份報表只保留 60 天**（補的歷史資料 30 天）。所以站台必須定期下載保存，不能等要用才去拿。
5. 同一天可能被重新產生（更正或補資料）：新的報表 id、同樣的 `startTime`／`endTime`、較新的
   `createTime`。官方要求只用 `createTime` 較新的那份，舊的整天換掉。
6. 範圍：`https://www.googleapis.com/auth/yt-analytics.readonly`（營收要
   `yt-analytics-monetary.readonly`，站台不要）。

2025-06-30 起 Shorts 觀看數的算法改了，報表版本從 a2 升到 a3，舊算法保留在新欄位 `engaged_views`；
2026-01-15 加了觸及報表（縮圖曝光次數與曝光點閱率）。站台不寫死版本：每次同步讀
`GET /v1/reportTypes`，每個家族挑沒有被棄用的最新版本（`reports.choose_types`）。

## 站台保存哪些報表

| 家族 | 回答的問題 |
| --- | --- |
| `channel_basic` | 每支影片每天的觀看、engaged views、觀看時間、平均觀看時長與百分比、喜歡、留言、分享、訂閱增減；依國家、是否訂閱者、直播或隨選分列 |
| `channel_reach_basic` | 每支影片每天的縮圖曝光次數與曝光點閱率 |
| `channel_reach_combined` | 縮圖曝光與點閱率，依流量來源、裝置與作業系統分列 |
| `channel_traffic_source` | 觀看從哪裡來（搜尋與搜尋字詞、推薦、Shorts 動態、外部網站…） |
| `channel_playback_location` | 在哪裡播放（觀看頁、嵌入、頻道頁、Shorts 動態…） |
| `channel_device_os` | 裝置與作業系統 |
| `channel_demographics` | 年齡層與性別（佔比） |
| `channel_sharing_service` | 分享到哪些服務 |
| `channel_subtitles` | 觀看時開的字幕語言 |
| `channel_end_screens` | 片尾畫面元素的曝光與點擊 |

不收 `channel_combined`（每個維度同時展開，最大的一份，其他報表已經回答它的問題）。報表**沒有**
逐秒的觀眾留存曲線（那是 Analytics API 的 `audienceWatchRatio`），也沒有「選擇觀看還是滑走」
（只有 Studio 看得到）；需要時照 `tasks/open/2026-09-28-video-shorts-analytics.md` 從 Studio 匯出。

## 保存與同步

- 每個報表類型與太平洋日一列（`video_youtube_reports`），CSV 原封不動 gzip 存起來，連欄位名一起；
  較新的 `createTime` 取代舊的，較舊的不會蓋掉新的。
- `sync` 每次最多下載 150 份（`limit` 可到 400），還有剩就回 `partial` 與 `remaining: true`，
  工具的 `sync` 會一直叫到沒有剩。沒有 `force` 時，距離上次完整同步不到 12 小時就回 `not_due`。
- 同步用 Redis 鎖（15 分鐘）防止兩個同時跑；同一天的唯一鍵讓重疊也不會變兩份。
- `downloadUrl` 不是 `https://youtubereporting.googleapis.com` 的報表一律不下載（權杖不送去別處），
  解壓後超過 32 MB 的也略過。
- **誰來觸發**：`app.analytics.scheduler` 每天在台北時間上午、下午各排一次 RQ 工作
  `app.video_youtube.jobs.sync_reports`（"analytics" 佇列），一次跑到沒有剩為止；12 小時內做過就不動，
  沒連結或沒有 Analytics 時什麼也不做。AI session 的 `sync` 與後台卡片的「立即下載報表」是手動補跑。

## 授權、刪除與 YouTube 的政策

- 連結頻道時同意畫面多要 `yt-analytics.readonly`。之前就連結的頻道只有 `youtube.force-ssl`，
  卡片顯示「要重新連結」，上架照常；站主按「重新連結」並勾選 Analytics 後才讀得到報表。
- 站主還要在自己的 Google Cloud 專案：「API 和服務」→「程式庫」啟用 **YouTube Reporting API**，
  並在 OAuth 同意畫面的「資料存取」加上這個範圍。沒啟用時 Google 回 403，站台會說「還沒有啟用」，
  不會誤報成要重新連結。
- 解除連結後，報表在下一次被讀時整批刪除（卡片在解除連結後會立刻讀一次）；換連到另一個頻道時，
  舊頻道的報表也一樣刪掉（Developer Policies III.E.4：授權沒了，經它取得的資料要刪）。授權每 25
  天由卡片用 channels.list 驗一次，沿用既有機制。
- **站台不算衍生指標**：伺服器與頁面只回 YouTube 寫的原值，不加總、不平均、不排名、不算比率；
  測試裡有一條檢查 overview 沒有這類欄位。YouTube 的開發人員政策原則上不准 API 用戶端把它自己
  從 API 資料算出的指標呈現給使用者（例外條款要稽核時選 Analytics & Reporting，見
  `tasks/open/2026-09-28-video-shorts-audit-update.md`）。AI 為站主做的分析是它自己的工作：
  報告裡算出來的數字要標明「依 YouTube 報表原始數據自行計算」，不能當成 YouTube 的數字，
  也不放上公開頁面。

## 工具權杖能讀什麼

任何有效的影片工具權杖都能讀（不另外勾權限）：報表只描述站主自己的頻道，讀它不花錢、不改任何
東西。路由（經 `https://mokaair.com/api/video/…`）：

| 路由 | 內容 |
| --- | --- |
| `GET youtube-reports` | 連結狀態、是否有 Analytics、上次同步、每種報表涵蓋的日期與欄位、站台已上 YouTube 的影片（slug、標題、分類、是否 Shorts、系列、公開時間）、政策說明 |
| `POST youtube-reports/sync` | `{"force": bool, "limit": 1–400}`；每小時 30 次 |
| `GET youtube-reports/rows` | `report`（家族或類型 id）、`start`、`end`（太平洋日，含頭尾，最多 120 天）、`video_id`（可重複，最多 50）、`format=json|csv`；JSON 最多 5 萬列、CSV 50 萬列，超過時 `truncated: true` |
