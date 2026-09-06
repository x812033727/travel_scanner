---
id: 2026-09-06-destination-catalog-labels-i18n
title: 目的地目錄的國家與興趣標籤未五語系化
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:53:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/destinations.ts
---

# 目的地目錄的國家與興趣標籤未五語系化

## Why

`lib/destinations.ts` 是一份資料檔，裡面 165 句繁中：國家名（日本／韓國／泰國…）、
國家說明（「城市、文化與四季自然」）、城市名、`recommendedStay`、`summary`、
`areas`、`tags`，以及 `interests` 的九個標籤（深度旅遊／美食／購物…）。

首頁精靈 2026-09-06 已經五語系化，但**它渲染的選項文字來自這個資料檔**，所以英文使用者
看到的是英文表單配繁中的國家按鈕與興趣標籤。這是精靈翻譯留下的最後一塊。

## Definition of done

- [ ] `/en` 首頁的國家按鈕、興趣標籤、目的地卡片內文都是英文；日／韓／簡中同樣。
- [ ] `CI=1 npm run check:i18n` 通過。
- [ ] `search-workbench.test.tsx` 通過（它用 `/泰國/`、`海灘／跳島` 這類中文名查按鈕，
      改法會影響它）。

## Steps

- [ ] 決定放哪：這是資料不是 UI 文案。兩個選項——
      (a) 把顯示名搬進 `messages/*/destinations.json`，資料檔只留代碼；
      (b) 資料檔改成 `name: { en, ja, ko, "zh-CN", "zh-TW" }` 的多語結構。
      後端 `app/destinations/catalog.py` 也有一份平行資料，決定時要一起看，別讓兩邊分岔。
- [ ] `interestLabel()` 目前直接回傳中文，要改成吃 locale。
- [ ] 更新 `search-workbench.test.tsx` 的查詢字串。

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
