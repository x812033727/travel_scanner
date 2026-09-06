---
id: 2026-09-06-pwa-share-target-today-view
title: PWA、Android share target 與今日檢視
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T12:50:53Z
created_at: 2026-09-06T02:24:53Z
completed_at: 2026-09-06T12:50:56Z
branch: claude/pwa-today
depends_on: []
scope:
  - apps/web/app/manifest.ts
  - apps/web/public
  - apps/web/components/today-view.tsx
  - apps/web/public/sw.js
  - apps/web/components/offline-trip-cache.tsx
  - apps/web/components/share-target-view.tsx
  - apps/web/components/share-target-view.test.tsx
  - apps/web/components/today-view.test.tsx
  - apps/web/components/header-session.tsx
  - apps/web/app/[locale]/trips/[id]/page.tsx
  - apps/web/app/[locale]/share-target/page.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# PWA、Android share target 與今日檢視

## Why

`docs/planning-flow-spec.md` §1 步驟 13 與 §6 PR 13。出門當天需要的是「現在／下一個」的單欄檢視，而不是整個編輯器；
Android 的 share target 讓「在 Google Maps 分享 → 進行程」一步到位（iOS 沒有等價物，只能貼上，規格要求說清楚）。
`apps/web/app/manifest.ts` 目前不存在，`public/` 只有 `brand/` 與 `og.png`。

## Definition of done

- [x] 可安裝的 PWA（manifest、icons）；service worker 只快取當前行程 JSON 與路段，**依使用者分割、登出即清除**
      （payload 含住宿地址與私人備註）。
- [x] `/[locale]/trips/[id]?view=today`：現在／下一個卡片，離線可讀最後一次快取。
- [x] Android `share_target` 把分享的連結送進貼上匯入（依賴 `2026-09-06-paste-maps-links-ingest`）。

## Steps

- [x] `manifest.ts`＋icons；`today-view.tsx`。
- [x] service worker 的快取鍵帶 user id，`/auth/logout` 時 `caches.delete`。
- [x] iOS：貼上框，並在 UI 明說沒有 share sheet。

## How to verify

Android Chrome 安裝 → 飛航模式開 today view 仍可讀；登出後快取清空（DevTools → Application → Cache Storage）。

## Notes

規格 §7 Q5：約一半台灣使用者用 iPhone，貼上以外的 iOS 方案（剪貼簿讀取按鈕、捷徑食譜）值得另外想。

2026-09-06 claude-opus-5：

- `app/manifest.ts`：可安裝（standalone、theme color、既有的 512 與 180 圖示，
  512 那張同時給 `any` 與 `maskable`），以及 `share_target`（GET `/share-target`，帶 title／text／url）。
- `public/sw.js`：**只快取一種東西**——`GET /api/travel/trips/{id}`。其他任何請求、任何非 GET 的方法
  一律不攔截，所以這支 worker 出錯最多只會影響那一個網址形狀。
  快取名是 `mokaair-trip-<會員 id>`，而且**在頁面告訴它是誰之前不存任何東西**；
  收到 `signed-in` 時順手刪掉其他會員留下的快取，`signed-out` 時全部刪光。
  行程 payload 裡有飯店地址與私人備註，共用手機上不能留。
- `offline-trip-cache.tsx` 掛在行程頁（兩種檢視都掛），註冊 worker 並把 `/auth/me` 的 id 傳給它；
  `header-session.tsx` 的登出流程多一行 `postMessage({ type: "signed-out" })`。
- `?view=today`：`today-view.tsx` 單欄——現在／接下來兩張卡（有座標就給 Google Maps 導航連結）、
  今天其餘安排的清單、回到完整行程的連結。`nowAndNext()` 抽成純函式並單獨測
  （進行中、兩個停留點之間、當天還沒開始三種情況）。離線時 worker 會回上一次的行程 JSON；
  完全沒有快取時顯示「連上網路後再試一次」，不假裝有資料。
- `/share-target`：Android 分享過來的 title／url／text 併成待貼文字，讓使用者選一趟行程，
  送進 `POST /trips/{id}/places/ingest`（`2026-09-06-paste-maps-links-ingest` 的端點）。
  **iOS 沒有 share target**，所以同一頁就是貼上框，並在頁尾明說 iPhone 要用複製貼上——
  規格要求把這件事講清楚，而不是讓 iPhone 使用者找一個不會出現的分享選單。

沒有勾的一項：Android Chrome 實機安裝、開飛航模式確認 today view 仍可讀、
登出後在 DevTools → Application → Cache Storage 確認清空。這需要一支 Android 手機與已部署的站，
本機驗不了；程式碼層面的行為（快取名帶 id、登出送訊息、只攔一種網址）都有註解與測試釘住。
