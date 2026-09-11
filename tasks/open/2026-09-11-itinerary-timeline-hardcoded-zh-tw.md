---
id: 2026-09-11-itinerary-timeline-hardcoded-zh-tw
title: 行程時間軸硬編碼繁中而它正是分享頁的主體
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:36Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/itinerary-timeline.tsx
  - apps/web/lib/itinerary-messages
  - apps/web/lib/itinerary-copy.ts
---

# 行程時間軸硬編碼繁中而它正是分享頁的主體

## Why

`itinerary-timeline.tsx` 寫死繁中：餐點與飯店標籤 `:29-33`／交通標頭 `:96,98`／「個安排」`:137`／每個停留點的時間模式 `:155-158`／徽章 `:181,186`／「尚未設定地點」與「待選餐廳」`:192`。

關鍵在於它被誰渲染：`shared-trip-view.tsx:262`。而該檔 `:218-219` 的註解白紙黑字寫著——

> 這是唯一一個全部觀眾都來自擁有者寄出的連結的頁面，它以前不管 `/en`、`/ja`、`/ko` 都用繁體中文迎接他們。

也就是說，上一次的修正落在外層包裝，沒有進到時間軸本體。使用者把行程分享給日本朋友，對方點開連結，頁首是日文，行程內容整片繁中——而行程內容就是他被分享的全部理由。

## Definition of done

- [ ] `itinerary-timeline.tsx` 不再有寫死的使用者可見中文。
- [ ] `/en/share/<token>`、`/ja/share/<token>`、`/ko/share/<token>` 從頭到尾沒有中文。

## Steps

- [ ] 用既有的 `apps/web/lib/itinerary-messages/` 側 catalog（五語系皆已存在且完整），不要另開 namespace。
- [ ] 把上列字串搬進去，透過 `lib/itinerary-copy.ts` 取用。
- [ ] 時間格式同樣要依 locale。
- [ ] 順手補 `:87-88` 的空狀態（目前回傳一個空的 `<div className="space-y-6">`，沒有項目的行程分享出去只有標題、空白、然後一個 CTA）。

## How to verify

```bash
cd apps/web && npm run test:web -- itinerary-timeline shared-trip-view
```

手動：建一個行程、產生分享連結，用 `/ja/share/<token>` 開啟，內容應為日文。

## Notes

- `lib/itinerary-messages/` 這類側 catalog **不在 `npm run check:i18n` 的檢查範圍內**（`tools/check-i18n.mjs:8` 只讀 `apps/web/messages`），只靠 TypeScript 的 `Record<keyof typeof en, string>` 把關，無法偵測 ICU 參數漂移或重複 key。加字串時要自己核對五語系。
