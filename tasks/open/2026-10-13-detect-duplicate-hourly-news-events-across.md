---
id: 2026-10-13-detect-duplicate-hourly-news-events-across
title: Detect duplicate hourly news events across feed categories
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-13T04:01:10Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - apps/api/app/news_automation/duplicates.py
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# Detect duplicate hourly news events across feed categories

## Why

On 2026-10-13, the hourly Decrypt candidate
`eed553a6-baaa-4e03-b5bc-449d10c54c97` was held for a zh-CN locale
review failure even though Mokaair had already published the same October 12
Meta Muse Wonder / Wonder Full launch from The Verge at
`/zh-TW/life/ai-news-meta-muse-wonder-models-20261012`. Both report the two
models, Muse Code / API availability and Meta's performance claim. Decrypt adds
benchmark and price context but no distinct later event. A human rejected the
candidate as a duplicate with an audited reason, avoiding another paid rewrite.

The Decrypt candidate inherited `crypto` from its fixed feed while the existing
article is `ai`. `duplicates.py` currently searches recent published articles
and candidates only when their vertical equals the candidate's vertical; this
can miss an otherwise identical event when feed category is wrong. The open
candidate-category correction ticket fixes held records, not this earlier
cross-category duplicate check.

## Definition of done

- [ ] A candidate about the same event as an existing published article is
      identified for duplicate review even if their verticals differ, without
      auto-rejecting unrelated stories that share company or product names.
- [ ] The duplicate evidence includes the matched article identity, event
      rationale and an auditable decision; no existing article is altered.
- [ ] The query/model-call budget is bounded for the hourly scanner, including
      large backlogs and ambiguous CJK text. Automatic publication must not
      proceed on an unresolved credible duplicate.

## Steps

- [ ] Inspect current title/event matching and the scanner's category
      inheritance. Decide whether a cheap cross-category candidate pool can be
      screened before any paid comparison; keep the existing source/evidence
      ownership gates.
- [ ] Add focused regression cases for the Meta Muse cross-category miss and
      a same-brand different-event non-match. Document the review behavior and
      costs in `docs/news-automation.md`.

## How to verify

Run the focused duplicate tests in `apps/api/tests/test_news_automation.py`,
then inspect a seeded AI published article versus a crypto-feed report of the
same event, plus a different event about Meta. Both candidate decisions and
any model usage must be visible in the test assertions.

## Notes

- Production readback: the Decrypt candidate is `已退件`, with the reason
  pointing to the published The Verge article. The existing public article
  still renders. Receipt:
  `docs/news-hourly-review-2026-10-13.md` (same-day operations branch).
- Related but distinct: `2026-10-06-match-news-evidence-by-event` concerns
  attaching a second source to an open candidate and requires a cost decision;
  `2026-10-10-add-audited-held-news-category-correction` concerns correcting
  the category of one held candidate. Coordinate the designs before coding.
