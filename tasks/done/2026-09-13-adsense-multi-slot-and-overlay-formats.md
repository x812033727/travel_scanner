---
id: 2026-09-13-adsense-multi-slot-and-overlay-formats
title: 文章頁多個文中廣告與自動廣告疊加格式
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T13:16:34Z
created_at: 2026-09-13T13:16:28Z
completed_at: 2026-09-13T13:38:59Z
branch: claude/article-ad-revenue-optimization-9c5bd8
depends_on: []
scope:
  - apps/web/lib/adsense.ts
  - apps/web/lib/adsense.test.ts
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/ads
  - apps/web/app/globals.css
  - apps/web/e2e/guides-adsense.spec.ts
  - docs/adsense-feasibility.md
  - docs/travel-guides.md
---

# 文章頁多個文中廣告與自動廣告疊加格式

## Why

站主問「文章裡怎麼放廣告收益最高」。原本每篇最多 1 個文中廣告，而且只放在第一個合作按鈕之前的那一段，
110 份文件裡有 34 份因為按鈕太靠前，一個廣告都沒有。
正式站 2026-09-13 實測：`zh-TW/guides/howto/tokyo-where-to-stay` 有 slot，
`en/guides/howto/taoyuan-airport-to-taipei` 載入了腳本卻沒有 slot。

站主選的做法（`docs/adsense-feasibility.md` 的「D3 修訂」）：

- **混合**：文中廣告維持手動，錨定、插頁、Multiplex 用自動廣告開啟，頁內自動廣告維持關閉。
- 文中依長度放 1–3 個，全部共用現有 slot。

## Definition of done

- [x] 一般長度的文章都有文中廣告。長文最多 3 個，每個都跟合作按鈕、文末面板保持距離。
- [x] 第 2、3 個版位接近畫面才請求廣告；沒填到的版位不留空框。
- [x] 手機上的錨定廣告不會蓋住底部導覽列或頁首。
- [x] AdSense 後台設定、封鎖清單查證與兩週後的比較，拆到後續票 `2026-09-13-adsense-auto-ads-overlay-setup`。

## Steps

- [x] `lib/adsense.ts`：`adsenseSplit` 換成 `adsensePlacements`，規則與常數都 export。
- [x] `components/guides/article.tsx` 依 pieces 交錯渲染，heading 編號跨片段連續。
- [x] `components/ads/article-ad-slot.tsx` 加 `lazy`；`globals.css` 收起 `data-ad-status="unfilled"` 的版位。
- [x] `components/ads/anchor-ad-offset.tsx` 用幾何量錨定廣告，並由 `AdsenseLoader` 掛上；`globals.css` 讓導覽列、頁首、底部留白讓位。
- [x] 單元測試、content pack 覆蓋率測試、e2e（長文 3 個版位與延遲請求、未填滿收起、錨定讓位）。
- [x] 文件：`docs/adsense-feasibility.md` D3 修訂、`docs/travel-guides.md` Advertising 一節。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/web && npm run build && PLAYWRIGHT_SERVE_BUILD=true PLAYWRIGHT_PORT=3217 npx playwright test e2e/guides-adsense.spec.ts
```

部署後：

- 正式站長文（例如 `zh-TW/guides/howto/tokyo-where-to-stay`）的 HTML 裡，slot 數字出現次數等於版位數 × 2（HTML＋RSC）。
- 審核通過、自動廣告開啟後，用手機看錨定廣告出現時，底部導覽列有沒有往上移。

## Notes

- 規則以 content pack 模擬（2026-09-13，50 個 slug、110 份文件）：0 個廣告的 3 份都是 15–20 區塊的短文
  （japan-tax-free-refund、japan-winter-illumination、korea-winter-events 的 zh-TW）；1 個 12 份、2 個 57 份、3 個 38 份，平均 2.18。
  `lib/adsense.test.ts` 的「the rules against the articles actually published」會讀 content pack，
  新文章如果長度正常卻拿不到版位就會失敗。
- 錨定偵測刻意不用 Google 的 `data-anchor-status`：那是未公開屬性。看的是 `position: fixed` 的 `ins.adsbygoogle`
  貼齊哪一邊、露出多少；蓋住半個畫面以上的算插頁，不處理。
- jsdom 的 `requestAnimationFrame` stub 如果同步呼叫 callback，`frame` 會在 apply 之後才被設成非 0，
  之後的排程全部被略過。測試改用 `setTimeout` 模擬。
- e2e 裡直接 `scrollIntoViewIfNeeded()` 跳到最後一個版位時，中間那個從沒進過畫面，不會請求廣告；
  真實讀者是連續捲動。測試照讀者的方式依序捲。
- 第一次平行跑 e2e 時，fixture 的 Next 伺服器 30 秒內沒起來（build 後第一次冷啟動），重跑兩次都 20/20 通過。
