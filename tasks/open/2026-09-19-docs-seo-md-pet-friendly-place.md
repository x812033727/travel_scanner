---
id: 2026-09-19-docs-seo-md-pet-friendly-place
title: docs/seo.md: pet-friendly place pages now emit lastmod from verified_at
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T09:51:00Z
completed_at:
branch:
depends_on:
  - 2026-09-14-sitemap-lists-pet-friendly-places
scope:
  - docs/seo.md
---

# docs/seo.md: pet-friendly place pages now emit lastmod from verified_at

## Why

`docs/seo.md` ("Runtime sitemap and robots") says: "Nothing outside the guides emits `lastmod`,
because the sitemap does not know when a city guide's places last moved." Since
`2026-09-14-sitemap-lists-pet-friendly-places` the static child also lists every published
`/{locale}/pet-friendly/{id}` page, and each carries `lastmod` from the place's `verified_at`
when the API sent one -- a real date, when its rules were last verified -- and no date at all
otherwise. The sentence is now false for one family of pages, and the section says nothing about
the place rows at all: where they live (the `static` child, after the routes), what gates them
(the community switch), and how the read is bounded (20 pages of 50, 3 s per page, 10 s in all,
partial reads keep what they got).

## Definition of done

- [ ] `docs/seo.md` describes the place rows: static child, community-gated, `verified_at` as the
      only `lastmod` source, and the read's caps, in one short paragraph beside the existing one
      about the guide children.
- [ ] The "Nothing outside the guides emits `lastmod`" sentence is reworded so it is true again
      (the city guides and the other routes still emit none).
- [ ] The routes table's `/pet-friendly` row, if it mentions the sitemap, says the place pages are
      listed too.

## Steps

- [ ] Read `petPlaceSitemap` in `apps/web/app/sitemaps/sitemap.ts` and `petPlaceSitemapEntries` in
      `apps/web/lib/community/public.server.ts`; their doc comments hold the reasoning to summarise.
- [ ] Amend the paragraph and the sentence; keep the section's existing shape.

## How to verify

```bash
grep -n "lastmod" docs/seo.md
```

Every statement about which entries carry `lastmod` must match `apps/web/app/sitemaps/sitemap.ts`:
articles (`published_at`/`modified_at`), place pages (`verified_at` only when present), nothing else.

## Notes

- Filed 2026-09-19 by claude-fable-5-1 while closing the sitemap ticket; `docs/` was outside that
  ticket's scope. Do this after that ticket's pull request merges, so the doc describes what is live.
