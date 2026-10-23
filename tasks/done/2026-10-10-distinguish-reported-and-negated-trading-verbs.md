---
id: 2026-10-10-distinguish-reported-and-negated-trading-verbs
title: Distinguish reported and negated trading verbs from crypto recommendations
status: done
priority: P2
area: api
owner: codex-news-crypto-policy
claimed_at: 2026-10-13T03:39:06Z
created_at: 2026-10-10T01:09:25Z
completed_at: 2026-10-13T03:55:44Z
branch: codex/news-crypto-policy-20261013
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

- [x] Supported reporting, regulation and explicit negation are distinguished
      from a recommendation to trade, without weakening actual advice checks.
- [x] Existing held-candidate decisions and drafts are not automatically approved.

## Steps

- [x] Reproduce the three stored examples' false-positive contexts and contrasting
      actionable advice with representative wording (see Notes).
- [x] Define a narrow context rule or replace the unconditional match with an
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
- Regression fixtures cover the Bitfinex denied sale, ESMA regulated buying/selling
  service, MoonPay not-advice FAQ, and Evernorth shareholder lockup contexts. The
  source JSON was unavailable in this worktree, so these are reconstructed phrases
  rather than byte-for-byte copies of the saved drafts. Contrasting direct advice
  is checked in zh-TW, zh-CN, en, ja and ko, including advice against selling.
- The hard gate now reads localized prose and treats transaction verbs and price
  movement alone as reporting. It still blocks explicit reader instructions and
  buy/sell signals. The change does not touch stored candidates, reviews or drafts;
  the existing editorial judge must still decide market-led stories such as Bitmine.
- Verification in the isolated worktree: 62 policy tests passed; 802 news tests
  passed with 6 existing skips; Ruff, mypy app/tests, and check:tasks passed.
  Full API pytest was started and interrupted at about 15% because the 7,680-test
  run was much longer than the affected news suite; no failure had appeared.
