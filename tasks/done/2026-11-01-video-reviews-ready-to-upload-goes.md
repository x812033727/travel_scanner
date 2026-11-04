---
id: 2026-11-01-video-reviews-ready-to-upload-goes
title: Video reviews: ready-to-upload goes under the catalog, each card collapsed by default
status: done
priority: P2
area: web
owner: claude-opus-5.5
claimed_at: 2026-11-01T11:02:44Z
created_at: 2026-11-01T11:01:56Z
completed_at: 2026-11-01T11:08:06Z
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
---

# Video reviews: ready-to-upload goes under the catalog, each card collapsed by default

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [x] On /admin/videos the 可以上架 group sits under 全部影片 (above 需要你), and each ready video is one folded line until opened.

## Steps

- [x] ProjectList order; ReadyCard folded by default, fetching its package only when opened; the open-video button does not toggle it.
- [x] admin-video-reviews.test.tsx: region order, folded state, no package request before opening (85 passed; tsc and eslint clean).

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Notes

Owner, 2026-11-01: 「可以上架不要在最上面，應該在全部影片下面；可上架的要可以折疊，預設每部摺疊。」
