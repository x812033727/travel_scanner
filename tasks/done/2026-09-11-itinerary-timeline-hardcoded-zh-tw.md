---
id: 2026-09-11-itinerary-timeline-hardcoded-zh-tw
title: 行程時間軸硬編碼繁中而它正是分享頁的主體
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T16:08:20Z
created_at: 2026-09-11T03:20:36Z
completed_at: 2026-09-11T16:19:39Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/itinerary-timeline.tsx
  - apps/web/lib/itinerary-messages
  - apps/web/lib/itinerary-copy.ts
  - apps/web/components/itinerary-timeline.test.tsx
---

# 行程時間軸硬編碼繁中而它正是分享頁的主體

## Why

`itinerary-timeline.tsx` 寫死繁中：餐點與飯店標籤 `:29-33`／交通標頭 `:96,98`／「個安排」`:137`／每個停留點的時間模式 `:155-158`／徽章 `:181,186`／「尚未設定地點」與「待選餐廳」`:192`。

關鍵在於它被誰渲染：`shared-trip-view.tsx:262`。而該檔 `:218-219` 的註解白紙黑字寫著——

> 這是唯一一個全部觀眾都來自擁有者寄出的連結的頁面，它以前不管 `/en`、`/ja`、`/ko` 都用繁體中文迎接他們。

也就是說，上一次的修正落在外層包裝，沒有進到時間軸本體。使用者把行程分享給日本朋友，對方點開連結，頁首是日文，行程內容整片繁中——而行程內容就是他被分享的全部理由。

## Definition of done

- [x] `itinerary-timeline.tsx` 不再有寫死的使用者可見中文。
- [ ] `/en/share/<token>`、`/ja/share/<token>`、`/ko/share/<token>` 從頭到尾沒有中文。

## Steps

- [x] 用既有的 `apps/web/lib/itinerary-messages/` 側 catalog（五語系皆已存在且完整），不要另開 namespace。
- [x] 把上列字串搬進去，透過 `lib/itinerary-copy.ts` 取用。
- [x] 時間格式同樣要依 locale。
- [x] 順手補 `:87-88` 的空狀態（目前回傳一個空的 `<div className="space-y-6">`，沒有項目的行程分享出去只有標題、空白、然後一個 CTA）。

## How to verify

```bash
cd apps/web && npm run test:web -- itinerary-timeline shared-trip-view
```

手動：建一個行程、產生分享連結，用 `/ja/share/<token>` 開啟，內容應為日文。

## Notes

- `lib/itinerary-messages/` 這類側 catalog **不在 `npm run check:i18n` 的檢查範圍內**（`tools/check-i18n.mjs:8` 只讀 `apps/web/messages`），只靠 TypeScript 的 `Record<keyof typeof en, string>` 把關，無法偵測 ICU 參數漂移或重複 key。加字串時要自己核對五語系。

## 瀏覽器實測補充（2026-09-11 第二輪）

用真實瀏覽器對 `en` / `ja` / `ko` 共 12 條路由，搜尋第一輪點名的 27 個寫死繁中字串，**零命中**。

**這不代表本任務的問題不存在，而是那些程式路徑在唯讀環境下走不到**：刪除確認框需要帳號裡有行程（測試帳號 0 筆）、機票與飯店卡需要完成一次搜尋（環境只轉讀取，不送寫入）、行程時間軸需要行程裡有項目。

所以本任務的狀態是**未驗證**，不是**已推翻**。接手的人請自己建一筆有內容的行程再確認，不要因為「掃描沒掃到」就把它關掉。

順帶澄清一個第二輪用過的無效指標：曾以「頁面漢字佔比」推估洩漏程度，但**日文本來就使用漢字**（實測 `ja` 頁面漢字 28–37%，同時有大量假名，是真正的日文），該指標對日文無效，不可採信。英文頁實測漢字僅 0.2–5.2%，且經逐一檢查後確認全部來自語言切換器的語言名稱（繁體中文／简体中文／日本語），屬正確做法。

## 完成紀錄（claude-opus-5, 2026-09-11）

`itinerary-timeline.tsx` 的漢字歸零，字串進 `lib/itinerary-messages/*.json`（依任務指示用既有的側 catalog，沒有另開 namespace）。19 個新 key：餐點與飯店標籤、交通與住宿區塊的標題與說明、「個安排」、三種時間模式、兩個徽章、三種「地點未設定」、空狀態兩句，加上 `flexibleTime`。

空狀態照 Steps 補了：沒有任何項目的行程分享出去，以前是一個空的 `<div>`，收到連結的人看到標題、一片空白、然後一個 CTA。

### `flexibleTime` 為什麼在這裡

`lib/trip-types.ts:402` 的 `formatTime()` 在沒有時間時回傳寫死的「彈性時段」。那個檔在 `2026-09-10-seoul-day2-transport-ux` 的 scope 裡，而且被很多元件共用，所以沒有動它；改成時間軸自己有一個 `time()` 小包裝，沒有值就用 catalog 的 `flexibleTime`。`formatTime` 本身的 fallback 另外開一張任務。

### 驗證

`itinerary-timeline.test.tsx` 加了兩個案例。這裡不必 mock next-intl —— `itineraryCopy(activeLocale())` 讀的就是 `document.documentElement.lang`，所以直接把它設成 `"en"`，用**真的英文 catalog** 渲染，再斷言畫面零漢字。比 stub 更強：連翻譯漏字都會被抓到。

fixture 刻意不放 route，也不放 flight anchor —— `RouteSegmentCard` 與 `FlightAnchorCard` 各自還有自己的中文字串，屬於別張任務，放進來會讓這個斷言在別人的問題上變紅。這件事寫在測試的註解裡。

把三個「地點未設定」還原成寫死之後該案例變紅，復原後 6 passed。

### 沒打勾的那一項

「`/en/share/<token>` 從頭到尾沒有中文」—— **還沒成立，而且不是因為沒驗證**：時間軸自己乾淨了，但它渲染的 `FlightAnchorCard` 與 `RouteSegmentCard` 仍是寫死繁中（「去程航班」「步行 · 18 分鐘」）。有航班或有路線的行程分享出去，畫面上還是會有中文。

已建檔：`2026-09-11-anchor-and-route-cards-hardcoded-zh`（P1）。那張做完之後，把 route 與 flight anchor 放回 `itinerary-timeline.test.tsx` 的跨語系 fixture，這一項才算數。
