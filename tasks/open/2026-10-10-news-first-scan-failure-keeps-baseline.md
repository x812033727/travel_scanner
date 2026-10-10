---
id: 2026-10-10-news-first-scan-failure-keeps-baseline
title: News scanner: a first scan that fails must not use up the baseline
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-10T15:13:09Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
---

# News scanner: a first scan that fails must not use up the baseline

## Why

A source's first scan is a baseline: everything already on an HTML listing is recorded as
`rejected/news_baseline` and nothing is fetched or written, so only entries that appear later
become news. `scan_source` decides "first" by `first_scan = source.last_scanned_at is None`
(`apps/api/app/news_automation/scanner.py`, about line 399), and the failure path (about lines
681-689) also writes `source.last_scanned_at = now`. So when the first scan fails while reading
the listing (robots.txt answering 403 raises `UnsafeNewsUrl` in `fetch.py`, a timeout, a 5xx),
the second scan is no longer a first scan: the baseline is never applied, and an HTML listing's
entries carry no date for the staleness check to catch. Every old article on the listing is
fetched and queued as a candidate.

Found on 2026-10-10 by the pre-deploy review of #1420 and reproduced against that commit's
`scan_source` with a fake fetcher and the Anthropic engineering row's configuration (25 links):
a successful first scan gives 25 `rejected/news_baseline`, 0 pages fetched, 0 candidates; a
first scan that raises `UnsafeNewsUrl` is followed by a second that fetches 25 pages and queues
25 candidates. This is existing behaviour, not something #1420 wrote, but #1420 adds three HTML
listings (Claude blog, Anthropic engineering, OpenRouter announcements; about 45 entries
together) on hosts whose Cloudflare the load ticket already records answering 403 to a few
requests in a few minutes. Each candidate costs at least a duplicate check and a writer call,
all three rows are first-party, and with automatic mode and AI auto-publish on, a single page
can publish without a person; `event_date_problems` does not refuse an old date. RSS sources
are not affected: their old entries have dates and fall outside the 72-hour window.

## Definition of done

- [ ] A scan that fails before the baseline was taken leaves the source still owed its
      baseline: the next successful scan records what is on the listing as `news_baseline`
      and queues nothing. (For example: do not write `last_scanned_at` on a failed first scan,
      or keep a separate "baseline taken" fact; the retry schedule must still advance so a
      failing source is not hammered.)
- [ ] A test with a fetcher that fails once and then succeeds: 0 pages fetched, 0 candidates,
      every listing entry `rejected/news_baseline`.
- [ ] `2026-10-10-load-the-changelog-and-developer-news` says whether it waited for this fix
      or loaded first and checked each new HTML listing's first scan by hand.

## Steps

- [ ] Read `scan_source`, `claim_due_sources` and how `next_scan_at` is computed on failure.
- [ ] Decide what marks "baseline taken" and whether sources already in the database need a
      backfill (a source with `last_scanned_at` set and no `news_baseline` rows).
- [ ] Test, then tell the session that owns the load ticket.

## How to verify

`cd apps/api && uv run pytest tests/test_news_automation.py -k baseline`; on the host after the
sources are loaded, each new HTML listing has `news_baseline` rows from its first successful
scan and no burst of `discovered` rows.

## Notes

- 2026-10-10 filed from the pre-deploy review of the range that carried #1420 (a reviewer and
  an independent skeptic both reproduced the reasoning from the code). Until it is fixed: after
  `sources_cli --apply`, check every new HTML listing's first scan before the next hour's scan
  and disable a row whose first scan failed.
- Also seen by the same review, for the load ticket: `sources_cli --apply` creates a second
  row named 「Claude blog」 (the URL changed, and rows are matched by URL) and leaves the old
  `https://claude.com/blog` row enabled; it has to be disabled on /admin/news.
