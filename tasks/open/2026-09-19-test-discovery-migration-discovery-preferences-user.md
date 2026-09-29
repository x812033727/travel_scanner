---
id: 2026-09-19-test-discovery-migration-discovery-preferences-user
title: test_discovery_migration 單獨收集時 discovery_preferences.user_id 是 NullType，DDL 生不出來
status: in-progress
priority: P3
area: api
owner: codex-discovery-migration
claimed_at: 2026-09-29T14:39:24Z
created_at: 2026-09-19T10:06:50Z
completed_at:
branch: codex/discovery-migration-isolation
depends_on: []
scope:
  - apps/api/tests/test_discovery_migration.py
---

# test_discovery_migration 單獨收集時 discovery_preferences.user_id 是 NullType，DDL 生不出來

## Why

`uv run pytest tests/test_discovery_migration.py -q` 單獨跑會紅一個：

```
test_sqlite_frozen_and_current_metadata_upgrade_idempotent[True]
sqlalchemy.exc.CompileError: (in table 'discovery_preferences', column 'user_id'):
Can't generate DDL for NullType(); did you forget to specify a type on this Column?
```

同一個檔案排在任何有 import `app.models` 的模組後面（例如和 `tests/test_collection_item_lookup_migration.py`
一起跑，或整個測試套件）就 6 個全綠。原因是 `discovery_preferences.user_id` 是外鍵欄位，型別要等
`app.models` 把 `users` 表註冊進 metadata 才解析得出來；這支測試自己只 import 了 discovery 那半邊的 model，
單獨收集時 metadata 裡沒有 `users`，型別就停在 `NullType`。

2026-09-19 修 `mypy tests` 的 511 個錯誤時發現（`HEAD~1` 沒改過的版本單獨跑一樣紅），不是那次改動造成的。
一支測試的結果取決於它前面收集了什麼，是整套測試裡最會浪費人時間的那種紅燈。

## Definition of done

- [x] `uv run pytest tests/test_discovery_migration.py -q -p no:cacheprovider` 單獨跑全綠。
- [x] 整套一起跑仍然全綠，測試斷言的東西沒變。

## Steps

- [x] 在測試模組頂端 import `app.models`（`import app.models  # noqa: F401`，讓 `users` 進 metadata），
      或改用 `app.db.Base.metadata`／`app.models` 匯出的表來建 frozen metadata；看哪個和檔案現有寫法一致。
- [x] 單獨跑一次、和整套跑一次，都綠。
- [x] 順手看看 `tests/` 裡其他只 import 半邊 model 的 migration 測試有沒有同一個形狀（`grep -l "metadata.create_all" tests/*.py`）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_discovery_migration.py -q -p no:cacheprovider
cd apps/api && uv run pytest -q -p no:cacheprovider
```

## Notes

- 2026-09-19 由 claude-fable-5-1 的一個修 mypy 錯誤的 agent 回報；那次只把該檔的兩個 mypy 錯誤修掉，沒動這個問題。

### 2026-09-29 local repair (codex-discovery-migration)

- Started from main `a5ff4674`. All files of 12 open PRs, 43 remote heads,
  385 local branches and 217 other worktrees were checked before claiming.
  The sole historical scoped branch has the same file as merged PR #372;
  no active scope owner or competing implementation was found.
- A fresh process reproduced the original failure: 1 failed, 2 passed,
  2 PostgreSQL cases skipped. Adding only the explicit `app.models` import
  makes that same standalone run pass: 3 passed, 2 PostgreSQL cases skipped.
  The ticket's historical six-test count is now five collected cases.
- This is collection-time model registration: pytest imports all selected
  modules before running tests. Either order of discovery plus the collection
  migration test passed on the old source (6 passed, 2 skipped), which explains
  why a combined run alone cannot guard this defect.
- Sibling audit: collection, guides and site-pages migration tests explicitly
  import User; hotel uses typed frozen metadata. Their standalone checks passed
  (3; 21 with 1 skip; 3 with 1 skip), while hotel's PostgreSQL-only case skipped.
  No additional defect was established and no product or migration code changed.
- Full local verification uses `RUN_INTEGRATION_TESTS=0`,
  `RUN_MIGRATION_TESTS=0` and `COMMUNITY_TEST_S3=0`; external service coverage
  remains with CI. Full API Ruff passed.
- Full native Windows `mypy tests` passed (331 files). Independent AST and
  textual review confirmed that the explicit import is the sole test-code change:
  all test/helper bodies, parameterization, skip conditions and 11 assertions
  are identical to main.
- Full `mypy app` passed (444 files). The pre-PR collision check again found no
  competing active work; the full local pytest run collected 5,459 cases.
- The full local suite on base `a5ff4674` passed: **5,040 passed, 419 skipped,
  2 warnings**, exit 0, in 1,087.93 seconds. Skips require external integration
  services or POSIX features. Warnings are the existing Redis `setex` deprecation
  (tracked by `2026-09-19-app-places-router-py-redis-setex`) and AsyncMock coroutine
  warning previously recorded in `2026-09-09-frontend-flow-saved-api`.
- Rebased onto `9656d0d9` after the full suite: intervening main commits #977/#978
  change video tooling/content/API, not discovery models, migrations, this test
  or Python dependencies. The standalone migration check passed again after the
  rebase (3 passed, 2 PostgreSQL skips). The six affected upstream API modules
  passed separately: 94 passed, 5 PostgreSQL skips. Full API Ruff, `mypy app`
  (444 files) and `mypy tests` (332 files) passed again on the rebased source.
  The earlier full-suite result remains
  attributed to its actual base, rather than being presented as a newer-base run.
- Final pre-push collision refresh: 10 open PRs / 170 fully paginated files,
  41 remote heads, 386 local branches and 217 other worktrees. No active collision;
  the same historical branch and absent P: checkout remnants are preserved.
