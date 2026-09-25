# Alembic migration：規則與理由

目錄在 `apps/api/migrations/versions/`，`env.py` 載入 `app.models` 與 `app.config.get_settings()`。正式站由 `docker-compose.prod.yml` 的 `migrate` 服務跑 `alembic upgrade head`，api、worker 等服務都等它 `service_completed_successfully` 才起來；它失敗，部署腳本就回滾。

## 為什麼 CI 綠了還會在正式站炸

`0001_initial` 呼叫 `Base.metadata.create_all(bind=op.get_bind())`，用**目前的** models 建出整個 schema。之後每支 migration 在乾淨資料庫上看到的都是「欄位已經在了」，所以：

- `if "x" not in columns:`、`if "t" not in tables:` 底下的 SQL 在 CI 從不執行，第一次執行就是正式站。
- 舊 constraint、舊資料形狀在 CI 根本不存在。

曾經的後果：一支 migration 在 `trip_plans.data`（`json`）上寫了 `data ? 'notes'`，Postgres 在解析階段就拒絕，migrate exit 1，部署腳本自動回滾，站台沒掛但那次部署白做。對策是兩層測試（`references/migration-tests.md`）加上本檔的規則。

## 編號與 id

- 檔名 `NNNN_<snake>.py`，四位數接在目前最高號後面。`tests/test_schema.py` 檢查：只有一個 head、head 是最高號、每個 `revision` 以四位數開頭、head 長度 ≤ 32。它在 CI 裡單獨一步、比 `alembic upgrade head` 早跑，撞號時錯誤訊息會列出兩支檔案。
- **`revision` 字串不等於檔名**的舊檔（`down_revision` 要抄右邊）：

  | 檔名 | `revision` |
  | --- | --- |
  | `0009_usage_account_status_default` | `0009_usage_account_status` |
  | `0019_hotspot_destination_identity` | `0019_hotspot_destination_id` |
  | `0028_restaurant_source_workflows` | `0028_restaurant_sources` |
  | `0031_trip_item_coordinate_provenance` | `0031_trip_item_coordinates` |
  | `0033_social_login_identities` | `0033_social_login` |
  | `0041_ai_itinerary_refine_cost` | `0041_ai_itinerary_refine` |
  | `0062_food_merchant_platform_links` | `0062_merchant_platform_links` |

  超過 32 字元的 id 寫進 `alembic_version` 會失敗，所以長檔名的 id 要縮短；新檔盡量讓兩者一致。
- 用檔名去接 `down_revision` 會得到兩個 head，`app.schema.expected_schema_revision()` 對**每一個** import app 的測試模組 raise，不只 schema 測試紅。
- 平行 session 撞號是常態（一個下午 rebase 三次、從 0040 改到 0042 發生過）。改號時一起改：檔名、docstring 的 `Revision ID:` 與 `Revises:`、`revision`、`down_revision`、測試檔裡的 `MIGRATION = "..."` 常數與 `load_migration("...")` 呼叫。不要改別人已經在 main 上的那支。
- 不用 `alembic revision` 的 mako 樣板（`script.py.mako` 的型別寫法與現行檔案不同），抄最新一支的開頭。

## json 與 jsonb

models 用 `mapped_column(JSON)` 的欄位，Postgres 建出來是 `json`。能用：`->`、`->>`、`json_*` 函式、`(data -> 'preferences' ->> 'budget_twd')::numeric` 這類轉型、`data ->> 'key' IS NOT NULL` 當「有這個鍵」。不能用：`?`、`?|`、`?&`、`@>`、`<@`、`||`、`-`、`jsonb_set(col, ...)`，除非先 `::jsonb`。`tests/test_migration_sql_dialect.py` 從 models 找出所有 `JSON` 欄位、把 migration 當文字掃，看到這些運算子沒轉型就紅；它是便宜的守門，不能取代整合測試。

## 離線模式與測試的 monkeypatch

兩種寫法都在 repo 裡，理由不同：

- **新檔（0083 起）**：`def _offline() -> bool: return bool(op.get_context().as_sql)`。不需要 alembic 的 EnvironmentContext proxy，測試用裸 `MigrationContext` + `Operations.context` 驅動也能回答。
- **舊檔（約 47 支）**：`from alembic import context` 後呼叫 `context.is_offline_mode()`。這個 proxy 只在 env.py 驅動時存在，裸 `MigrationContext` 下呼叫會 `NameError: ... proxy object has not yet been established`。所以它們的測試用 `monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)`（十幾個測試檔），而 `tests/test_migration_dead_branches.py` 有 autouse 的 `never_offline` fixture 一次蓋住整個檔案。
- 因此：舊檔別為了「現代化」拿掉 `from alembic import context`，那會讓 monkeypatch 那一側紅。新檔別用 `is_offline_mode()`，否則每個新測試都要再 patch 一次。
- 不開 Postgres 就能驗：建 SQLite 的 `MigrationContext`，進 `Operations.context`，呼叫那個 helper。

## 其他寫法規則

- 定義 `@dataclass` 的 migration **不能** `from __future__ import annotations`：測試用 `importlib.util.spec_from_file_location` 載入、沒登記進 `sys.modules`，dataclasses 解析字串註解時拿到 `None` 而失敗（`0047_ai_vendor_settings.py` 是有 dataclass 的例子）。沒有 dataclass 的檔案不受影響。
- 回填用 Core 陳述，別 import ORM model（model 會隨之後的 migration 改變）：`provider_configs = sa.table("provider_configs", sa.column("id", sa.Uuid()), sa.column("config", sa.JSON()), ...)`，`json` 欄位經 `sa.JSON()` 綁參數。
- migration 可以 `from app.config import get_settings`（env.py 已經這樣做）。要搬 `provider_configs` 的加密欄位時，金鑰是 `sha256(settings_encryption_key or app_secret_key)` 包成 Fernet，照 `0047_ai_vendor_settings.py` 的做法，不要自己發明。
- 欄位用函式每次新建（`sa.Column` 只能屬於一張表），「不在才加」；離線模式下無條件產生 DDL。
- 改 CHECK constraint：放寬很安全；縮窄（包括 downgrade）前先查有沒有會違反新條件的列，有就明確 raise 說明，不要默默改資料（`0073_catalog_run_enrich_mode` 的 downgrade 在還有新模式的列時拒絕）。
- 應用程式回滾不會降資料庫，`/ready` 用 `schema_is_current()` 比對 `alembic_version` 與程式的 head，不符回 503。所以 migration 要向下相容：先加、後用、再刪，刪欄位放在另一次發布。真的要退回舊程式，先 `alembic downgrade <前一個 revision>` 再部署舊版，這要站主同意。

## 回填與資料修補

- 程式內建的回填是 `python -m app.cli` 的子指令，`python -m app.cli --help` 列全部。有 `--dry-run` 的先跑 dry-run，看筆數。
- 規矩：回填只補空白，不覆蓋管理員設過或清過的值（例如食物目錄用 `area_source='admin'` 與既有分類連結擋住）；加城市到既有資料時確認指令是「補齊」而不是「只在沒有時建立」。
- 用手寫 SQL 驗回填時，在真資料庫上包在 `BEGIN; … ROLLBACK;` 裡，把 `.sql` 檔複製上主機再用 `psql -f` 跑，不要把引號塞進一行 `psql -c`。正式站的寫入、帶 jsonb 運算子的查詢，auto 模式的分類器會擋，要站主同意或自己跑；連線方式與限制見 skill `deploy`。
- 需要部署後跑的指令寫進 PR 描述與票的 Notes，不要只留在對話裡。

## 部署後

1. `alembic current` 等於新 head（指令在 skill `deploy` 的驗證段）。
2. 內部 `/ready` 200。
3. 有回填的：跑 CLI（先 dry-run），再用一句簡單的唯讀 `select count(*)` 對筆數。
4. 部署腳本只在 incoming commit 動到 migrations 時先做 `pg_dump`；migrate 失敗會自動回滾程式，Postgres 的 DDL 在交易裡，資料庫停在舊 revision。
