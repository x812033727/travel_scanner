---
id: 2026-09-24-skip-stale-feed-entries-when-a
title: Skip stale feed entries when a news source is scanned
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T02:39:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# Skip stale feed entries when a news source is scanned

## Why

The hourly news scanner turns every feed entry it has not seen into a candidate, however
old. A feed lists weeks or months of posts (OpenAI's has 100 entries over 44 days,
Hugging Face's 100 over five months), and `max_entries_per_scan` (default 20) only caps
how many are read per scan. So the first scan of each new source files up to 20 old posts
as candidates, and if a feed ever republishes an old entry it comes back too. When the
scanner was switched on in production on 2026-09-24, the first three sources alone filed
87 candidates, most of them old posts.

Nothing downstream stops them. The writer is not told to reject old news, and
`event_date_problems` only rejects dates in the future, after the evidence, or out of
step with the slug. First-party candidates mostly stop at the evidence gate and pile up
in manual review (no model cost, but they crowd out real work, and the review list only
shows the newest 100 candidates). Press candidates that do pass the gate spend Jev's
daily budget (up to six calls each) and about ten MiniMax calls on news that is weeks
old.

## Definition of done

- [ ] A feed entry whose own date (`Entry.published_at`) is older than the source's
      freshness window is skipped before its page is fetched: no request and no
      candidate.
- [ ] The window is per source (`config.max_entry_age_hours`), with a default of 72
      hours, and a source can switch it off.
- [ ] How undated entries are handled is decided and written down (HTML listings such
      as Anthropic's news page carry no date in the listing; options: use the article's
      own date metadata after the fetch, or accept undated entries only after a source's
      first scan).
- [ ] The scan report on the source counts skipped stale entries separately from failed
      pages, so a `partial` status still means something went wrong.
- [ ] The candidates already filed from old posts on 2026-09-24 are dealt with in a way
      the site owner chooses (leave them, or reject `discovered`/`manual_review`
      candidates whose `source_published_at` is older than the window, with an audit
      reason).

## Steps

- [ ] Add the age check in `scan_source` right after the allow-list and seen-URL checks.
- [ ] Decide and implement the undated-entry rule.
- [ ] Record the stale count in the scan note without marking the scan `partial`.
- [ ] Set `max_entry_age_hours` where a source needs a different window in
      `sources.json`, and document the key in `docs/news-automation.md`.
- [ ] Tests: stale dated entry skipped without a fetch, fresh one kept, undated per the
      chosen rule, window switched off.
- [ ] Ask the owner about the existing backlog before touching production rows.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

On the host, after deploying: the next scan of a source adds no candidate whose
`source_published_at` is older than the window, and its `last_error` note reports the
skipped stale entries.

## Notes

- Filed at the site owner's request on 2026-09-24, right after the scanner was switched
  on (MiniMax writer and checker, Jev review, shadow mode).
- Dates come from the feed (`pubDate`, `published`, `updated`, `date`, or the JSON
  feed's `date_field`); `updated` can be newer than the event, so the check must not be
  the only freshness guard for the writer.
- Related open tasks: 2026-09-24-keep-every-news-review-item-reachable (review list
  limited to the newest 100) and 2026-09-24-attach-a-second-evidence-source-to (why
  first-party candidates stop at the evidence gate).
