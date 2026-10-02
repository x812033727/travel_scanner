---
id: 2026-09-22-catchtable-one-pass-importer
title: CatchTable 候選檔一次匯入：店家與平台列同一支指令、稽核記 alias
status: in-progress
priority: P3
area: api
owner: claude-opus-5-5-catchtable-import
claimed_at: 2026-10-02T17:36:29Z
created_at: 2026-09-22T16:10:00Z
completed_at:
branch: claude/catchtable-one-pass-import
depends_on:
  - 2026-09-22-catchtable-ranking-discovery-batch-1
scope:
  - apps/api/app/foods/catchtable_import.py
  - apps/api/app/cli.py
  - apps/api/tests/test_catchtable_import.py
  - tools/catchtable_build_batches.py
  - apps/api/app/foods/platform_review_import.py
  - apps/api/tests/test_catchtable_build_batches.py
  - apps/api/app/foods/data/catchtable/README.md
  - docs/catchtable-ranking-discovery.md
  - .agents/skills/catchtable-discovery/SKILL.md
  - .claude/skills/catchtable-discovery/SKILL.md
  - .agents/skills/catalog-import/references/commands.md
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

- [x] `python -m app.cli import-catchtable-candidates --file <candidates.json> [--limit N] [--apply]`：
      讀候選檔（欄位同 `apps/api/app/foods/data/catchtable/README.md`），`import` 記錄一次寫店家
      （pending／inactive／unverified，走 `trend_import` 同一套建列與去重規則）與 `catchtable_global`
      平台列（走 `platform_review_import` 同一套驗證、分店身分鎖與 `skipped_admin_reviewed` 保護）；
      `duplicate` 記錄只寫平台列；稽核記錄帶 alias 與名次證據，來源標 `catchtable-ranking-sweep`。
      永不寫座標、`naver_map_url`、`map_match_status`、`review_status`、`is_active`。
- [x] dry-run 與 apply 報告同形；一筆一交易，skipped 的理由逐筆印。
- [x] 候選檔的驗證搬進 pydantic 模型；`tools/catchtable_build_batches.py` 改成只呼叫這個模型，或退役。
- [x] 測試：每種 outcome、`ko` 網址被拒、平台網域當來源被拒、dry-run／apply 同形、既有店家的平台列保護。

## Steps

- [x] 先讀 `apps/api/app/foods/trend_import.py`、`platform_review_import.py`、`enrichment_import.py`
      三個 docstring；店家建列抄 `trend_import._create`，平台列抄 `platform_review_import._review_one`。
- [x] `cli.py` 掛子命令；`ruff`、`mypy app`、`mypy tests`、pytest。
- [x] 用第一批的候選檔 dry-run 一次，結果要和第一批兩段式的實際寫入一致（同樣的 slug 集合、同樣的
      verified／disabled 數）。（本機 SQLite，見 Notes；正式站的 dry-run 是部署後站主的事。）

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

### 2026-10-03 claude-opus-5-5-catchtable-import

做了什麼、為什麼：

- 新模組 `apps/api/app/foods/catchtable_import.py`：`CandidateBatch`（pydantic，`extra="forbid"`）是候選檔
  的規則，搬自轉檔腳本並改用 API 端的正本（`is_latin_script`、`CATEGORY_SEEDS_BY_SLUG`、
  `enrichment.is_platform_host` 再加韓國常見的發現網域）。載入時還把整檔丟給 `trend_import.parse_merchants`
  與 `platform_review_import.check_review_batch`，兩支匯入器會拒的東西在開 session 前就整檔拒收、錯誤一次列完。
- 店家建列直接呼叫 `trend_import._create`、去重照 `persist_trend_merchants` 的順序（slug → 同名 →
  商圈 → 分類）；平台列直接呼叫 `platform_review_import._review_one`，所以分店身分鎖、
  `skipped_admin_reviewed`、`skipped_branch_conflict` 是同一份程式，不是抄本。為此 scope 加了
  `platform_review_import.py`：抽出 `check_review_batch`（`load_review_file` 改呼叫它），`_review_one`
  多一個 `audit` 參數併進稽核 metadata。舊行為不變（`test_food_platform_review_import.py` 全綠）。
- 一筆一交易：`--apply` 有寫入才 commit，其餘 rollback；dry-run 走同一條路（新店家先 flush 讓平台列檢查
  看得到它）再 rollback，所以報告同形。逐筆一行印 stderr，JSON 報告在 stdout（`skipped` 逐筆、`rows` 全部）。
- 稽核：新店家 `food_merchant_created`（target `food_merchant:<id>`），平台列沿用
  `food_merchant.cli_platform_link_reviewed`；兩者 `source=catchtable-ranking-sweep`，帶 `alias` 與
  `ranking_evidence`（頁、名次、擷取時間）。名次本來就在平台列的 `review_note` 裡（兩段式也是），稽核只在後台。
- 兩條比 `_review_one` 嚴的規則，都寫在模組 docstring：(1) 已有同狀態、同網址的平台列一律報
  `unchanged`，即使備註不同——第二批對 alice_cheongdam 手動刪列的那個站主條件，現在由程式做；
  (2) 新店家的 CatchTable 店頁已掛在別的店家上（`skipped_branch_conflict`）時整筆不建店家，因為 alias 是唯一
  可靠的身分，那是研究漏掉的重複。
- `--check` 是多加的：本機不開資料庫驗檔（取代腳本的 `--check`）。`--limit` 只算 import／duplicate 筆數。
- 轉檔腳本沒有退役，改成只呼叫模型的兩段式備援（要用 API 的 venv 跑），輸出改成固定 LF；它的舊測試
  `apps/api/tests/test_catchtable_build_batches.py` 刪掉，案例搬進 `test_catchtable_import.py`。
- 不接 Jev；不寫 Naver：候選檔帶 `naver_map_url` 會因 `extra="forbid"` 整檔拒收（有測試）。
- skill `catchtable-discovery`（兩份逐字相同）、`catalog-import/references/commands.md`、資料目錄 README、
  設計文件那段「要改就是這張票」都改成一次匯入為主、兩段式備援；所以 scope 也加了這幾個檔。

驗證：

- 五個已提交的候選檔全部通過新模型，轉出的 `merchants*.json` 與已提交的完全相同，平台列除了
  merchant_id 也完全相同；唯一多出的是第二批首爾的 `seoul-alice-cheongdam`（當時手動刪的那列）。
  轉檔腳本對第一批寫出的兩個檔與已提交的逐位元組相同。
- 第一批 dry-run（SQLite、種好首爾商圈與全部分類、補上 duplicate 指向的 `seoul-buchon-yukhoe`）：
  `would_create` 的店家 slug 集合等於 `merchants.json`，平台列 slug 集合等於 `platform-reviews.json`，
  statuses `verified 12／disabled 3`，與第一批兩段式的實際寫入相同。用 `seed_food_catalog` 的完整種子手動
  跑過一次 dry-run → apply → 再 apply：14 would_create → 14 created → `skipped_existing_slug 14／unchanged 14`。
- 沒有對正式站跑任何東西。部署 API 之後，站主照 skill 先 `--file /dev/stdin` dry-run 再決定。
