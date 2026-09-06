---
id: 2026-09-06-backfill-merchant-english-names
title: 已匯入的店家沒有拿到資料檔後來補上的英文名
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T21:18:47Z
created_at: 2026-09-06T21:18:21Z
completed_at:
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
- [ ] 正式站跑過，`X-Travel-Locale: en` 讀回來的 28 筆只剩招牌本來就是漢字的那些。

## Steps

- [x] `plan_english_name_backfill(rows, merchants)` 純函式：決定哪些要改、哪些不動。
      抽成純函式是為了能在沒有 PostgreSQL 的機器上測——整合測試需要 `RUN_INTEGRATION_TESTS=1`。
- [x] `backfill_english_names(apply=False)` 包住 session；`names_json` 要**重新指派**不能就地改，
      JSON 欄位只有在指派時才會被視為 dirty。
- [x] CLI `backfill-merchant-english-names`，預設 dry-run。
- [ ] 部署後在正式站跑一次 dry-run 看清單，再 `--apply`。

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
