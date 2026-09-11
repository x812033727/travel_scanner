---
id: 2026-09-11-format-time-chinese-fallback
title: formatTime 在沒有時間時回傳寫死的繁中
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T21:26:26Z
created_at: 2026-09-11T16:15:01Z
completed_at: 2026-09-11T21:43:10Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-types.test.ts
  - apps/web/components/itinerary-timeline.tsx
  - apps/web/components/itinerary-timeline.test.tsx
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

- [x] `formatTime()` 不再回傳寫死的中文。
- [x] 所有呼叫點都拿得到自己語系的字。
- [x] `itinerary-timeline.tsx` 裡那個 `time()` 包裝的迴避部分拿掉了（綁 `timezone` 的那層留著）。

## Steps

- [x] 決定介面。→ **兩個選項都沒採用**，改成在 `formatTime` 內部讀 catalog，理由見完成紀錄。
- [x] 列出呼叫點。→ 十幾處，散在六個檔案；因為介面沒變，一個都不必改。
- [x] 拿掉 `time()` 包裝的迴避部分。`flexibleTime` 保留——現在是 `formatTime` 在用它。

## How to verify

```bash
cd apps/web && npm run test:web -- trip-types && npm run check:i18n
```

## Notes

- `lib/itinerary-messages/*.json` 已經有 `flexibleTime`（五語系），可以直接沿用那五句翻譯。
- 這個 fallback 不算高頻——大多數安排都有時間——所以標 P2。

## 完成紀錄（claude-opus-5, 2026-09-11）

`formatTime()` 沒有值時改成讀 `itineraryCopy(reader).flexibleTime`——`lib/itinerary-messages/`
已經有這句話的五個語系版本，而且會顯示它的那幾個畫面（時間軸、編輯器、當日檢視、列印）本來
就在讀同一份 catalog。

**介面沒有改**，Steps 裡列的兩個選項（多一個 `fallback` 參數、或回傳空字串由呼叫端決定）
都沒有採用。理由是：這個函式有十幾個呼叫點，散在六個檔案裡，其中好幾個不在這張任務的 scope；
而兩個選項都會強迫每一個呼叫點做決定，等於把一個一行的修正變成六個檔案的改動。而
`formatTime` 本來就已經在呼叫 `activeLocale()` 決定 `Intl` 的語系——讓 fallback 用同一個
語系，是把既有的行為補齊，不是加新的概念。

順帶把 `locale || activeLocale()` 抽成一個 `reader` 變數，fallback 與 `Intl.DateTimeFormat`
共用，免得哪天兩邊各自算出不同的語系。

`itinerary-timeline.tsx` 的 `time()` 包裝拿掉了迴避的部分（註解也一起刪，它描述的情況已經
不存在），只留下綁 `timezone` 的那層。`itinerary-messages` 的 `flexibleTime` 保留——現在是
`formatTime` 在用它。

### 驗證

`lib/trip-types.test.ts` 新增一條，五個語系各斷言一次。把 fallback 改回寫死的字串後，
**兩條**測試轉紅：新的那條，以及 `itinerary-timeline.test.tsx` 的跨語系漢字斷言——後者是
因為拿掉包裝之後，時間軸真的會走到 `formatTime` 的 fallback。這個耦合是對的：以後有人把
`formatTime` 改回寫死的字串，時間軸那條會先叫。
