---
id: 2026-09-11-format-time-chinese-fallback
title: formatTime 在沒有時間時回傳寫死的繁中
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T16:15:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-types.test.ts
---

# formatTime 在沒有時間時回傳寫死的繁中

## Why

`apps/web/lib/trip-types.ts:402` 的 `formatTime()` 在 `value` 為空時回傳寫死的「彈性時段」：

```ts
export function formatTime(value?: string | null, locale?: string, timeZone?: string) {
  if (!value) return "彈性時段";
```

這個函式被行程編輯器、時間軸、路線卡等多處共用，所以任何沒有時間的安排，在 `/en`、`/ja`、`/ko` 都會出現這四個字。

發現的經過：做 `2026-09-11-itinerary-timeline-hardcoded-zh-tw` 時，時間軸自己包了一層 `time()` 迴避掉，因為 `trip-types.ts` 當時在 `2026-09-10-seoul-day2-transport-ux` 的 scope 裡。迴避只解決了時間軸這一個呼叫點。

## Definition of done

- [ ] `formatTime()` 不再回傳寫死的中文。
- [ ] 所有呼叫點都拿得到自己語系的字。
- [ ] `itinerary-timeline.tsx` 裡那個 `time()` 包裝可以拿掉（它的註解寫明了為什麼存在）。

## Steps

- [ ] 決定介面：多一個 `fallback` 參數，或讓它在沒有值時回傳空字串、由呼叫端決定要顯示什麼。後者比較乾淨，但要逐一檢查現有呼叫點。
- [ ] `grep -rn "formatTime(" apps/web` 把呼叫點列出來，一個一個給字。
- [ ] 拿掉 `itinerary-timeline.tsx` 的 `time()` 包裝與 `itinerary-messages` 的 `flexibleTime`（如果沒有別的地方用）。

## How to verify

```bash
cd apps/web && npm run test:web -- trip-types && npm run check:i18n
```

## Notes

- `lib/itinerary-messages/*.json` 已經有 `flexibleTime`（五語系），可以直接沿用那五句翻譯。
- 這個 fallback 不算高頻——大多數安排都有時間——所以標 P2。
