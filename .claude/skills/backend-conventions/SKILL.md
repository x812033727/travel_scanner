---
name: backend-conventions
description: travel_scanner 後端與後台的既有慣例：apps/api/migrations 的 Alembic migration（接在目前 head 後面編號、down_revision 鏈、revision id 不一定等於檔名且上限 32 字元、json 欄位不是 jsonb、平行 session 撞號、離線旗標與測試 monkeypatch 的慣例、每支 migration 的整合測試、回填指令與部署後檢查），在呼叫端 session 上順手寫一筆的 helper 規則（不 begin_nested、不 autoflush），以及新增後台頁面或設定（四處導覽登記、設定歸屬、API 權限與 step-up、/admin/settings 的供應商分類）。要寫或改 migration、重新編號、寫回填、寫分析或計數類 helper、加後台頁、加供應商或設定欄位時，先讀這個 skill。部署本身走 deploy，本機環境與 CI 走 dev-and-ci，主機操作走 prod-host-ops，前端翻譯與 e2e 走 web-i18n-e2e，看板走 task-board，文章走 content-pipeline。Conventions for Alembic migrations, caller-session helpers and new admin pages or settings in travel_scanner.
metadata:
  short-description: Migration、session helper、後台頁與設定的慣例
---

# 後端與後台慣例（backend-conventions）

> 本文提到的 `references/…`、`scripts/…` 都在 `.agents/skills/backend-conventions/` 底下；`.claude/skills/backend-conventions/` 只放這份 SKILL.md 的逐字複本。

這個 skill 只放規則、指令與去哪裡讀；每條規則背後的事故與機制在 `references/`。程式裡已經寫下的理由（docstring、測試檔開頭的說明）是正本，這裡只指過去。

## 不變的規矩

1. **migration 的 SQL 在 CI 的「乾淨資料庫」上多半沒跑過。** `0001_initial` 用 `Base.metadata.create_all` 從**目前的** models 建表，所以 `if "x" not in columns:` 之類的回填分支在 CI 一律跳過，第一次執行就是正式站。每一個會動資料的分支都要有自己的整合測試（`references/migration-tests.md`）。
2. **`data` 這類 `JSON` 欄位在 Postgres 是 `json`，不是 `jsonb`。** `?`、`?|`、`?&`、`@>`、`<@`、`||`、`-`、`jsonb_set(...)` 在 `json` 上解析就失敗，空表也一樣；曾讓 migrate 容器 exit 1、整個部署自動回滾。用 `data ->> 'key' IS NOT NULL`、`->`、`->>` 與明確的 `::jsonb` 轉型。
3. **`revision` 字串才是 id，檔名不是。** 有七支舊檔兩者不同（例如 `0041_ai_itinerary_refine_cost.py` 的 id 是 `0041_ai_itinerary_refine`）。`down_revision` 一律照上一支檔案裡的 `revision` 抄；id 最長 32 字元（`alembic_version.version_num` 是 `VARCHAR(32)`）。
4. **編號會撞。** 別的 session 隨時合進 main；rebase 後 `alembic heads` 出現兩個，就把**自己的**那支改號：檔名、docstring 的 `Revision ID:`／`Revises:`、`revision`、`down_revision` 一起改，引用它的測試常數（`MIGRATION = "..."`）也要改。`tests/test_schema.py` 不寫死 head，不用動。
5. **新的 migration 用 `op.get_context().as_sql` 判斷離線模式**（0083 起的慣例），不要呼叫 `context.is_offline_mode()`。舊檔裡已經用 `context.is_offline_mode()` 的，**不要順手改掉 `from alembic import context`**：它的測試靠 `monkeypatch.setattr(module.context, "is_offline_mode", ...)`。
6. **定義 dataclass 的 migration 不能 `from __future__ import annotations`**：測試用 `spec_from_file_location` 載入、沒登記進 `sys.modules`，dataclasses 解析字串註解時會炸。
7. **在呼叫端 `AsyncSession` 上寫東西的 helper**（分析事件、每日計數、標記）：不 `begin_nested()`、所有查詢與 insert 包在 `session.no_autoflush` 裡，insert 用 ORM entity 形式；測試斷言 `session.new`，不是發出的 SQL（`references/session-helpers.md`）。
8. **後台頁要在四處登記**，只加前端 fallback 在正式站會是 forbidden（`references/admin-pages.md`）。每個後台 API 都自己用 `require_capability(...)` 檢查；破壞性操作再加 `require_admin_step_up(...)`。
9. **應用程式回滾不會降資料庫。** migration 要能讓上一版程式繼續跑（只加欄位、先不刪），否則回滾後 `/ready` 因 head 不符回 503。

## 主幹：寫一支 migration

| # | 做什麼 | 關卡 |
| --- | --- | --- |
| 1 | `git fetch origin` 後在 `apps/api` 跑 `uv run alembic heads`，拿到目前 head 的 `revision` 字串 | 只有一個 head |
| 2 | 抄最新一支（例如 `0093_video_project_dropped.py`）的樣子，不要用 `alembic revision` 產的 mako 樣板：檔名 `NNNN_<snake>.py`、`revision` ≤ 32 字元、`down_revision` = 上一步的字串、docstring 寫 `Revision ID:`／`Revises:` 與為什麼 | `uv run pytest tests/test_schema.py -q` 綠 |
| 3 | `upgrade()`：「欄位不在才加」＋ `_offline()` 分支；回填用 Core（`sa.table(..., sa.column(...))`）寫；`downgrade()` 反向 | 沒有 jsonb-only 運算子（`tests/test_migration_sql_dialect.py` 會擋） |
| 4 | 模型同步改（`apps/api/app/models.py` 或各模組的 `models.py`），新 CHECK constraint 兩邊同名 | `uv run mypy app` |
| 5 | 會動既有資料、改 constraint 或回填的，寫 `tests/test_migration_NNNN_<name>.py`（或在 `test_migration_dead_branches.py` 加一例） | 本機有 Postgres 就 `RUN_INTEGRATION_TESTS=1` 跑；沒有就明講「只在 CI 跑」 |
| 6 | 要跑 CLI 回填的，在 PR 與票寫清楚部署後要跑哪一行、先 `--dry-run` | 見下方指令 |
| 7 | rebase 到最新 main 再推；撞號照規矩 4 改號 | CI 的 `tests/test_schema.py` 步驟綠 |
| 8 | 部署後：`alembic current` 等於新 head、`/ready` 200、回填筆數對得上 | 部署與驗證走 skill `deploy` |

## 指令

```bash
cd apps/api
uv run alembic heads                      # 不需要資料庫；應該只有一行
uv run pytest tests/test_schema.py tests/test_migration_sql_dialect.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0088_news_needs_redraft_status.py -q   # 需要本機 Postgres
uv run ruff check . && uv run mypy app && uv run mypy tests
# 回填 CLI（在正式站 api 容器裡、部署之後；先 dry-run）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli backfill-trip-item-names --dry-run
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli seed-foods
```

`python -m app.cli --help` 列出全部子指令；回填類的有 `seed-foods`、`backfill-trip-item-names`、`backfill-merchant-english-names`、`fill-simplified-names`、`fill-food-merchant-coordinates`、`match-food-merchant-places` 等，各自的旗標以 `--help` 為準。主機上的連線與分類器限制在 skill `deploy`。

## 主幹：加一個後台頁或設定

1. API：在 `apps/api/app/admin/operations_service.py` 的 `NAVIGATION_REGISTRY` 加一列（id、group、href、label_key、capability、可選 badge_key；有 badge 的還要在同檔 `_live_pending_counts` 算數），並在 `apps/api/tests/test_admin_operations.py` 加一條斷言。
2. Web：`apps/web/lib/admin-operations.ts` 的 `fallbackAdminNavigation`（id 是 snake_case 的話在同檔 `aliases` 加對照）、`apps/web/components/admin-nav.tsx` 的圖示、五語 `apps/web/messages/<locale>/admin.json` 的 `navigation.<key>`，頁面放 `apps/web/app/[locale]/admin/<slug>/page.tsx`。
3. e2e：`apps/web/e2e/admin-operations-full-stack.spec.ts` 的 `OWNER_NAVIGATION` 與 `ROLE_NAVIGATION`（對真 API）；若也要進隔離 fixture，`tools/e2e-runtime-api.mjs` 的 `adminNavigation` 與 `apps/web/e2e/admin-operations.spec.ts` 的 `ADMIN_PAGES`／`ROLE_NAVIGATION` 一起改。
4. 頁內分頁與篩選狀態走 URL：`apps/web/lib/admin-workspace-navigation.ts` 的 `useAdminWorkspaceNavigation`、`useAdminQueryValue`、`adminNavigate`。
5. 設定欄位：先決定歸屬（`apps/web/lib/admin-settings-ownership.ts`），新供應商要在 `apps/web/components/admin-settings-panel.tsx` 的 `providerCategoryOf` 登記，否則掉進「其他」。

## 去哪裡讀

| 問題 | 讀 |
| --- | --- |
| 編號、id、json、離線旗標、加密設定搬家、回填、部署後 | `.agents/skills/backend-conventions/references/migrations.md` |
| 每支 migration 的整合測試長什麼樣、dead branches、SQL 方言守門、`RUN_MIGRATION_TESTS` | `.agents/skills/backend-conventions/references/migration-tests.md` |
| 在呼叫端 session 上寫東西的 helper：機制與測法 | `.agents/skills/backend-conventions/references/session-helpers.md` |
| 後台頁四處登記、設定歸屬、API 權限與 step-up、供應商分類、前端 lint 的坑 | `.agents/skills/backend-conventions/references/admin-pages.md` |
| 角色與能力表（機器核對）、step-up、資料庫中心邊界 | `docs/admin-operations-center.md` |
| 領域工作區、設定單一擁有者、API 隔離 | `docs/admin-domains.md` |
| 新增搜尋供應商的 adapter | `README.md` 的「Adding a provider」 |
| 部署、`alembic current`、回滾 | skill `deploy` |

`.claude/skills/backend-conventions/SKILL.md` 是這一份的逐字複本（references 只放在 `.agents/` 這邊），`npm run test:tools` 會比對。
