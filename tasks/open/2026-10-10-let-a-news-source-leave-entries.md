---
id: 2026-10-10-let-a-news-source-leave-entries
title: Let a news source leave entries out by title and add the VS Code feed
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-10T08:30:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
  - docs/official-ai-accounts.md
---

# Let a news source leave entries out by title and add the VS Code feed

## Why

A source can keep entries by title (`include_title_keywords`) but cannot leave any out.
The VS Code feed (`https://code.visualstudio.com/feed.xml`) is why it matters: on
2026-10-10 it listed the next version as "(Insiders)" with a date in the future. Read as
it is, that entry would be filed before the release exists, and once its URL is seen the
real release notes at the same address are never read again.

## Definition of done

- [ ] `exclude_title_keywords` in a source's config drops entries whose title contains
      one of the words, for every format, before the per-scan cap.
- [ ] The VS Code updates feed is a source, without its Insiders entries, validated
      through the scanner.
- [ ] `docs/news-automation.md` and `docs/official-ai-accounts.md` say so.

## Steps

- [ ] `feeds.parse_entries`: apply the exclusion next to `include_title_keywords`.
- [ ] A test beside `test_html_listing_filters_by_query_string_and_every_format_by_title_keyword`.
- [ ] Check what the feed does when the Insiders entry becomes the release: same URL or a
      new one. If the URL is the same, the exclusion is enough only if the title changes.
- [ ] Add the row and its pinned test; update the documents.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_sources_cli.py -q
```

## Notes

- The observation about the feed is from a curl probe on 2026-10-10, not from a run
  through the scanner; confirm it first.
