---
id: 2026-09-07-fixed-email-in-integration-tests
title: 整合測試用固定 email，同一個資料庫跑第二次就 UniqueViolation
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-07T01:10:00Z
completed_at:
branch:
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

- [ ] 同一個資料庫連跑兩次 `RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py`
      都是綠的。

## Steps

- [ ] email 帶 `uuid4()`，或在測試結尾刪掉自己建的列。
- [ ] 順手看一下其他整合測試有沒有同樣寫死的識別值。

## How to verify

```bash
cd apps/api
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py -q   # 第二次也要綠
```

## Notes

- 暫時的解法是手動刪掉那一列：
  `psql … -c "delete from users where email = 'food-owner-integration@example.test'"`。
