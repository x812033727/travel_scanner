---
id: 2026-09-11-offline-today-e2e
title: 當日檢視的離線 e2e 與 CI 接線
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T18:38:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/offline-today.spec.ts
  - .github/workflows/ci.yml
---

# 當日檢視的離線 e2e 與 CI 接線

## Why

`2026-09-11-planner-mobile-navigation-and-offline` 修好了當日檢視的離線快取競態（worker 回報就緒後由 `OfflineTripCache` 自己再抓一次行程），並用元件測試釘住了「順序正確、確實有抓」。但**「斷網後重新載入仍看得到內容」這件事只有瀏覽器能證明**，那張任務沒有做，原因兩個：

1. 新的 spec 檔在 CI 跑不到——`.github/workflows/ci.yml` 逐一列出要跑哪些 spec，而那個檔當時在兩張 review 中任務的 scope 裡。
2. 既有的 spec 用 `page.route` 攔 API，而 service worker 發出的請求不走那條路；把 worker 放進那些 spec 的環境，很可能讓原本穩定的 mock 開始不穩。

## Definition of done

- [ ] 一個 e2e：登入後開 `?view=today`，`context.setOffline(true)`，重新載入，畫面仍有今天的安排。
- [ ] 這個 spec 真的會在 CI 執行。

## Steps

- [ ] 新增 `apps/web/e2e/offline-today.spec.ts`，用自己的 context（`serviceWorkers: "allow"`），不要共用其他 spec 的 `page.route` mock。
- [ ] 等 `navigator.serviceWorker.controller` 出現、且 `OfflineTripCache` 的補抓完成，再 `setOffline(true)`。
- [ ] 把它加進 `.github/workflows/ci.yml` 的 browser spec 清單。
- [ ] 順手確認 worker 只攔 `^/api/travel/trips/[^/]+$`，不會影響同一個 context 裡其他 spec 的請求。

## How to verify

```bash
cd apps/web && npx playwright test e2e/offline-today.spec.ts
```

## Notes

- 已經有的保護：`components/offline-trip-cache.test.tsx` 釘住「worker 回報 ready 之後才抓行程」，包含 `/auth/me` 必須排在 `/trips/` 之前。缺的是真的斷網那一段。
- `sw.js` 只攔 GET 且只攔單一 URL 形狀，所以爆炸半徑很小；這也是為什麼可以用一個獨立 context 測。
