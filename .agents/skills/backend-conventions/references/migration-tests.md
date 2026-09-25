# Migration 的測試

CI 的 api job 依序跑：`tests/test_schema.py`（單一 head）→ 兩個專門的 migration 驗證（`RUN_MIGRATION_TESTS=1`）→ `alembic upgrade head` → 整個測試套件（`RUN_INTEGRATION_TESTS=1`，有 Postgres、Redis、MinIO）。本機沒設這兩個環境變數時，需要 Postgres 的測試會 skip，看起來全綠但什麼都沒驗；PR 裡要寫明哪些只在 CI 跑過。

## 三層，各擋一種錯

| 層 | 檔案 | 擋什麼 | 要不要 Postgres |
| --- | --- | --- | --- |
| 樹的形狀 | `tests/test_schema.py` | 兩個 head、head 不是最高號、id 沒有四位數開頭、head 超過 32 字元 | 不用 |
| SQL 方言 | `tests/test_migration_sql_dialect.py` | 對 `json` 欄位用 jsonb-only 運算子（從 models 自動找欄位） | 不用 |
| 真的執行 | `tests/test_migration_NNNN_<name>.py`、`tests/test_migration_dead_branches.py`、`tests/test_<domain>_migration.py` | 回填算錯、舊 constraint 下的 SQL、downgrade 還原不了 | `RUN_INTEGRATION_TESTS=1` |

## 什麼時候要寫第三層

- 任何 `if ... not in columns／tables` 分支裡，除了建空欄位、空表之外還會執行 SQL 的（回填、搬資料、改值）。
- 改 CHECK constraint、搬狀態值、搬加密設定。
- 規則寫在 `tests/test_migration_dead_branches.py` 的開頭：還原舊形狀（`DROP COLUMN`／`DROP TABLE`／換回舊 constraint），種一列該改的、一列不該動的、一列在邊界上的。

只加一個 nullable 欄位、沒有回填的，不用寫。

## 單檔測試的骨架（照 `test_migration_0088_news_needs_redraft_status.py` 或 `test_migration_0073_catalog_run_mode.py` 抄）

1. `pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")`。
2. 模組級 autouse fixture `dispose_engine_after_module`（`engine.dispose(close=False)` → yield → `engine.dispose()`），避免跨 event loop 共用連線。
3. `load_migration()`：`importlib.util.spec_from_file_location(f"migration_{MIGRATION}", VERSIONS / f"{MIGRATION}.py")`，`MIGRATION` 是**檔名**（不是 revision id）。
4. `run(connection, "upgrade"|"downgrade")`：`MigrationContext.configure(connection)`，`with Operations.context(context): getattr(load_migration(), direction)()`。這就是 migrate 容器會發出的 SQL，只是不寫 `alembic_version`。
5. `in_a_rolled_back_transaction(exercise)`：`connection.begin()`，跑完一律 `rollback()`，共用的測試資料庫保持原樣。
6. `_exercise(connection)`：用 DDL 還原舊形狀 → 用 `Session(bind=connection)` 種 ORM 列 → `upgrade` → 斷言 → 再 `upgrade` 一次證明冪等 → `downgrade` → 斷言還原。
7. 測試本體：`@pytest.mark.asyncio(loop_scope="module")`，`async with engine.connect() as connection: await connection.run_sync(in_a_rolled_back_transaction(_exercise))`。

測試檔自己可以用 `from __future__ import annotations`；限制只在 migration 檔（有 dataclass 時）。

## 被測的 migration 用舊的離線判斷時

migration 呼叫 `context.is_offline_mode()` 的，裸 `MigrationContext` 下會 `NameError`。在測試裡 `monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)`；`test_migration_dead_branches.py` 已有 autouse 的 `never_offline`，放進那個檔案的案例自動涵蓋。新 migration 用 `op.get_context().as_sql` 就不需要 patch。

## `RUN_MIGRATION_TESTS`

`tests/test_admin_operations_migration.py`（從 0066 的種子資料升上來）與 `tests/test_usage_migration.py` 需要能建資料庫的權限，用 `RUN_MIGRATION_TESTS=1` 開；CI 在 `alembic upgrade head` 之前單獨跑前者與 `tests/test_site_pages_migration.py`。一般新 migration 不需要加到這一層。

## 本機跑

```bash
cd apps/api
uv run pytest tests/test_schema.py tests/test_migration_sql_dialect.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0088_news_needs_redraft_status.py -q
```

第二行需要 `DATABASE_URL` 指到一個已經 `alembic upgrade head` 的 Postgres。本機環境怎麼起（venv、Windows 上的已知失敗）走 skill `dev-and-ci`。整合測試要新使用者時直接建列並簽 token；`tests/conftest.py` 已把註冊的每 IP 上限調高給測試用，但別再增加經 `/auth/register` 的呼叫。
