---
id: 2026-09-06-pwa-share-target-today-view
title: PWA、Android share target 與今日檢視
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T02:24:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/manifest.ts
  - apps/web/public
  - apps/web/components/today-view.tsx
---

# PWA、Android share target 與今日檢視

## Why

`docs/planning-flow-spec.md` §1 步驟 13 與 §6 PR 13。出門當天需要的是「現在／下一個」的單欄檢視，而不是整個編輯器；
Android 的 share target 讓「在 Google Maps 分享 → 進行程」一步到位（iOS 沒有等價物，只能貼上，規格要求說清楚）。
`apps/web/app/manifest.ts` 目前不存在，`public/` 只有 `brand/` 與 `og.png`。

## Definition of done

- [ ] 可安裝的 PWA（manifest、icons）；service worker 只快取當前行程 JSON 與路段，**依使用者分割、登出即清除**
      （payload 含住宿地址與私人備註）。
- [ ] `/[locale]/trips/[id]?view=today`：現在／下一個卡片，離線可讀最後一次快取。
- [ ] Android `share_target` 把分享的連結送進貼上匯入（依賴 `2026-09-06-paste-maps-links-ingest`）。

## Steps

- [ ] `manifest.ts`＋icons；`today-view.tsx`。
- [ ] service worker 的快取鍵帶 user id，`/auth/logout` 時 `caches.delete`。
- [ ] iOS：貼上框，並在 UI 明說沒有 share sheet。

## How to verify

Android Chrome 安裝 → 飛航模式開 today view 仍可讀；登出後快取清空（DevTools → Application → Cache Storage）。

## Notes

規格 §7 Q5：約一半台灣使用者用 iPhone，貼上以外的 iOS 方案（剪貼簿讀取按鈕、捷徑食譜）值得另外想。
