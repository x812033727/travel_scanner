---
id: 2026-09-19-docs-seo-md-pet-friendly-place
title: docs/seo.md: pet-friendly place pages now emit lastmod from verified_at
status: done
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:16:38Z
created_at: 2026-09-19T09:51:00Z
completed_at: 2026-09-19T11:18:26Z
branch: claude/travel-scanner-pr-552-rpq36m
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

- [x] `docs/seo.md` describes the place rows: static child, community-gated, `verified_at` as the
      only `lastmod` source, and the read's caps, in one short paragraph beside the existing one
      about the guide children.
- [x] The "Nothing outside the guides emits `lastmod`" sentence is reworded so it is true again
      (the city guides and the other routes still emit none).
- [x] The routes table's `/pet-friendly` row, if it mentions the sitemap, says the place pages are
      listed too.

## Steps

- [x] Read `petPlaceSitemap` in `apps/web/app/sitemaps/sitemap.ts` and `petPlaceSitemapEntries` in
      `apps/web/lib/community/public.server.ts`; their doc comments hold the reasoning to summarise.
- [x] Amend the paragraph and the sentence; keep the section's existing shape.

## How to verify

```bash
grep -n "lastmod" docs/seo.md
```

Every statement about which entries carry `lastmod` must match `apps/web/app/sitemaps/sitemap.ts`:
articles (`published_at`/`modified_at`), place pages (`verified_at` only when present), nothing else.

## Notes

- Filed 2026-09-19 by claude-fable-5-1 while closing the sitemap ticket; `docs/` was outside that
  ticket's scope. Do this after that ticket's pull request merges, so the doc describes what is live.

### 2026-09-19 done in repo (claude-fable-5-1)

- The claim needed `--force`: the dependency `2026-09-14-sitemap-lists-pet-friendly-places` is
  still in `review` under the same owner, but its sitemap change is on `origin/main` (#563), so
  the doc now describes what is live.
- "Runtime sitemap and robots" gained one paragraph after the guide-children one: the place rows
  live in the `static` child after the routes, gated by the community switch; the directory is
  read with `include_uncertain=false` in pages of 50 through at most 20 pages, 3 s per page
  inside a 10 s budget; a failed page, a timeout or either cap keeps what was read; `lastmod` is
  `verified_at`, only when the API sent one. "They are the only entries carrying `lastmod`" (the
  articles) became "Each carries `lastmod`", and the closing sentence now says that outside the
  articles only the place pages emit it, the routes and hubs none.
- `docs/seo.md` has no routes table, and nothing in it named `/pet-friendly` or mentioned the
  sitemap for it, so the third item had nothing to change. Two adjacent statements the place rows
  made stale were corrected in passing: the static child's ceiling (thirteen base routes today,
  six conditional: 395 open, 365 closed, plus five rows per place) and the surface table's
  "pet public shells ... noindex" row, which is now its own row matching `pet-friendly/page.tsx`
  (indexable once the list is in the HTML) and `pet-friendly/[id]/page.tsx` (indexable once the
  record was read), `noindex, follow` otherwise.
- `grep -n "lastmod" docs/seo.md`: articles (`modified_at`, falling back to `published_at`), place
  pages (`verified_at`, only when present), hubs and routes none -- as `sitemap.ts` does.
- Documentation only; nothing to import or deploy.
