---
id: 2026-10-13-catch-direct-crypto-trade-imperatives-without
title: Catch direct crypto trade imperatives without reported-trade false positives
status: done
priority: P2
area: api
owner: codex-news-policy-review
claimed_at: 2026-10-13T04:38:59Z
created_at: 2026-10-13T04:38:30Z
completed_at: 2026-10-13T05:00:36Z
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_policy.py
---

# Catch direct crypto trade imperatives without reported-trade false positives

## Why

The prior crypto-news policy repair correctly allowed reported trades, but also let
direct instructions such as `現在買進比特幣。` and `買進比特幣，等待價格上漲。` pass the hard
recommendation gate. An English instruction, `Buy bitcoin before the rally.`,
likewise passed. All three appeared after the unconditional trade-verb rule was
removed or narrowed; the editorial judge alone should not carry this hard gate.

## Definition of done

- [x] Direct Chinese and English trade instructions are blocked by the hard gate.
- [x] Reported company trades and lockups still pass that gate.

## Steps

- [x] Add direct-vs-reported regression cases, and confirm the direct cases fail first.
- [x] Narrowly extend imperative matching without restoring the blanket trade-verb check.

## How to verify

`cd apps/api && uv run pytest tests/test_news_policy.py -q`
`cd apps/api && uv run ruff check app/news_automation/policy.py tests/test_news_policy.py`
`git diff --check -- apps/api/app/news_automation/policy.py apps/api/tests/test_news_policy.py`

## Notes

Red phase: 3 direct-advice cases failed, then 4 more standalone imperative
cases failed. Green phase: 79 policy tests passed, Ruff and diff check passed.
Added paired zh-TW/zh-CN direct cases plus reported company-trade cases;
English direct and reported cases are also paired. A bare Chinese trade verb
with a comma requires an explicit profit-seeking follow-up. A standalone
Chinese imperative must name a traded asset and end the sentence; an English
imperative must begin a sentence and finish within a short clause. These
boundaries leave `買進比特幣的上市公司...` and `Buy orders.` as reporting/noun phrases.
