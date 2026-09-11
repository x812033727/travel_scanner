---
id: 2026-09-11-bottom-nav-covers-page-content
title: 手機底部導覽列蓋住七成頁面的內容含登入鈕
status: open
priority: P0
area: web
owner:
claimed_at:
created_at: 2026-09-11T13:05:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/app/[locale]/login/page.tsx
---

# 手機底部導覽列蓋住七成頁面的內容含登入鈕

## Why

用真實瀏覽器掃過 162 個頁面（手機 390px 與桌面 1440px），量測結果：

- 手機頁面 81 個，其中 **79 個有固定底部導覽列**
- 這 79 個裡，**56 個（71%）有可互動元素被那條列蓋住**
- 桌面 0 個 —— 這是純手機問題

最嚴重的是 **`/login` 頁面本身**：「登入」送出鈕直接壓在導覽列下，只露出上緣；「忘記密碼」完全看不見。一個用手機想登入的人，第一眼看不到登入按鈕。

被遮住的內容依類型：

| 被遮住 | 路由 |
| --- | --- |
| 「登入」送出鈕、「忘記密碼」 | `/login` 與六條 `/admin/*` |
| 篩選條件（賞雪、藥妝、壽司、海鮮、櫻花…） | `/hotspots`、`/foods`，五語系皆然 |
| 頁尾連結（目的地、關於 Mokaair、聯絡我們） | `/about`、`/privacy`、`/terms`、`/contact` |
| 卡片的「收藏」「加入旅程」 | 首頁、`/explore` |

`globals.css:290-293` 的 `.public-app-shell` 有保留 `5rem + env(safe-area-inset-bottom)`，所以機制是存在的——問題在於**有些頁面沒有用到那個 shell，或保留量小於導覽列的實際高度**（量到的底部保留約 69px，而導覽列含外距約 86px）。

## Definition of done

- [ ] 手機上沒有任何可互動元素被固定底部列蓋住。
- [ ] `/login` 的送出鈕在預設捲動位置就看得見。
- [ ] 有自動化斷言防止再犯。

## Steps

- [ ] 先確認 `.public-app-shell` 的保留量與 `app-bottom-nav` 的實際高度（含 margin 與 safe-area）是否一致；不一致就以導覽列的實際高度為準。
- [ ] 找出沒有套用該 shell 的頁面（`/login`、`/admin/*`、靜態內容頁是已知的），讓它們也取得同樣的底部保留。
- [ ] `/hotspots` 與 `/foods` 的篩選列需額外確認——那是可捲動區域內的內容，可能要調整容器的 padding-bottom 而非整頁。
- [ ] 加 e2e 斷言：Pixel 7 尺寸下，走訪主要路由，斷言沒有可互動元素與底部列的矩形相交。`e2e/navigation.spec.ts:64` 已有無橫向溢位的同類斷言可照抄。

## How to verify

```bash
cd apps/web && npx playwright test --project="Pixel 7"
```

手動：手機尺寸開 `/zh-TW/login`，不捲動就要看得到登入鈕。

## Notes

- 量測方法：對每個可見的可互動元素取 `getBoundingClientRect()`，與固定底部列的矩形做相交判定。不是目測。
- 桌面 1440px 完全沒有此問題（0/81），所以修正時不要動到桌面版面。
- 這條與 `2026-09-11-no-sign-in-entry-in-discovery` 相關但不同：那張講的是「頁首沒有登入入口」，這張講的是「登入頁自己的按鈕被蓋住」。兩張都要修才算完整。
