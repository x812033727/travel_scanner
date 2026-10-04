---
id: 2026-09-28-sqlalchemy-2-1-upgrade
title: SQLAlchemy 2.1 升級（mypy 的 Select 型別）
status: in-progress
priority: P3
area: api
owner: claude-opus-5-5-sqlalchemy-21
claimed_at: 2026-10-04T15:54:35Z
created_at: 2026-09-28T23:06:39Z
completed_at:
branch: claude/sqlalchemy-2-1
depends_on: []
scope:
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - apps/api/app/hotspots/guides.py
  - apps/api/app/hotspots/guide_scan.py
  - apps/api/app/foods/coordinate_queue.py
  - apps/api/app/foods/service.py
  - apps/api/app/foods/admin_router.py
  - apps/api/app/admin/operations_service.py
  - apps/api/app/saved/router.py
  - apps/api/app/guides/service.py
  - apps/api/app/discovery/display_topics.py
---

# SQLAlchemy 2.1 升級（mypy 的 Select 型別）

## Why

每週的 Dependabot uv 群組 PR #958 把 `sqlalchemy` 從 2.0.54 升到 2.1.1，CI 的 `api` job 在 `uv run mypy app` 報 16 個錯誤、9 個檔案（job 109141901043）。主因是 2.1 把 `select(Model)` 的型別從 `Select[tuple[Model]]` 改成 `Select[Model]`：

- 回傳型別不符：`app/hotspots/guides.py:827`、`app/foods/coordinate_queue.py:162`、`app/hotspots/guide_scan.py:120`、`app/admin/operations_service.py:425`
- 連帶的解包與 list 型別：`guides.py:845`、`guide_scan.py:126`、`operations_service.py:507`、`app/foods/admin_router.py:1496`
- 2.1 推斷得更細、揭露的既有變數重用：`app/saved/router.py:186/229/272/291`、`app/foods/service.py:696`、`app/guides/service.py:507/750`、`app/discovery/display_topics.py:52`

SQLAlchemy 是整個 API 的 ORM，站主 2026-09-29 決定不把型別修正塞進每週升級，#958 留言 `@dependabot ignore sqlalchemy minor version` 讓群組先合 boto3、pyjwt、ruff，這個升級單獨做。

## Definition of done

- [ ] `apps/api` 用 SQLAlchemy 2.1.x，`uv run mypy app`、`uv run mypy tests`、`uv run pytest` 全過，完整 CI 綠。
- [ ] 讀過 2.1 的 changelog／migration notes 的 breaking 段，對 repo `git grep` 用到的 API，結論寫在 Notes。
- [ ] Dependabot 之後會照常提 sqlalchemy 的 minor 升級（撤銷 ignore：`@dependabot unignore sqlalchemy` 或在新的群組 PR 上處理）。

## Steps

- [ ] `uv add 'sqlalchemy>=2.1,<2.2'`（或放寬 specifier）＋`uv lock`。
- [ ] 修 16 個 mypy 錯誤：回傳型別改成 2.1 的寫法；變數重用改成各自的名字，不要加 `cast` 壓過去。
- [ ] 讀 breaking changes，跑全部檢查；有執行期行為差異就補測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
```

## Notes

判斷規則見 `.agents/skills/dev-and-ci/references/dependabot.md`：跨版本的 runtime 依賴要當遷移票做。

### 2026-10-05 claude-opus-5-5-sqlalchemy-21（分支 `claude/sqlalchemy-2-1`）

- **認領用了 `--force`。** scope 與 `2026-09-14-redis-py-8-migration`、`2026-09-19-api-keys-in-logged-urls`、`2026-09-19-foreign-place-reason` 重疊（三張都是 claude-fable-5-1、`review`、認領已 364 小時）。三張的分支 `claude/travel-scanner-pr-552-rpq36m` 已由 #561、#563、#565 在 2026-09-19 合進 main（main 上也已是 `redis>=8.1,<9`），只是票沒搬到 done。
- **版本與 lock。** PyPI 上最新的 2.1.x 是 2.1.3（2026-10-03）。specifier 從 `>=2.0.43,<3` 改成 `>=2.1,<3`：下限擋掉 2.0（程式現在依賴 2.1 的型別），上限照這個檔其他依賴「到下一個大版本為止」的寫法，所以 2.2 出來時 Dependabot 群組 PR 只要動 lock 就能提（DoD 第三項）。`uv lock --upgrade-package sqlalchemy` 只動了 sqlalchemy 一個套件（2.0.54 → 2.1.3）。lock 裡 sqlalchemy 對 greenlet 的依賴邊消失了，因為 2.1 把 greenlet 移到 `[asyncio]` extra；greenlet 3.5.6 仍因 pyproject 直接列了 `greenlet>=3.2,<4` 而留在 lock 與環境裡。沒有其他套件移動。
- **mypy 的 16 個錯誤**（本機 2.1.3 下報的與 Why 列的完全相同，行號也一樣）。四個回傳型別 `Select[tuple[...]]` 改成 2.1 的 `Select[...]`（`guides.py`、`coordinate_queue.py`、`guide_scan.py` 兩處、`operations_service.py`），連帶的 list 與解包錯誤跟著消失，所以 scope 裡的 `foods/admin_router.py` 不用改。變數重用改成各自的名字：`saved/router.py` 五個迴圈的 `favorite` 改成 `hotspot_favorite` 等，`foods/service.py` 商家迴圈的 `relation` 改成 `merchant_relation`，`display_topics.py` 第二次出現的 `merchant_id` 改成 `item_merchant_id`。`guides/service.py` 兩處是 2.1 把 nullable 欄位的 `str | None`／`datetime | None` 如實傳出來：目的地 facet 的 WHERE 已排除 NULL，照 `app/` 的慣例加 `assert destination_id is not None`；sitemap 的下一頁游標改從已驗證的 `entries[-1]`（`published_at: datetime`）取，不再用 `rows[-1][4]` 這種位置索引。沒有 `cast`，也沒有 `type: ignore`。

### 2.1 的 breaking 與行為變更，逐條對照這個 repo

來源：docs.sqlalchemy.org 的 `changelog/migration_21.html` 與 `changelog/changelog_21.html`（2026-10-05 讀，含 2.1.0b1 到尚未釋出的 2.1.4）。`git grep` 範圍是 `apps/api`、`ops`、`docker-compose*.yml`、`.env*`。

- Python 需要 3.11 以上：我們是 3.13。不受影響。
- greenlet 不再預設安裝：我們用 asyncio（`AsyncSession`），但 greenlet 是直接依賴，仍在 lock 裡。不用改。
- `MappedAsDataclass` 的預設值改走 descriptor（`DONT_SET`）：`MappedAsDataclass|mapped_as_dataclass|unmapped_dataclass` 0 筆，模型都是一般的 `DeclarativeBase`。不受影響。
- Session 的 autoflush 變成無條件（`text()` 與 Core 語句也會 flush）：用到。`app/` 裡的 Core 語句只有 `text()`：四個 `pg_advisory_xact_lock`（`community/policy.py`、`community/admin.py`、`catalog_review/service.py`、`locations/map_identity_review.py`）與 `video_automation/planning_cli.py` 開頭的 `SET TRANSACTION READ ONLY`。每個鎖之後緊接的就是一個會 autoflush 的 ORM SELECT（2.0 也是），所以待寫入的列最多提早一個語句送出；不能 flush 呼叫者的 helper（analytics 的 `record_event`、community 的 `metric`）本來就包在 `no_autoflush` 裡；`app/` 沒有對 `Table` 物件下的 Core insert／update。不用改。
- `composite()` 回傳 None 的新規則：`composite(` 0 筆。不受影響。
- 較深路徑的 loader option 不再套到頂層物件：查詢沒有 `joinedload`／`selectinload`／`raiseload` 之類的 option（0 筆），只有 `TravelServiceProduct.hotel_options` 的 `lazy="selectin"`。不受影響。
- Row／Select 改用 PEP 646（`Select[tuple[X]]` 變 `Select[X]`，解包得到各欄真正的型別）：用到，就是上面修的 16 個錯誤；`mypy tests` 沒有因此報錯。
- `Select.filter_by()` 改成搜尋全部 FROM：`.filter_by(` 0 筆。不受影響。
- `ForeignKeyConstraint` 本地與遠端欄數不同改成 `ArgumentError`：用 AST 數過 migrations 與 `app/` 裡 115 個 FK 宣告（`ForeignKeyConstraint`、`create_foreign_key`）兩邊的欄數，全部一致。不受影響。
- `before_cursor_execute`／`after_cursor_execute` 的錯誤處理：只有 `tests/test_discovery_display_topics.py` 一個只記錄 SQL 的 listener，不碰 DBAPI cursor。不受影響。
- URL 的 database 部分改做 URL escape：資料庫名（`travel_scanner` 等）沒有特殊字元，`tests/fixtures/frontend_flow_seed.py` 的 `make_url` 只讀 host。不受影響。
- Operator class（JSON 欄位用 `.contains()` 會發 deprecation 警告）：7 個 `.contains()` 都先 `cast(..., Text)` 再做字串 LIKE，`trips/hours.py` 那個是 Python 物件。完整 pytest 的警告摘要裡沒有 SQLAlchemy 的 deprecation 警告。不受影響。
- Python float 字面值的 CAST 改成 DOUBLE：只影響產生的 SQL 字串，PostgreSQL 的 FLOAT 就是 double precision。不受影響。
- PostgreSQL 的預設 driver 改成 psycopg 3：所有連線字串都寫明 `postgresql+asyncpg://`（`app/config.py` 的預設、`alembic.ini`、`.env.example`）；tests 裡的 `postgresql://` 只是遮蔽用的字串，沒有拿去建 engine。不受影響。
- Enum／DOMAIN 等具名型別改綁 MetaData、建立與刪除的規則改變：models 與 migrations 都沒有 `Enum`／`ENUM`／`DOMAIN` 型別（用字串欄位加 CHECK）。不受影響。
- Computed 預設 VIRTUAL、BIT 改回傳 `BitString`、HSTORE 下標語法、collation schema、新的 SQLite JSONB 型別：都 0 筆。不受影響。
- `Select.c`／`.columns`／`Select.select()` 被移除：沒有對 Select 用 `.c` 的地方，mypy 也沒報（移除的屬性會是型別錯誤）。不受影響。
- Float 與 Numeric 拆開、`TypeEngine.python_type` 改回傳 `object`：`isinstance(..., Numeric|Float)`、`python_type` 0 筆。不受影響。
- `Session.execute(Query)` 的自動轉換被移除：`session.query(` 0 筆。不受影響。
- PostgreSQL 的 `select().distinct(*cols)` 棄用（改用 `distinct_on()`）：只有聚合函式裡的 `func.distinct()`／`distinct()`，沒有在欄位清單單獨用。不受影響。
- ARRAY 的 `Comparator.any()`／`all()` 棄用：`hotel_options.any()` 是 relationship 的 EXISTS，不是 ARRAY。不受影響。
- `noload`、`Session.flush(objects)`、`declarative_mixin` 棄用，mypy plugin 移除：都 0 筆；mypy 的 plugins 只有 `pydantic.mypy`。不受影響。
- asyncio driver 的模擬例外統一成 `EmulatedDBAPIException`：**用到，執行期行為有差。** asyncpg 的 unique／FK／not-null 違規現在是 `UniqueViolationError` 等子類，`str(exc.orig)` 只剩主訊息（2.0 的 `<class ...>:` 前綴與 `DETAIL:` 那一行沒了，DETAIL 改在 `exc.orig.detail`）。讀 `exc.orig` 的五處逐一看過：`guides/admin_service.py` 判斷 `"slug" in str(error.orig)`、`hotspots/admin_router.py` 判斷 `"wikidata_item_id" in str(exc.orig)`，約束名 `uq_guide_article_slug`、`uq_travel_hotspots_wikidata_item_id` 就在主訊息裡，仍然成立，PostgreSQL 上分別由 `tests/test_guides.py::test_a_duplicate_slug_is_a_conflict[postgresql]` 與 `tests/test_hotspot_review_identity_editor.py::test_postgres_stale_writer_waits_and_competing_qid_fill_is_unique` 在 CI 驗證（這兩個測試已存在，所以沒有另外補測試）；`news_automation/service.py` 的 `"unique" in str(error)` 仍會命中 `violates unique constraint`；`foods/catchtable_import.py`、`foods/enrichment_import.py` 寫進報表的 `detail=type(exc.orig).__name__` 在正式站會從 `IntegrityError` 變成更精確的 `UniqueViolationError`／`ForeignKeyViolationError` 等，沒有程式、測試或文件比對這個字串。不用改。
- aiosqlite 改用通用的 asyncio adapter：測試的 `connect` listener 會在連線上呼叫 `create_function` 與 `execute("PRAGMA ...")`，完整 pytest 有跑到。不受影響。
- SQLite 的 JSON 存取（`as_string()` 等）改用 CAST：`admin/operations_service.py` 的 `metadata_json[...].as_string()` 在 SQLite 測試裡跑過。不受影響。
- SQLite URL 帶 `mode=memory` 時選 pool 的行為棄用：0 筆。不受影響。
- bind 是 Engine 時一律忽略 `join_transaction_mode`：測試只在 bind 到 Connection 時用 `create_savepoint`。不受影響。
- 移除 1.3 以前棄用的 API（`Session.close_all`、`Mapper.mapped_table`、多參數的 `defer()` 等）：命中的只是同名的自家函式（`ai_accounts_agent` 的 `close_all`、測試的 `mapped_table()` helper）。不受影響。
- `ForeignKey.target_fullname`、`relationship(secondary=...)` 不再 eval、單表繼承的 `with_polymorphic`、`@validates` 被子類覆寫、屬性名叫 `metadata`／`registry`：都 0 筆。不受影響。
- import 的 SQLAlchemy 模組路徑（`sqlalchemy.sql.elements` 的 `ColumnElement`／`Null`、`sqlalchemy.sql.selectable.Subquery`、`sqlalchemy.orm.attributes.flag_modified`、`sqlalchemy.engine.reflection.Inspector`）：2.1.3 都還在，mypy 通過。不受影響。
- 已知回歸（2.1.0 到 2.1.3，修正在還沒釋出的 2.1.4）：直接迭代 `Result` 或用 `.scalars()` 會形成循環參照，Result 與已緩衝的列要等循環 GC 才釋放。我們大量用這兩種寫法；影響是記憶體回收延後，連線仍在 session 關閉時歸還。2.1.4 是 patch 版，#958 的 ignore 只擋 minor，Dependabot 會照常提。

### 沒勾的 DoD 第三項

撤銷 #958 上的 `@dependabot ignore sqlalchemy minor version`，要在一個 Dependabot PR 上留言 `@dependabot unignore sqlalchemy`。這個代理不在 GitHub 上留言，留給站主做。它不擋這個 PR 合併：ignore 只擋 minor（下一次是 2.2），2.1.x 的 patch 照常會提。
