---
id: 2026-09-22-catchtable-one-pass-importer
title: CatchTable 候選檔一次匯入：店家與平台列同一支指令、稽核記 alias
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-22T16:10:00Z
completed_at:
branch:
depends_on:
  - 2026-09-22-catchtable-ranking-discovery-batch-1
scope:
  - apps/api/app/foods/catchtable_import.py
  - apps/api/app/cli.py
  - apps/api/tests/test_catchtable_import.py
  - tools/catchtable_build_batches.py
---

# CatchTable 候選檔一次匯入：店家與平台列同一支指令、稽核記 alias

## Why

第一批（`2026-09-22-catchtable-ranking-discovery-batch-1`）走兩段式：`tools/catchtable_build_batches.py`
把候選檔轉成 trend 匯入格式建店家，套用後再拿 merchant_id 轉平台列。能跑，但每批要進出主機兩次、
稽核來源標成潮流街區的 `trend-merchant-sweep`、CatchTable 的 alias 與名次證據沒有進稽核。
這張票只在第一批證明「還會再跑」時才值得做，所以是 P3 並依賴第一批。

依 2026-09-22 站主原則，這張票**不接 Jev**；理由與重看條件在
`docs/catchtable-ranking-discovery.md` 文末。

## Definition of done

- [ ] `python -m app.cli import-catchtable-candidates --file <candidates.json> [--limit N] [--apply]`：
      讀候選檔（欄位同 `apps/api/app/foods/data/catchtable/README.md`），`import` 記錄一次寫店家
      （pending／inactive／unverified，走 `trend_import` 同一套建列與去重規則）與 `catchtable_global`
      平台列（走 `platform_review_import` 同一套驗證、分店身分鎖與 `skipped_admin_reviewed` 保護）；
      `duplicate` 記錄只寫平台列；稽核記錄帶 alias 與名次證據，來源標 `catchtable-ranking-sweep`。
      永不寫座標、`naver_map_url`、`map_match_status`、`review_status`、`is_active`。
- [ ] dry-run 與 apply 報告同形；一筆一交易，skipped 的理由逐筆印。
- [ ] 候選檔的驗證搬進 pydantic 模型；`tools/catchtable_build_batches.py` 改成只呼叫這個模型，或退役。
- [ ] 測試：每種 outcome、`ko` 網址被拒、平台網域當來源被拒、dry-run／apply 同形、既有店家的平台列保護。

## Steps

- [ ] 先讀 `apps/api/app/foods/trend_import.py`、`platform_review_import.py`、`enrichment_import.py`
      三個 docstring；店家建列抄 `trend_import._create`，平台列抄 `platform_review_import._review_one`。
- [ ] `cli.py` 掛子命令；`ruff`、`mypy app`、`mypy tests`、pytest。
- [ ] 用第一批的候選檔 dry-run 一次，結果要和第一批兩段式的實際寫入一致（同樣的 slug 集合、同樣的
      verified／disabled 數）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_catchtable_import.py -q
uv run python -m app.cli import-catchtable-candidates --file app/foods/data/catchtable/<batch-id>/candidates.json   # dry-run
```

## Notes

- `apps/api/app/cli.py` 也在 `2026-09-12-food-merchant-enrichment` 的 scope 裡；兩張不要同時認領。
- 「菜單連結」沒有欄位，不在這張票；要開欄位是獨立的 schema 票（migration、後台、卡片、五語系）。
- Naver 精準頁若站主決定走「候選檔帶欄位」（設計文件待決事項 2），匯入器只寫 `naver_map_url`、
  `map_match_status` 留 `unverified`，而且要站主明確同意再做；預設不做。
