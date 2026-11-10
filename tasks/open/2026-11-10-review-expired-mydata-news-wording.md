---
id: 2026-11-10-review-expired-mydata-news-wording
title: Review expired student loan MyData news wording
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-10T12:21:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/tech-news-moda-mydata-student-loan-20260917.json
---

# Review expired student loan MyData news wording

## Why

The static tech-news-moda-mydata-student-loan-20260917 pack contains "現在辦還來得及" alongside a September 30 deadline. A November audit identified potential stale urgency. The public article has not been compared in this task, so this is a source/content review lead, not a confirmed production defect.

## Definition of done

- [ ] Read the current public article and official period/deadline sources; establish the affected text and locales.
- [ ] Prepare a dated, independently reviewed correction or record why the existing archival context is sufficient.
- [ ] Keep merge/deploy/import/publication authorization and verification distinct.

## Steps

- [ ] Check task/worktree/PR ownership before claiming; expand scope only for confirmed affected locale/assets paths.
- [ ] Replace stale urgency with event-date context if supported by source and public readback.
- [ ] Validate the precise content pack and record publication steps if any remain.

## How to verify

Compare source, static pack and public readback; use content-pipeline factual review and pack lint for the exact slug. Do not present old deadlines as current application availability.

## Notes

- Discovered during news reader-value research on 2026-11-10. No official/public-page verification or content change has been performed for this slug.
- This task is unclaimed and does not authorize production writes.
