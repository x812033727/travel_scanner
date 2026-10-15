---
id: 2026-10-10-distinguish-reported-and-negated-trading-verbs
title: Distinguish reported and negated trading verbs from crypto recommendations
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T01:09:25Z
completed_at:
branch:
depends_on:
  - 2026-10-10-news-disclaimer-correction-loop
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_policy.py
---

# Distinguish reported and negated trading verbs from crypto recommendations

## Why

The crypto recommendation check treats every occurrence of 買入 or 賣出 as
actionable advice. The October 10 held cohort includes a Bitfinex question
about whether the US government sold seized bitcoin (the answer says it did
not), an ESMA article describing regulated services, and a MoonPay FAQ saying
the report is not advice to buy or sell. These are reporting/negation contexts.
Current drafts can be edited and independently rechecked, but the same wording
can hold future factually valid reporting.

## Definition of done

- [ ] Supported reporting, regulation and explicit negation are distinguished
      from a recommendation to trade, without weakening actual advice checks.
- [ ] Existing held-candidate decisions and drafts are not automatically approved.

## Steps

- [ ] Reproduce the three stored examples and contrasting actionable advice.
- [ ] Define a narrow context rule or replace the unconditional match with an
      existing review gate; check multilingual behavior before implementation.

## How to verify

Run the policy tests with the worktree API environment. Include positive advice,
reported transactions, regulatory service descriptions and explicit negation;
do not merely test rewritten synonyms that avoid the original false positive.

## Notes

- External evidence: news-review/20261010-6f71/editorial-holds-plan.json and
  editorial-holds-patches.json. Exact stored strings are retained as JSON
  pointer before/after preconditions. No policy change is attempted in the
  disclaimer-loop repair; keep this follow-up separate.
