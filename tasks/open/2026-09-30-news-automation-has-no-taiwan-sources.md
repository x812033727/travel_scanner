---
id: 2026-09-30-news-automation-has-no-taiwan-sources
title: News automation has no Taiwan sources: add readable feeds from FSC, MODA, the central bank and others
status: review
priority: P1
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T11:05:11Z
created_at: 2026-09-30T11:04:56Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
  - apps/api/app/news_automation/fetch.py
  - apps/api/app/news_automation/feeds.py
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# News automation has no Taiwan sources: add readable feeds from FSC, MODA, the central bank and others

## Why

`sources.json` has no Taiwan source at all, although the site's readers are in Taiwan. Batch 4.8
hand-wrote ten stories the automation missed, every one because its publisher is not a source
(Taiwan's central bank among them). Found 2026-09-30 by fetching every source in `sources.json` the way the scanner does (listing, then the two newest articles, UA `Mokaair-editorial/1.0`), from a cloud container rather than the host.

## Definition of done

- [x] Each Taiwan candidate tested from the scanner's code path: listing parses, entries
      carry dates, article pages return 200 and `read_article` keeps the story.
- [x] The readable ones added to `sources.json` with a `note` and a small `max_entries_per_scan`;
      the unreadable ones listed here with the reason (SPA shell, 403, no listing).
- [ ] Loaded on the host with `sources_cli` after the deploy.

## Notes

- Candidates: FSC (金管會), MODA (數位發展部) and its Administration for Cyber Security,
  the central bank (中央銀行), NSTC (國科會), NCC (known SPA, see DELTA-4-7 item 11).
- 2026-09-30, first finding: **no gov.tw page could be read at all.** Production runs
  `python:3.13-slim`, whose default TLS context is strict X.509, and the TWCA chain of every
  Taiwan government site tested (cbc, fsc, moda, nstc) fails it with "Missing Subject Key
  Identifier". `fetch.tls_context()` drops only that flag; expired and wrong-host certificates
  are still refused (tested against badssl.com), with a unit test on the flags.
- Added: **MODA** (home page as an HTML listing of `/press/press-releases/`, five newest, pages
  1,100-1,400 characters) and **FSC** (news list page, items told apart from the menu by
  `include_query_contains: mcustomize=news_view.jsp`, only crypto titles via
  `include_title_keywords`, extracted from `.maincontent` so the view counter stays out of the
  evidence hash). Both `max_entries_per_scan` 3. `feeds.py` gained those two config keys.
- Not added, and why:
  - **Central bank** (`cbc.gov.tw/tw/rss-302-1.xml`): the feed is 3.4 MB, over the fetcher's
    2 MB cap, the extractor keeps 0 characters of its pages, and the newest items are monthly
    statistics. Needs its own look (a smaller list page, `article_classes`).
  - **NSTC** (`/folksonomy/rss?l=ch`): the feed declares a DTD, which the XML parser refuses by
    design. An HTML listing of its news page is the next thing to try.
  - **NCC**: Angular SPA (DELTA-4-7 item 11).
- Tested with httpx through this container's proxy: `SafeNewsFetcher` pins the resolved IP,
  which the container's egress proxy does not allow, so the end-to-end check is the host's
  `sources_cli` dry run after the deploy (it fetches each source and its newest article).
- Later the same day: **central bank and NSTC added too.** The central bank's 45 KB
  press-release list page (`/tw/lp-302-1.html`) replaces the 3.4 MB feed, `.cp` is the release
  body, and only crypto and digital-currency titles are kept (its current 20 are all statistics,
  so it files nothing today). NSTC's news list page (`/folksonomy/list/9aa56881-…`) replaces
  the DTD feed, `#templateF` is the release with its headline, and only technology titles are
  kept. NCC remains out (SPA).
