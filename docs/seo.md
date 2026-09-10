# Search indexing and SEO

Mokaair serves five locales from one Next.js App Router application. This document records
what is indexable, why, and the rules a change must not break. It exists because the rules
were previously nowhere: before 2026-09-10 the repository had no `robots.txt`, no
`sitemap.xml`, no structured data, and no written account of which routes were meant to rank.

The work itself is queued as tasks — see the `2026-09-10-seo-*` entries in
[`tasks/BOARD.md`](../tasks/BOARD.md). This document is the shared reasoning behind them.

## What the audit found

Three problems held at once.

**Canonical URLs pointed every page at its locale home page.** `app/[locale]/layout.tsx`
returned a fixed ``alternates: { canonical: `${siteUrl}/${locale}` }``. Next.js merges metadata
shallowly from parent to child, and `alternates` is a top-level field, so only a page that
sets its own `alternates` replaces it. Exactly one route did — the destination services page.
Every other page under `/[locale]/*` therefore told search engines it was the locale home
page. `alternates.languages` had the same defect: five `hreflang` links, all pointing at
locale home pages rather than at the five translations of the current page, and no
`x-default`.

**The index directives were inverted.** Private surfaces carried no `robots` directive at all
— the whole admin console, the planner, auth forms, per-token share links, search results.
Meanwhile the site's own content — `/explore`, `/pet-friendly`, community posts and profiles —
was hard-coded `noindex`.

**The home page has no indexable content.** `lib/discovery.ts` passes
`() => ({ enabled: false, loading: true })` as the `getServerSnapshot` argument to
`useSyncExternalStore`. `DiscoveryHomeGate` reads that value, sees `loading: true` on the
server, and renders a skeleton. The hero `<h1>`, the marketing copy and the country/city link
rail in `app/[locale]/page.tsx` are never in the response body — on any request, regardless of
whether the discovery flag is on. `/explore` behaves the same way through `DiscoveryExplorer`.
The existing home-page test does not catch this because it mocks the hook.

## URL and language rules

`i18n/routing.ts` sets `localePrefix: "always"`, so every page has a real per-locale URL:
`/en/foods`, `/ja/foods`, `/ko/foods`, `/zh-TW/foods`, `/zh-CN/foods`. There is no unprefixed
form. This is the correct shape for multilingual SEO and must not change.

- **Canonical** is the page's own URL in its own locale, without query string.
  `/zh-TW/hotspots?destination_id=tokyo` canonicalizes to `/zh-TW/hotspots`. Folding query
  variants into their base path is intentional: the filters produce the same content set, not
  distinct documents.
- **hreflang** lists all five locales plus `x-default`. Google requires the set to be
  reciprocal and self-inclusive; Next.js does not add the self link automatically, so the
  builder emits all five explicitly.
- **`x-default` is `en`.** It is the widest-reach fallback for a reader whose language the site
  does not carry. It deliberately does not point at an unprefixed path: that would depend on
  `localeDetection` redirect behaviour, which is not something to hand a crawler.
- The canonical origin is `NEXT_PUBLIC_SITE_URL` (`https://mokaair.com` in production). It is
  inlined at Docker build time and also supplied at runtime. Every URL builder reads it through
  `lib/seo.ts` so the layout, the sitemap and the structured data can never disagree.

Because `proxy.ts` matches `/((?!api|_next|_vercel|.*\..*).*)`, any path containing a dot is
excluded from locale rewriting. `/robots.txt` and `/sitemap.xml` are therefore served as-is.

## Which routes are indexable

| Category | Routes | Directive |
| --- | --- | --- |
| Public content | `/`, `/hotspots`, `/foods`, `/destinations`, `/destinations/{id}`, `/flights/status`, `/labs/airlines`, `/pricing` | indexable |
| Managed documents | `/about`, `/privacy`, `/terms`, `/contact` | indexable **only when published**; `site-information-page.tsx` already returns `noindex` for an unpublished document |
| Gated features | the six routes wrapped in `PublicFeatureGate` | indexable while the feature is enabled; `noindex` when it is closed or `site-visibility` is unreachable |
| Community and pets | `/explore`, `/pet-friendly`, `/pet-friendly/{id}`, `/community/posts/{id}`, `/community/profiles/{handle}` | `noindex` until the content is server-rendered, then indexable while the feature is public |
| Member surfaces | `/my`, `/account`, `/trips*`, `/alerts`, `/search*`, `/login`, `/register`, `/forgot-password` | `noindex` |
| Token URLs | `/share/{token}`, `/share-target`, `/account/confirm`, `/line/link`, `/{locale}/out/*` | `noindex` **and** `Disallow` |
| Admin | `/admin/**` | `noindex, nofollow` **and** `Disallow` |
| BFF | `/api/**` | `Disallow` |

Three rules govern that table.

**Never `Disallow` a path you are also `noindex`-ing.** A blocked URL cannot be fetched, so the
crawler never reads the `noindex` and the page can persist in results as a URL-only listing.
`Disallow` is for machine endpoints and unguessable token URLs that were never indexed in the
first place; `noindex` is for user-facing pages that must be removed or kept out. `/admin/**`
appears in both columns deliberately: it was never intended to be indexed, there is no existing
index entry to clear, and blocking it at the door saves crawl budget.

**Server-render before you index.** Removing `noindex` from a page whose content arrives in a
`useEffect` publishes an empty document. Every route in the community and pets row is currently
a client shell; the `noindex` stays until the content is in the server HTML.

**A degraded page must not be indexable.** `PublicFeatureGate` renders an "unavailable" page
with HTTP 200 and the page's normal metadata when `/runtime/site-visibility` fails. A backend
blip during a crawl would index empty pages, so the gated routes emit `noindex` in that state.
The directive belongs in each gated route's `layout.tsx`, not in the gate component — a
component cannot contribute metadata.

## Sitemap

One entry per locale per route, each carrying the full five-locale plus `x-default` alternate
set. Roughly 200 URLs against a 50,000-per-file limit, so there is no sitemap index and no
`generateSitemaps()`. Revisit that when hotspot, merchant or article detail URLs exist.

The sitemap does **not** call the API. The 33 destination slugs are already in the web bundle
(`PUBLIC_DESTINATIONS` in `components/travel-services/options.ts`) and the sitemap needs URLs,
not names, so it needs neither localization nor network access. This is not a preference:
`API_INTERNAL_URL` is runtime-only, Next prerenders `sitemap.ts` at build time, and the CI web
job has no API — a build-time fetch would silently bake in an empty sitemap.

A route only enters the sitemap once it is genuinely indexable. The managed document pages stay
out until `2026-09-06-legal-content-from-owner` publishes them, because listing a `noindex` URL
just accumulates "Excluded by noindex" in Search Console. They are linked from the footer, so
nothing is lost by waiting.

A guard test walks `app/[locale]/` and asserts every path in the sitemap resolves to a real
`page.tsx`. That is the only thing standing between a refactor and a sitemap full of 404s.

## Structured data

JSON-LD is emitted by a shared server component. Two details are load-bearing:

- **Escape `<`.** Merchant names, hotspot names and post titles flow into these graphs; one
  containing `</script>` would close the element. `JSON.stringify(data).replace(/</g, "\\u003c")`
  produces a JSON escape that is equivalent to `<` inside a JSON string.
- **No nonce.** `type="application/ld+json"` is a data block: the browser never executes it, so
  `script-src` does not apply. Adding a nonce would mean calling `headers()` inside the
  component, which forfeits static rendering for every page that uses it. If a real browser ever
  reports a CSP violation, revisit — the policy is Report-Only today.

| Type | Where |
| --- | --- |
| `Organization`, `WebSite` + `SearchAction` | home page only |
| `BreadcrumbList` | every nested page |
| `TouristDestination` | `/destinations/{id}`, with `geo` from the catalog's `center` |
| `ItemList` | `/destinations`, `/hotspots`, `/foods` |
| `FAQPage` | only where a real question-and-answer block is rendered |

`/pricing` does not get `Product` or `Offer`. Usage plans are not products, and mislabelled
structured data is a Search Console violation. `Article` and `Person` wait until the community
pages have server-rendered content.

## Performance

Every route under `app/[locale]/` is rendered per request: the root layout awaits `cookies()`
for session detection and `headers()` for the CSP nonce in its body, which makes
`generateStaticParams` inert. That is a deliberate design, not a defect, and SEO is not a reason
to unpick it.

Not being able to cache HTML is not the same as not being able to cache data. The public,
non-personalized endpoints — the destination catalog, hotspot rankings, the food merchant list —
currently use `cache: "no-store"` and go back to origin on every request, which lands directly in
TTFB and therefore in LCP. They should use `next: { revalidate: N }` instead, sized to how often
each actually changes. Anything carrying a session cookie or user identity stays `no-store`;
the revalidated cache is shared across users.

Two other things matter more than any config change: server-rendering the home page (see the
audit above — it is currently a skeleton, which is simultaneously the largest LCP problem, a
full-page CLS shift, and the reason the site has no indexable home page), and seeding
`/foods` with its merchant list the way `/hotspots` already seeds its ranking.

`next.config.ts` deliberately has no `images` configuration. Every `next/image` call site passes
`unoptimized`, and all five of them are on signed-in, `noindex` surfaces, so `remotePatterns`
would be dead configuration with no effect on any indexable page.

## Adding a new public page

1. Give it its own `title` and `description` keys in all five `messages/*/metadata.json`, unique
   within each locale. `app/[locale]/metadata.test.ts` walks the app directory and will find the
   page automatically; it reads the source with `/title:\s*t\("([A-Za-z]+)"\)/`, so the literal
   `title: t("yourKey")` must appear in the page file even when a shared helper builds the rest
   of the metadata. Dynamic segments (`[id]`) are skipped by that walk but still deserve real
   metadata.
2. Decide `index` or `noindex` using the table above. If the content is client-fetched, the
   answer is `noindex` until it is not.
3. Add it to `SITEMAP_ROUTES` — but only once it is genuinely indexable.
4. Pick a structured-data type, or none. None is a valid answer; invented markup is not.
5. Do not add a new `messages/` namespace for body copy. `tools/check-i18n.mjs` cross-checks the
   namespace list against `lib/ui-text.ts` and `apps/api/app/ui_text/schemas.py`, so a new
   namespace drags an API change into a web change. Locale-keyed copy modules under `lib/`
   (`discovery-copy.ts`, `stay22-script-copy.ts`, `frontend-flow-copy.ts`) are the established
   pattern.

## Verifying

SEO assertions belong in vitest, not Playwright. `vitest.config.ts` excludes only `e2e/**`, so a
new `*.test.ts` is picked up automatically, whereas the CI Playwright spec list is hard-coded in
`.github/workflows/ci.yml`. Every assertion here — canonical strings, sitemap shape, robots
meta, JSON-LD escaping, whether the `<h1>` is in the HTML — is a server-output check that vitest
makes faster and more precisely.

Against a production build:

```bash
npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/robots.txt
curl -s localhost:3000/sitemap.xml | head -40
curl -s localhost:3000/en/foods              | grep -o '<link rel="canonical"[^>]*>'
curl -s localhost:3000/en/foods              | grep -o '<link rel="alternate" hreflang="[^"]*"[^>]*>'
curl -s localhost:3000/en/login              | grep -o '<meta name="robots"[^>]*>'
curl -s localhost:3000/ja/destinations/tokyo | grep -c 'application/ld+json'
curl -s localhost:3000/zh-TW                 | grep -c '<h1'
```

After deploying: submit `sitemap.xml` in Google Search Console, check `/destinations/{id}` in the
Rich Results Test, and use URL Inspection to confirm the declared canonical is the one Google
selected.
