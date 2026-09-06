---
id: 2026-09-06-destination-catalog-labels-i18n
title: 目的地目錄的國家與興趣標籤未五語系化
status: done
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T05:16:58Z
created_at: 2026-09-06T00:53:22Z
completed_at: 2026-09-06T05:51:32Z
branch: claude/web-p2-ux
depends_on: []
scope:
  - apps/web/lib/destinations.ts
  - apps/api/app/destinations/localized.py
  - apps/api/app/places/router.py
  - apps/api/tests/test_destinations_localized.py
  - apps/web/app/[locale]/page.tsx
  - apps/web/components/search-workbench.tsx
  - apps/web/components/search-experience.tsx
  - apps/web/components/search-criteria-editor.tsx
  - apps/web/components/search-criteria-editor.test.tsx
  - apps/web/components/new-trip-form.tsx
  - apps/web/lib/currency.test.ts
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 目的地目錄的國家與興趣標籤未五語系化

## Why

`lib/destinations.ts` 是一份資料檔，裡面 165 句繁中：國家名（日本／韓國／泰國…）、
國家說明（「城市、文化與四季自然」）、城市名、`recommendedStay`、`summary`、
`areas`、`tags`，以及 `interests` 的九個標籤（深度旅遊／美食／購物…）。

首頁精靈 2026-09-06 已經五語系化，但**它渲染的選項文字來自這個資料檔**，所以英文使用者
看到的是英文表單配繁中的國家按鈕與興趣標籤。這是精靈翻譯留下的最後一塊。

## Definition of done

- [x] `/en` 首頁的國家按鈕、興趣標籤、目的地卡片內文都是英文；日／韓／簡中同樣。
- [x] `CI=1 npm run check:i18n` 通過。
- [x] `search-workbench.test.tsx` 通過（它用 `/泰國/`、`海灘／跳島` 這類中文名查按鈕，
      改法會影響它）。

## Steps

- [x] 決定放哪：這是資料不是 UI 文案。兩個選項——
      (a) 把顯示名搬進 `messages/*/destinations.json`，資料檔只留代碼；
      (b) 資料檔改成 `name: { en, ja, ko, "zh-CN", "zh-TW" }` 的多語結構。
      後端 `app/destinations/catalog.py` 也有一份平行資料，決定時要一起看，別讓兩邊分岔。
- [x] `interestLabel()` 目前直接回傳中文，要改成吃 locale。
- [x] 更新 `search-workbench.test.tsx` 的查詢字串。

## How to verify

```bash
cd apps/web && npx vitest run components/search-workbench.test.tsx lib/currency.test.ts
cd ../.. && CI=1 node tools/check-i18n.mjs
```

`lib/currency.test.ts` 有一則測試斷言「每個上架目的地的幣別都在會員可選清單裡」，
它會讀 `destinations.ts`，改資料結構時會一起紅，是好事。

## Notes

**動態目錄會覆蓋靜態資料**：`search-workbench.tsx` 的 `dynamicCities` 從
`GET /destinations` 取回後會蓋掉 `destinations.ts` 的清單（只有 API 掛掉時才 fallback）。
所以**後端 `app/destinations/catalog.py` 才是實際來源**，只翻前端資料檔的話，
正式站上看到的仍是後端回傳的繁中。這個任務要嘛連後端一起處理，要嘛只當作 fallback 的翻譯
—— 接手時先確認清楚，不然會白做。

（scope 目前只寫前端檔案，如果決定要動後端，請把 `apps/api/app/destinations/catalog.py`
加進 scope 再開始，避免和別人的 api 任務撞。）

**`SECONDARY_TAG`**：`search-workbench.tsx` 有一個 `const SECONDARY_TAG = "二線城市"` 的
哨兵值，用來把動態城市分到「二線城市」optgroup。改資料結構時這個比對要一起改，
不然分組會全空。

2026-09-06 claude-fable-5-1：兩邊一起做，因為 Notes 說得對，後端才是實際來源。

- **後端**：新增 `app/destinations/localized.py`，33 個目的地的城市名與一句 reason、7 個國家標籤
  各四個語系（zh-TW 就是 catalog 本身的文字，不重複）。`GET /destinations` 與 `POST /destinations/discover`
  接 `CurrentLocale`（BFF 已經把 `travel_locale` cookie 轉成 `X-Travel-Locale` 送過來），回傳的
  `city`／`country`／`reason` 依語系；`local_name`／`english_name`／`areas` 不動（是地名與搜尋詞）。
  `validate_localized_catalog()` 由 `tests/test_destinations_localized.py` 跑，少一個語系就紅。
- **前端**：選 (a)。`lib/destinations.ts` 只剩代碼與數字（`destinationSeeds`：id、機場、
  `recommendedDays: {min,max}`、areas、tag 代碼），顯示文字進 `search.json` 的 `catalog`
  （`countries.*.name/caption`、`cities.*.name/summary`、`interests.*`、`recommendedStay`），由
  `localizeDestinations(t)`／`destinationByAirport(code, t)`／`interestLabel(code, t)` 在渲染時取。
  `SECONDARY_TAG = "二線城市"` 改成 `SECONDARY_CITY_TAG = "secondary"`，動態城市的 tag 跟著改。
  首頁、精靈、搜尋結果頁標頭、條件編輯器的興趣按鈕、新行程表單都改吃代碼。
- zh-TW 的值與原字面完全相同，`search-workbench.test.tsx` 不必改；`currency.test.ts` 改讀
  `destinationSeeds`；`search-criteria-editor.test.tsx` 多傳一個 translator。
- 驗證（production build）：`/en/search?...` 標頭「Thailand · Phuket full trip / Beaches, island
  hopping, resorts and nightlife · Local time zone Asia/Bangkok · Suggested stay 5–7 days」，
  `/ko` 同樣是韓文；`/en` 首頁 `main` 內無任何漢字。
- 沒做的：`areas`（76 個地名）與精靈推薦卡裡 API 回的 `areas`／`assumptions` 仍是繁中，
  是地名與估算說明，另案處理；搜尋頁其餘殘留（條件編輯器、Airbnb 面板）在
  `2026-09-06-leftover-chinese-copy-on-the-search`。
