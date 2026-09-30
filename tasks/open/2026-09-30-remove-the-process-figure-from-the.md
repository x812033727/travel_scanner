---
id: 2026-09-30-remove-the-process-figure-from-the
title: Remove the process figure from the 69 published automated news articles
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-30T11:10:10Z
completed_at:
branch:
depends_on:
  - 2026-09-27-every-news-article-carries-a-diagram
scope:
  - docs/news-automation.md
---

# Remove the process figure from the 69 published automated news articles

## Why

`2026-09-27-every-news-article-carries-a-diagram` stopped new automated news articles from
getting the fixed "Mokaair 編輯查核流程 … 再交由 Jev 判斷" figure (owner's decision
2026-09-30: drop it). Articles already published keep it: a read-only count on 2026-09-30
found 69 published candidates with public diagram assets (345 files, five locales each;
540 diagram assets over 108 candidates in all). Published revisions are versioned, so
removing the figure is a republish, not an edit in place.

## Definition of done

- [ ] Each published automated news article, in every published locale, has no image block
      whose `src` is a `/guides/news-assets/…-diagram-….svg`, as a new published revision.
- [ ] The diagram assets are no longer served (`is_public` false or `deleted_at` set).
- [ ] Hero, social image and every other block unchanged; a dry run lists exactly the
      affected articles first, and the owner approves the write.

## Steps

- [ ] Read-only: list candidate id, slug and locales with a public diagram asset, and check
      the live revision's blocks for the diagram `src`.
- [ ] Build the change through the existing guide revision/publish service (not raw SQL),
      with expected versions; dry run; owner approval; apply; read back.
- [ ] Mark the old diagram assets not public; record counts in `docs/news-automation.md`.

## How to verify

Public article pages for a sample of the 69 show no process figure; the asset URLs answer 404.
