---
id: 2026-09-19-test-discovery-migration-discovery-preferences-user
title: test_discovery_migration 單獨收集時 discovery_preferences.user_id 是 NullType，DDL 生不出來
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-19T10:06:50Z
completed_at:
branch:
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

- [ ] `uv run pytest tests/test_discovery_migration.py -q -p no:cacheprovider` 單獨跑全綠。
- [ ] 整套一起跑仍然全綠，測試斷言的東西沒變。

## Steps

- [ ] 在測試模組頂端 import `app.models`（`import app.models  # noqa: F401`，讓 `users` 進 metadata），
      或改用 `app.db.Base.metadata`／`app.models` 匯出的表來建 frozen metadata；看哪個和檔案現有寫法一致。
- [ ] 單獨跑一次、和整套跑一次，都綠。
- [ ] 順手看看 `tests/` 裡其他只 import 半邊 model 的 migration 測試有沒有同一個形狀（`grep -l "metadata.create_all" tests/*.py`）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_discovery_migration.py -q -p no:cacheprovider
cd apps/api && uv run pytest -q -p no:cacheprovider
```

## Notes

- 2026-09-19 由 claude-fable-5-1 的一個修 mypy 錯誤的 agent 回報；那次只把該檔的兩個 mypy 錯誤修掉，沒動這個問題。
