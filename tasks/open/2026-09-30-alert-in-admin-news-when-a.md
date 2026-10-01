---
id: 2026-09-30-alert-in-admin-news-when-a
title: Alert in /admin/news when a source keeps skipping the same entries
status: review
priority: P2
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T12:15:05Z
created_at: 2026-09-30T10:34:33Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages
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
