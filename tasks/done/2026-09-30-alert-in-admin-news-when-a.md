---
id: 2026-09-30-alert-in-admin-news-when-a
title: Alert in /admin/news when a source keeps skipping the same entries
status: done
priority: P2
area: api
owner: claude-opus-5-5-news-admin-followups
claimed_at: 2026-10-06T00:41:19Z
created_at: 2026-09-30T10:34:33Z
completed_at: 2026-10-06T01:13:37Z
branch: claude/news-admin-followups
depends_on: []
scope:
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_admin_operations.py
  - apps/web/components/admin-dashboard.tsx
  - apps/web/components/admin-dashboard.test.tsx
  - apps/web/lib/admin-domains-messages
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - docs/news-automation.md
---

# Alert in /admin/news when a source keeps skipping the same entries

## Why

A source whose entries fail every hour sits at `partial` with the same `last_error`, and
nothing tells the owner. OpenAI News lost every first-party story this way for days. Found 2026-09-30 while writing batch 4.9 by hand (`tasks/open/2026-09-30-news-batch-4-9-gpt-6.md`).

## Definition of done

- [x] A source that has skipped the same entry URL on N consecutive scans (N configurable,
      default 6) is flagged in `/admin/news` with the URLs and the error, and counted on the
      dashboard.
- [ ] Optional: a daily summary to the owner (existing notification channel, if any).

## How to verify

Scanner tests with a fetcher that refuses one entry on consecutive scans.

## Notes

- 2026-09-30, done without a migration: a skipped entry carries its publish date and the scanner
  retries it every hour, so an entry published 6 hours to 7 days ago that is still skipped has
  failed on every scan since. The scan then reports the source `stuck` (not `partial`) and puts
  those URLs first in `last_error`; `/admin/news` sources tab shows a warning and lists stuck
  sources first. The week cap keeps a refused back catalogue (OpenAI's feed keeps ~100 entries)
  from marking the source stuck for good. Undated HTML listings cannot be judged this way.
- Not done: a count on the dashboard and a daily summary to the owner.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus-5-5-news-4-9 (since 2026-09-30T12:15:05Z) was stale and is released so it stops locking its scope. Landed: #1041. Still open: Optional: daily summary to the owner via existing notification channel; Notes: dashboard count not done.
- 2026-10-06 (claude-opus-5-5-news-admin-followups): the dashboard count is done. The operations
  pending counts (`_live_pending_counts` in `apps/api/app/admin/operations_service.py`) carry
  `news_sources_stuck`, the enabled sources whose `last_status` is `stuck`; it stays out of
  `pending_total` and `alerts_total`, because a stuck source is an incident, not a review, and
  the cache key moved to `admin:operations:pending:v5`. The `/admin` dashboard's News card shows
  it as a second line linked to `/admin/news?tab=sources`, in red with an icon when above zero,
  and the client's Pending total leaves it out (copy `newsSourcesStuck` in the five
  `apps/web/lib/admin-domains-messages` files, not in `messages/*/admin.json`). `/admin/news` now
  counts and sorts only enabled stuck sources too, so the two numbers agree: a switched-off
  source keeps its last status but is no longer scanned. Tests:
  `test_stuck_news_sources_are_counted_apart_from_the_pending_reviews` runs the count on SQLite
  (five sources, two counted), the cache test expects v5, and two dashboard tests plus the
  extended sources-tab test cover the web side.
- "N configurable" in the first box means `STUCK_AFTER` in `scanner.py` (6 hours), a code
  constant, not a per-source setting; the stuck test at `test_news_automation.py`
  (`test_a_source_that_keeps_failing_on_a_recent_entry_is_reported_stuck`) pins it. A per-source
  `config.stuck_after_hours` is described in the follow-up in case anyone asks for it.
- The optional daily summary is not built: the site has no channel for messages to the owner
  (community SMTP sends account mail to users, LINE push sends price alerts to users who linked
  LINE), and choosing one is the owner's call. It moves to
  `2026-10-06-daily-summary-of-stuck-news-sources`.
- Scope was narrowed to the files this change touches; `scanner.py`, `test_news_automation.py`
  and `admin-news-messages` were the scope of the #1041 part.
