---
id: 2026-09-24-skip-stale-feed-entries-when-a
title: Skip stale feed entries when a news source is scanned
status: done
priority: P2
area: api
owner: claude-opus-5-5-news-stale-feed
claimed_at: 2026-10-02T14:52:37Z
created_at: 2026-09-24T02:39:30Z
completed_at: 2026-10-02T15:27:06Z
branch: claude/news-skip-stale-feed-entries
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

- [x] A feed entry whose own date (`Entry.published_at`) is older than the source's
      freshness window is skipped before its page is fetched: no request and no
      candidate.
- [x] The window is per source (`config.max_entry_age_hours`), with a default of 72
      hours, and a source can switch it off.
- [x] How undated entries are handled is decided and written down (HTML listings such
      as Anthropic's news page carry no date in the listing; options: use the article's
      own date metadata after the fetch, or accept undated entries only after a source's
      first scan).
- [x] The scan report on the source counts skipped stale entries separately from failed
      pages, so a `partial` status still means something went wrong.
- [ ] The candidates already filed from old posts on 2026-09-24 are dealt with in a way
      the site owner chooses (leave them, or reject `discovered`/`manual_review`
      candidates whose `source_published_at` is older than the window, with an audit
      reason).

## Steps

- [x] Add the age check in `scan_source` right after the allow-list and seen-URL checks.
- [x] Decide and implement the undated-entry rule.
- [x] Record the stale count in the scan note without marking the scan `partial`.
- [x] Set `max_entry_age_hours` where a source needs a different window in
      `sources.json`, and document the key in `docs/news-automation.md`.
- [x] Tests: stale dated entry skipped without a fetch, fresh one kept, undated per the
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

- 2026-10-02, claude-opus-5-5-news-stale-feed (branch claude/news-skip-stale-feed-entries).
  Claimed with `--force`: the overlapping claims were stale, held by
  claude-opus-5-5-news-4-9 on claude/gifted-rubin-umw5s4 (PR #1041, merged 2026-09-30) and
  codex-p1-news on codex/p1-task-audit (PR #966, merged 2026-09-29), with no open PR on
  either branch.
- What was already there: PR #1041 added the first-scan baseline (`scanner.BASELINE`): a
  source's first scan records every entry older than 72 hours, or undated, as seen
  (`rejected`, `news_baseline`) without fetching it. So the first-scan half of this task
  was done; what was missing was every later scan, where an old entry that reached the
  scanner (a republished post, a renamed URL, a page that failed until now and was retried
  every hour) still became a candidate.
- Window: `scanner.max_entry_age(source)` reads `config.max_entry_age_hours`; 72 hours by
  default, `0`, a negative number or `null` switches it off, a value that is not a number
  (a string, `true`, NaN) keeps 72 rather than switching the check off by accident, and a
  huge one is capped at ten years so `timedelta` cannot overflow. No validation at save
  time: `validation.py` and the schemas are outside this scope, and the fallback is safe.
- Order in `scan_source`: allow-list, seen URL, first-scan baseline, then the stale check.
  The first scan's baseline cutoff is now the source's window (72 hours when it is off), so
  a first scan records its back catalogue as seen instead of reporting it as stale on every
  later scan, and switching the window off never opens the back catalogue to a first scan.
  On later scans a stale entry gets no request, no candidate and no row; it is only counted.
  A seen entry is never counted (the seen check comes first).
- Report: the count goes into `last_error` as "Left out N feed entries older than 72
  hours, without fetching them", after the skip and summary notes. It does not make the
  scan `partial` and does not hold the listing's ETag back (a stale entry only gets older,
  so a 304 hiding it is fine). `/admin/news` prints `last_error` in red whatever the
  status, so a succeeded scan with stale entries shows a red informational line; changing
  that is a web change outside this scope.
- Undated entries: option two, by the listing. The first scan records them as seen; after
  that an undated entry is new to the listing and is read. The article's own date after
  the fetch was not used: it cannot save the request, which is this task's point, and it
  would need a date extractor per publisher in `feeds.py`. Known gap, written in the doc's
  Known limits: an undated listing that renames its URLs makes every entry look new.
- `sources.json`: unchanged. No source has a known reason for another window (posts that
  reach the feed days after their own date would be one); scans are hourly, so a
  low-volume feed does not need a wider window. The doc says when to raise it.
- Tests changed: the refused-lead test now gives its source a 30-day window so the 10-day
  entry still reaches the fetch and `SUMMARY_LEAD_MAX_AGE` keeps it out, and the stuck
  test switches the window off so `STUCK_UNTIL` is still what keeps the month-old entry out
  of the stuck list. Both would otherwise have stopped testing what they test. The new
  stale test fails with the stale branch disabled (checked by mutation).
- Not done: the backlog item and the "ask the owner" step. Nothing in production was read
  or changed. Filed as 2026-10-02-decide-on-news-candidates-from-old for the owner's
  decision. Per the session notes, the owner already had all 140 `needs_evidence`
  candidates (most first-party old posts) rejected on 2026-09-25.
- Takes effect after an API deploy (the news-worker runs the scanner); no migration, no
  `sources_cli --apply` needed.
