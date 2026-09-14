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
- The separate `(stay22-public)` services tree retains its own valid canonical/language builder.
  Its optional `x-default` is supplied through the sitemap, not HTML. Google accepts HTML and
  sitemap localization annotations as equivalent methods.
- `NEXT_PUBLIC_SITE_URL` is set at build time (the Dockerfile requires it). Changing the public
  origin requires a rebuild; request-time sitemap generation does not change that fact.

## Index directives and feature visibility

| Surface | Policy |
| --- | --- |
| Home, food directory, destination directory/guides/services | Indexable public content |
| Travel intel and guides (`/guides`, `/guides/{kind}`, articles) | Indexable public content; an article only in the locales it is published in |
| Lifestyle (`/life`, `/life/{slug}`) | Indexable public content; same per-locale publication rule. Topic-filtered views are `noindex` |
| An article hub in a locale with nothing published (`/guides`, `/guides/{kind}`, `/life`) | `noindex, follow`, and absent from the sitemap for that locale |
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

`robots.ts` points to `/sitemap.xml`. The sitemap uses `dynamic = "force-dynamic"` and reads
the six public visibility flags once at request time with `no-store`. This avoids freezing
deployment-time flags or needing the API during `next build`.

The static list is at most **385 URLs**: five locales times eleven base routes, 33
destination guides, and 33 services pages. Four base routes are conditional; all four
closed/unavailable gives **365 URLs**. The three `/guides` hubs and `/life` carry no feature
switch, so they are never among the conditional ones -- but they are listed per locale rather
than per route, which is the second way the static count can fall short of 385.

### An article hub in a locale that has nothing published

Articles are published one locale at a time, so a section that exists only in zh-TW still
answers 200 at `/en/guides`, `/ja/life` and their siblings -- with a heading and one sentence
saying the section is empty. Those are the pages Search Console files as soft 404s and thin
content, and there is nothing on them to rank. So:

- each hub's `generateMetadata` emits `robots: { index: false, follow: true }` when the
  listings behind it are empty. `/guides` covers two kinds and is empty only when both are.
  It stays `follow`: the header, the section links and the language switcher are still the
  crawler's way into the locales that do publish.
- `app/sitemap.ts` lists a hub only in the locales one of its kinds publishes in, and its
  hreflang set names only those locales -- `x-default` only when English is among them.
  Advertising an alternate that answers `noindex` would contradict this file's own output.

**An API failure is not an empty section.** `loadGuideList` reports `available`, and
`guideSitemapEntries` reports `complete`; the rules above apply only to a read that actually
answered and was not truncated at the entry cap. A guides outage therefore leaves every hub
exactly as indexable and as listed as it is today, rather than `noindex`-ing all five locales
at once. A hub returns to the index and to the sitemap with the first article published in
that locale, with no deployment.

`/life` is listed at `priority 0.6` / `changeFrequency weekly`, matching `/guides/howto`
rather than the dated `/guides/intel` feed: its articles are evergreen and are emitted at
`0.5` / `monthly`, and a hub claiming daily change over monthly articles is the
false-freshness signal this file warns about below. This file has never carried a priority
policy; that reasoning lives in a comment beside the route list. Static destination IDs come from `PUBLIC_DESTINATIONS`; no names or
authenticated data are needed to enumerate them. All entries include language alternates.
No sitemap index is needed.

Published guide articles are appended after that static list, one entry per published
translation, capped at `SITEMAP_GUIDE_ENTRY_LIMIT` (1000) so one large response cannot dominate
the file. They are the one publication-aware section, enumerated through `GET /guides/sitemap`,
and the only entries carrying `lastmod`: the timestamp of the revision readers currently see
(`modified_at`), which moves on every republication, falling back to the first `published_at`
when an older API omits it. An article's
alternates name only the locales it is genuinely published in, with `x-default` only where
English is one of them, and an expired intel notice leaves the sitemap while keeping its page.
If the guides API fails or times out, the sitemap degrades to exactly its static entries rather
than failing or emptying.

The four managed site documents stay outside the sitemap. `site-information-page.tsx` returns
`noindex` until an administrator publishes that locale's document, so listing them now would
only accumulate "Excluded by noindex"; they wait for `2026-09-06-legal-content-from-owner` and
remain discoverable through footer links. Private and client shell routes stay out. Nothing
outside the guides emits `lastmod`, because the sitemap does not know when a city guide's places
last moved.

Tests verify each listed path resolves to an App Router page, language URLs agree, private
routes are absent, and each feature can close/reopen without a rebuild. The browser suite
additionally renders three synthetic articles into the XML Next actually emits, which is the only
check that exercises `lastmod` serialisation and an article's partial hreflang set.

## `/llms.txt`

`app/llms.txt/route.ts` serves a short, annotated map of the site as `text/plain; charset=utf-8`
with `Cache-Control: no-store`, in the shape [llmstxt.org](https://llmstxt.org/) describes: an
H1, a blockquote, then H2 sections of `- [title](url): note` lines. Next has no file convention
for it, so it is a Route Handler in a dotted folder, the pattern its own documentation names for
`rss.xml`. `proxy.ts`'s matcher already excludes any path containing a dot, so next-intl never
sees the request and no locale is inferred -- every URL in the file names its locale explicitly,
and the annotations are English, the language `x-default` points at.

The file is not a second sitemap and does not try to be. `/sitemap.xml` stays the complete list
and the file says so in its own header. What llms.txt adds is what each section *is*, which the
sitemap's bare URLs cannot carry.

It reuses `SITEMAP_ROUTES` rather than restating which pages are public. The gating is four
feature switches plus the discovery switch, and a second file re-deriving that list would
advertise a `noindex` page the first time a route changed on one side only. A route module
importing another route module is unusual here; drifting from the sitemap would be worse.
Destination annotations come from the same catalogue read the destination index makes, and an
outage leaves the destinations listed without their annotation rather than dropping the section --
those pages are still there.

**Who can actually read it.** Three of the agents that advertise consuming llms.txt -- `GPTBot`,
`ClaudeBot` and `PerplexityBot` -- are refused in `robots.ts` under the policy recorded there, so
they will never fetch this file. That is not a reason to revisit the refusals, and a flat metric
here is not evidence that it should be. The readers it does have are the agents that fetch on a
person's behalf and cite what they found (`ChatGPT-User`, `OAI-SearchBot`), ordinary search
crawlers, and tooling. The convention also has no registered discovery directive -- a client
probes the well-known path or does not -- so `robots.txt` is not modified to point at it.

Serving the file implies nothing about being indexed, cited, or summarised anywhere. It is one
document that costs one request; it is not a ranking mechanism, and no part of this repository
should be read as claiming it is.

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
| Article | Published intel, how-to and lifestyle articles: real headline, body, `datePublished`, `dateModified`, and `image` only when the article has a hero |
| CollectionPage + ItemList | A series hub, listing the members the series read actually returned |
| citation | Every source the article lists, through the same sanitizer that draws the visible list |
| WebPage `lastReviewed` / `reviewedBy` | The newest `checked_on` across those sources, on the article's `mainEntityOfPage` |
| about | The article's destination, pointing at that destination's own page |

There is no invented review or FAQ markup. `TouristDestination` is a Place, so it does
not claim the CreativeWork-only `inLanguage` property. Purchases are not enabled; this work
does not add Product/Offer markup or represent plans as bookable offers.

### The article graph, and what it deliberately leaves out

The article graph is built by `guideArticle()` in `lib/structured-data.ts`, not inline in the
page. It used to be an object literal in `components/guides/article-page.tsx` -- the only graph
on the site built outside that library, and so the only one with no unit test -- and it had
drifted to six fields while the page under it rendered four more: the dated source list, the
topic chips, the destination, and the reading time.

`citation` is the point of the change. Every published document carries its sources and the page
prints each with the date it was checked, so the graph states the same provenance a reader sees.
The references are passed through `contentBlockLink` at the call site, exactly as the visible
list is drawn, so the graph can never cite a link the page itself refused. `about` is emitted
only for a `destination_id` that has a destination page behind it, so it can never point at a 404.

Left out on purpose, each for a reason that is not "we ran out of time":

- **`HowTo`, for the `howto` articles.** 20 of 106 slugs hold an ordered list at all, and those
  are itineraries rather than procedures. `taoyuan-airport-departure-guide` holds two ordered
  lists, one procedural and one enumerating who is *barred* from self-registration -- as
  `HowToStep` that instructs a reader to obtain an exit ban. `ordered: true` in these packs means
  "numbered for reading". A step list needs an author to declare one, not a renderer to infer it.
- **`FAQPage`.** No FAQ member exists in `RichContentBlock` or in the API's block union, and only
  10 of 498 documents hold two question-heading-and-answer pairs -- where the matching headings
  are section titles with colons, not questions. Google has restricted FAQ rich results to health
  and government sites since 2023, so the only audience is machine readers, who are also the
  audience that discounts a site whose markup does not match its page.
- **`expires`, from an intel notice's `valid_until`.** schema.org reads `expires` as *stop
  serving this*, and the product deliberately keeps an expired notice online with its URL
  working; `components/guides/article.tsx` states that rule as "no expiry banner, no date it
  applied until". Publishing the withheld date to ask an answer engine to stop citing the page
  would be both dishonest and the opposite of what the graph is for.
- **`author` as a Person.** No document carries a byline. The only `author` in the content schema
  is a photographer's credit. An Organization author is accurate and is accepted.
- **`dateAccessed` on a citation.** Not a schema.org property. `checked_on` says when *we* read
  the source, which is `lastReviewed` on the WebPage node, not a claim about the source itself.

`lastReviewed` is honest today -- the page prints the same dates -- but every `checked_on` in the
corpus currently holds one of two dates, so it reads as a bulk verification stamp. It stays
truthful only while re-verification actually happens on republication; if it stops, the graph will
keep asserting a review that no longer occurs.

An article with a hero image also puts it on the Open Graph and Twitter cards, restating the
layout's locale and alternate locales beside it (Next replaces the whole `openGraph` key);
without one the page inherits the site card, `/og.png`.

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
CMS publication isolation, robots and the runtime sitemap. Unit tests separately cover
visibility failures/reopening, filter seeds and moderation-sensitive fetch policies.

Still outside this revision: full discovery/community SSR, indexable item detail pages,
publication-aware CMS sitemap/hreflang, Search Console configuration and measured Lighthouse
improvements. Single-city Osaka/Kyoto services are distinct from the combined guide (one
service section versus two); do not consolidate their canonicals as if they were duplicates.
City-specific service descriptions and shared metadata helpers are optional future improvements.

Deployment and Search Console submission are separate actions requiring authorization.
After deployment, inspect representative URLs and selected canonicals; a passing test or merge
does not prove Google has indexed the pages.

## Primary references

- [Canonical consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Sitelinks search box retirement](https://developers.google.com/search/blog/2024/10/sitelinks-search-box)
- [schema.org `citation`](https://schema.org/citation), [`lastReviewed`](https://schema.org/lastReviewed) (WebPage only) and [`expires`](https://schema.org/expires)
- [The llms.txt convention](https://llmstxt.org/)

Next implementation details were checked against the bundled `node_modules/next/dist/docs`
metadata, sitemap and fetch documentation, plus its current metadata resolver.
