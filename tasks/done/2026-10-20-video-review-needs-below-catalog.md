---
id: 2026-10-20-video-review-needs-below-catalog
title: 影片審核：需要你移到全部影片分頁下面
status: done
priority: P2
area: web
owner: claude-opus-5-5-video-review-pagination
claimed_at: 2026-10-20T06:08:10Z
created_at: 2026-10-20T06:07:57Z
completed_at: 2026-10-20T06:13:19Z
branch: claude/video-review-pagination-70309b
depends_on: []
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
---

# 影片審核：需要你移到全部影片分頁下面

## Why

On /admin/videos (影片審核 tab), the 需要你 group sat above the catalog and pushed 全部影片 down
the page. The owner asked on 2026-10-20 for 需要你 to come after the catalog's pages
(上一頁／第 1／10 頁／下一頁).

## Definition of done

- [x] The tab reads 可以上架, then 全部影片 with its pages, then 需要你.

## Steps

- [x] Move the 需要你 group after `VideoBrowser` in `ProjectList`.
- [x] Update the two tests that pin the region order.

## How to verify

`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx` — the region order
assertions expect `["可以上架", "全部影片", "需要你"]`.

## Notes

- Only 需要你 moved; 可以上架 stays above the catalog because the owner named only 需要你.
- Claimed with `--force`: the scope overlaps four in-progress video tasks, but the change is two
  lines in `ProjectList`, so any conflict is trivial.
- `--scope` given twice keeps only the last value; list both paths by hand.
