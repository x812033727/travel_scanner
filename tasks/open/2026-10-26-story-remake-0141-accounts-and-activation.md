---
id: 2026-10-26-story-remake-0141-accounts-and-activation
title: Story remake 0141 accounts and activation
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-26T15:34:03Z
completed_at:
branch:
depends_on:
  - 2026-10-26-c11-ucc-remake-0140-account-and
scope:
  - apps/api/migrations/versions/0141_story_remake_budgets.py
  - apps/api/app/video_budget
  - apps/api/tests/test_story_remakes_budget_rollback_integration.py
  - apps/api/tests/test_migration_0141_story_remake_budgets.py
  - apps/api/tests/test_migration_0138_everyday_story_budget.py
  - apps/api/tests/test_video_pilot_budget.py
  - tools/video/core/pending-pilot-budget.mjs
---

# Story remake 0141 accounts and activation

## Why

站主 2026-10-26 要 C11 之後接著做 C14、C03、C04、C06、C05、C08 的 2026-10-25 remake，照新規則，有問題用建議的做法不必問。六支都是新 slug、沒有付費紀錄，各自需要 US$25 帳戶才能離開 `video_budget_preproduction_hold`。前一張票（`2026-10-26-c11-ucc-remake-0140-account-and`）已讓 0140 映像能在 0141 上回滾；**那一版部署之後**才能做這張。

## Definition of done

- [ ] `apps/api/migrations/versions/0141_story_remake_budgets.py` 與 `tests/test_story_remakes_budget_rollback_integration.py` 的 `FUTURE_SOURCE` 逐位元相同（SHA-256 `0f611614…f534a5afb`）。
- [ ] 六個 slug 進 `REMAKE_PILOT_LIMITS_USD` 與 `ACTIVATED_STORY_SLUGS`（API 與本機 `pending-pilot-budget.mjs`）；原集 slug 與其他 remake 照舊保留。
- [ ] 0141 的 migration 測試（衝突、離線、不可 downgrade）；0138 測試倒回 0137 時也拿掉 0141 的帳戶。
- [ ] 部署後讀回：`migration_guard --status` exact 0141，六個帳戶各 US$25、0 筆 operation。

## Notes

- 六個 slug（順序照站主）：`story-everyday-camelbak-c14-remake-20261025`、`story-everyday-moleskine-c03-remake-20261025`、`story-everyday-bubble-wrap-c04-remake-20261025`、`story-everyday-play-doh-c06-remake-20261025`、`story-everyday-kincho-c05-remake-20261025`、`story-everyday-kikkoman-c08-remake-20261025`。2026-10-26 後台讀回：花費都是 0；C03 remake 在 narration synthesized，其他在 outline approved。
- 原稿、八語文字與製作檔在 Codex 分支 `codex/brand-remakes-20261025` 的 `docs/videos/brand-story-remakes-20261025/<cNN>/`。
