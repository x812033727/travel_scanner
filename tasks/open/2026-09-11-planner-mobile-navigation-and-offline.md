---
id: 2026-09-11-planner-mobile-navigation-and-offline
title: 行程規劃器在手機沒有全域導覽且離線頁無入口
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/today-view.tsx
  - apps/web/components/offline-trip-cache.tsx
  - apps/web/app/[locale]/trips/[id]/page.tsx
  - apps/web/public/sw.js
---

# 行程規劃器在手機沒有全域導覽且離線頁無入口

## Why

**一、`/trips/[id]` 在手機上沒有任何站台導覽。** 三層隱藏疊加：

- `app/[locale]/trips/[id]/page.tsx:26,31` — `<div className="hidden lg:block"><SiteHeader /></div>`
- `app-bottom-nav.tsx:78` — 對 `/trips/` 回傳 `null`
- `site-footer.tsx:9` — `HIDDEN_ON = ["/admin", "/trips/"]`

規劃器自己補了一顆 44px 的返回鈕（`trip-editor.tsx:1820`）回到 `/trips`，勉強可以。

**二、但當日檢視完全沒有補。** `today-view.tsx:90-111` 唯一的對外連結是「開啟規劃器」到 `/trips/[id]`。使用者要兩跳才離得開，而且沒有回首頁的路。這偏偏是旅途中在路上會開的頁面。

**三、離線快取首次通常抓不到東西。** `?view=today` 全站沒有任何連結指向它（grep `app/` 與 `components/` 只找到 `trips/[id]/page.tsx:24` 的一句註解），只能手打 query string。而就算打進去了：`offline-trip-cache.tsx:96-113` 先註冊 SW、等 `navigator.serviceWorker.ready`、再等 `/auth/me` 回來才 post `signed-in`；`today-view.tsx:52-56` 卻立刻發行程請求；`public/sw.js:49` 在 `cacheName` 還是 null 時直接 bail out。結果是**第一次線上造訪通常什麼都沒快取到**——旅客得在還有訊號的時候開兩次，這頁才會在沒訊號時有用。而他根本不知道有這頁。

## Definition of done

- [ ] 當日檢視有回到行程列表與首頁的路。
- [ ] `?view=today` 在規劃器裡有可見的入口。
- [ ] 第一次線上開啟當日檢視就會完成快取，離線時可用。

## Steps

- [ ] `today-view.tsx` 加上最小導覽（回行程列表、回首頁），或讓 `app-bottom-nav.tsx:78` 對 `?view=today` 不要隱藏。
- [ ] 在規劃器加一顆「當日檢視／離線用」入口，並說明它的用途。
- [ ] 修快取競態：`today-view.tsx` 等 `offline-trip-cache` 回報就緒後再發請求，或讓 `sw.js` 在 `cacheName` 未就緒時把請求排隊而不是 bail out。
- [ ] 加一個 e2e：第一次線上開啟 `?view=today`，斷網後重新載入仍看得到內容。

## How to verify

```bash
cd apps/web && npm run test:web -- today-view offline-trip-cache
cd apps/web && npx playwright test --project="Pixel 7"
```

## Notes

- `today-view.tsx:52-56` 的 `.catch(() => setOffline(true))` 把 401、404、500 全部標成「離線」，使用者看到 `t("unavailable")` 且無重試、無回程。那部分歸 `2026-09-11-ux-dead-ends-and-empty-states`，本任務只處理導覽與快取。
