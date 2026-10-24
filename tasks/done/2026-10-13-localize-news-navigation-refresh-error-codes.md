---
id: 2026-10-13-localize-news-navigation-refresh-error-codes
title: Localize news navigation refresh error codes
status: done
priority: P1
area: api
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:13:38Z
created_at: 2026-10-13T08:16:24Z
completed_at: 2026-10-24T13:13:48Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - apps/api/app/i18n.py
---

# Localize news navigation refresh error codes

## Why

PR #1480's API CI shard failed because the four error codes introduced by the guarded
navigation evidence refresh lack translated public error sentences.

## Definition of done

- [x] All four navigation refresh/receipt error codes have distinct public sentences
  in en, ja, ko, zh-TW, and zh-CN.
- [x] The public error localization test and relevant API checks pass locally.

## Steps

- [x] Add the locale strings beside existing navigation repair errors.
- [x] Validate locally; the same draft PR's replacement CI head remains to be checked.

## How to verify

`cd apps/api && uv run pytest tests/test_error_localization.py -q` and
`uv run ruff check app/i18n.py`.

## Notes

The failing CI test was `test_every_public_error_code_has_a_sentence_in_every_locale`;
the new codes are `news_navigation_receipt_mismatch`,
`news_navigation_receipt_missing`, `news_navigation_refresh_busy`, and
`news_navigation_refresh_unavailable`.

2026-10-13 local result: `test_error_localization.py` 3 passed, combined AI
account/news review action tests 122 passed, Ruff and `git diff --check` passed.
Previous PR head's `api-tests (3/4)` failed on missing translations; push this
fix to the same PR and check the replacement head before closing the ticket.


### 2026-10-24 owner-directed reconciliation

站主要求處理全部open任務：不再需要或已有完成證據的項目結案。此為純任務紀錄接手；不接管其他live producer、不改產品scope檔、不發起付費、正式站寫入或YouTube操作。

Disposition: close_completed.

- PR #1480 MERGED 2026-10-18T20:30:54Z at 86c6d9bce117af85ce9267d408721c1f0f7c7dab with SUCCESS rollup.
- Fresh read-only current-main-based Windows validation: tests/test_ai_accounts_agent_runs.py plus tests/test_error_localization.py 69 passed, exit 0.

四錯誤碼五語與原CI故障已#1480落地；可結票，勿重新改i18n。
