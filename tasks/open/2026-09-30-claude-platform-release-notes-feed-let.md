---
id: 2026-09-30-claude-platform-release-notes-feed-let
title: Claude Platform release notes feed: let a source use its feed summary as evidence
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-30T11:25:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/validation.py
  - apps/api/tests/test_news_automation.py
---

# Claude Platform release notes feed: let a source use its feed summary as evidence

## Why

`https://platform.claude.com/docs/en/release-notes/feed.xml` is Anthropic's official feed of
API release notes (Claude Sonnet 5.5's API launch on 2026-09-28 is its newest entry). Each
entry links to an anchor on one shared page (`…/overview#september-28-2026`), so the scanner
would fetch the same 40,000-character page for every entry, store it under one canonical URL
and treat every later entry as already seen. The feed's own `description` carries the day's
notes in full (about 1,200 characters), which is the evidence we want.

## Definition of done

- [ ] A source config key (e.g. `evidence_from_feed_summary`) makes the scanner use the entry
      summary as the evidence text and the entry URL, fragment included, as canonical URL.
- [ ] Publication revalidation (`validation.revalidate_evidence`) re-reads such evidence from
      the feed, not the page, so a changed release-notes page does not mark it changed.
- [ ] The source added to `sources.json`.
