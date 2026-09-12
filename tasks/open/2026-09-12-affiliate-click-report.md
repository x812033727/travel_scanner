---
id: 2026-09-12-affiliate-click-report
title: Affiliate click report by partner, module and placement
status: in-progress
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T05:36:24Z
created_at: 2026-09-12T05:34:36Z
completed_at:
branch: claude/affiliate-controls-and-guide-cta
depends_on: []
scope:
  - apps/api/app/analytics/affiliates.py
  - apps/api/app/analytics/router.py
  - apps/api/app/affiliates/sub_id.py
  - apps/api/tests/test_analytics_affiliates.py
  - apps/web/components/admin-analytics-panel.tsx
  - apps/web/components/admin-analytics-panel.test.tsx
---

# Affiliate click report by partner, module and placement

## Why

`/admin/analytics` showed one number for affiliate clicks. Every dimension needed to decide
which partner or surface to promote (partner, module, placement, destination, brand,
target host, sub_id) is indexed in `affiliate_clicks` and was never queried.

## Definition of done

- [x] `GET /admin/analytics/affiliates?range=` returns the total, the previous-window total, the
      percentage change and the top ten per dimension, admin-only and `no-store`.
- [x] Legacy member-derived `sub_id` values are folded into `unknown`, never echoed.
- [x] The analytics page renders the section under the existing "聯盟外連" heading; a failure of
      this read leaves the rest of the dashboard intact.

## Steps

- [x] `analytics/affiliates.py` modelled on `analytics/discovery.py`.
- [x] `is_catalog_sub_id` shared between the egress gate and the report.
- [x] Section in `admin-analytics-panel.tsx`; ASCII tile titles until message keys are free.

## How to verify

```
cd apps/api && uv run pytest tests/test_analytics_affiliates.py -q
cd apps/web && npx vitest run components/admin-analytics-panel.test.tsx
```

## Notes

These are redirect counts, not bookings or commission; there is still no postback. The
window uses an inclusive end like the dashboard. `affiliate_clicks.created_at` has no index,
so a 12-month range is a sequential scan; add one when the table grows (needs `models.py`,
currently claimed by the site-experience task).
