---
id: 2026-09-19-orphan-pages-hotspots-foods-and-explore
title: Orphan pages: hotspots, foods and explore have no internal links
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-19T13:55:22Z
created_at: 2026-09-19T13:55:12Z
completed_at: 2026-09-19T16:00:03Z
branch: claude/google-indexing-issues-efbfb9
depends_on: []
scope:
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
---

# Orphan pages: hotspots, foods and explore have no internal links

## Why

`/hotspots`, `/foods` and `/explore` are listed in the sitemap but **nothing on the site links
to them**. Crawling production as Googlebot, the clean anchors `href="/zh-TW/hotspots"` and
`href="/zh-TW/foods"` appear zero times on `/zh-TW`, `/zh-TW/guides`, `/zh-TW/life`,
`/zh-TW/destinations` and `/zh-TW/search/articles`. The only inbound links are the
query-parameter forms `?destination_id=tokyo` on city pages, and those canonicalise to the
base page, so they pass no signal to the URL that is actually in the sitemap.

Two causes, both real:

1. `components/site-header.tsx` renders `SiteNavigation`, which is a client component gating
   on `useDiscoveryStatus()`. Its server snapshot is a fixed `{loading: true}`
   (`lib/discovery.ts:67`), so during SSR it emits a grey placeholder -- **every header link is
   absent from every page's HTML**.
2. `components/site-footer.tsx` carried 8 links and none of these three.

A sitemap entry with no inbound link is a page Google crawls once and forgets, which is the
"已找到－目前尚未建立索引" bucket. The 593 curated places and the whole verified merchant
directory sit behind the first two of these URLs.

## Definition of done

- [x] `/hotspots`, `/foods` and `/explore` are reachable by a server-rendered `<a href>` from
      every public page
- [x] a failed settings read does not remove them

## Steps

- [x] add the three to the footer's site nav
- [x] gate `/hotspots` with `featureVisible`, not `featureEnabled`
- [x] reuse the existing `hotspots` / `foods` / `bottomExplore` labels rather than inventing
      a sixth translation of "explore"
- [x] tests, including the closed-switch and unreadable-switch cases

## How to verify

```bash
npx vitest run components/site-footer.test.tsx    # 23 passed
npm run check:i18n                                # 5 locales, 25 namespaces
```

After deploying:

```bash
curl -sA Googlebot https://mokaair.com/zh-TW | grep -c 'href="/zh-TW/hotspots"'   # was 0
```

## Notes

`featureVisible` rather than `featureEnabled` is deliberate and `lib/site-features.ts:38-44`
records why: "unavailable" means the switches could not be read, not that the owner closed
everything. Since the footer is now the only inbound link these pages have, a settings blip
stripping it would re-orphan them.

`/pet-friendly` was left out. It is gated by the community switch rather than by site
visibility, and that switch is only readable through `useCommunity()`, which has the same
first-paint loading problem as the header -- adding it there would put a link in the footer
that is absent from exactly the response bodies this task exists to fix.

**The bigger half of this is still open: the header.** Making `SiteHeader` async and awaiting
`getDiscoveryStatus()` there would put `/explore`, `/guides`, `/life`, `/trips` and `/my` in
the HTML of every page, and the same for `MobileNav` and `AppBottomNav`. It is a larger,
riskier change (it alters what paints before hydration on every route) and belongs in its own
task.

**Verified on production after #566 (`ecc6cbc0`) deployed 2026-09-19 15:56 UTC.** Clean
anchors now present in the server HTML of `/zh-TW` and `/en`: `/hotspots`, `/foods`,
`/explore` -- all three were zero before.
