---
id: 2026-10-06-confirm-search-console-services-duplicates
title: Confirm Search Console stopped reporting destination services pages as duplicates
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-06T01:37:47Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-06-confirm-search-console-services-duplicates.md
---

# Confirm Search Console stopped reporting destination services pages as duplicates

## Why

On 2026-09-22 Search Console listed 23 `/zh-TW/destinations/<city>/services` pages under
「這是重複網頁；Google 選擇的標準網頁和使用者的選擇不同」. The pages differed only by the city
name in the title. The owner chose `noindex, follow` for every services page, and #661 shipped
it, also removing the pages from the sitemap. Both are live (checked 2026-10-06, see Notes).
Whether Google has recrawled the pages and moved them out of the duplicate report can only be
seen in Search Console, which only the owner can sign in to.

## Definition of done

- [ ] Search Console's 網頁索引狀態 report no longer lists any `/destinations/*/services` URL
      under 「這是重複網頁；Google 選擇的標準網頁和使用者的選擇不同」. The URLs show up under
      「已排除：noindex」 instead, or drop out.

## Steps

- [ ] Owner: open 網頁索引狀態 and read the duplicate row and its examples. Note the report's
      "last updated" date.
- [ ] If services URLs are still listed, run URL inspection on one of them. If Google last
      crawled it before the noindex went live, wait and look again later. If it crawled after
      and the URL is still a duplicate rather than excluded by noindex, reopen the
      investigation in `apps/web/components/travel-services/destination-services-page.tsx`
      and widen this ticket's scope.

## How to verify

```bash
UA='Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'
curl -sSL -A "$UA" https://mokaair.com/zh-TW/destinations/hiroshima/services | grep -o '<meta name="robots" content="[^"]*"'
```

That should print `noindex, follow`. The real check is the Search Console report, read by
the owner.

## Notes

- Split on 2026-10-06 (claude-opus-5-5-board-closures) from
  `2026-09-22-destination-services-pages-differ-only-by`. That ticket's code (#661) and its
  live check are done, and only its Search Console item was left.
- Live state, 2026-10-06, editorial User-Agent. Eight pages across all five locales (zh-TW
  hiroshima, nagoya, kaohsiung and sapporo; en tokyo; ja osaka; ko seoul; zh-CN taipei) return
  200 with `<meta name="robots" content="noindex, follow">` and a self-canonical. There is no
  `X-Robots-Tag` header. None of the 11 sub-sitemaps under `https://mokaair.com/sitemap.xml`
  has a `/destinations/*/services` URL.
- Background from the original ticket: report data was last refreshed 2026-09-18, the sitemap
  was first read on 2026-09-21, and #661 merged on 2026-09-22.
