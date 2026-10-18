---
id: 2026-10-10-read-each-dated-section-of-a
title: Read each dated section of a single-page changelog as a news entry
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-10T08:30:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
  - docs/official-ai-accounts.md
---

# Read each dated section of a single-page changelog as a news entry

## Why

Some official changelogs are one long page with a heading per date and no address of
their own for each entry, and no feed that carries the text. The HTML listing parser
takes every link on a page as an article, so it cannot read them:

- the Claude apps release notes
  (`https://support.claude.com/en/articles/12138966-release-notes`; robots.txt allows it),
- the OpenAI API changelog, and the ChatGPT and Codex changelog,
- the Gemini API changelog and the Gemini app release notes.

The owner asked on 2026-10-10 whether the Claude page could be read. Most of what it
lists also appears as articles the scanner reads ("Claude blog", "Anthropic news"). In
September and October 2026 only two items were on that page alone: "Smart reports (beta)"
and "Monthly API credits for Max and Team plans". For OpenAI and Gemini the gap is wider:
their product changelogs have no readable counterpart at all.

## Definition of done

- [ ] Measured first: a week after the 2026-10-10 sources are loaded on the host, count
      the changelog items of that week that no source brought in. Build this only if the
      count says so; otherwise close the task with the numbers.
- [ ] A source format (or config) that splits one page into entries by its date headings:
      title from the entry's heading, date from the date heading, the section's text as
      the evidence, and a stable address per entry.
- [ ] The Claude apps release notes added as a source and validated through the scanner.

## Steps

- [ ] Do the measurement and write it here.
- [ ] Decide the entry address: the page has anchors per month only, so an entry needs a
      fragment made from its date and title, and revalidation has to find it again when
      the page is re-read (compare `evidence_from_feed_summary`, which re-reads the feed).
- [ ] Decide what happens when a section is edited after it was read.
- [ ] Parser, a pinned test from the live markup, the source row, the two documents.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_sources_cli.py -q
```

## Notes

- The Claude page on 2026-10-10: month headings ("October 2026") with in-page anchors, day
  subheadings ("October 7, 2026"), then one titled entry or more under each day. Entries
  link out to help articles, anthropic.com and claude.com.
- The Claude Code changelog did not need this: its feed carries each version's text
  (in `<content:encoded>`), and it is read as a summary-evidence source.
- The feed advertised for the ChatGPT and Codex changelog was seen on 2026-10-10 with
  summaries of 15 to 47 characters and links that all lead to one page of about 800 KB
  (probed with curl, not through the scanner).
