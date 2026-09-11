# Search indexing and SEO

Mokaair serves five locales from one Next.js App Router application. This document records
what is indexable, why, and the rules a change must not break. It exists because the rules
were previously nowhere: before 2026-09-10 the repository had no `robots.txt`, no
`sitemap.xml`, no structured data, and no written account of which routes were meant to rank.

The `2026-09-10-seo-*` entries in [`tasks/BOARD.md`](../tasks/BOARD.md) track the work. Six of
them have landed; each task file records what was verified and how. This document is the shared
reasoning behind all of them.

## What the audit found

Three problems held at once. The first two are fixed; the third is fixed for the home page's
structured data and still open for the page body.

**Canonical URLs pointed every page at its locale home page.** *(Fixed.)* `app/[locale]/layout.tsx`
returned a fixed ``alternates: { canonical: `${siteUrl}/${locale}` }``. Next.js merges metadata
shallowly from parent to child, and `alternates` is a top-level field, so only a page that
sets its own `alternates` replaces it. Exactly one route did — the destination services page.
Every other page under `/[locale]/*` therefore told search engines it was the locale home
page. `alternates.languages` had the same defect: five `hreflang` links, all pointing at
locale home pages rather than at the five translations of the current page, and no
`x-default`.

**The index directives were inverted.** *(Fixed.)* Private surfaces carried no `robots` directive at all
— the whole admin console, the planner, auth forms, per-token share links, search results.
Meanwhile the site's own content — `/explore`, `/pet-friendly`, community posts and profiles —
was hard-coded `noindex`.

**The home page has no indexable content.** *(Open — the files belong to two in-review
branches; see `2026-09-10-seo-server-render-home-and-explore`. The Organization and WebSite
graphs are emitted outside the gate, so those do reach a crawler today.)* `lib/discovery.ts` passes
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
| Public content | `/`, `/hotspots`, `/foods`, `/destinations`, `/destinations/{id}`, `/destinations/{id}/services`, `/flights/status`, `/labs/airlines`, `/pricing` | indexable |
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
set — 365 URLs today, against a 50,000-per-file limit, so there is no sitemap index and no
`generateSitemaps()`. Revisit that when hotspot, merchant or article detail URLs exist.

`robots.ts` and `sitemap.ts` are prerendered, and `siteUrl` is fixed at build time. That is not a
limitation to work around: `NEXT_PUBLIC_*` is inlined into the server bundle, so making the routes
dynamic reads the same baked value — it buys nothing. `apps/web/Dockerfile` fails the build
outright when the arg is missing, so there is no "built without an origin" case to defend against.

Neither route emits `lastmod`. Google honours it only where it tracks real content change, and
nothing here knows when a city guide's places last moved — that lives behind the API the sitemap
deliberately does not call. An omitted field is a missing signal; one that always says "now"
teaches Google to distrust the whole file.

The sitemap does **not** call the API. The 33 destination slugs are already in the web bundle
(`PUBLIC_DESTINATIONS` in `components/travel-services/options.ts`) and the sitemap needs URLs,
not names, so it needs neither localization nor network access. This is not a preference:
`API_INTERNAL_URL` is runtime-only, Next prerenders `sitemap.ts` at build time, and the CI web
job has no API — a build-time fetch would silently bake in an empty sitemap.

A route only enters the sitemap once it is genuinely indexable. The managed document pages stay
out until `2026-09-06-legal-content-from-owner` publishes them, because listing a `noindex` URL
just accumulates "Excluded by noindex" in Search Console. They are linked from the footer, so
nothing is lost by waiting.

A guard test walks both `app/[locale]/` and `app/(stay22-public)/[locale]/`, letting a
`[dynamic]` folder stand in for a literal segment, and asserts every path in the sitemap resolves
to a real `page.tsx`. That is the only thing standing between a rename and a sitemap full of 404s.
It carries a guard of its own — a path that does not exist must be reported missing — because a
walk that silently stops matching would make every case pass vacuously.

A destination whose slug the API catalog does not carry answers 404, not 500. Those are different
failures: a catalog that cannot be read at all is an outage and should say "come back later",
while a catalog that loaded without this slug means the destination really is absent. The first
version conflated them, and a URL-by-URL audit of the sitemap surfaced it as 29 guides returning
500.

## Structured data

JSON-LD is emitted by a shared server component. Two details are load-bearing:

- **Escape `<`.** Merchant names, hotspot names and post titles flow into these graphs; one
  containing `</script>` would close the element. `JSON.stringify(data).replace(/</g, "\\u003c")`
  produces a JSON escape that is equivalent to `<` inside a JSON string.
- **No nonce.** `type="application/ld+json"` is a data block: the browser never executes it, so
  `script-src` does not apply. Adding a nonce would mean calling `headers()` inside the
  component, which forfeits static rendering for every page that uses it. If a real browser ever
  reports a CSP violation, revisit — the policy is Report-Only today.

| Type | Where | Why not elsewhere |
| --- | --- | --- |
| `Organization`, `WebSite` + `SearchAction` | home page only | one canonical place per site |
| `BreadcrumbList` | the content pages: `/hotspots`, `/foods`, `/destinations`, `/destinations/{id}` | `/pricing`, `/flights/status` and `/labs/airlines` are tools, not content; a two-level `Home › Plans` trail tells a reader nothing the URL does not |
| `TouristDestination` | `/destinations/{id}`, `geo` from the catalog's `center` | — |
| `ItemList` | `/destinations` only | a `ListItem` needs a URL to be worth emitting, and hotspot and merchant entries have no pages of their own |
| `FAQPage` | **not implemented** | there is no question-and-answer block on any page to describe |

`TouristDestination` deliberately carries no `inLanguage`: it derives from `Place`, and `inLanguage`
is a `CreativeWork` property that validators flag as unexpected. It is correct on `WebSite`.

A builder returns `null` rather than an empty graph — an empty `itemListElement` is a Rich Results
"invalid object" — and the component drops nulls instead of writing them into the document.

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

`/foods` now seeds its merchant list the way `/hotspots` already seeded its ranking, so the page
ships merchants rather than filter controls with nothing behind them. The server fetches only the
unfiltered first page — which is what a crawler asks for — and the client reuses it only when this
reader also arrived without filters.

Server-rendering the home page is the one large item still outstanding. It is simultaneously the
biggest LCP problem, a full-page CLS shift, and the reason the site has no indexable home page
body; the files belong to two in-review branches, so it is queued rather than done.

Two things about the cache are worth knowing before debugging it. Next keys the fetch cache per
request headers, so `X-Travel-Locale` keeps the locales apart — worth re-checking after any change,
because a cache keyed on URL alone would serve one language's data to every reader. And the cache
lives in `.next/cache/fetch-cache`, which survives a server restart: to test whether a cold load
really goes to the API, delete it first.

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

## Known gaps in the `(stay22-public)` tree

`/{locale}/destinations/{id}/services` is 165 of the 365 sitemap URLs, and it lives in a second
root layout under `app/(stay22-public)/`. That whole tree belongs to another task's scope, so the
following are recorded rather than fixed:

- **It builds its own `alternates`** in `components/travel-services/destination-services-page.tsx`
  instead of using `lib/seo.ts`, and omits `x-default`. The sitemap publishes `x-default` for the
  same URLs, so the page markup and the sitemap declare different hreflang sets — the exact drift
  `lib/seo.ts` exists to prevent, on the one route that bypasses it.
- **All 165 share one meta description.** The page uses `t("intro")`, which takes no arguments,
  so every city ships "Stay, explore and arrive ready…" and titles that differ only by city name.
  `app/[locale]/metadata.test.ts` cannot catch this: its walk starts at `app/[locale]` and never
  enters the route group.
- **`/destinations/osaka/services` and `/destinations/kyoto/services` resolve** because the page
  accepts `CITIES` as well as `PUBLIC_DESTINATIONS`. They self-canonicalize, duplicate
  `/destinations/osaka-kyoto/services`, and their guides (`/destinations/osaka`) 404. They are
  kept out of the sitemap; the canonical belongs on the services page itself.
- **No JSON-LD, and no `SiteFooter`** — so those 165 URLs carry no breadcrumb and none of the
  site-wide footer links, including the one to `/destinations`.

Whoever next owns that tree should point its metadata at `lib/seo.ts` and give each city its own
description.
