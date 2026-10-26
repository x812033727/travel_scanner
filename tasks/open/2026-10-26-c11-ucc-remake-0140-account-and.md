---
id: 2026-10-26-c11-ucc-remake-0140-account-and
title: C11 UCC remake 0140 account and paid activation
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-26T14:06:13Z
completed_at:
branch:
depends_on:
  - 2026-10-26-stage-exact-c11-ucc-remake-0140
scope:
  - apps/api/migrations/versions/0140_c11_ucc_remake_budget.py
  - apps/api/app/video_budget
  - apps/api/app/migration_guard.py
  - apps/api/tests/test_c11_remake_budget_rollback_integration.py
  - apps/api/tests/test_video_pilot_budget.py
  - tools/video/core/pending-pilot-budget.mjs
---

# C11 UCC remake 0140 account and paid activation

## Why

站主 2026-10-26 核准 `story-everyday-ucc-c11-remake-20261025` 整片 US$25、約 10 分鐘，要做到可以上架。前一張票（`2026-10-26-stage-exact-c11-ucc-remake-0140`）讓 0139 映像能在 C11 remake 的 0140 上回滾；**那一版部署到主機之後**才能做這張。

## Definition of done

- [ ] `apps/api/migrations/versions/0140_c11_ucc_remake_budget.py` 與整合測試的 `FUTURE_SOURCE` 逐位元相同（SHA-256 `b6a8707d…94583f6`）。
- [ ] 這個 slug 進 API `ACTIVATED_STORY_SLUGS` 與本機 `pending-pilot-budget.mjs`；其他 `story-everyday-*` 照舊保留。它沒有舊費用，不需要 C03 那種 pre-ledger 結算。
- [ ] 部署後主機讀回：`migration_guard --status` exact 0140、帳戶 US$25、餘額 25、0 筆 operation。
- [ ] 付費生成前把旁白秒數、插圖張數與總額報給站主；之後旁白→插圖→配樂→組片（5 秒片頭、21 秒 v4 片尾、燒字幕）→QA→八語→上傳包，每一關照後台審核。

## Notes

- 工作區：這支是手動推上後台的（`hand_pushed`），worker_state `unavailable`，主機工人不會接；原稿與八語文字在 Codex 分支 `codex/brand-remakes-20261025` 的 `docs/videos/brand-story-remakes-20261025/c11/`。要先決定由哪個工作區製作，不要跟那個 session 同時改。
- 長度：已核准的劇本 78 場、80 句、紙上約 10.4 分鐘；站主接受約 10 分鐘，不必撐到 13 分鐘。
