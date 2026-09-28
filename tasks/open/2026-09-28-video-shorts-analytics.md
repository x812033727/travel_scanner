---
id: 2026-09-28-video-shorts-analytics
title: Video shorts M2: engaged views and retention from YouTube Analytics, and Studio exports for the numbers the API does not have
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T04:20:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-youtube-auto
scope:
  - apps/api/app/video_shorts/analytics.py
  - apps/api/app/video_shorts/exports.py
  - apps/api/app/video_shorts/stats.py
  - apps/api/app/video_youtube/connection.py
  - apps/api/app/video_youtube/client.py
  - apps/api/tests/test_video_shorts_analytics.py
  - apps/api/tests/test_video_youtube.py
  - apps/web/components/admin-video-shorts-metrics.tsx
  - apps/web/components/admin-video-shorts-metrics.test.tsx
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video shorts M2: engaged views and retention from YouTube Analytics, and Studio exports for the numbers the API does not have

## Why

第一期的成效只有觀看、喜歡、留言（Data API 的 `statistics`）。要判斷一支 Shorts 好不好，#871 的企劃用的是 engaged views、選擇觀看的比例、平均觀看百分比、分享與新增訂閱。這些數字：

- engaged views、平均觀看百分比、平均觀看時間、分享、新增訂閱在 YouTube Analytics API 有，但要多一個唯讀的 OAuth scope，站主得重新按一次允許。
- 「選擇觀看，還是滑走」API 沒有，只有 Studio 看得到、匯得出。

另外，YouTube 的開發人員政策原則上不准用 API 的數字算衍生指標，所以 #871 那套「中位數、兩倍、連續五支」的算式不能直接拿 API 的數字去跑；它可以跑在站主自己從 Studio 匯出的資料上。2026-06-01 起有例外條款（`developers.google.com/youtube/terms/derived-metrics-policy`）：稽核時用途選了「Analytics & Reporting」並接受增修條款的開發者，可以算自訂的分數、比率與排行，要跟 API 的原值分開標示。

設計全文在 `docs/videos/SHORTS.md`（§成效與每週報告、§政策與依據）。

## Definition of done

- [ ] 連結頻道時多要 `https://www.googleapis.com/auth/yt-analytics.readonly`；已經連結的頻道在卡片上顯示「要重新授權才讀得到進階數字」，站主不重新授權時第一期的數字照常。
- [ ] 每支已公開的 Shorts 讀三個區間報表：公開日起算第 1 天、第 1–3 天、第 1–7 天（太平洋時間的日；資料齊了才讀，通常晚兩到三天），寫進 `video_shorts_metrics`（`source: "analytics_api"`）；每個時間窗只寫一次。
- [ ] 頂列的 90 天目標改讀頻道層級的報表（加上維度 `creatorContentType`、留 `SHORTS` 那一列、開跑日到今天）的觀看數與 engaged views，那是 YouTube 直接回報的總數，不是把每支加起來。官方只把 `creatorContentType` 列為維度，沒有列為篩選條件；不要用沒寫在文件裡的 `filters=creatorContentType==SHORTS`。
- [ ] 成效區多五欄，數字旁標來源與區間；Data API 與 Analytics 的觀看數定義不同，兩欄分開、不互相取代。
- [ ] Studio 匯出檔上傳（`POST /admin/video-shorts/metrics/import`）：收站主從 Studio 進階模式匯出的檔案，依影片 id 對回 Shorts，寫成 `source: "studio_export"` 的快照；缺欄位的列放進待補清單，不補零。
- [ ] 只在 `studio_export` 的資料上提供 #871 的系列判定（至少五支、各滿七天、至少 1,000 engaged views；擴大、修改、暫停、資料不足），畫面上標明「依你從 Studio 匯出的資料計算，不是 YouTube 的數字」。
- [ ] 伺服器與頁面預設不從 `data_api`、`analytics_api` 的數字算任何分數、排名、中位數或達成率；測試裡有一條專門檢查回應裡沒有這類欄位。站主在設定分頁勾了「稽核已接受 Analytics & Reporting 用途」之後，系列判定才可以改吃 API 的數字，畫面上照樣標明是本站自己算的。
- [ ] pytest 與 vitest：重新授權前後、三個區間、資料還沒齊時不寫、匯入的對應與待補、判定只吃匯出資料。

## Steps

- [ ] 先等 `2026-09-28-video-shorts-audit-update` 決定申請書怎麼寫 Analytics；申請書沒寫到的用途不要先上線。
- [ ] 重讀 Analytics API 的指標與維度頁（記下讀取日期）；確認 Shorts 的篩選與每支影片的區間報表怎麼下。
- [ ] `connection.py` 的 scope 與重新授權、`client.py` 的報表方法。
- [ ] `analytics.py`、`exports.py`；把 `tools/video/shorts/tracking.mjs` 的判定規則照樣移過來（同一組測試案例）。
- [ ] 成效區的欄位與匯入表單。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts_analytics.py tests/test_video_youtube.py -q
cd apps/web && npx vitest run components/admin-video-shorts-metrics
```

## Notes

- 經授權取得的 Analytics 資料與統計數字可以存到不需要為止，但每 30 天要確認授權還在、影片沒有被刪（開發人員政策 III.E.4）；Y1 的 `tick` 已經每天驗一次。
- 非 API 的數字跟 API 的數字並列時，要清楚標示它不是來自 YouTube（同一份政策）。
- Studio 匯出檔的欄位名稱會跟著介面語言變：照站主實際匯出的檔案寫對應表，原檔的欄位名與單位原樣保留在 `raw`。
- Analytics 的資料通常晚 48–72 小時、以太平洋時間的日為單位；每個請求算 1 單位；限定單一影片時 `subscribersGained` 只算從那支影片的頁面訂閱的。
- 既有的權杖不會自己多出新的 scope：站主要重新走一次同意畫面，同意之後拿到的權杖同時涵蓋新舊兩個 scope。
- 兩種觀看數不要混：Data API 的 `viewCount` 是公開的觀看數（每次開始播放都算）；營利資格看的是 engaged views（官方現在叫合格的 Shorts 觀看）。
