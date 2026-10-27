---
id: 2026-10-26-stage-exact-c11-ucc-remake-0140
title: Stage exact C11 UCC remake 0140 rollback compatibility
status: done
priority: P1
area: api
owner: claude-opus-5-5-happy-brahmagupta
claimed_at: 2026-10-26T13:58:18Z
created_at: 2026-10-26T13:58:12Z
completed_at: 2026-10-26T15:07:12Z
branch: claude/happy-brahmagupta-ibjkpd
depends_on: []
scope:
  - apps/api/app/schema.py
  - apps/api/app/migration_guard.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_c11_remake_budget_rollback_integration.py
  - .github/workflows/ci.yml
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
---

# Stage exact C11 UCC remake 0140 rollback compatibility

## Why

站主 2026-10-26 要 `story-everyday-ucc-c11-remake-20261025`（UCC奶咖1969上市，方便為何還這麼難？｜品牌故事）做到可以上架，核准整片 US$25 上限、接受約 10 分鐘。後台讀回：企劃與劇本 11:03 已核准，旁白以後全部沒做、花費 0；`story-everyday-*` 一律被 `video_budget_preproduction_hold` 擋在付費前，這支沒有預算帳戶。

新帳戶要一支 migration，而 repo 規則（`apps/api/app/video_budget/PENDING_EVERYDAY.md`）要求先部署一個能在新 revision 上回滾的相容版本。main 已預留的 0140 是給 `story-everyday-kikkoman-c08-short-v8`（#1820），但那支片 2026-10-26 12:18 已在後台放棄（站主改做 C08 remake），0140 本體從沒寫過。站主同意把 0140 改給 C11 remake，不排在 0141 等一支不會做的片。

## Definition of done

- [x] 0139 映像只認 `0140_c11_ucc_remake_budget`：讀回 18 個帳戶（含 C20 與 C11 remake 各 US$25）、四筆歷史保留、兩張 ownership 表；其他 0140 一律拒絕。
- [x] 舊的 C08 0140 預留整個換掉（guard、`/ready`、host-verify、CI、固定 SHA 的未來 migration 原文）。
- [x] 這個版本不建帳戶、不解除任何付費保留。

## Steps

- [x] `migration_guard.py`、`schema.py`、`host-verify.sh` 與測試改成 C11 remake 的 0140。
- [x] C08 的整合測試改名 `test_c11_remake_budget_rollback_integration.py`；未來 migration 原文改 slug、revision 與 docstring，SHA 重新固定。
- [x] PR 合併後由站主在自己電腦照 skill `deploy` 部署（站主 2026-10-26 回報已部署）；部署後 `python -m app.migration_guard --status` 為 `state=exact current=0139_c20_zippo_pilot_budget`。

## How to verify

`cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest -q tests/test_schema.py tests/test_migration_guard.py tests/test_c11_remake_budget_rollback_integration.py`；本機有 PostgreSQL 與 Redis 時加 `RUN_INTEGRATION_TESTS=1` 跑 `tests/test_c11_remake_budget_rollback_integration.py tests/test_c20_budget_rollback_integration.py`；`node --test tools/deploy-host-verify.test.mjs`；`bash -n .agents/skills/deploy/scripts/host-verify.sh`；`npm run check:tasks`。

## Notes

- 2026-10-26 雲端 session：ruff、mypy（app 489、tests 420 檔）通過；focused pytest 17 passed、1 skip（PostgreSQL 專用）；在容器裡起 PostgreSQL 16 與 Redis 後，C11 remake 與 C20 兩支整合測試 3 passed（真的套用固定原文的 0140、跑舊 0139 的 Compose migrate 指令、`/ready`、損壞合約都被拒）。host-verify 測試 5 pass。
- 未來 0140 原文 SHA-256 `b6a8707dc220819ccfae8f54ca9c90a790d0eb1cea448f7f030da93fe94583f6`；下一張票的 migration 必須逐位元相同。docstring 改成「帳戶本身不放行付費，由應用程式的啟用清單決定」，因為下一版會同時把這支加進 `ACTIVATED_STORY_SLUGS`。
- 只換掉 0140 的預留，沒有動 C08 remake 或 Codex `codex/brand-remakes-20261025` 那批（scope 只有 `docs/videos/brand-story-remakes-20261025`）。其他 remake 要付費時各自要帳戶，接在 0141 之後。
- PR：https://github.com/x812033727/travel_scanner/pull/1870
- 下一步：`2026-10-26-c11-ucc-remake-0140-account-and`。
- #1870 2026-10-26 14:27Z squash 合併為 `2edb6eaab`；站主回報已部署。雲端 session 連不到主機，`migration_guard --status` 那一行由站主讀回，下一張票合併前要先確認。
