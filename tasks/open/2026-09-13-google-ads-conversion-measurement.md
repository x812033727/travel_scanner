---
id: 2026-09-13-google-ads-conversion-measurement
title: 付費 Google Ads 導流的轉換量測
status: blocked
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-13T05:16:19Z
completed_at:
branch:
depends_on:
  - 2026-09-12-attribute-affiliate-clicks-to-the-guide
scope:
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
  - apps/web/lib/analytics.ts
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
  - apps/api/app/affiliates/router.py
  - apps/api/app/analytics/affiliates.py
  - apps/api/app/models.py
  - apps/api/migrations/versions
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_analytics_affiliates.py
---

# 付費 Google Ads 導流的轉換量測

## Why

評估文件 `docs/adsense-feasibility.md` 第九節的結論：現在花錢投 Google Ads 導流大多會賠錢，
**補齊量測前不建議投**。這張票就是那個「補齊量測」。

**先別動手**：要等站主決定真的要投放（小額實驗），並選好下面的量測路線。沒投放就不需要這些程式。

現在量不出來的原因（2026-09-13 讀程式）：

- GA4 的 `page_location` 只保留路徑（`analytics-provider.tsx:62`、`:117` 用 `sanitizedPath`），
  網址上的 `gclid`／`gbraid`／`wbraid` 會被丟掉。所以就算把 GA4 連到 Google Ads，也歸因不到廣告點擊。
- Consent Mode 四項永遠是 denied（`:59`），Google 那邊只收得到 cookieless 訊號，轉換大多是模型推估。
- web 只接受 `G-` 開頭的 ID（`:165`，API 端 `admin/service.py:1264`、`analytics/service.py:177`），沒有 Google Ads 轉換標記。
- 第一方分析有記 `utm_source`／`utm_medium`／`utm_campaign`，但只存在 React ref 裡（`analytics-provider.tsx:71`），
  沒有傳到分潤點擊；`affiliate_clicks`（`apps/api/app/models.py:282`）也沒有 campaign 欄位。
  結果是算不出「某個廣告活動帶來多少分潤點擊」。

## Definition of done

- [ ] 站主選的路線寫在 Notes：
      - **A. 只用第一方資料（建議）**：落地頁的 `utm_campaign` 存進 sessionStorage；分潤 clickout 帶一個**粗粒度、白名單驗證**的
        campaign 標籤，規則比照 `affiliates/sub_id.py`，不接受任意字串，也不能長得像識別碼。
        `affiliate_clicks` 加欄位，`GET /admin/analytics/affiliates` 多一個 by_campaign。
      - **B. 另外接 Google Ads 歸因**：落地頁那一次的 GA4 `page_location` 保留 `gclid`／`gbraid`／`wbraid`，其他參數照樣去掉；
        站主在 GA4 把 outbound `click` 事件標成關鍵事件，再連結 Google Ads。
        這些點擊 ID **絕不寫進我們自己的資料庫或日誌**。
- [ ] 不管哪條路線，DNT／GPC 時一樣完全不送。
- [ ] 評估文件第九節更新成實際採用的做法。

## Steps

- [ ] 跟站主確認要投放、預算、要測哪幾篇文章（建議高意圖主題：機場交通、eSIM、交通票券）。
- [ ] 路線 A：`lib/analytics.ts` 保存 campaign → `destination-affiliate-options.tsx` 帶上 → clickout 驗證並寫入 → migration → 報表。
- [ ] 路線 B（如果選）：`analytics-provider.tsx` 的落地頁 `page_location` 規則與測試。
- [ ] 投放前寫好給站主的清單：品牌否定關鍵字（Klook、Booking、Agoda、KKday、Trip.com 等）、
      廣告只連到自己的文章頁、廣告文字不提品牌。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_affiliates.py tests/test_analytics_affiliates.py -q
cd apps/web && npx vitest run components/analytics-provider.test.tsx components/destination-affiliate-options.test.tsx
```

在瀏覽器用 `?utm_source=google&utm_medium=cpc&utm_campaign=esim-test` 開一篇文章，點分潤按鈕，
後台報表的 by_campaign 出現 `esim-test`；開 GPC 重做一次，什麼都不送。

## Notes

- 夥伴條款（評估文件第九節）：
  - Klook 禁止品牌字競價，不能把付費廣告當轉址，也不能在廣告裡放 Klook 的網址或商標。
  - Travelpayouts 多數方案禁付費搜尋；允許的也只能導到自己的網站，還要加品牌否定字。
  - Booking 禁止品牌字競價。
  違反會被取消分潤，所以廣告一定只連到自己的文章頁。
- 範圍重疊：`affiliates/router.py` 目前在 in-progress 的 `2026-09-12-trip-partner-offer-availability` 裡；
  `models.py` 在 `2026-09-12-food-merchant-enrichment` 裡。claim 前先 `npm run tasks -- list`。
