---
id: 2026-09-11-flight-status-checked-at-utc
title: 航班動態的查詢時間把 UTC 當成地方時顯示
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T20:22:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/flight-anchor-card.tsx
  - apps/web/components/flight-anchor-card.test.tsx
---

# 航班動態的查詢時間把 UTC 當成地方時顯示

## Why

`flight-anchor-card.tsx` 的 `localDateTime()` 用正規表示式從 ISO 字串取出年月日時分，
**丟掉時區位移**。這對 `flight_info.departure_local` 是對的——那本來就是機場當地的牆上時間，
沒有位移可言，丟進 `Date` 反而會被讀者瀏覽器的時區平移。

但同一個函式也被拿來顯示 `flight_status.checked_at`，而那個值是 UTC：
`apps/api/app/trips/router.py:5835` 寫的是 `datetime.now(UTC).isoformat()`，
`apps/api/app/trips/flight_anchor.py:86` 則是 `checked_at.isoformat()`（值來自 `lookup.updated_at`）。
結果台灣的讀者看到的「查詢時間」比實際晚八小時，日本韓國晚九小時。

值得修的原因：這行的用途就是讓人判斷「這份動態是多久以前查的」。差八小時的話，
一份三十分鐘前的動態看起來像是昨天半夜的，反而讓人不敢相信它。

## Definition of done

- [ ] 帶時區的時間戳（`checked_at`）依讀者所在時區顯示。
- [ ] 不帶時區的牆上時間（`departure_local` / `arrival_local`）維持現在的行為，不被平移。
- [ ] 有測試同時蓋住這兩種輸入。

## Steps

- [ ] 把兩種情況分開：字串結尾有 `Z` 或 `±HH:MM` 的走 `Date` + `Intl.DateTimeFormat`，
      沒有的走現在的逐欄取值。
- [ ] 測試固定 `TZ`（vitest 可用 `process.env.TZ`）才不會隨執行機器變動。

## How to verify

```bash
cd apps/web && npm run test:web -- flight-anchor
```

## Notes

- 在 `2026-09-11-anchor-and-route-cards-hardcoded-zh` 修 i18n 時順手看到的，當時沒改，
  因為那張任務是語系不是時區。
- `localDateTime` 為什麼刻意不走 `Date`，函式上的註解有寫，改的時候別把那個理由弄丟。
