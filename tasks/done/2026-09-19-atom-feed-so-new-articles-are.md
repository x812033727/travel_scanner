---
id: 2026-09-19-atom-feed-so-new-articles-are
title: Atom feed so new articles are discovered quickly
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-19T15:16:12Z
created_at: 2026-09-19T15:16:01Z
completed_at: 2026-09-19T16:00:07Z
branch: claude/google-indexing-issues-efbfb9
depends_on: []
scope:
  - apps/web/app/feed.xml
  - apps/web/lib/seo.ts
  - apps/web/app/[locale]/layout.tsx
---

# Atom feed so new articles are discovered quickly

## Why

The site owner publishes news and guides in batches and wants them searchable quickly. The
sitemap is the wrong instrument for that half of the job: it lists every article with its own
`lastmod`, which is what decides **re-crawling**, but it is one index over eleven children
totalling ~1,800 URLs and a crawler has to walk it to find the few rows that changed. A feed
is the opposite shape -- short, newest-first, cheap to poll -- and publishing both is Google's
own recommendation.

Context from the Search Console read on 2026-09-19: the sitemap had **never been submitted**
(0 rows under "已提交的 Sitemap"; submitted that day), and Google's first index data for the
property is dated 2026/9/14. 400 pages indexed, 145 not -- of which 47 are deliberate
`noindex` (filter views, `/login`, `/alerts`) and 30 are correct canonical alternates. The
real gap is discovery, not rejection: the sitemap advertises 1,798 URLs and Google knows
about ~545.

Considered and rejected first: adding `<lastmod>` to the eleven `<sitemap>` entries in the
index. It only saves fetching the unchanged children -- per-URL `lastmod` inside each child
already tells Google what to recrawl -- and the clean version needs `lib/guides.server.ts`
(held by 2026-09-14-codex-learning-series) and `app/sitemaps/sitemap.ts` (held by
2026-09-14-sitemap-lists-pet-friendly-places), plus a timestamp the summary endpoint does not
return. Poor value for the reach.

## Definition of done

- [x] `/feed.xml` lists the newest articles from both public sections, newest first
- [x] a failed read does not produce an empty feed
- [x] the feed is advertised from the document head
- [x] submitted in Search Console

## Steps

- [x] `apps/web/app/feed.xml/route.ts`, Atom, `force-dynamic`, 30 entries
- [x] `FEED_PATH` in `lib/seo.ts` so the handler and the `<link rel="alternate">` cannot drift
- [x] `types: { "application/atom+xml": ... }` on the locale layout's `alternates`
- [x] 4 tests

## How to verify

```bash
npx vitest run app/feed.xml/route.test.ts     # 4 passed
```

After deploying:

```bash
curl -sA Googlebot https://mokaair.com/feed.xml | head -20
curl -sA Googlebot https://mokaair.com/zh-TW | grep -o 'application/atom[^>]*'
```

Then add `https://mokaair.com/feed.xml` in Search Console under Sitemaps. Google accepts a
feed there; it is polled far more often than the sitemap index.

## Notes

**One locale on purpose.** 1,036 of 1,720 article-locale rows are zh-TW and 885 articles are
zh-TW-only, so a feed mixing five languages would bury the thing it exists to announce.
Per-locale feeds are an easy later addition -- the route reads `defaultLocale` in one place.

**Not added to `robots.ts`'s `Sitemap:` line.** A feed is not a sitemap; listing it as one
puts its URL into the coverage report as a page. It is advertised the way feeds are, and
submitted by hand.

**Both sections are queried explicitly** rather than relying on an unfiltered `/guides` call:
`lib/guides.server.ts:68-70` records that the API intersects `section` and `kind`, and a feed
should not depend on what an unfiltered request happens to mean.

The 503-on-failed-read is the same rule as
`2026-09-19-a-failed-settings-read-tells-google-noindex`: never assert "there is nothing here"
from a read that did not answer.
