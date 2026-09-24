---
id: 2026-09-24-keep-every-news-review-item-reachable
title: Keep every news review item reachable in the admin queue
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-24T00:27:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/service.py
---

# Keep every news review item reachable in the admin queue

## Why

`/admin/news` loads `GET /admin/news/candidates?limit=100` with no status filter and then
keeps only `manual_review`, `shadow_review`, `failed` and `published` in the browser. The
API orders by `updated_at`, so once more than 100 candidates exist (duplicates, rejected,
discovered and in-flight ones count too) older items waiting for review silently drop out
of the review list, even though the badge still counts them. During the planned 14-day
shadow period with hourly scans this happens within days.

## Definition of done

- [ ] The review list shows every candidate that needs a person, however many other
      candidates exist, with paging.
- [ ] Status filters (review, failed, published, duplicate/rejected) are available and
      survive a reload through the URL, like the other admin workspaces.

## Steps

- [ ] Accept several statuses in `GET /admin/news/candidates` (e.g. repeated `status`).
- [ ] Request the reviewable statuses from the workspace and add paging and filters.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_admin.py -q
npm run test:web -- admin-news-workspace
```

## Notes

- 2026-09-24 (task 2026-09-24-keep-news-candidates-without-enough-evidence): the API now
  takes a repeatable `status` and the workspace asks for exactly the statuses of the
  chosen list (待審查 / 已發布 / 缺證據, kept in `?queue=`), so rows of other statuses no
  longer crowd the review list. Paging beyond 100 rows is what remains here.

- Found while hardening the news automation (task
  2026-09-24-harden-hourly-news-automation-before-first).
