---
id: 2026-09-11-offline-day-view-needs-an-app
title: 當日檢視要真的離線可用，需要預先快取 app shell
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T22:18:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/public/sw.js
  - apps/web/components/offline-trip-cache.tsx
  - apps/web/components/offline-trip-cache.test.tsx
---

# 當日檢視要真的離線可用，需要預先快取 app shell

## Why

`public/sw.js` 的註解說「the day the traveller last opened is still readable」，
`app/[locale]/trips/[id]/page.tsx` 的註解說當日檢視是「readable without a signal」。
在真的 Chromium 裡量過之後，這兩句話**只在分頁沒有被關掉的前提下成立**。

worker 只快取一樣東西：`/api/travel/trips/{id}` 的回應。**document 沒有快取，JavaScript
沒有快取。** 所以真的沒有訊號時，瀏覽器連頁面都載不到——`page.reload()` 直接
`net::ERR_INTERNET_DISCONNECTED`，快取裡有什麼完全無關。

實際會發生的情況：旅客站在月台上打開當日檢視，把手機收進口袋，走進地鐵。再拿出來時，
分頁很可能已經被系統回收了。他看到的是瀏覽器的離線頁，不是今天的行程——而這正是這個功能
存在的理由。

完整的量測過程（包含 Playwright 的兩個限制）寫在
`tasks/done/2026-09-11-offline-today-e2e.md`。

## 要先決定的事

**這是不是想做的功能？** 預先快取 app shell 是一個真的 PWA，不是一個小修補：

- 要快取 document 殼、Next 的 JS chunk、CSS。chunk 的檔名每次 build 都會變，所以需要
  build 時產生的資產清單，或是一個 stale-while-revalidate 的策略。
- 快取版本要跟著部署失效，否則使用者會被鎖在舊版前端。
- 爆炸半徑會從「一個 URL 形狀」變成「整個站」。現在的 worker 刻意寫得極小，就是為了
  「這裡有 bug 也只會影響一個 URL」——那份保證會消失。

**或者換個方向**：不做 app shell，改成把註解與文案講清楚——當日檢視是「開著就不怕斷線」，
不是「離線可開」。這個選擇便宜很多，而且誠實。

## Definition of done

- [ ] 站主決定方向：做 app shell，或改成如實描述現有能力。
- [ ] 若做 app shell：沒有訊號時冷開 `?view=today` 仍看得到今天的安排，且部署後不會卡舊版。
- [ ] 若不做：`sw.js` 與 `trips/[id]/page.tsx` 的註解、以及任何對使用者說「離線可看」的文案，
      都改成分頁開著時才成立。

## Notes

- 現有保護：`components/offline-trip-cache.test.tsx` 釘住「worker 回報 ready 之後才抓行程」。
  快取確實會被寫入，這一點沒有問題。
- Playwright 1.62 沒辦法測這件事：`page.route` / `context.route` 攔不到 worker 的 fetch，
  `context.setOffline(true)` 也到不了 worker。要驗證得用獨立的 Node + Chromium 腳本，
  或改用其他工具。
