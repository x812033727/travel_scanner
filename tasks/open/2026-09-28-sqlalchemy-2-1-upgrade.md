---
id: 2026-09-28-sqlalchemy-2-1-upgrade
title: SQLAlchemy 2.1 升級（mypy 的 Select 型別）
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T23:06:39Z
completed_at:
branch:
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
