---
id: 2026-11-11-e2e-pin-clock-fixture-dates
title: e2e：行程拖曳與天氣可讀性測試沒有固定時鐘，2026-11-11 東京換日後必失敗
status: done
priority: P2
area: web
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T17:22:24Z
created_at: 2026-11-11T17:22:06Z
completed_at: 2026-11-11T17:22:25Z
branch:
depends_on: []
scope:
  - apps/web/e2e/navigation.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/e2e/planner-calm.spec.ts
  - apps/web/e2e/trip-stay-areas.spec.ts
---

# e2e：行程拖曳與天氣可讀性測試沒有固定時鐘，2026-11-11 東京換日後必失敗

## Why

web-e2e 從 2026-11-11 17:00 UTC（東京已是 11-12）起固定失敗四項：navigation.spec 的「itinerary drag handle…」與 readability.spec 的三個 planner weather 測試。測試資料把行程與天氣預報寫死在 2026-11-11–12，卻沒有固定瀏覽器時鐘；真實日期一過，行程變成過去（「排序行程」被停用），天氣摘要的 2026-11-11 那天也不再顯示。同一檔案裡其他測試早就用 page.clock.setFixedTime 固定時鐘。

## Definition of done

- [x] 兩處在 page.goto 之前固定時鐘（拖曳測試 2026-11-01T03:00Z，同檔既有寫法；天氣夾具 2026-11-11T03:15Z，即預報的 retrieved_at），四個測試在真實日期 11-12 之後仍通過。

## Steps

- [x] 本機用 /opt/pw-browsers/chromium 重現四項失敗。
- [x] 加上固定時鐘後重跑 navigation.spec 與 readability.spec 兩個 project。

## How to verify

`cd apps/web && npx playwright test e2e/navigation.spec.ts e2e/readability.spec.ts`（本機需指定系統 chromium）。

## Notes

本機用 next dev 跑 mobile-chromium 時，navigation.spec 另有三個 30 秒逾時（:10、:945、:1003），拿掉這次修改也一樣，看起來是 dev 伺服器第一次編譯太慢，CI 用 build 版不受影響。夾具有寫死日期的測試都要固定時鐘。

補充：重跑後 planner-browser 另有 planner-calm.spec（三項）與 trip-stay-areas.spec（一項）同樣因為沒固定時鐘失敗，一起在 page.goto 前固定為 2026-11-01T03:00Z，本機兩個 project 10 項全過。其餘引用 2026-11-11 的 spec（planner-route-tones、korea-dual-maps、travel-services、full-stack）在換日後的 CI 都通過，沒有改。
