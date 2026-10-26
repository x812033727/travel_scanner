---
id: 2026-10-26-c11-ucc-remake-0140-account-and
title: C11 UCC remake 0140 account and paid activation
status: review
priority: P1
area: api
owner: claude-opus-5-5-happy-brahmagupta
claimed_at: 2026-10-26T15:07:13Z
created_at: 2026-10-26T14:06:13Z
completed_at:
branch: claude/happy-brahmagupta-ibjkpd
depends_on:
  - 2026-10-26-stage-exact-c11-ucc-remake-0140
scope:
  - apps/api/migrations/versions/0140_c11_ucc_remake_budget.py
  - apps/api/app/video_budget
  - apps/api/app/migration_guard.py
  - apps/api/app/schema.py
  - apps/api/tests/test_c11_remake_budget_rollback_integration.py
  - apps/api/tests/test_story_remakes_budget_rollback_integration.py
  - apps/api/tests/test_migration_0140_c11_ucc_remake_budget.py
  - apps/api/tests/test_migration_0138_everyday_story_budget.py
  - apps/api/tests/test_migration_guard.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_video_pilot_budget.py
  - tools/video/core/pending-pilot-budget.mjs
  - .github/workflows/ci.yml
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
---

# C11 UCC remake 0140 account and paid activation

## Why

站主 2026-10-26 核准 `story-everyday-ucc-c11-remake-20261025` 整片 US$25、約 10 分鐘，要做到可以上架。前一張票（`2026-10-26-stage-exact-c11-ucc-remake-0140`）讓 0139 映像能在 C11 remake 的 0140 上回滾；**那一版部署到主機之後**才能做這張。

## Definition of done

- [x] `apps/api/migrations/versions/0140_c11_ucc_remake_budget.py` 與整合測試的 `FUTURE_SOURCE` 逐位元相同（SHA-256 `b6a8707d…94583f6`）。
- [x] 這個 slug 進 API `ACTIVATED_STORY_SLUGS` 與本機 `pending-pilot-budget.mjs`；其他 `story-everyday-*` 照舊保留。它沒有舊費用，不需要 C03 那種 pre-ledger 結算。
- [x] 同一版放進 0141（C14、C03、C04、C06、C05、C08 remake 各 US$25）的回滾相容：0140 映像只認固定原文的 `0141_story_remake_budgets`，六支在這版照樣保留。
- [ ] 部署後主機讀回：`migration_guard --status` exact 0140、帳戶 US$25、餘額 25、0 筆 operation。
- [ ] 付費生成前把旁白秒數、插圖張數與總額報給站主；之後旁白→插圖→配樂→組片（5 秒片頭、21 秒 v4 片尾、燒字幕）→QA→八語→上傳包，每一關照後台審核。

## Notes

- 工作區：這支是手動推上後台的（`hand_pushed`），worker_state `unavailable`，主機工人不會接；原稿與八語文字在 Codex 分支 `codex/brand-remakes-20261025` 的 `docs/videos/brand-story-remakes-20261025/c11/`。要先決定由哪個工作區製作，不要跟那個 session 同時改。
- 長度：已核准的劇本 78 場、80 句、紙上約 10.4 分鐘；站主接受約 10 分鐘，不必撐到 13 分鐘。

## 做法（2026-10-26，claude-opus-5-5-happy-brahmagupta）

- 站主 2026-10-26 回報 #1870 已部署；雲端 session 讀不到主機，`migration_guard --status` 那一行要站主讀回。
- `models.py`：`C11_REMAKE_SLUG`、`REMAKE_PILOT_LIMITS_USD` 與 `ACTIVATED_STORY_SLUGS`。**不放進 `C_SERIES_PILOT_LIMITS_USD`**：0138／0139 的回滾讀回、0139／0140 的 `PRIOR_LIMITS` 都用那個集合，放進去會讓它們多數一個帳戶。`service._reviewed_limit` 讓 reserve 與 summary 認得它的 US$25。
- 0138 的整合測試會把 head 的帳戶倒回 0137，要先拿掉 0140 的 C11 帳戶與 ownership 表（CI 先 `alembic upgrade head` 再跑 pytest）。
- `test_c11_remake_budget_rollback_integration.py` 的「舊映像」是今天的程式碼，所以 C11 已放行；真正部署的 0139 映像（#1870）靠它自己的程式碼擋 C11，這裡只再驗 C20 被擋。
- 站主同時要接著做 C14、C03、C04、C06、C05、C08 remake，並說有問題用建議的做法、不必問。照 C11 的條件各 US$25，新 slug、沒有舊費用、不借原集帳戶。為了不再多兩次部署，把 0141 的相容檢查放進這版；0141 本體與放行在 `2026-10-26-story-remake-0141-accounts-and-activation`。
- 驗證：ruff、mypy app 489／tests 422；本機 PostgreSQL 16＋Redis 全新資料庫 upgrade 到 head（0140 實跑），預算、migration、三支回滾整合測試與影片相關共 233 passed、1 skip；`node --test` 影片工具 677 tests 0 fail；host-verify 5 pass。
- PR：https://github.com/x812033727/travel_scanner/pull/1875
