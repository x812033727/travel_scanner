# Search indexing and SEO

Mokaair serves five locales through Next.js. This document describes the implementation
and its limits; it does not promise indexing, ranking, or a measured performance improvement.
The original `2026-09-10-seo-*` tasks and the PR #388 review task record separate verification
results. Historical task notes describe their original snapshots, not necessarily this revision.

## URL and language rules

- Public page canonicals use `NEXT_PUBLIC_SITE_URL`, the current locale and current pathname.
  Filter/query variants canonicalize to the base page; they are not separately listed.
- `proxy.ts` overwrites the trusted pathname header; root metadata strips query strings.
  The default used to canonicalize every child page to its locale home and is now corrected.
- Shared `lib/seo.ts` builds reciprocal, self-inclusive five-language alternate sets and an
  English `x-default` fallback for the common public page tree.
- CMS documents have independent publication states in each language. Their metadata overrides
  root alternates with a self canonical only; unconfirmed translations are never advertised.
  Adding CMS hreflang later requires knowing the actual published variants, not exposing drafts.
- Guide articles (`/guides/{kind}/{slug}`) also publish per language, but the guides API reports
  which translations exist. The article page and its sitemap entries declare exactly those, with
  `x-default` only when English is among them; an unwritten translation is `noindex`.
- The separate `(stay22-public)` services tree retains its own valid canonical/language builder.
  Its optional `x-default` is supplied through the sitemap, not HTML. Google accepts HTML and
  sitemap localization annotations as equivalent methods.
- `NEXT_PUBLIC_SITE_URL` is set at build time (the Dockerfile requires it). Changing the public
  origin requires a rebuild; request-time sitemap generation does not change that fact.

## Index directives and feature visibility

| Surface | Policy |
| --- | --- |
| Home, food directory, destination directory/guides/services | Indexable public content |
| Guides hub, intel and how-to lists, published guide articles | Indexable; filtered list views and unwritten translations are `noindex` |
| Hotspots, pricing, flight status, airline fares | Indexable only while the effective Web switch is enabled |
| Privacy, terms, about, contact | Only the requested locale's published document is indexable |
| Community/discovery/pet public shells | Existing `noindex` retained pending public server content |
| Account, trips, alerts, search results, auth forms | `noindex` regardless of feature switches |
| Admin | `noindex, nofollow`, plus robots exclusion |
| Private/token links and machine endpoints | Existing privacy/auth checks plus robots exclusions |

A visibility outage is treated like a closed feature: gated layouts emit `noindex` and their
routes leave the sitemap. Destination guides do not fetch or render hotspot lists/CTAs when the
hotspot switch is off or unavailable. Marketing shortcuts and the homepage search graph follow
the same public switch. A destination's lodging/food directory remains useful independently.

Robots directives are **not authorization**. A blocked crawler cannot read a page's `noindex`;
`Disallow` alone also cannot guarantee removal of an already indexed URL. The private routes
continue to enforce their own access controls. If Search Console reveals old indexed token/admin
URLs, handle removal explicitly rather than assuming the robots file cleared them.

Our public-shell policy favors server-rendered content before relaxing `noindex`. Search engines
may execute JavaScript, but that is not a substitute for verified public/private isolation.

## Runtime sitemap and robots

`robots.ts` points to `/sitemap.xml`. The sitemap uses `dynamic = "force-dynamic"` and makes two
`no-store` reads at request time, in parallel: the six public visibility flags, and the guides
API's publication-aware list (`GET /api/v1/guides/sitemap`). This avoids freezing deployment-time
flags or published articles into the build, and needing the API during `next build`.

The static part has at most **380 URLs**: five locales times ten base routes, 33 city guides and
33 services pages. The base routes include `/guides`, `/guides/intel` and `/guides/howto`, which
have no feature switch. Four base routes are conditional; all four closed/unavailable gives
**360 URLs**. Static destination IDs come from `PUBLIC_DESTINATIONS`; no names or authenticated
data are needed to enumerate them. Every static entry carries all five languages plus `x-default`.

Guide articles follow the static entries: one per published, unexpired translation, newest first,
capped at 1,000 by the API and again by the Web loader. The API filters with the rule the list and
the article page share (`apps/api/app/guides/publication.py`), so the sitemap cannot advertise a
URL the site will not serve; an expired notice keeps its page but leaves the sitemap. Each entry's
alternates are only that article's published translations, with `x-default` only when English is
one of them: the set the article page declares. The whole file is therefore at most about
**1,380 URLs** (380 static plus 1,000 translations), far below Google's 50,000-URL / 50 MB limit,
so no sitemap index is needed. If the guides API fails or times out, the sitemap degrades to
exactly its static entries rather than failing or emptying.

`lastmod` is deliberately split. Static entries have none: the sitemap does not know when a city
guide's places change, and a value that always says "now" teaches Google to distrust the file.
Guide entries carry the API's `published_at`, a real date. It records a translation's first
publication and survives republication, so an edited article's `lastmod` does not move yet
(`2026-09-11-guide-lastmod-republication`).

Managed site documents (`/about`, `/privacy`, `/terms`, `/contact`) remain outside the sitemap
until their per-locale publication can be enumerated the same way. Published ones are still
discoverable through footer links. Private and client shell routes stay out.

Tests verify each listed static path resolves to an App Router page, language URLs agree, private
routes are absent, each feature can close/reopen without a rebuild, and guide entries follow
per-locale publication, carry their date, stay capped and fall back to the static list when the
guides API fails.

## Server content and data freshness

- Discovery **off**: the homepage includes its real hero, search body and 19 city-guide links
  in server HTML. The server snapshot seeds `DiscoveryHomeGate` instead of removing it, so a
  failed server read can recover when the shared browser status resolves. The status request
  has a three-second abort bound.
- Discovery **on**: the interactive feed still loads on the client. Full feed SSR and
  `/explore` SSR remain follow-up work; this PR does not claim those pages are completed.
- The directory has 33 localized city guides plus one index (**170 guide/index URLs**).
  Unknown IDs from a valid catalog return 404; catalog service failures are not fabricated 404s.
  A failed place/merchant listing is shown as unavailable, distinct from a confirmed empty list.
- `/foods` reads normalized URL filters server-side and seeds the matching first page.
  Results and pagination cursors belong to that query; changing filters or a failed request
  cannot retain another city's actionable cards.
- Hotspot rankings/facets, merchant lists and food taxonomy use `no-store`. Public does not
  mean immutable: moderation, source withdrawal and visibility changes must not wait behind
  Next's cross-request cache. React `cache()` still deduplicates repeated loaders in a render.
- The non-personal destination catalog alone may use a one-hour revalidation window.
  Server loaders bound new network waits; they never forward session cookies to public feeds.

Introducing cross-request caching for moderated content later requires coordinated invalidation
and tests for withdrawal, source revocation, and stale-on-error behavior. Changing a TTL alone is
not sufficient. Existing member feeds and private records must never enter a shared public cache.

## Structured data and social metadata

The server `StructuredData` component serializes plain graphs and escapes `<` as `\\u003c`
so content cannot close its script tag. It emits only nonempty graphs that describe the page.

| Graph | Surface |
| --- | --- |
| Organization and WebSite | Home |
| SearchAction | Home, only when the hotspot search is available |
| BreadcrumbList | Hotspots, foods, destination index and guides |
| ItemList | Destination index with actual guide URLs |
| TouristDestination | Guide using public catalog names/country/coordinates |

There is no invented review, FAQ or article markup. `TouristDestination` is a Place, so it does
not claim the CreativeWork-only `inLanguage` property. Purchases are not enabled; this work
does not add Product/Offer markup or represent plans as bookable offers.

SearchAction is optional descriptive metadata, **not a promised Google sitelinks search box**;
Google retired that search result feature in November 2024. JSON-LD is a non-executable data
block; no executable inline behavior is added.

Home retains brand social copy. Child pages inherit their own resolved title/description into
Open Graph and Twitter metadata through Next's metadata resolver, not the homepage wording.
Production-output browser tests cover this behavior in all five languages.

## Verification and follow-ups

Run focused Vitest tests and then:

```bash
npm run lint:web
npm run check:i18n
npm run typecheck:web
npm run test:web
npm run test:tools
npm run check:tasks
npm run build:web
```

The CI browser list includes `e2e/seo.spec.ts`: production Next output, JavaScript disabled,
desktop and Pixel 7, five-language canonicals/alternates/social tags, server homepage content,
CMS publication isolation, robots and the runtime sitemap, including synthetic guide translations'
`lastmod` and per-article alternates. Unit tests separately cover visibility failures/reopening,
filter seeds and moderation-sensitive fetch policies.

Still outside this revision: full discovery/community SSR, indexable item detail pages,
publication-aware sitemap/hreflang for the managed site documents, Search Console configuration
and measured Lighthouse improvements. Single-city Osaka/Kyoto services are distinct from the
combined guide (one service section versus two); do not consolidate their canonicals as if they
were duplicates.
City-specific service descriptions and shared metadata helpers are optional future improvements.

Deployment and Search Console submission are separate actions requiring authorization.
After deployment, inspect representative URLs and selected canonicals; a passing test or merge
does not prove Google has indexed the pages.

## Primary references

- [Canonical consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Sitelinks search box retirement](https://developers.google.com/search/blog/2024/10/sitelinks-search-box)

Next implementation details were checked against the bundled `node_modules/next/dist/docs`
metadata, sitemap and fetch documentation, plus its current metadata resolver.
