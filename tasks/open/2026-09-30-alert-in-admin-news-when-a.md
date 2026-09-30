---
id: 2026-09-30-alert-in-admin-news-when-a
title: Alert in /admin/news when a source keeps skipping the same entries
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-30T10:34:33Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scheduler.py
  - apps/api/app/news_automation/router.py
  - apps/web/components/admin-news-workspace.tsx
---

# Alert in /admin/news when a source keeps skipping the same entries

## Why

A source whose entries fail every hour sits at `partial` with the same `last_error`, and
nothing tells the owner. OpenAI News lost every first-party story this way for days. Found 2026-09-30 while writing batch 4.9 by hand (`tasks/open/2026-09-30-news-batch-4-9-gpt-6.md`).

## Definition of done

- [ ] A source that has skipped the same entry URL on N consecutive scans (N configurable,
      default 6) is flagged in `/admin/news` with the URLs and the error, and counted on the
      dashboard.
- [ ] Optional: a daily summary to the owner (existing notification channel, if any).

## How to verify

Scanner tests with a fetcher that refuses one entry on consecutive scans.
