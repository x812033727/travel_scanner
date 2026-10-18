---
id: 2026-10-13-localize-news-navigation-refresh-error-codes
title: Localize news navigation refresh error codes
status: in-progress
priority: P1
area: api
owner: codex-news-hourly-navigation-i18n
claimed_at: 2026-10-13T08:16:31Z
created_at: 2026-10-13T08:16:24Z
completed_at:
branch:
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
