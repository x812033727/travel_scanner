---
id: 2026-09-22-destination-services-pages-differ-only-by
title: Destination services pages differ only by their title, so Google picks its own canonical
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-22T10:43:12Z
created_at: 2026-09-22T10:39:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/travel-services/destination-services-page.tsx
  - apps/web/components/travel-services/destination-services-page.test.tsx
  - apps/web/app/sitemaps/sitemap.ts
  - apps/web/app/sitemaps/sitemap.test.ts
---

# Destination services pages differ only by their title, so Google picks its own canonical

## Why

Search Console reports 23 pages under "這是重複網頁；Google 選擇的標準網頁和使用者的選擇不同"
(duplicate, Google chose a different canonical from the one declared). Every sampled one is
`/zh-TW/destinations/<city>/services`, and fetching four of them shows why:

| city | title | description | HTML bytes |
| --- | --- | --- | --- |
| hiroshima | 廣島 · 旅行服務 | 住宿、體驗與交通，在這裡挑選，到外部網站預訂。 | 288,963 |
| nagoya | 名古屋 · 旅行服務 | *identical* | 288,944 |
| kaohsiung | 高雄 · 旅行服務 | *identical* | 288,963 |
| sapporo | 札幌 · 旅行服務 | *identical* | 288,932 |

Thirty-one bytes separate the largest from the smallest. The city name in the `<title>` is
the only thing on the page that names the city; the description is word-for-word the same,
and the services themselves render client-side from Stay22, so a crawler sees one page
repeated. Each declares itself canonical, Google disagrees, and the self-canonical is
discarded — which is exactly what that report means.

This is not a crawling or configuration fault. Google is right: as far as text goes these
are the same page.

## Definition of done

- [x] Either each city's services page carries content that is actually about that city, or
      the route is deliberately kept out of the index and says so in its own code.
      **The owner chose the second on 2026-09-22: `noindex, follow`, all of them.**
- [ ] Search Console's duplicate count for `/destinations/*/services` falls to zero on a
      later crawl.

## Steps

- [x] Decide which way this goes. The owner picked `noindex` over writing 33 city
      introductions: these are affiliate funnels reached from the destination page, and the
      crawl budget is better spent on the articles.
- [x] `robots: { index: false, follow: true }` in the shared `generateMetadata`
      (`components/travel-services/destination-services-page.tsx`), which both the Stay22
      route and its fallback re-export, so one edit covers every locale and every city.
- [x] Take them out of `SITEMAP_ROUTES`. A sitemap that advertises a `noindex` page is the
      site contradicting itself, and Search Console reports it as such.
- [x] Tests for both halves.
- [ ] Deploy, then confirm on the live site.

## How to verify

```bash
for c in hiroshima nagoya kaohsiung sapporo; do
  curl -s "https://mokaair.com/zh-TW/destinations/$c/services"     | grep -o '<meta name="description" content="[^"]*"'
done
```

Four different lines, or one `noindex` on each. Then watch the "這是重複網頁" count in
Search Console's 網頁索引狀態 report.

## Notes

- `follow`, not `nofollow`: the outbound lodging links are the page's entire purpose, and the
  destination page that links here stays indexable and carries the city-specific writing.
- The self-canonical and the hreflang set are left in place. Google ignores both on a
  `noindex` page, and the canonical still folds the query-string variants of the URL into the
  clean one, which is worth keeping while the page is still reachable.
- `apps/web/app/sitemaps/sitemap.ts` was inside the scope of
  `2026-09-14-sitemap-lists-pet-friendly-places`, which had sat in `review` since
  2026-09-19 with every box ticked. Its code (`petPlaceSitemapEntries`) is in `main`, so the
  claim was stale bookkeeping holding a scope; it is archived into `tasks/done/`.
- Found 2026-09-22 while reading Search Console for an unrelated ads.txt question. The same
  report's other rows are healthy: the 55 `noindex` pages are `/login`, `/account`, `/alerts`
  and filtered guide lists (all deliberate), the one 5xx (`/zh-CN/login?next=…`, crawled
  2026-09-15) answers 200 today, and the one soft 404 is also a `/login` URL.
- Report data was last refreshed 2026-09-18; the sitemap (2,371 URLs) was only submitted on
  2026-09-19 and first read successfully on 2026-09-21, so none of those counts have seen it
  yet.
- `/login` is crawlable and Google is spending fetches on it (it supplies both the 5xx and the
  soft 404 example). Worth its own ticket if anyone is tidying crawl budget.
