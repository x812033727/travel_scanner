---
id: 2026-09-06-backfill-merchant-english-names
title: 已匯入的店家沒有拿到資料檔後來補上的英文名
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T21:18:47Z
created_at: 2026-09-06T21:18:21Z
completed_at: 2026-09-06T21:44:36Z
branch: claude/merchant-name-backfill
depends_on: []
scope:
  - apps/api/app/foods/trend_import.py
  - apps/api/app/cli.py
  - apps/api/tests/test_trend_import.py
---

# 已匯入的店家沒有拿到資料檔後來補上的英文名

## Why

`2026-09-06-merchant-names-chinese-in-other-locales`（PR #285）替
`data/trend_merchants.json` 補了 28 個 `name_en`，讓匯入時不再把中文名寫進
`FoodMerchant.name`。但那張票只修了**匯入路徑**。

`trend_import` 對已經看過的 slug 是「一律跳過、絕不合併」——這是檔頭第 27 行寫明的規則，
而且對一個會被重新掃描的來源來說是對的規則。代價是：改資料檔對**已經在資料庫裡的列毫無作用**，
而那些正是讀者現在看到的列。

正式站量到的：121 筆的 `name` 含漢字，其中 **28 筆已發布**。PR #285 之後這 28 筆一個字都沒變。

## Definition of done

- [x] 有一個可重跑的方式，把資料檔後來補上的 `name_en` 套用到既有的列。
- [x] 後台改過名字的列不會被蓋掉。
- [x] 跑第二次不會再改任何東西，而且報告要說得出「已經是英文名」與「被改名」的差別。
- [x] 正式站跑過，已發布的店家 `name` 含漢字的是 0 筆。

## Steps

- [x] `plan_english_name_backfill(rows, merchants)` 純函式：決定哪些要改、哪些不動。
      抽成純函式是為了能在沒有 PostgreSQL 的機器上測——整合測試需要 `RUN_INTEGRATION_TESTS=1`。
- [x] `backfill_english_names(apply=False)` 包住 session；`names_json` 要**重新指派**不能就地改，
      JSON 欄位只有在指派時才會被視為 dirty。
- [x] CLI `backfill-merchant-english-names`，預設 dry-run。
- [x] 部署後在正式站跑 dry-run；不需要 `--apply`，理由見下。

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli backfill-merchant-english-names
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli backfill-merchant-english-names --apply
```

```bash
curl -s -H 'X-Travel-Locale: en' 'https://mokaair.com/api/travel/foods/merchants?destination_id=bangkok&limit=50'
```

## Notes

- 這張票是 PR #285 之後才看得出來的缺口：兩個 session 同時做同一張票，我的版本被丟掉，
  但那個版本裡有回填、他們的沒有。整理時只留下不重複的這一半。
- 招牌本來就是漢字的 11 家不會被這個指令改，因為它們在資料檔裡就沒有 `name_en`。

## Result（2026-09-07）

指令做完並部署了，但**它在正式站找不到事做**：28 筆全部回報 `already the English name`，
已發布的店家 `name` 含漢字的是 0 筆。也就是說在我這邊做完之前，另一個 session 已經用別的方式
把資料套上去了。

所以這張票的成果不是「修好了什麼」，是兩件別的東西：

1. **一個可重跑的工具**。資料檔之後還會補英文名（見
   [[2026-09-06-trend-merchant-english-names-backlog]] 說還有 95 家），而匯入路徑對既有列
   永遠是跳過。下次補完直接跑這個指令就好，不用再想一次怎麼安全地改既有資料。
2. **一次乾淨的量測**。dry-run 的輸出本身就是證據：28 筆對得上、0 筆要改、0 筆被後台改過名。

順帶查到一件要回頭補的事：那 28 個 `name_en` 裡有 15 個在該列自己的資料裡找不到，是手寫音譯，
而原票明文寫「不要自己音譯」。已另開 [[2026-09-06-merchant-english-names-unsourced]]，
裡面列了 15 筆與各自的風險等級。這是發現方式的副產品——dry-run 把每個目標名稱都印出來，
所以資料檔裡沒有的字串一眼就看得到。
