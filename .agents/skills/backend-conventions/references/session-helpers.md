# 在呼叫端 session 上寫東西的 helper

適用：任何接收呼叫端的 `AsyncSession`、順手寫一筆的函式——分析事件、每日指標、去重標記、通知計數。正本是 `apps/api/app/analytics/service.py` 的 `record_event` docstring 與 `apps/api/app/community/policy.py` 的 `metric()` 註解，動手前先讀那兩段。

不適用：自己開 session 的背景工作（`catalog_review/jobs.py`、`community/jobs.py` 等用 `begin_nested()` 是合理的，因為沒有「呼叫端待寫的列」）。

## 兩條規則

1. **不要 `begin_nested()`。** 進入 savepoint 之前 SQLAlchemy 會先 flush 整個 session（`SessionTransaction` 為 nested 交易取快照時做的）。所以 `try: async with session.begin_nested(): ...` 的 `try` 罩住的範圍比 savepoint 大：呼叫端還沒送出的 INSERT 在這裡被沖出去，它的 `IntegrityError` 被 helper 的 except 吃掉，呼叫端的 `commit()` 拿到 `PendingRollbackError`，它自己的 `except IntegrityError`（例如回 409）永遠不會執行。真實後果：兩個成員同時建立同一個提醒，拿到 500 而不是 409。
2. **所有查詢與寫入包在 `with session.no_autoflush:` 裡。** 一個 `SELECT`（例如讀設定）也會在出門前 flush 呼叫端的待寫列，後果同上。

剩下的做法：insert 跟著呼叫端的交易一起 commit。這是刻意的——建立失敗而回滾的東西不該被計數。殘餘風險（helper 自己的 insert 因別的原因失敗而毒化呼叫端交易）在程式註解裡明寫，不要用 savepoint 去「修」。

## ORM entity 與 Core insert 的差別

- `insert(Model)`（ORM entity）走 ORM 執行路徑，會先 autoflush 呼叫端。
- `insert(Model.__table__)`（純 Core）不會。
- **兩者編譯出的 SQL 完全相同**，所以「斷言發出的 SQL 含 `ON CONFLICT`」的測試分不出來。
- mypy 只接受 entity 形式（`__table__` 的型別是 `FromClause`），所以正解是 entity 形式＋`no_autoflush`：

```python
marker = postgres_insert(CommunityMetric).values(values).on_conflict_do_nothing(index_elements=conflict)
with session.no_autoflush:
    await session.execute(marker)
```

SQLite 分支用 `sqlite_insert`，依 `session.get_bind().dialect.name` 選。

## 怎麼測

斷言待寫集合，不是 SQL：

```python
session.add(caller_row)
await helper(session, ...)
assert caller_row in session.new        # 或 len(session.new) == 1
await session.commit()
```

現有回歸測試：`apps/api/tests/test_analytics_integration.py` 的 `test_a_pending_row_is_not_flushed_by_measuring_it`、`apps/api/tests/test_community_foundation.py` 的 `test_daily_metric_does_not_flush_the_callers_pending_rows`。新 helper 照抄一個。前者需要 `RUN_INTEGRATION_TESTS=1`（Postgres＋Redis）；後者的 harness 本機跑 SQLite，設了該變數再加跑 Postgres。
