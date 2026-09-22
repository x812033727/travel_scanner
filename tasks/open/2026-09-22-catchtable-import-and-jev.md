---
id: 2026-09-22-catchtable-import-and-jev
title: CatchTable 候選匯入指令與 Jev 判斷：去重、分類、商圈、本店確認
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-22T15:26:39Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/catchtable_import.py
  - apps/api/app/foods/catchtable_jev.py
  - apps/api/app/cli.py
  - apps/api/tests/test_catchtable_import.py
  - apps/api/tests/test_catchtable_jev.py
  - docs/catchtable-ranking-discovery.md
---

# CatchTable 候選匯入指令與 Jev 判斷：去重、分類、商圈、本店確認

## Why

第一批（`2026-09-22-catchtable-ranking-discovery-batch-1`）走兩段式：候選檔轉成 trend 匯入格式
建店家，套用後再拿 merchant_id 轉平台列。能跑，但每批要進出主機兩次、稽核來源標成潮流街區的
`trend-merchant-sweep`、CatchTable 的 alias 與名次證據沒有進稽核。同時，去重（這家是不是目錄裡
那家）、分類、商圈、官方頁是否指本店，四件事現在全靠人一筆一筆看；README 明寫這正是 Jev
（`apps/api/app/ai/jev.py`）該做的分類工作，而它目前只接在 hotspot 導覽搜尋的影子模式。

設計在 `docs/catchtable-ranking-discovery.md`；四題的 state、門檻與影子量測在
`.agents/skills/catchtable-discovery/references/jev-questions.md`。

## Definition of done

- [ ] `python -m app.cli import-catchtable-candidates --file <candidates.json> [--apply]`：讀候選檔，
      `import` 記錄一次寫店家（pending／inactive／unverified，走 `trend_import` 同一套建列與去重規則）
      與 `catchtable_global` 平台列（走 `platform_review_import` 同一套驗證、分店身分鎖與
      `skipped_admin_reviewed` 保護）；`duplicate` 記錄只寫平台列；稽核記錄帶 alias 與名次證據，
      來源標 `catchtable-ranking-sweep`。永不寫座標、`naver_map_url`、`map_match_status`、
      `review_status`、`is_active`。dry-run 與 apply 報告同形。
- [ ] `python -m app.cli catchtable-jev-report --file <candidates.json> [--worklist …]`：問四題
      （同店 noul、分類 choice、商圈 choice、本店 noul），用 `route_answer` 分 tier，與候選檔裡人的
      判定並排，印每題的 agreement（整體與分語言）與不一致清單；什麼都不寫；過 `consume_jev_call`
      預算；`JevRequestTooLarge` 對半切；Jev 沒設定就明說並退出。
- [ ] 測試：候選檔驗證（每種 outcome、`ko` 網址被拒、平台網域當來源被拒）、匯入的 dry-run／apply
      同形、既有店家的平台列保護、Jev 報告用假 transport（照 `apps/api/tests/test_jev_client.py`）。
- [ ] 設計文件補一節「已落地的指令」與第一次影子量測的數字。

## Steps

- [ ] 先讀 `apps/api/app/foods/trend_import.py`、`platform_review_import.py`、`enrichment_import.py`
      三個 docstring，決定候選檔的 pydantic 模型放哪裡（建議 `catchtable_import.py`，與 skill 的
      `build_batches.py` 同一套欄位，腳本之後改成只呼叫這個模型或直接退役）。
- [ ] 匯入器：一筆一交易；店家建列抄 `trend_import._create`，平台列抄
      `platform_review_import._review_one`；skipped 的理由逐筆印。
- [ ] `catchtable_jev.py`：state 組法與問題名照 `references/jev-questions.md`；分類 criteria 用
      `category_catalog.py` 的英文名；商圈 criteria 用該城市 `area_catalog.py` 的韓文與英文名。
- [ ] 報告指令：照 `apps/api/app/hotspots/guide_shadow_cli.py` 的 agreement 算法，分題、分語言。
- [ ] `cli.py` 掛兩個子命令；`ruff`、`mypy app`、`mypy tests`、pytest。
- [ ] 用第一批的候選檔跑一次影子報告，把數字與不一致的例子寫進設計文件。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_catchtable_import.py tests/test_catchtable_jev.py -q
uv run python -m app.cli import-catchtable-candidates --file app/foods/data/catchtable/<batch-id>/candidates.json   # dry-run
uv run python -m app.cli catchtable-jev-report --file app/foods/data/catchtable/<batch-id>/candidates.json
```

## Notes

- `apps/api/app/cli.py` 也在 `2026-09-12-food-merchant-enrichment` 的 scope 裡；兩張不要同時認領。
- Jev 現況：`JEV_CJK_AUTOPILOT_ENABLED=false`，非英文 state 的 act 一律降 confirm；門檻
  `jev_act_confidence` 0.9、`jev_flag_confidence` 0.5 是全站設定，不另開一套。分類與商圈是低風險欄位，
  agreement 夠才值得為它們開自動駕駛；同店與本店維持 confirm。
- 不問名次、價格、營業時間、日期（TypeSafe 公布的弱點）。
- 「菜單連結」沒有欄位，不在這張票；要開欄位是獨立的 schema 票（migration、後台、卡片、五語系）。
- Naver 精準頁若站主決定走「候選檔帶欄位」（設計文件待決事項 2），匯入器只寫 `naver_map_url`、
  `map_match_status` 留 `unverified`，而且要站主明確同意再做；預設不做。
