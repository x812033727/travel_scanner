---
id: 2026-09-07-ui-text-overrides-api
title: 後台可改前台文案：API、資料表、快取與稽核
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-07T00:34:15Z
created_at: 2026-09-07T00:32:52Z
completed_at: 2026-09-07T00:53:42Z
branch: claude/ui-text-overrides-api
depends_on: []
scope:
  - apps/api/app/ui_text
  - apps/api/app/models.py
  - apps/api/app/config.py
  - apps/api/app/i18n.py
  - apps/api/app/main.py
  - apps/api/app/admin/service.py
  - apps/api/migrations/versions/0053_ui_text_overrides.py
  - apps/api/tests/test_ui_text.py
  - apps/api/tests/test_ui_text_integration.py
  - docs/ui-text-overrides.md
  - .env.example
---

# 後台可改前台文案：API、資料表、快取與稽核

## Why

前台所有文字都在 `apps/web/messages/<locale>/<namespace>.json`（22 個 namespace × 5 語系、
3,254 個 key），由 `apps/web/i18n/request.ts` 用 `import()` 打包進 bundle，所以今天改一個字
就要重新 build 部署。營運者要能在後台直接改文案。

做法是把 JSON 留作版本控管的預設值，資料庫只存「覆寫」，前台渲染時疊上去。這張任務是三張
中的第一張（→ `2026-09-07-ui-text-loader` 前台載入器 → `2026-09-07-ui-text-admin-editor`
後台編輯器），只做 API 端：資料表、公開讀取端點與 Redis 快取、後台寫入端點、稽核。合併後
前台行為完全不變（沒有覆寫時 `entries` 為空），所以可以先上。

## Definition of done

- [x] `GET /api/v1/runtime/ui-text?locale=` 匿名可讀、`no-store`，回 `{locale, version, entries}`；
      `entries` 是平面的 `"<namespace>.<key>": text`
- [x] 後台 `GET / PUT / DELETE /api/v1/admin/ui-text…` 與 `POST …/batch`，每次寫入回該
      (locale, namespace) 刷新後的 snapshot
- [x] 存檔時驗證：不 trim、只擋純空白；CRLF→LF、其他控制字元拒絕；大括號要平衡；
      `{參數}` 集合要與 `default_value` 相同；`legacy` 鎖定、未知 namespace 拒絕
- [x] 每次寫入 commit 後清掉五個語系的 Redis 快取 `ui-text:overrides:<locale>`
- [x] 稽核 `ui_text_updated` / `ui_text_reset` 進 `admin_audit_logs`，並出現在設定頁活動清單
- [x] 九個新錯誤碼在 en / ja / ko / zh-CN 的 `ERROR_DETAILS` 都有句子
- [x] migration `0053_ui_text_overrides` idempotent、單一 head、無 JSON 欄位

## Steps

- [x] migration `0053_ui_text_overrides.py`（照 0050 的 `_offline()` / `_tables()` 守衛）
- [x] `models.py` 加 `UiTextOverride`：`UNIQUE(namespace, key, locale)`、locale CHECK、
      `namespace <> 'legacy'` CHECK、`length(value) > 0` CHECK、`ix_ui_text_overrides_locale`
- [x] `config.py` 加 `ui_text_cache_ttl_seconds`（預設 300）；`.env.example` 列出
- [x] `i18n.py` 九碼 × 四語系（zh-TW 走 `AppError.detail`，該字典本來就不對齊，沿用）
- [x] 新套件 `app/ui_text/{schemas,service,router}.py`；`main.py` 掛 `runtime_router` 與
      `admin_router`
- [x] `admin/service.py` 的 `action.in_([...])` 加兩個 action
- [x] `tests/test_ui_text.py`（FakeSession + fakeredis）、`tests/test_ui_text_integration.py`
- [x] `docs/ui-text-overrides.md`

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_ui_text.py \
  tests/test_schema.py tests/test_error_localization.py tests/test_migration_sql_dialect.py
# 有 PostgreSQL / Redis 時
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_ui_text_integration.py
# 部署後
curl -s 'https://mokaair.com/api/travel/runtime/ui-text?locale=zh-TW'   # {"locale":..,"version":..,"entries":{}}
```

## Notes

給下一張任務（載入器、編輯器）的合約與決定：

- **合約**：`PUT /admin/ui-text/{locale}/{namespace}/{key}` body `{value, default_value}`；
  `POST /admin/ui-text/batch` body `{locale, namespace, entries:[{key, value|null, default_value}]}`
  限單一 namespace、≤100 筆、全部驗過才寫、一次 commit；`value: null` = 還原預設且**不驗參數**
  （孤兒清理才不會被擋）；有 `value` 沒 `default_value` → `ui_text_default_required`。
  回傳 `UiTextSnapshot`：`entries[].updated_by_email` 可為 null、`namespace_counts` 是該語系
  每個 namespace 的覆寫數、`version` 是該語系**全部**覆寫的內容雜湊（與公開端點一致）。
- **為什麼送 `default_value` 而不是參數清單**：API 沒有 JSON catalog；送文字兩邊各一條 regex
  就夠，而且直接存成 `default_snapshot`，編輯器拿它跟現在的預設比就能顯示「預設改過了」。
- **驗證是 UX 不是安全**：載入器要對「現在的」預設再比一次參數，UI 送錯 `default_value`
  也不會讓正式環境出現 `FORMATTING_ERROR`。
- **絕對不能 trim**：47 個預設值前後空白有意義（`", "`、`" · Return {times}"`）。
- **`en` 有 7 個 ICU plural**，參數 regex 抓得到 `count`，但少一個 `}` 只有大括號檢查抓得到。
- **快取**：這是 repo 第一個「後台寫入時清快取」的地方。讀 Redis 失敗直接落 DB、寫失敗只記
  log；清除用一道 `DELETE` 五個 key，不會算錯語系。前台端不另做 TTL 快取（下一張任務）。
- **測試手法**：service 的四個 `_` 開頭查詢函式是唯一碰資料庫的地方，單元測試用 monkeypatch
  換成操作 `FakeSession.rows` 的 closure，其餘邏輯（驗證、快取、稽核、snapshot）原樣跑。
  FakeSession 在 `add()` 時補 `id` / `created_at` / `updated_at`，因為 ORM 是 flush 時才填。
- **踩過的坑**：用 Write 工具寫 regex 時，字元類裡的 U+2028 / U+2029 被寫成字面字元
  進了原始碼，`splitlines()` 會在那裡斷行。要寫成反斜線 u2028 的跳脫（`re` 認得），不要放字面字元。
- `test_error_localization` 把 `app/ui_text/` 視為公開面（路徑不含 admin），所以錯誤碼要有
  四語系句子；zh-TW 字典本來就不完整（handler 用 `AppError.detail`），沒有加。
