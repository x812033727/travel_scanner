---
id: 2026-11-14-portal-wave-4-searchaction-and-news
title: Portal Wave 4: SearchAction and news-sitemap SEO fixes, LCP/CLS image priorities, and destinations/guides/videos UX upgrade
status: done
priority: P1
area: web
owner: antigravity
claimed_at: 2026-11-14T04:51:03Z
created_at: 2026-11-14T04:50:52Z
completed_at: 2026-11-14T05:05:44Z
branch: claude/portal-wave4-seo-web-ux
depends_on: []
scope:
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/page.seo.test.tsx
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/components/home-portal-tabs.tsx
  - apps/web/components/home-guides.test.tsx
  - apps/web/components/guides/card.tsx
  - apps/web/components/guides/card.test.tsx
  - apps/web/components/videos/video-card.tsx
  - apps/web/app/[locale]/videos/page.tsx
  - apps/web/app/[locale]/videos/page.test.tsx
  - apps/web/app/[locale]/destinations/page.tsx
  - apps/web/app/[locale]/destinations/page.test.tsx
  - apps/web/app/[locale]/guides/page.tsx
  - apps/web/app/[locale]/guides/page.test.tsx
  - apps/web/app/[locale]/guides/[kind]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/page.test.tsx
---

# Portal Wave 4: SearchAction and news-sitemap SEO fixes, LCP/CLS image priorities, and destinations/guides/videos UX upgrade

## Why

Auditing `apps/web` after Wave 3 surfaced five concrete SEO, Core Web Vitals, and public webpage UX gaps:

1. **Live home page omits `WebSite` `SearchAction` JSON-LD across all 5 locales**: `webSite(locale)` in `apps/web/lib/structured-data.ts` targets `/${locale}/search/articles?q={search_term_string}` (the public article search route, always enabled), yet `apps/web/app/[locale]/page.tsx` still calls `webSite(locale, hotspotsEnabled)`. Because `hotspots` is disabled on production `mokaair.com`, the live home page drops `SearchAction` on all 5 locales.
2. **Google News Sitemap (`sitemap-news.xml`) is missing from `/robots.txt`**: `apps/web/app/sitemap-news.xml/route.ts` serves the 48-hour Google News sitemap, and `llms.txt` lists it, but `apps/web/app/robots.ts` only advertises `${siteUrl}/sitemap.xml`.
3. **Missing `fetchPriority="high"` on home & hub LCP hero images and missing intrinsic dimensions on `/videos` thumbnails**: `HomePortalTabs` (`leadHero`) and `GuideCard` (`variant="featured"`) load their above-the-fold hero with `loading="eager"` without `fetchPriority="high"`, and `VideoCard` renders YouTube `hqdefault.jpg` thumbnails without `width`/`height` or `decoding="async"`.
4. **`/videos` emits `BreadcrumbList` JSON-LD with no `ItemList` graph and no visible breadcrumb trail**: `/videos`, `/destinations`, `/guides`, and `/guides/[kind]` all emit `BreadcrumbList` JSON-LD while rendering no visible breadcrumb `<nav>` in HTML, and `/videos` emits no `ItemList` structured data for the server-rendered videos.
5. **`/destinations` and `/guides/[kind]` lag behind the portal UX system**: `/destinations` still renders an unstyled `<h1>`, no mobile/desktop country quick-jump bar across its 33 cities, and plain bordered cards without `portal-card-surface`, stretched links, or stay-area preview chips; `/guides/[kind]` uses a plain bordered header and does not promote the page-1 lead article to `variant="featured"`.

## Definition of done

- [x] `apps/web/app/[locale]/page.tsx` emits `webSite(locale)` with `SearchAction` targeting `/${locale}/search/articles?q={search_term_string}` regardless of `hotspotsEnabled`, while keeping `/hotspots` and `/trips` links gated.
- [x] `apps/web/app/robots.ts` advertises both `${siteUrl}/sitemap.xml` and `${siteUrl}/sitemap-news.xml`.
- [x] `HomePortalTabs` lead hero and `GuideCard` `variant="featured"` set `fetchPriority="high"`, and `VideoCard` sets `width={480}`, `height={360}`, `decoding="async"`, and stable `#video-<slug>` anchors.
- [x] `/videos` emits `videoItemList` JSON-LD for its server-rendered videos alongside `BreadcrumbList`, and `/videos`, `/destinations`, `/guides`, and `/guides/[kind]` all render visible breadcrumb `<nav>` trails matching their `BreadcrumbList` JSON-LD.
- [x] `/destinations` renders a `portal-hero-shell` header with a country quick-jump anchor bar (`min-h-11` pills + `scroll-mt-24` sections) and `portal-card-surface` city cards showing suggested stay badge, summary, and up to 3 area chips; `/guides/[kind]` renders a `portal-hero-shell` header and promotes the unfiltered page-1 lead card to `variant="featured"`.

## Steps

- [x] Fix `webSite(locale)` call on home page (`apps/web/app/[locale]/page.tsx` + `page.seo.test.tsx`) and add `sitemap-news.xml` to `apps/web/app/robots.ts` (+ `robots.test.ts`).
- [x] Add `videoItemList` to `apps/web/lib/structured-data.ts` (+ `structured-data.test.ts`) and add `fetchPriority="high"` / thumbnail dimensions across `home-portal-tabs.tsx`, `guides/card.tsx`, and `videos/video-card.tsx` (+ tests).
- [x] Upgrade `/videos`, `/destinations`, `/guides`, and `/guides/[kind]` with visible breadcrumbs, portal hero/card styling, country quick-jump navigation on `/destinations`, and unit tests.
- [x] Run `check:tasks`, `check:i18n`, `lint:web`, `typecheck:web`, and Vitest suites cleanly before marking `done`.

## How to verify

```bash
npm run check:tasks && npm run check:i18n && npm run lint:web && npm run typecheck:web
cd apps/web && npx vitest run 'app/[locale]/page.seo.test.tsx' app/robots.test.ts lib/structured-data.test.ts components/home-guides.test.tsx components/guides/card.test.tsx 'app/[locale]/videos/page.test.tsx' 'app/[locale]/destinations/page.test.tsx' 'app/[locale]/guides/page.test.tsx' 'app/[locale]/guides/[kind]/page.test.tsx'
```

## Notes

- Scoped to be completely disjoint from in-flight PRs (`#2102`, `#2065`, `#2061`) and all active open tasks, reusing existing 5-locale translation keys (`common.guides.breadcrumb` and `destinations-copy.json`) so `apps/web/messages/*.json` are untouched.
- `videoItemList` intentionally emits `ItemList` (`ListItem` with `position`, `name`, and `url` pointing to each rendered video's canonical YouTube watch URL, plus `subjectOf` when linked to a first-party Mokaair article) rather than `VideoObject`, because `PublicVideo` carries no `description` field and Google Search Console flags `VideoObject` nodes without `description`.
