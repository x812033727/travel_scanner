---
id: 2026-09-11-anchor-and-route-cards-hardcoded-zh
title: 航班錨點卡與路線卡仍是硬編碼繁中
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T20:16:20Z
created_at: 2026-09-11T16:15:03Z
completed_at: 2026-09-11T20:23:10Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/flight-anchor-card.tsx
  - apps/web/components/route-segment-card.tsx
  - apps/web/lib/itinerary-messages
  - apps/web/components/itinerary-timeline.test.tsx
---

# 航班錨點卡與路線卡仍是硬編碼繁中

## Why

行程時間軸本體已經在 `2026-09-11-itinerary-timeline-hardcoded-zh-tw` 清乾淨了，但它渲染的兩張子卡沒有：

- `flight-anchor-card.tsx`：「去程航班」「回程航班尚未設定」等。
- `route-segment-card.tsx`：「步行 · 18 分鐘」這類交通摘要。

和時間軸同一個問題、同一個後果：行程分享給日本或韓國朋友，頁首是他的語言，行程內容混著中文。時間軸的新測試（`itinerary-timeline.test.tsx` 的「the timeline in a language that is not Chinese」）刻意不放 route 與 flight anchor，就是因為這兩張卡會讓那個斷言在別人的問題上變紅——修完這張之後，那個 fixture 應該補回去。

## Definition of done

- [x] 兩個檔案都沒有寫死的使用者可見中文。
- [x] `itinerary-timeline.test.tsx` 的跨語系案例把 flight anchor 放回 fixture，仍然零漢字。
      route segment **不能**放回去，理由見完成紀錄——不是元件的問題，是測試環境的問題。

## Steps

- [x] 用既有的 `lib/itinerary-messages/` 側 catalog，透過 `itineraryCopy(activeLocale())` 取用——和時間軸一致。
- [x] 時間格式同樣依 locale。
- [x] 更新 `itinerary-timeline.test.tsx` 的 fixture 與註解。

## How to verify

```bash
cd apps/web && npm run test:web -- itinerary && npm run check:i18n
```

## Notes

- 做法可以照抄 `itinerary-timeline.tsx` 這次的 commit：`itineraryCopy` + `itineraryText`，加上一個 `document.documentElement.lang = "en"` 的跨語系測試。
- `route-segment-card.tsx` 在 `2026-09-10-seoul-day2-transport-ux` 的 scope 裡（該任務已 stale 且工作已併入 main），claim 前先確認一下。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

`route-segment-card.tsx` 在 `2026-09-10-seoul-day2-transport-ux`（codex-seoul-day2-release）
的 scope 裡。那張 claim 於 09-10 06:16，距今已超過 24 小時（協定上已 stale），遠端分支
`codex/seoul-day2-transport-ux` 已不存在，工作也已合併進 main——最後一次動到那個檔的 commit
`5f34f77 fix: restore Seoul transit queries and readable travel details` 就在 `origin/main` 上。
只是那張任務沒標 `done`。

## 完成紀錄（claude-opus-5, 2026-09-11）

### `route-segment-card.tsx`：撤回，這半張不成立

實際掃過整個檔，**沒有任何寫死的使用者可見中文**。任務描述舉的例子「步行 · 18 分鐘」實際上是
`{t(modeMeta.key)} · {t("durationMinutes", { minutes })}`，走的是 `useTranslations("trips.route")`，
本來就照讀者的語言出。整個檔的字串都是這樣。

建檔時我是從時間軸的跨語系測試「加上 route 就變紅」推論它有硬編碼——推錯了。變紅的原因是
`vitest.setup.tsx:57-62` 把 `next-intl` 整個 mock 成 zh-TW（一個 module 層級的 `translators`
Map，永遠回 `messages/zh-TW/*.json`）。也就是說：**任何走 next-intl 的元件，在測試裡都必然吐
繁中**，不管它在瀏覽器裡多正確。那個漢字斷言只能覆蓋走 `activeLocale()` 側 catalog 的元件。

所以 route segment 不能放回那個 fixture，而這不是缺陷、也不需要修——是測試環境的限制。要驗
它的多語系行為，得另外做（例如在 e2e 裡切語系實測），不該靠這條斷言。

掃描方式：對兩個檔逐行找 `[㐀-䶿一-鿿]+`。`route-segment-card.tsx` 零筆；
`flight-anchor-card.tsx` 十三筆（第 26、53、56、57、69、70、87、101、102、113 行）。

### `flight-anchor-card.tsx`：成立，已修

十四個 key 進 `lib/itinerary-messages/` 五個語系（`flightOutbound`、`flightReturn`、
`flightFixedTime`、`flightOutsideCityRoute`、`flightTimePending`、`flightTimezonePending`、
`flightNonstop`、`flightConnections`、`flightOutboundUnset`、`flightReturnUnset`、
`flightAnchorHint`、`flightEdit`、`flightSetOutbound`、`flightSetReturn`）。

字串拼接的兩處（原本是 `${label}` 加「尚未設定」、「設定」加 `${label}`）改成去／回程各一個
完整句子，而不是把 key 接起來——中文接得起來，日文韓文接不起來。

`localDateTime` 原本手寫 `M/D HH:MM`。改成把日期交給 `Intl.DateTimeFormat(locale, …)`，
時鐘的數字原樣保留：錨點存的是機場當地的牆上時間，丟進 `Date` 會被讀者瀏覽器的時區平移，
台北的 08:40 在別人螢幕上就變成別的時刻。

檔裡原有的 `useTranslations("trips")` 幾處（`quotedPrice`、`flightStatusLine`、
`searchFlights`、`statusSearch`）沒動——它們本來就是多語系的，而且在時間軸裡根本不會渲染
（時間軸只給 `item`，不給 `search`／`flightStatus`／`onEdit`，也沒有報價與動態快照），
所以錨點可以乾淨地進入那個零漢字的 fixture。

### 驗證

`itinerary-timeline.test.tsx` 的跨語系案例加了兩張錨點卡：一張填好的（JAL JL802，直飛）
與一張未設定的，涵蓋兩個分支。把 `label` 改回寫死的字串後這條會紅（實測 `expected '去程航班'
to be undefined`），復原後綠。`lint:web`、`typecheck:web`、`check:i18n`（含 staged 的漢字
ratchet）都過。

### 順手發現，另開任務

`flight-anchor-card.tsx` 顯示 `flight_status.checked_at` 時走同一個 `localDateTime`，
但那個值是 `datetime.now(UTC).isoformat()`（`apps/api/app/trips/router.py:5835`）——正規表示式
把時區位移丟掉，直接把 UTC 的數字當地方時顯示，台灣的讀者會看到晚八小時的「查詢時間」。
這是既有行為，我沒有在這張任務裡改，另開 `2026-09-11-flight-status-checked-at-utc`。
