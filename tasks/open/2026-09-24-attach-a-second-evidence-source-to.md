---
id: 2026-09-24-attach-a-second-evidence-source-to
title: Attach a second evidence source to first-party news candidates
status: review
priority: P2
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T11:25:43Z
created_at: 2026-09-24T00:27:44Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
  - apps/web/lib/admin-news-messages
  - docs/news-automation.md
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

- [x] Decide the matching rule (exact outbound link to the candidate's canonical URL is
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
- 2026-09-30 (claude-opus-5-5-news-4-9): done for the case that now matters most. Since the
  owner decision of 2026-09-25 one evidence page is enough to draft and a first-party page
  is enough to publish, so a first-party candidate no longer waits on a second site. What
  waits is a story with *no* usable evidence: a refused page kept as a feed-summary lead
  (`news_page_refused`, same day) or a candidate with only lead-only pages. `scan_source`
  now attaches a readable page from an `evidence` source that links to such a candidate
  (exact link, ignoring query, fragment and trailing slash), requeues the candidate and
  closes the report as `duplicate` / `news_attached_as_evidence`, with
  `test_a_report_linking_to_a_waiting_story_becomes_its_evidence`.
- Not done: attaching a second site to a candidate that already drafts (only useful for
  automatic publication without a first-party page), and matching by event rather than
  by link (Jev). Left open for that; release it if nobody wants them.
