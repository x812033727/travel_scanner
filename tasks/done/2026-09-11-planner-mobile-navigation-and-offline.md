---
id: 2026-09-11-planner-mobile-navigation-and-offline
title: 行程規劃器在手機沒有全域導覽且離線頁無入口
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T18:27:00Z
created_at: 2026-09-11T03:21:00Z
completed_at: 2026-09-11T18:38:43Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/today-view.tsx
  - apps/web/components/offline-trip-cache.tsx
  - apps/web/app/[locale]/trips/[id]/page.tsx
  - apps/web/public/sw.js
  - apps/web/components/trip-editor.tsx
  - apps/web/components/today-view.test.tsx
  - apps/web/components/offline-trip-cache.test.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
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

- [x] 當日檢視有回到行程列表與首頁的路。
- [x] `?view=today` 在規劃器裡有可見的入口。
- [x] 第一次線上開啟當日檢視就會完成快取，離線時可用。

## Steps

- [x] `today-view.tsx` 加上最小導覽（回行程列表、回首頁），或讓 `app-bottom-nav.tsx:78` 對 `?view=today` 不要隱藏。
- [x] 在規劃器加一顆「當日檢視／離線用」入口，並說明它的用途。
- [x] 修快取競態：`today-view.tsx` 等 `offline-trip-cache` 回報就緒後再發請求，或讓 `sw.js` 在 `cacheName` 未就緒時把請求排隊而不是 bail out。
- [ ] 加一個 e2e：第一次線上開啟 `?view=today`，斷網後重新載入仍看得到內容。

## How to verify

```bash
cd apps/web && npm run test:web -- today-view offline-trip-cache
cd apps/web && npx playwright test --project="Pixel 7"
```

## Notes

- `today-view.tsx:52-56` 的 `.catch(() => setOffline(true))` 把 401、404、500 全部標成「離線」，使用者看到 `t("unavailable")` 且無重試、無回程。那部分歸 `2026-09-11-ux-dead-ends-and-empty-states`，本任務只處理導覽與快取。

## claim 用了 --force（scope 擴到 `trip-editor.tsx`），理由（claude-opus-5, 2026-09-11）

Steps 第二條要在規劃器加入口，那就得動 `trip-editor.tsx`，而它在 `2026-09-10-seoul-day2-transport-ux`（codex-seoul-day2-release）的 scope 裡。理由與本分支前面幾張相同：claim 已逾 36 小時（board 標為 stale），工作已合併進 main（`5f34f77`），遠端分支已不存在。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 一、當日檢視有出口了

`today-view.tsx` 頂端加一列「我的旅程 / 首頁」。三層隱藏（page 的 `hidden lg:block`、`app-bottom-nav` 對 `/trips/` 回 `null`、`site-footer` 的 `HIDDEN_ON`）沒有動——它們各有理由，而且動任何一層都會影響規劃器。載入中與讀不到行程的兩種狀態也有這列，因為那正是最需要離開的時候。

### 二、`?view=today` 在規劃器的「旅行準備」有入口了

一張 `planner-tool-card`，標題「今日檢視（可離線）」，副標說明它的用途——出發前開一次就會存在手機裡。原本全站沒有任何連結指向 `?view=today`，只能手打 query string。

### 三、快取競態

**原因比任務寫的更常發生。** `sw.js` 的 `cacheName` 是 worker 的 module 變數，而瀏覽器會積極地把 service worker 殺掉重啟——所以「第一次請求發生在 worker 還不知道自己是誰的時候」不只是首次造訪會遇到，是每次 worker 重啟都會再發生一次。

修法：`OfflineTripCache` 現在收 `tripId`，在 worker 回報它已經有 cache name 之後，**自己再抓一次行程**。用 `MessageChannel` 讓 worker 明確回覆（`sw.js` 收到 `signed-in` 時 `event.ports[0].postMessage({type:"ready"})`），所以不是靠 `setTimeout` 猜——但還是留了 1 秒的上限，避免舊版 worker 不會回覆時整個卡住。

代價是當日檢視每次多一個 GET。沒有改成「讓 `TodayView` 等 worker 就緒再發請求」，因為那要在兩個兄弟元件之間拉一條共用狀態，而多一次 GET 換到的是這頁存在的唯一理由——在沒訊號的月台上讀得到。

### 驗證

- `today-view.test.tsx` 兩個案例：載入中與讀取失敗時，兩個出口都在，`href` 分別是 `/trips` 與 `/`。
- `offline-trip-cache.test.tsx`（新檔）兩個案例：worker 回覆之後才抓行程（**順序也斷言了**——`/auth/me` 必須排在 `/trips/` 前面），以及沒有 `tripId` 時只報身分、不多抓。把 priming 拿掉之後第一條變紅。
- `trip-editor.test.tsx` 一個案例：「旅行準備」裡有指向 `?view=today` 的連結。

整套 230 files / 2329 tests 全過。

### 沒做的那一項

Steps 第四條「加一個 e2e：第一次線上開啟 `?view=today`，斷網後重新載入仍看得到內容」**沒有做**，原因有兩個，都寫清楚：

1. **新的 spec 檔在 CI 跑不到。** `.github/workflows/ci.yml` 逐一列出要跑的 spec，而那個檔在 `2026-09-09-clarify-stay22-module-switch` 與 `2026-09-11-pr388-seo-review` 的 scope 裡（兩張都在 review，claim 未逾時），我不該去改。加一個永遠不會執行的 spec 沒有意義。
2. **既有 spec 用 `page.route` 攔截 API**，而 service worker 發出的請求不走那條路。把 worker 放進那些 spec 的環境裡，很可能讓原本穩定的 mock 開始不穩。

已建檔：`2026-09-11-offline-today-e2e`，內容包含要把它接進 `ci.yml` 這件事。
