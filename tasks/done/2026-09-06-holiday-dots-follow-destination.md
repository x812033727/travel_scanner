---
id: 2026-09-06-holiday-dots-follow-destination
title: 日曆的假日圓點應該跟著目的地國家
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T16:13:06Z
created_at: 2026-09-06T14:19:52Z
completed_at: 2026-09-06T16:24:57Z
branch: claude/holiday-dots
depends_on: []
scope:
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/date-range-picker.tsx
  - apps/web/lib/holidays.ts
  - apps/web/components/new-trip-form.test.tsx
---

# 日曆的假日圓點應該跟著目的地國家

## Why

`2026-09-06-public-holidays-tw-jp-kr` 讓 `/trips/new` 的月曆標出假日，但它同時標台日韓三國，
因為那張任務的 scope 只有 `date-range-picker.tsx` 與 `lib/holidays.ts`，碰不到表單。

結果是：去日本的人也會看到韓國的추석圓點。`aria-label` 有寫國名（「日本 憲法紀念日」），
所以資訊不算錯，但一個月裡有四、五顆點時，圓點本身就不再是訊號。
真正有價值的組合是**目的地國家 ＋ 旅客自己的市場**：前者決定新幹線和旅館滿不滿，後者決定他請不請得到假。

`DateRangePicker` 已經留好 `countries?: readonly string[]` prop（預設 `holidayCountries`），
所以這張任務其實是「表單怎麼知道國碼」，不是日曆要改。

## Definition of done

- [x] 目的地是東京時，`/trips/new` 的月曆只標日本與台灣的假日，不標韓國。
- [x] 目的地還沒填或認不出來時，行為與現在一致（三國都標），不會變成一顆點都沒有。
- [x] 沒有新增任何中文字面量在 tsx 裡：國名與假日名一律來自 API 回應。
- [x] `new-trip-form.test.tsx` 有一個案例釘住「選了東京之後不再請求 KR」。

## Steps

- [x] 目的地國碼的來源二選一，在 PR 裡寫下理由：
      (a) `PlacePicker` 的 `onSelect` 目前回的 `Place` 沒有國碼，可請 `GET /places/*` 一起回
      `country_code`（後端已有 `destination_country_code()`）；
      (b) 純前端：拿 `form.destination_name` 比對 `localizeDestinations(t)` 的在地化名稱與 city id。
      (b) 不用動後端但對自由輸入很脆；(a) 比較準但跨了 api/web。
- [x] 旅客自己的市場用 locale 推（zh-TW → TW、ja → JP、ko → KR、en/zh-CN → 無），與目的地國取聯集。
- [x] `<DateRangePicker countries={...} />`；空陣列代表不查，日曆不應該因此壞掉。

## How to verify

```bash
cd apps/web && npx vitest run components/new-trip-form components/date-range-picker
```

瀏覽器：`/zh-TW/trips/new` 選東京，翻到 2026-09，只有 09-21/22/23（日）與 09-28（台）有點，
09-24/25/26（韓）沒有；把目的地清空，三國的點都回來。

## Notes


- 日曆一年查一次（effect key 是可見年份），所以改 `countries` 會重新請求整年，這是預期行為。
- 顯名字串是授權義務，只在「該國真的有假日出現在畫面上」時顯示；縮減國家清單會連帶少一段顯名，
  這是對的，不要改成永遠顯示三段。
- 假日資料本身涵蓋到 2027-12-31，日本 2028 要等 2027 年 2 月才公告，見 `docs/public-holidays.md`。

### 做完之後（2026-09-07，claude-opus-5）

選了 (b)：純前端比對 `localizeDestinations(catalog)` 的在地化名稱與 city id，不動後端。
理由是 scope 只有 web，而且 (a) 要讓 `/places/*` 多回一個欄位，跨了 api/web 兩邊，
為了一顆圓點不值得——真的需要國碼的地方（例如行程建立後）後端本來就有 `destination_country_code()`。

比對規則寫在 `lib/holidays.ts` 的 `holidayCountriesFor()`：輸入至少兩個字才比，
城市名與輸入互為子字串即算命中（「日本東京」對上「東京」），另外也接受 city id（`tokyo`）。
命中就回「目的地國 ＋ 讀者自己的市場」，認不出來就維持三國全標——這是誠實的預設，
表單只知道使用者打了什麼。

讀者市場由 locale 推：zh-TW→TW、ja→JP、ko→KR；en 與 zh-CN 沒有對應的市場，
所以英文與簡中讀者去日本時只會看到日本的假日，不會硬塞一個市場給他們。

測試釘住「打了日本東京之後只請求 JP 與 TW，不再請求 KR」，用的是既有 `stubFetch` 收集到的網址。
