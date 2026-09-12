---
id: 2026-09-12-food-merchant-enrichment
title: 反向用美食定位平台補齊待審店家資料（Gemini 補齊模式與瀏覽器批次匯入）
status: in-progress
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T06:14:34Z
created_at: 2026-09-12T06:14:22Z
completed_at:
branch: claude/food-merchant-enrichment
depends_on: []
scope:
  - apps/api/app/catalog_review/schemas.py
  - apps/api/app/catalog_review/errors.py
  - apps/api/app/catalog_review/service.py
  - apps/api/app/catalog_review/jobs.py
  - apps/api/app/catalog_review/repository.py
  - apps/api/app/catalog_review/provider.py
  - apps/api/app/catalog_review/router.py
  - apps/api/app/catalog_review/enrichment.py
  - apps/api/app/catalog_review/enrich_cli.py
  - apps/api/app/foods/enrichment.py
  - apps/api/app/foods/enrichment_import.py
  - apps/api/app/foods/place_matching.py
  - apps/api/app/foods/data/enrichment
  - apps/api/app/foods/data/platform_reviews/2026-09-12-pending-merchants.json
  - apps/api/app/cli.py
  - apps/api/app/models.py
  - apps/api/app/i18n.py
  - apps/api/migrations/versions/0073_catalog_run_enrich_mode.py
  - apps/api/tests/test_catalog_review.py
  - apps/api/tests/test_catalog_review_provider.py
  - apps/api/tests/test_catalog_review_jobs.py
  - apps/api/tests/test_catalog_review_scope.py
  - apps/api/tests/test_catalog_review_integration.py
  - apps/api/tests/test_catalog_review_enrichment.py
  - apps/api/tests/test_catalog_review_enrich_cli.py
  - apps/api/tests/test_food_enrichment.py
  - apps/api/tests/test_food_enrichment_import.py
  - apps/api/tests/test_food_place_matching.py
  - apps/api/tests/test_migration_0073_catalog_run_mode.py
  - apps/web/components/admin-catalog-review-panel.tsx
  - apps/web/components/admin-catalog-review-panel.test.tsx
  - apps/web/messages/en/catalogReview.json
  - apps/web/messages/ja/catalogReview.json
  - apps/web/messages/ko/catalogReview.json
  - apps/web/messages/zh-CN/catalogReview.json
  - apps/web/messages/zh-TW/catalogReview.json
  - apps/web/e2e/admin-domains.spec.ts
  - docs/catalog-review.md
  - docs/catalog-content-reviews/2026-09-12-pending-merchant-enrichment.md
---

# 反向用美食定位平台補齊待審店家資料（Gemini 補齊模式與瀏覽器批次匯入）

## Why

正式站 163 筆待審店家卡在同一組缺口：沒有 Google Place ID、沒有地址、沒有店家官網或觀光局的直接來源、
沒有商圈與分類。2026-09-12 使用者決定「反向透過美食定位平台補資料」，邊界維持不變：Google／Naver／米其林
與食べログ、OpenRice 等平台只當定位與發現用，寫進資料庫的地址、來源、商圈、分類仍要有官網或觀光局頁佐證；
AI 與批次永遠不寫座標、地圖身分、審核狀態。既有 `catalog_review` 只會顯示 corrections 從不套用，也沒有
「找官網」的搜尋；沒有共用的寫入函式，也沒有補資料的 JSON 匯入指令。

## Definition of done

- [x] `apps/api/app/foods/enrichment.py`：共用寫入函式，只填空欄位、來源以網址 upsert、分類只增、Place ID 只在空且無主時寫，永不碰座標／地圖／審核狀態，一家店一筆 `food_merchant_enriched` 稽核。
- [x] catalog_review 新模式 `enrich_merchants`（scope 限 foods）：identify（Google Place ID）→ 每批 5 家 2 次 Gemini（有根據搜尋＋結構化）；候選頁由伺服器抓取並以店名／地點比對；`apply_corrections` 套用。
- [x] 匯入指令 `apply-food-merchant-enrichment` 與工作清單匯出 `export-food-merchant-worklist`，資料檔在 `apps/api/app/foods/data/enrichment/`。
- [x] 後台 `/admin/foods` → 審核 → AI 有第三張「補齊店家資料」卡、corrections 列表與套用動作，五語系齊。
- [ ] 待審店家經瀏覽器研究批次補齊（先 30 家試點），正式站前後計數記錄在 `docs/catalog-content-reviews/2026-09-12-pending-merchant-enrichment.md`；核准／拒絕數不變，沒有任何列的座標或地圖狀態被批次改動。

## Steps

- [x] A：models `ck_catalog_run_mode` 放寬、migration 0073、`foods/enrichment.py`、`place_matching` 多 actor／origin／run_id／should_continue。
- [x] B：catalog_review schemas／enrichment 純函式／provider `enrich_search`＋`enrich_assess`／service／jobs／enrich_cli。
- [x] C：`foods/enrichment_import.py`、cli 子命令、測試。
- [x] D：後台面板與五語系。
- [ ] E：部署後匯出工作清單、瀏覽器研究、dry-run、套用、報告。

## How to verify

- `cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest`（`RUN_INTEGRATION_TESTS=1` 跑 integration 與 0073 測試）。
- `npm run lint:web && npm run typecheck:web && npm run test:web`；提交後 `CI=1 npm run check:i18n`；`npm run check:tasks`。
- 部署後 `python -m app.cli enrich-food-merchants --actor-email <admin> --dry-run`，再小跑 `--destination tokyo --limit 5 --max-calls 6`。
- 正式站唯讀 psql 前後比對：待審數、`address IS NULL`、`area_id IS NULL`、`official_website_url IS NULL`、非 KR 無 Place ID、
  缺直接店家來源數、無分類數必須下降；有座標數與 `map_match_status<>'unverified'` 的待審數必須不變；核准／拒絕維持 273／3。

## Notes

- 交付切成 PR 1（後端＋CLI）、PR 2（後台 UI＋五語系，base PR 1）、PR 3+（研究資料，每個分片一個 PR）。
- 全量一次跑約 66 次 Gemini（最壞 99），每 run 上限 `catalog_review_max_calls` 預設 80，要先在後台調到 120 或用 `--destination` 分目的地跑。
- 座標這次不碰：補上官網／觀光局頁後走 `fill-food-merchant-coordinates`、政府開放資料、Wikidata；座標佇列的人不可把 Google 候選當耐久（見 `2026-09-08-prevent-google-coordinates-being-labelled-durable`）。
- KR 列的 `naver_map_url` 仍卡在 `2026-09-06-naver-maps-key`；內建瀏覽器拒開 map.naver.com，資料檔記 `not_possible_in_pane`。
- 2026-09-12 實作紀錄（claude-fable-5-1）：A–D 在同一分支 `claude/food-merchant-enrichment` 完成。
  - 共用寫入函式 `apply_merchant_enrichment` 先驗證再寫（不用 `begin_nested`、讀取走 `no_autoflush`，遵守 `app/analytics/service.py:record_event` 的規則），拒絕時什麼都不留。
  - Gemini 路每批 5 家 2 次呼叫（有根據搜尋＋結構化），網址歸屬由伺服器以店名／地點比對決定；`identify` 階段用既有 `match_merchant_places` 只寫 Place ID。
  - 新錯誤碼 `catalog_enrichment_nothing_pending`、`catalog_source_untrusted` 已加五語系（`apps/api/app/i18n.py`）。
  - 資料檔骨架 `apps/api/app/foods/data/enrichment/2026-09-12-pending-merchants.json`（`records: []`），研究批次另開 PR。
  - E（部署後研究批次）尚未開始；需先合併部署 PR 1，再匯出工作清單。
