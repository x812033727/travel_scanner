---
id: 2026-09-30-claude-platform-release-notes-feed-let
title: Claude Platform release notes feed: let a source use its feed summary as evidence
status: review
priority: P2
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T12:10:03Z
created_at: 2026-09-30T11:25:23Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
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

- [x] A source config key (e.g. `evidence_from_feed_summary`) makes the scanner use the entry
      summary as the evidence text and the entry URL, fragment included, as canonical URL.
- [x] Publication revalidation (`validation.revalidate_evidence`) re-reads such evidence from
      the feed, not the page, so a changed release-notes page does not mark it changed.
- [x] The source added to `sources.json`.

## Notes

- Done 2026-09-30: `feeds.summary_is_evidence` / `summary_article`; the scanner skips the page
  fetch for such a source; `revalidate_evidence`, `refresh_evidence` and
  `validate_source_configuration` read the entry from the feed (once per source per call) and
  fall back to reading the page for a URL the feed does not list, so a page of the same site
  linked from another source still revalidates. Test:
  `test_a_feed_whose_summary_is_the_story_is_scanned_and_revalidated_from_the_feed`.
