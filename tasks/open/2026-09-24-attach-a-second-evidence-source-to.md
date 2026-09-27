---
id: 2026-09-24-attach-a-second-evidence-source-to
title: Attach a second evidence source to first-party news candidates
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T00:27:44Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
---

# Attach a second evidence source to first-party news candidates

## Why

The news pipeline publishes nothing on fewer than two `evidence` pages, one of them
first-party (`news_evidence_insufficient` → manual review). The scanner finds the second
page only by following links inside the article it just read. That works when a press
article links to the official announcement. It almost never works the other way: an
official blog post from a first-party feed rarely links to independent coverage, so
every candidate discovered from a first-party feed arrives with one evidence page and
stops in manual review. Retrying does not help, because evidence is never refetched or
extended after the scan.

## Definition of done

- [ ] When a later scan reads an evidence page (from any enabled evidence source) that
      links to, or is the same event as, an open candidate's first-party page, that page
      is attached to the candidate as evidence and the candidate is re-queued.
- [ ] Attaching is idempotent, respects the existing host allow-list and SSRF rules, and
      never attaches `lead_only` pages as evidence.

## Steps

- [ ] Decide the matching rule (exact outbound link to the candidate's canonical URL is
      the safe first step; semantic matching through Jev is a second step).
- [ ] Attach, update `evidence_hash`, re-queue candidates waiting on
      `news_evidence_insufficient`, with scanner tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

## Notes

- Found while hardening the news automation (task
  2026-09-24-harden-hourly-news-automation-before-first). Measure it in the shadow period
  first: the share of candidates ending in `news_evidence_insufficient` tells how urgent
  this is.
