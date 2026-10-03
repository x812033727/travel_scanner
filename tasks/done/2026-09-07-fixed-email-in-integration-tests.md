---
id: 2026-09-07-fixed-email-in-integration-tests
title: 整合測試用固定 email，同一個資料庫跑第二次就 UniqueViolation
status: done
priority: P3
area: api
owner: codex-fixed-email-acceptance-20261003
claimed_at: 2026-10-03T11:43:03Z
created_at: 2026-09-07T01:10:00Z
completed_at: 2026-10-03T11:43:06Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/api/tests/test_food_integration.py
---

# 整合測試用固定 email，同一個資料庫跑第二次就 UniqueViolation

## Why

`tests/test_food_integration.py::test_reseeding_corrects_seed_owned_text_and_leaves_admin_edits_alone`
建立的管理者用寫死的 `food-owner-integration@example.test`，而且沒有在結尾刪掉。CI 每次都是
全新的資料庫所以看不出來；本機開發者對同一個資料庫跑第二次，就會拿到

```
asyncpg.exceptions.UniqueViolationError: duplicate key value violates unique constraint
"ix_users_email"
DETAIL:  Key (email)=(food-owner-integration@example.test) already exists.
```

看起來像自己的改動弄壞的，其實只是上一次跑剩的一列。2026-09-07 在 PR F 的驗證裡撞到，
確認在 `claude/better-workflow-planning-324ki8` 的 head 上也一樣失敗，才判斷不是那個 PR 的問題。

`tests/test_alerts_integration.py` 的 `register()` 用 `uuid4()` 產 email，是同一個檔案家族裡
做對的那個作法。

## Definition of done

- [x] 同一個資料庫連跑兩次 `RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py`
      都是綠的。

## Steps

- [x] email 帶 `uuid4()`，或在測試結尾刪掉自己建的列。（兩個都做了）
- [x] 順手看一下其他整合測試有沒有同樣寫死的識別值。（見 2026-09-19 的筆記）

## How to verify

```bash
cd apps/api
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py -q   # 第二次也要綠
```

## Notes

- 暫時的解法是手動刪掉那一列：
  `psql … -c "delete from users where email = 'food-owner-integration@example.test'"`。

### 2026-09-19 done in repo (claude-fable-5-1)

**原因**：`update_food()` 會寫一列 `AdminAuditLog` 然後 `session.commit()`，所以那個管理者
在第二個 session 區塊結束時已經落地；`_clear()` 只清美食相關的表，不碰 `users` 與
`admin_audit_logs`；`users.email` 是 unique。三件事加起來，寫死的 email 就會活過整次測試，
第二次跑到 `session.flush()` 就撞 `ix_users_email`。

**改法**（只動 `apps/api/tests/test_food_integration.py`）：

- `test_reseeding_corrects_seed_owned_text_and_leaves_admin_edits_alone`：email 改成
  `food-owner-integration-{uuid4().hex}@example.test`，並在最後一個 session 區塊、`_clear()`
  之前，刪掉這個管理者的 `AdminAuditLog` 列與 `User` 列（`actor_user_id` 是
  `ondelete="SET NULL"`，先刪 audit 列只是為了不留垃圾，順序不影響正確性）。uuid 讓「上一次
  跑到一半失敗」的資料庫也能再跑；結尾清掉讓成功的那次什麼都不留。
- `test_food_seed_public_filters_maps_and_admin_state_are_idempotent` 的
  `food-admin-integration@example.test` 也加上 uuid：它結尾有刪，但 `batch_foods()` 早就 commit
  了，測試中途一斷同樣會留下那列、下一次一樣 UniqueViolation。

**其他寫死的識別值**（都看過，不用改）：

- 同檔 `coverage@example.test`、`food-listing@example.test` 是沒 `session.add` 的暫時物件，只拿來
  過 `AdminUser` 型別（`list_admin_foods` 裡是 `_ = user`，`restaurant_editorial_coverage` 裡是
  `del user`），不會進資料庫。
- `reservation_records` fixture 本來就帶 `token = uuid4().hex`，而且 finally 會清。
- `tests/test_hotspot_admin_integration.py:42` 的 `hotspot-listing@example.test` 是同一種暫時物件，
  不在本票 scope，也不需要動。
- `test_admin_users_integration.py`、`test_registration_settings_integration.py`、
  `test_ui_text_integration.py`、`test_usage_settings_integration.py`、`test_saved_items_integration.py`
  都已經帶 suffix。

**驗證**：這台機器沒有 PostgreSQL，`RUN_INTEGRATION_TESTS` 沒開：

```
cd apps/api && uv run pytest tests/test_food_integration.py -q   # 8 skipped（import 正常）
uv run ruff check tests                                          # All checks passed!
```

Definition of done 的「同一個資料庫連跑兩次」要有 Postgres 才能打勾，所以狀態先放 `review`；
下一個有 `RUN_INTEGRATION_TESTS=1` 環境的人照「How to verify」跑兩次，綠了就 `done`。

### 2026-10-03 same-database acceptance completed

- Fresh task-only archive gate PASS across main4f8c3817, the sole own PR1175,
  33 remote heads, 430 local branches and 28 registered worktrees. No active
  duplicate closure or dirty task copy. PR563 merged14ce467d owns the original
  review branch; the two repaired fixture functions are still AST-identical.
  Only this task was reclaimed for acceptance; no API source was changed.
- Isolated, task-owned PostgreSQL18.3 / pg_trgm1.6 was privately extracted under
  WSL without a system installation. No repository .env was loaded by the Windows
  Python launcher; only the explicit loopback database was available to the test.
- Full migrations passed to0122_video_anime_production. The entire food module
  then passed twice:8passed/0skipped,53.61s/46.78s, both exit0. No database reset,
  recreation or migration occurred between runs. Database name, OID16384,
  cluster7692402131696837186, revision and postmaster start stayed identical.
- Food test SHA256 before/after:
  429bfa6fe34a8a84200a7787f1b5db416b0b715fa9a035a55d41bf024f2152ea.
  Private PG stop passed; both Windows/Linux55437 listeners and its PID file
  were absent afterward. This verifies localPG18.3, not CI's PG17 image.
- Receipt SHA256:d5f237d39eb6553e7ccb74289052011dcdf0d090dec86b63c8ccab58c4853926.
  Evidence:<home>/.codex/tmp/fixed-email-acceptance-20261003/fixed-email-20261003-319b084a/.
  Independent gate/receipt review:
  <home>/.codex/tmp/fixed-email-archive-gate-20261003/archive-gate-verdict.json.
- Archived local acceptance in draft PR1175; no production connection, deployment
  or publication was performed.
