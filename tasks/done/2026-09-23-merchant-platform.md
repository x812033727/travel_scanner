---
id: 2026-09-23-merchant-platform
title: 店家來源的較弱層級 merchant_platform：訂位平台頁與店家登記的社群帳號可當來源，公開頁另標
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-23T10:33:10Z
created_at: 2026-09-23T10:30:10Z
completed_at: 2026-09-23T12:13:34Z
branch: claude/merchant-platform-sources
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/migrations/versions/0083_merchant_platform_source.py
  - apps/api/app/foods/admin_router.py
  - apps/api/app/foods/trend_import.py
  - apps/api/tests/test_trend_import.py
  - apps/api/tests/test_catchtable_build_batches.py
  - apps/api/tests/test_migration_0083_merchant_platform_source.py
  - tools/catchtable_build_batches.py
  - apps/api/app/foods/data/catchtable/README.md
  - apps/web/components/food-merchant-card.tsx
  - apps/web/components/food-merchant-card.test.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/messages/zh-TW/foods.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/foods.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/foods.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/foods.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/foods.json
  - apps/web/messages/ko/admin.json
  - docs/catchtable-ranking-discovery.md
  - docs/catalog-review.md
  - .agents/skills/catchtable-discovery
  - .claude/skills/catchtable-discovery
---

# 店家來源的較弱層級 merchant_platform：訂位平台頁與店家登記的社群帳號可當來源，公開頁另標

## Why

CatchTable 榜單反推的兩批共 69 家餐廳裡，29 家（第一批 15、第二批 14）只有訂位平台頁和 Instagram、沒有官網或觀光局頁，
全部停在候選檔的 `no_official_source`，雖然 29 家幾乎都能線上訂位。站主 2026-09-23 問「來源不能用訂位網站或 IG 嗎」，
討論後決定**不把平台頁塞進「官方來源」，而是開一個較弱的來源層級**：店家自己在訂位平台登記的店頁，以及該店頁「網站」欄指向的社群帳號，
在責任鏈成立時可以當店家來源；公開頁另外標示，讓讀者分得出「官方資料」與「平台／社群登記」。

2026-09-12 的邊界（平台、社群只當發現）對 AI 補齊與人工提案仍然有效：`enrichment.py` 的 `_check_source_url` 不放行；
新層級只能從 CatchTable 管線的轉檔腳本（帶責任鏈檢查）與後台表單進來。

## Definition of done

- [x] `food_merchant_sources.source_type` 多一個值 `merchant_platform`（scope 固定 `merchant_listing`）：model 的 CHECK、migration 0083（放寬；縮回時有列就拒絕）、後台 payload 的 Literal 與驗證、`trend_import` 的 `SOURCE_SCOPES`。
- [x] 轉檔腳本 `tools/catchtable_build_batches.py`：`source.kind` 收 `merchant_platform`，但只在 (a) 網址是這個 alias 自己的 CatchTable 店頁或 `/info` 分頁，或 (b) 網址等於候選檔 `catchtable.website`（`/info` 分頁「網站」欄，店家自己登記的）時放行；其他 kind 對平台網域照擋。
- [x] 公開頁：`food-merchant-card` 的來源標籤多 `merchant_platform`，五語系 `foods.json` 有 `sourceTypes.merchant_platform`（zh-TW「平台／社群登記」）；後台來源類型下拉多一個選項，五語系 `admin.json` 有標籤。
- [x] 文件：設計文件的邊界表與「每家店要收的東西」、資料目錄 README 的 `source.kind` 與 `catchtable.website`、`docs/catalog-review.md` 的來源種類、skill 的規則一與代理提示。
- [x] 測試：`trend_import` 收新 kind；轉檔腳本的責任鏈三個案例；卡片標籤；migration 0083 的整合測試（照 0073 的寫法，無 PostgreSQL 時跳過）。
- [x] 部署後 `alembic current` 是 0083；之後另開一批把 29 家 `no_official_source` 依新規則重判（研究代理要記 `/info` 網站欄），這不在本票。

## Steps

- [x] model ＋ migration ＋ migration 測試。
- [x] admin_router、trend_import（含 `test_the_committed_batch…` 的集合斷言改成子集）。
- [x] 轉檔腳本 ＋ 新測試檔。
- [x] 卡片、後台下拉、十個語系檔、卡片測試。
- [x] 文件與 skill。
- [x] `ruff`、`mypy app`、`mypy tests`、`pytest`（相關檔）、`lint:web`、`check:i18n`、`typecheck:web`、`test:web`、`check:tasks`、`test:tools`。
- [x] PR → 合併 → 部署（站主同意）→ `alembic current` 驗證。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trend_import.py tests/test_catchtable_build_batches.py -q
npm run check:i18n && npm run test:web -- food-merchant-card
python tools/catchtable_build_batches.py --candidates <一個含 merchant_platform 記錄的候選檔> --check
```

## Notes

- 責任鏈的意思：店家在 CatchTable 登記店頁（平台會核對商家身分才開放訂位），店頁「網站」欄是店家自己填的，所以「CatchTable 店頁 → 它指向的 IG」是店家自己宣告的連結；
  反過來，IG 搜尋結果、IG 地點頁、任何人貼的連結都不算。
- 公開守門不改：任一 `is_current` 來源就算有來源；一家店只有 `merchant_platform` 來源時，核不核准仍是後台逐家的決定。
- 座標規則不變：平台頁不是耐久座標來源。
- 2026-09-23 實作：公開卡片的來源摘要「N 筆官方佐證」改成中性的「N 筆佐證」（五語系），否則只有平台來源的店會被標成官方。`mypy tests` 在 Windows 本機有一個既有的 `UnixStreamServer` 錯誤，與本票無關；migration 0083 的整合測試在本機無 PostgreSQL 時跳過，靠 CI 跑。
- revision id 上限 32 字元（`alembic_version.version_num` 是 VARCHAR(32)，`tests/test_schema.py` 會擋）：原本的 `0083_merchant_platform_source_type` 34 字元讓 CI 的 api 與 full-stack-smoke 都紅，改成 `0083_merchant_platform_source`。
- 2026-09-23 12:01 UTC 部署 a588cca1，`alembic current` = 0083_merchant_platform_source (head)；29 家 no_official_source 的重判在票 `2026-09-23-catchtable-29-no-official-source-merchant`（PR #688），店家與平台列已套用。
