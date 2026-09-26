---
id: 2026-09-26-article-pages-keep-their-query-string
title: Article pages keep their query string when ads are on
status: done
priority: P1
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-26T03:18:04Z
created_at: 2026-09-26T03:17:57Z
completed_at: 2026-09-26T03:42:00Z
branch: claude/article-query-string
depends_on: []
scope:
  - apps/web/app/(ads-public)/[locale]/layout.tsx
  - apps/web/app/(ads-public)/[locale]/layout.test.tsx
  - apps/web/lib/adsense.ts
  - apps/web/lib/adsense.test.ts
  - apps/web/lib/adsense.server.test.ts
  - apps/web/proxy.ts
  - apps/web/components/ads/adsense-loader.tsx
  - apps/web/components/ads/article-ad-slot.tsx
  - apps/web/components/ads/article-ad-slot.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/e2e/guides-adsense.spec.ts
---

# Article pages keep their query string when ads are on

## Why

On the production site every article page (`/{locale}/guides/{intel,howto}/{slug}` and
`/{locale}/life/{slug}`) answers a URL with a query string with a 307 to the bare path, so
`?utm_source=youtube&utm_medium=video&utm_campaign=<slug>` from the YouTube pipeline
(`tools/video/package/metadata.mjs`, `tools/video/core/metadata.mjs` `articleUrl`) and any
newsletter or social campaign tag never reaches the page. Hubs and the home page keep their
query. Measured 2026-09-26 with curl: `/zh-TW/life/ai-free-vs-paid-plans-2026?utm_source=youtube`
-> 307 `location: /zh-TW/life/ai-free-vs-paid-plans-2026`; without a query -> 200.

The redirect is not nginx or next-intl. It is `app/(ads-public)/[locale]/layout.tsx`, added in
#449: when AdSense is on for the request (production host, no DNT/GPC, published article,
admin switch on — true in production even though AdSense rejected the site on 2026-09-23),
`if (requestPath.includes("?")) redirect(pathname)`, a server `redirect()` and therefore a 307.
Its reason is deliberate privacy: third-party ad code can read `location.href`, so a search
term or campaign tag must not share a document with it. #583 already exempted the two
tutorial hubs because the redirect broke their shareable filters.

## Definition of done

- [x] An article URL with a query string answers 200 and keeps every parameter.
- [x] A document whose URL carries a query never loads the AdSense tag, never relaxes the CSP
      for it, and reserves no ad box — the privacy rule #449 wrote down still holds.
- [x] An article reached by client-side navigation from such a document (or from a tutorial
      hub) reserves no 280px box the tag will never fill.
- [x] The case-canonical 308 (`Narita-To-Tokyo` -> `narita-to-tokyo`) stays, and now carries
      the query string along.
- [x] Clean article URLs still carry ads exactly as before.

## Steps

- [x] `adsenseRequestGate` refuses a request whose path carries a query; `proxy.ts` passes the
      query to it so the CSP decision and the renderer's decision stay the same function.
- [x] Remove the layout's redirect; the gate now sends those requests down the ordinary,
      ad-free layout.
- [x] `ArticleAdSlot` renders only inside a document whose root loaded the tag
      (`AdsenseDocument` context, set by the `(ads-public)` root next to the loader).
- [x] `canonicalSlugOrRedirect` appends the request's query from `x-travel-pathname`.
- [x] Unit tests for each, and an e2e case on the isolated production-host server.

## How to verify

```bash
cd apps/web
npx vitest run "app/(ads-public)/[locale]/layout.test.tsx" lib/adsense.test.ts lib/adsense.server.test.ts components/ads components/guides/article-page.test.tsx
npm run build && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/guides-adsense.spec.ts
```

After deploy:

```bash
curl -sS -o /dev/null -w '%{http_code} %{redirect_url}
' -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' 'https://mokaair.com/zh-TW/life/ai-free-vs-paid-plans-2026?utm_source=youtube'
```

must print `200` with no redirect URL.

## Notes

- Chosen over "redirect but keep `utm_*`": that would hand the campaign tags to the ad tag and,
  through it, to ad buyers, which is exactly what #449 ruled out, and still costs a redirect hop.
  The cost of this route is that a query-bearing landing (and the soft navigations inside that
  document) carries no ad. With AdSense rejected that costs nothing today; once it is approved,
  note that Facebook appends `fbclid` to outbound links, so that traffic would be ad-free too.
- Soft navigation does not re-render the root layout, and Next strips `_rsc` before middleware
  (`stripInternalSearchParams` in `next/dist/server/web/adapter.js`), so the query rule only
  sees real query strings.
- GA4 still will not see the tags after this: `components/analytics-provider.tsx`
  `initializeGa4`/`sendGa4Event` set `page_location` to the sanitized path without the query.
  First-party analytics does read `utm_source`/`utm_medium`/`utm_campaign` from
  `location.search`, so it starts recording them on article landings. The GA4 half is
  `2026-09-26-ga4-page-views-carry-the-landing`.
- The `(stay22-public)` destination services pages (`/{locale}/destinations/{city}/services`)
  still redirect a query away when Stay22 is on, by the same reasoning. Not article pages, so
  left alone here; a campaign link to a services page loses its tags the same way.
- Not changed, noticed while reading: the rule is decided when a document opens. A reader who
  lands on a clean article (tag loaded) and then follows a client-side link to one of the two
  tutorial hubs keeps the tag in the document while the hub writes its search into the URL.
  The hub's own direct landing is ad-free (#583); this path is not. Unverified in a browser.
- Verified locally 2026-09-26: the new e2e case fails without the `AdsenseDocument` check
  (three `ins.adsbygoogle` boxes appear after the client-side move, with `window` unchanged,
  so it really was the same document) and passes with it. The whole spec passed on both
  projects; one run's `ads.txt` case timed out waiting for its own `next start` while both
  projects started servers at once, and passed alone.
- This worktree's Playwright 1.63 wants `chromium_headless_shell-1243`; the machine had only
  1234, so the local run pointed `launchOptions.executablePath` at the 1234 headless shell
  through an untracked config instead of downloading.
