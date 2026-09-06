---
id: 2026-09-06-migration-backfill-untested
title: 遷移裡的補資料分支在 CI 是死碼
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:29:37Z
created_at: 2026-09-06T00:53:38Z
completed_at:
branch: claude/ci-guards
depends_on: []
scope:
  - .github/workflows/ci.yml
  - apps/api/tests/test_migration_dead_branches.py
---

# 遷移裡的補資料分支在 CI 是死碼

## Why

`0001_initial` 的內容是 `Base.metadata.create_all` —— 它建的是**當前模型**的完整
schema。所以 CI 的全新資料庫從第一步開始就已經有每一個現行欄位。

後果：所有寫成這個形狀的遷移

```python
if "notes" not in columns:
    op.add_column(...)
    op.execute("UPDATE ... ")   # 補舊資料
```

在 CI **整段都不會執行**，因為欄位早就存在。這些補資料的 SQL 第一次真正被執行，
永遠是在正式機上。

2026-09-06 這件事就真的發生了：`0042_trip_notes` 用了 `data ? 'notes'`，而 `?` 只
存在於 jsonb、`trip_plans.data` 是 json，PostgreSQL 在**解析階段**就拒絕（跟有幾列
資料無關）。CI 八項全綠，部署時 migrate 容器 exit 1，部署腳本自動回滾。

我在 PR #176 修了那一句，並加了 `tests/test_migration_sql_dialect.py` 把遷移 SQL 當
文字讀、擋掉 json 欄位上的 jsonb 專屬運算子。但那只是貼在傷口上的膠布：**任何其他
種類的錯**（欄位名打錯、型別不合、約束衝突）在這些分支裡仍然完全沒有測試。

## Definition of done

- [ ] CI 會在一個「舊的」資料庫上跑一次完整的 upgrade，讓那些 `if 欄位不存在` 的
      分支真的被執行過一次。
- [ ] 拿掉這個保護（例如把 0042 的補資料 SQL 改回會炸的版本）時，CI 會紅。

## Steps

- [ ] 決定怎麼造出「舊資料庫」。幾個方向，擇一：
      - CI 多跑一個 job：先 `alembic upgrade <某個舊 revision>`，再 `upgrade head`。
        問題是 0001 就已經是 create_all，所以要挑一個真正早於這些欄位的基準點，
        或者改用下面這招。
      - 讓 0001 不再用 `create_all`：改成把當時的 schema 寫死。工程量大但一勞永逸，
        之後每個遷移都會在真正的舊 schema 上跑。
      - 折衷：在測試裡用 `op.drop_column` 造出缺欄位的狀態，再單獨執行該遷移的
        `upgrade()`，等於針對每個補資料分支寫一個回歸測試。
- [ ] 至少讓 `0042_trip_notes` 與 `0043_trip_expenses` 的補資料分支被實際執行到。
- [ ] 寫下判準，讓下一個人知道新增這種遷移時要補什麼測試。

## How to verify

把 `0042_trip_notes.py` 的 WHERE 條件改回 `AND data ? 'notes'`，CI 的 api 或
full-stack-smoke 必須紅。改回來之後必須綠。

## Notes

正式機的實際錯誤訊息（留著給下一個人比對）：

```
sqlalchemy.exc.ProgrammingError: operator does not exist: json ? unknown
[SQL: UPDATE trip_plans SET notes = data ->> 'notes'
      WHERE notes IS NULL AND data ? 'notes' AND nullif(trim(data ->> 'notes'), '') IS NOT NULL]
```

修法是拿掉 `?`：`nullif(trim(data ->> 'notes'), '') IS NOT NULL` 本來就蘊含 key 存在
且有內容，而 `->>` 在 json 與 jsonb 都可用。`0032_remove_plus_codes` 用的
`data::jsonb ? 'plus_code_global'` 是正確寫法 —— 顯式轉型就沒問題。

**現有的文字守則**（`tests/test_migration_sql_dialect.py`）只認得五個運算子
（`?` `?|` `?&` `@>` `<@`），而且是靠字串比對；它擋得住重蹈覆轍，擋不住新種類的錯。
這張任務要的是真的跑過一次，不是更聰明的正則。

**復現這個 bug 的方式**（我當時繞了不少路）：正式機回滾之後，映像標籤
`travel-scanner-api:local` 會指回舊的建置，直接跑 migrate 會「什麼都不做且 exit 0」，
看起來像沒事。要先 `git checkout <新 SHA>` 再 `docker compose build api`（不是
`build migrate` —— migrate 服務只有 `image:` 沒有 `build:`，會跑去 pull 然後失敗），
才能重現。
