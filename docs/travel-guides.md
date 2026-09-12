# 旅遊情報與攻略、生活分享專區

## What this is, and what it is not

First-party articles written by the team in `/admin/guides`, in two public sections that
share one set of tables:

**旅遊情報攻略** at `/guides` — **情報** (`intel` — time-bound notices: fare deals, transport
changes, entry rules, seasonal events) and **攻略** (`howto` — evergreen how-to: pre-trip
preparation, transfer tutorials, sample itineraries).

**生活分享** at `/life` — `life`, everything the site writes that is *not* about travel: AI
tools and tutorials, software, gadgets, productivity and everyday notes. It exists to give
the site a second body of indexable first-party writing, and hands the reader on to the
travel section and the destination pages, which is where the money is.

One system, not two: the identity, revision history, per-locale publication, audit trail and
back-office editor are shared. The sections differ in exactly four places — the URL, the
navigation entry, the topic vocabulary (`guide_topics.section`) and what ends an article.

It is deliberately separate from the three things it is easy to confuse it with:

| | stores content? | who writes it | indexable |
| --- | --- | --- | --- |
| `guides` (this) | yes | the team, in the back office | yes |
| `discovery` / `/explore` | no — it aggregates | nobody; it reads approved catalog rows, **external** article/video references (`HotspotGuide`) and community posts | no (`robots: noindex`) |
| `site_pages` | yes | the owner, four fixed legal slugs | no until published |

`攻略` used to be the zh-TW label for discovery's external-article kind as well
(`apps/web/lib/discovery-copy.ts`). Two things under one word was a defect; PR #404 relabelled
discovery's kind to 站外文章, so the word now belongs to this section alone.

## Classification

Three orthogonal axes, because no single one of them covers the content:

1. **Kind** — `intel`, `howto` or `life`. Three values, a `CHECK` constraint
   (`ck_guide_article_kind`, widened by `0074_lifestyle_guides`). It is part of the URL, so
   `update_article` refuses a *cross-section* change with `409 guide_kind_locked` once any
   locale is published. To move an article between sections: withdraw every language first.
   The old URL then answers "not published in this language" and is `noindex`; there is no
   redirect table and this is not the operation to build one for. Moving between `intel` and
   `howto` stays allowed, because the URL is the same section either way.

   `uq_guide_article_slug` is global, so `/life/x` and `/guides/{kind}/x` are mutually
   exclusive by construction — no cross-section slug check is needed anywhere.
2. **Destination** — `guide_articles.destination_id`, validated against
   `app/destinations/catalog.py` (the same ids as `/destinations/{id}`). **Nullable**: an
   article like "which Japan Rail Pass to buy" spans cities and must still have a home.
3. **Topics** — many per article, rows in `guide_topics` with one label per locale in
   `names_json`, the shape `HotspotTheme` already uses. Each topic belongs to one
   **section** (`guide_topics.section`, `travel` or `life`, `ck_guide_topic_section`), and
   `_resolve_topics` refuses a topic from the other section with `422
   guide_topic_section_mismatch` on both create and update. Without that column the seven
   lifestyle slugs would appear as filter chips on the travel hub and as checkboxes to a
   travel editor. Adding a topic still needs a seed migration — there is no write endpoint
   yet; `tasks/open/2026-09-12-guide-topic-admin-crud.md` holds that.

Seven topic slugs (`culture`, `nature`, `family`, `nightlife`, `viewpoint`, `food`,
`shopping`, `hotel`, `beach`) are shared verbatim with `app/discovery/taxonomy.py` so a
guide and an attraction that share a subject can find each other later. A test asserts the
labels stay byte-identical; nothing else stops two tables drifting. The lifestyle
vocabulary (`ai`, `tutorial`, `software`, `gadgets`, `productivity`, `daily`, `misc`) shares
nothing with either list on purpose, and a test holds the three sets disjoint.

## Storage

`site_pages` keys a document by `(slug, locale)` in one table because its slug set is four
fixed values. An article cannot: its slug, kind, destination, topics and validity belong to
the article, not to any one translation, and five copies drift. Hence two layers.

```
guide_articles          identity + taxonomy, language-independent, own `version`
guide_article_locales   one row per translation: version, draft_json, published_version,
                        published_at  (the SitePage role)
guide_article_revisions append-only history, enforced by a database trigger
guide_topics            slug + names_json + display_order + is_active + source + section
guide_article_topics    join
```

`guide_topics.section` carries a `server_default` as well as an ORM default. `0001` builds
current metadata on a fresh database, so `0072`'s seed — a `bulk_insert` that never names the
column — runs against a table the models created; without DDL-level default that insert
fails `NOT NULL` on every fresh deployment.

Migration `0072_travel_guides` creates them with `inspector.has_table` guards (0001 builds
current metadata on a fresh database) and seeds the **topic vocabulary only**. A migration
never writes an article and never publishes one.

The body reuses `app/site_pages/schemas.py`'s structured blocks — heading, paragraph, list,
link — including the validator that rejects HTML and control characters, and adds four of
its own in `app/guides/schemas.py` (`GuideBlock`): `image`, `table`, `callout` and `offer`.
They are guide-only on purpose: the legal pages keep the four-block `ContentBlock`, so their
editor never meets a block it has no fields for. An article may also carry a `hero`
(`GuideDocument.hero`, optional so every revision written before it validates), which is
the picture at the top of the page, on the listing cards and on the share card.

- `image` / `hero` — `src` must match `/guides/<slug>/<name>.(webp|jpg|png|svg)`, a path
  under the web app's own `public/`, never a URL: an article can never make a reader's
  browser fetch a picture from a third party, and the files ship and review with the code.
  The hero is raster only (`jpg|png|webp`), because social crawlers do not render SVG.
  `width`/`height` are stored so the browser reserves the box before the bytes arrive.
  `credit` is `{author, license, source_url?}`; the web renders "圖片：author (licence)",
  linking the author to the source page and a Creative Commons licence to its deed.
- `table` — `header` (1–6 cells) and rectangular `rows` (≤30), each cell plain text.
- `callout` — `tone` (`tip`/`warning`/`info`), optional `title`, `text`.
- `offer` — see "Partner buttons" below.

Articles add `sources`: an optional list of `{title, https url, checked_on}`, because a
notice that states a fare or a rule should be able to say where it read it.

## Publication

Per locale and independent. zh-TW can be live while the other four are not; nothing falls
back to another language and nothing invents a translation.

- Every write goes through one `_write_revision`: a conditional `UPDATE ... WHERE version =
  expected_version` (mismatch → `409 guide_version_conflict`), one appended revision, one
  `AdminAuditLog` row carrying before/after and the document SHA-256, one commit.
- Publishing and withdrawing additionally require an explicit `confirmed: true` and a
  `reason`. `confirmed: false`, `"true"` and `1` are all rejected.
- Restoring writes a **new draft** from an old revision and never moves the public pointer.
- A `published_version` pointing at a missing revision returns `503`, never the draft.
- `published_at` records the **first** publication and does not move when the article is
  edited and republished. `PublishedDocument.modified_at` is the timestamp of the revision
  readers currently see — it moves on every republication — and is what the page shows as
  "更新日期", what the `Article` JSON-LD reports as `dateModified`, and what the sitemap
  carries as `lastmod` (`SitemapEntry.modified_at`, an outer join on the published
  revision that falls back to `published_at` so a damaged pointer never drops the URL).

`app/guides/publication.py` holds the single definition of "public in this locale". The
list, the article and the sitemap all compose it, so they cannot disagree about what is
live.

**Hiding is article-wide.** `guide_articles.is_active` is the switch every public reader
already checks, so `POST /admin/guides/{id}/hide` takes every language off the site, the
lists and the sitemap at once and `.../unhide` puts them back — without touching any
translation's `published_version`, so the languages that were live come back together and
nothing has to be republished. Both carry the same gate as withdrawing a translation
(`confirmed: true`, a `reason`, the article's own `expected_version`) and write one
`guide_article_hidden` / `guide_article_unhidden` audit row. `POST /admin/guides/batch`
does the same for up to 100 articles in one transaction: one stale version and nothing is
written; rows already in the requested state are skipped rather than rewritten. A
classification save (`PUT /admin/guides/{id}`) no longer accepts `is_active`, so it can
never quietly put a hidden article back.

The editor-facing state is computed once, in `publication.article_status` (in memory) and
`admin_status_expression` (SQL), with the same precedence: `hidden` when the switch is
off, `expired` when `valid_until` has passed, `published` when at least one translation
is live, otherwise `draft`. The admin list filters and counts by it; a hidden article can
be restored, but `publish` still refuses it until it is.

**Expiry is not withdrawal.** An `intel` article past its `valid_until` keeps its URL —
retracting it would 404 every link already pointing at it — and is returned with
`expired: true` so the page can say what date it applied until. It leaves the listings and
the sitemap, which is where "current" is what a reader expects. Publishing something that
is *already* expired is refused rather than creating an invisible page.

## Permissions

`/admin/guides` maps to `content.read` / `content.manage` in `_admin_path_capability`
(`app/auth/service.py`), so the existing `content` admin role can write guides with no new
capability. This matters: `_admin_path_capability` falls through to `roles.manage` — owner
only — for any path it does not recognise.

## Endpoints

Public, all `Cache-Control: no-store` (the web layer does the caching):

```
GET /api/v1/guides?locale=&kind=&section=&destination=&topic=&cursor=&limit=
GET /api/v1/guides/topics?locale=&section=
GET /api/v1/guides/sitemap
GET /api/v1/guides/{kind}/{slug}?locale=
```

`section` expands to the kinds it covers and composes with `kind` as an intersection. An
empty intersection (`?section=life&kind=intel`) returns an empty list rather than an
unfiltered one — the natural "skip the filter when the tuple is empty" refactor is what
would leak lifestyle articles into a travel-scoped response. The keyset cursor encodes only
`published_at` and the slug, so a cursor minted on one section is accepted on the other;
harmless, because the section predicate is re-applied to every page.

`GET /guides/sitemap` is the publication-aware enumeration `apps/web/app/sitemap.ts` consumes:
one row per published, non-expired article × locale, capped at 1,000 and ordered newest first. The article response carries `published_locales` so the web layer can emit
hreflang for the translations that actually exist.

Admin (`content.manage` for writes):

```
GET    /api/v1/admin/guides?status=&kind=&destination=&topic=&q=&page=&limit=
                                                         list + per-locale state, total/pages,
                                                         status and kind facets
POST   /api/v1/admin/guides                              create + first locale draft
POST   /api/v1/admin/guides/batch                        hide or unhide up to 100 articles
GET    /api/v1/admin/guides/{id}?locale=
PUT    /api/v1/admin/guides/{id}                         taxonomy only (never visibility)
POST   /api/v1/admin/guides/{id}/hide
POST   /api/v1/admin/guides/{id}/unhide
POST   /api/v1/admin/guides/{id}/{locale}                open a new translation
PUT    /api/v1/admin/guides/{id}/{locale}/draft
POST   /api/v1/admin/guides/{id}/{locale}/publish
POST   /api/v1/admin/guides/{id}/{locale}/unpublish
POST   /api/v1/admin/guides/{id}/{locale}/restore
GET    /api/v1/admin/guides/{id}/{locale}/revisions/{revision_id}
```

Authoring lives in `app/guides/admin_service.py` and reading in `app/guides/service.py`.
The split is not only tidiness: `tests/test_error_localization.py` holds every non-operator
module to a translated sentence for each error code it raises, so keeping operator errors
out of the read path keeps that boundary honest.

## Verification

```bash
cd apps/api
uv run ruff check . && uv run mypy app
uv run pytest tests/test_guides.py tests/test_guides_migration.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_guides.py tests/test_guides_migration.py -q
```

The PostgreSQL leg and the migration test are what prove the append-only trigger; the
`tests/test_guides.py` tables are built with `Base.metadata.create_all` and never see it.

## Content packs: authoring in the repository

Ten launch articles with heroes, diagrams, tables and partner blocks are not something to
type into a form, and their source of truth should be reviewable next to the images they
reference. `app/guides/content/<slug>.json` is that source: the article's identity and
taxonomy plus one `GuideDocument` per locale (`app/guides/content_pack.py:ArticlePack`;
the first locale is the one the article is created with), with its pictures under
`apps/web/public/guides/<slug>/`. A test walks the directory: every pack validates, every
image it names exists and is ≤300 KB, every locale cites at least one source.

```
python -m app.cli guides-import --actor-email <admin> [--dir …] [--slug …] [--locale …] [--publish] [--dry-run]
```

The command goes through `admin_service` — create, new translation, draft save, optional
publish — so every import leaves the same revisions and audit rows an editor's clicks
would, attributed to `--actor-email` (an active administrator). It validates every pack
first (pydantic, destination, topics, the offer rules) and writes nothing if any fails;
`--dry-run` stops there and prints the plan. Then it writes per (slug, locale), each call
its own commit, exactly as the editor does; a refusal mid-run stops the run and is named in
the report (`created / updated / unchanged / published / taxonomy_updated / failed`). It is
idempotent: an article that already matches its pack — compared on normalised documents,
because rows written before `hero` existed lack the key — is `unchanged`, and `--publish`
republishes a locale only when the public version differs. Rerunning after fixing the
cause finishes the rest. A migration still never writes an article.

Deploy-time sequence: deploy, then on the host
`docker compose exec api python -m app.cli guides-import --actor-email <admin> --dry-run`,
read the plan, run it again with `--publish`.

### Editorial rules (the review standard for a pack)

Images:

- Files live under `apps/web/public/guides/<slug>/`: `hero.jpg` (1600×900, ≤200 KB),
  inline photos `photo-N.webp` (≤1200 px wide, ≤150 KB), diagrams `diagram-N.svg`
  (viewBox 1600×900, a `<title>` and `<desc>`, system-font fallbacks only, no external
  fonts or scripts). `apps/api/tests/test_guides_content_pack.py` checks existence and size.
- Photographs come from Wikimedia Commons only, under CC0, Public domain, CC BY or CC BY-SA
  (any version). Never NC or ND, never KOGL type 3/4 (its no-modification clause forbids
  even a resize), never a merchant's own interior shot. The licence, author and file page are
  read from the Commons API by the processing script and land in `credit`; the renderer
  links the author to the file page and a CC licence to its deed.
- Diagrams are drawn by the site (`credit.author` "Mokaair", `license` "© Mokaair") with
  local-script + English labels so one file serves every locale; the locale-specific words
  go in the caption.
- `alt` describes the picture; it does not repeat the caption. The hero is a photograph,
  not a diagram, because it doubles as the share card.

Partner buttons:

1. At most three `offer` blocks per article, placed after the paragraph that creates the
   intent (buying the ticket, the theme-park day, the day trip), never before the first
   level-2 heading. One disclosure line appears under the hero whenever the body carries one.
2. Topics with no honest module (entry, packing, budget, etiquette, safety, food, shopping,
   nightlife) get no end panel; an `offer` block there must be about that section itself
   (airport transport at the end of an entry-rules notice is fine; a shopping notice gets none).
3. Nothing under an expired notice — the renderer already enforces it.
4. The end panel skips modules already placed inline, so a button never shows twice.
5. Which article converts is read from `affiliate_clicks` once
   `2026-09-12-attribute-affiliate-clicks-to-the-guide` lands; revisit placements after a month.

Text:

- Every fare, duration and rule is checked against an official page on the day of writing
  and cited in `sources` with `checked_on`; a number the official page does not confirm is
  not written ("以官網為準" instead). Prices stay in the local currency.
- How-to articles run about 1,800–3,000 characters, notices 800–1,500; at least three
  level-2 headings (the table of contents starts at three), one table, one callout.
- Internal links are `link` blocks with absolute site URLs (destination page, food
  directory); the renderer keeps them in the same tab.

## The reader's side

```
/{locale}/guides                      hub: latest intel, featured guides, topic entries
/{locale}/guides/{kind}               intel | howto, with ?topic= and ?destination= filters
/{locale}/guides/{kind}/{slug}        the travel article
/{locale}/life                        hub and listing in one, with ?topic=
/{locale}/life/{slug}                 the lifestyle article
/{locale}/admin/guides                the list for both sections: status pills with counts,
                                      section / kind / topic / destination / search filters,
                                      paging, one badge per language, single and
                                      multi-select hide / restore
/{locale}/admin/guides?article=<id>&lang=<locale>   the editor for one translation
```

The list and the editor keep their state in the URL (`components/admin-guides-list.tsx`,
`lib/admin-workspace-navigation.ts`), so "back to the list" returns to the same filters
and a filtered view can be bookmarked. The section filter matters more than it looks: the
list is one paginated window over both sections, so without it a run of lifestyle articles
would push the travel ones off the first page of the only way an editor reaches them.
`/admin/guides` is registered in the API's `NAVIGATION_REGISTRY`; the web fallback list
alone is not enough, because the layout trusts the registry whenever the API answers and
marks any other path forbidden.

`[kind]` holds the two **travel** kinds; `isTravelGuideKind` rejects everything else, so
`/guides/life` and `/guides/life/{slug}` are 404 and a lifestyle article has exactly one
URL. The API path stays `/api/v1/guides/life/{slug}` — JSON behind a robots-disallowed
`/api/` prefix is not a competing HTML URL.

`guideHref` and `guideListHref` (`apps/web/lib/guides.ts`) are the only place either
section's URLs are built, so the split cannot drift between the cards, the chips, the
breadcrumbs, the sitemap and the hreflang set.

`guideArticleMetadata` and `renderGuideArticle` (`components/guides/article-page.tsx`) hold
the article screen once: per-locale hreflang, the `noindex` unpublished state, the `Article`
JSON-LD and the back link. Both route files are thin shells that await it, so what the route
hands back is a finished tree rather than an async component the reader's test cannot draw.
Two copies of that logic is two chances to get the SEO wrong, and the existing
`[kind]/[slug]` suite guards the extraction for free.
It is dynamic on purpose: `app/[locale]/metadata.test.ts` requires a `metadata.json` title
and description for every *static* public page, and one hub entry is the honest amount of
per-page metadata for a section whose two halves differ only by kind.

Filters are plain links resolved on the server, so a filtered view is shareable, works
without JavaScript and is already in the HTML. Filtered views are `noindex`: they are the
same collection reordered, and they should not compete with the section itself.

`ContentBlocks` (`apps/web/components/content-blocks.tsx`) renders the body for the public
page **and** the admin preview, and `lib/content-blocks.ts` holds the one link sanitizer
that both guides and managed site documents use. That sharing is the point: a rule
tightened for one surface cannot quietly miss the other. The renderer draws the
`RichContentBlock` superset (image, table, callout); the legal pages' documents stay typed
to the four shared blocks. Images are plain `<img>` with their stored size (`next/image`
has no optimizer in the standalone build); a wide table scrolls inside its own box; a link
back into this site opens in the same tab. A `link` block in the body is still an ordinary
anchor — not an affiliate link, and not `rel="sponsored"` (`2026-09-12-content-link-block-sponsored`).

### What a travel article looks like

Header (kind, city, title, description, published / updated dates, reading time) → hero with
its credit → one line of disclosure, only when the body itself carries partner buttons →
a table of contents once there are three level-2 headings (`section-N` anchors the renderer
numbers across the whole body) → the body in slices around each `offer` block → the end
panel → related reading → topic chips → sources → other languages. `lib/guides.ts` holds
`splitGuideBlocks`, `guideHeadings` and `readingMinutes` (CJK by character, the rest by
word); `article.tsx` stays synchronous and the page (`article-page.tsx`) does the fetching.

Related reading for a travel article is up to three other travel articles about the same
destination, topped up from the first topic, never the article itself and never a
lifestyle one — the same `TravelCrosslinks` component a lifestyle article ends with, with
no destination chips.

### Share cards and structured data

An article with a hero puts it on the share card: `guideArticleMetadata` reads the layout's
resolved `openGraph` through Next's `parent` argument and restates `siteName`, `locale` and
`alternateLocale` next to the image, `type: "article"`, `publishedTime` and
`modifiedTime`, because Next replaces a whole top-level metadata key rather than merging
inside it. The image path is relative; the layout's `metadataBase` makes it absolute the
same way it does for `/og.png`. Without a hero neither `openGraph` nor `twitter` is set and
the site card inherits. The `Article` JSON-LD claims `image` only when a hero exists, and
`dateModified` from `modified_at`.

### The end of a lifestyle article

Always, and with no commission attached: `components/guides/travel-crosslinks.tsx` — the
three newest travel articles as `GuideCard`s (omitted when there are none), then at most six
destination links. When the article names a destination the six come from that city's
country; otherwise one per country. It is a synchronous presentational component in its own
`<section>` with a `border-t` heading, fetched by `renderGuideArticle` and passed in through
`related`, so `GuideArticle` stays synchronous and testable. Internal links carry no
disclosure, and the separator is what keeps them visibly apart from any offer panel above —
`docs/travel-services.md` requires exactly that.

Then, only when the editor deliberately filled in a destination: the same
`DestinationAffiliateOptions` panel, `placement="life"`, every module. Lifestyle topics name
no travel module, so the topic allowlist can say nothing here; the destination is the only
contextual signal the article has, and the panel matches what the destination page itself
shows. Three gates still stand before a button appears — the editor's (a destination is
set), the operator's (the `life` placement is off by default) and the article's own
(`!expired`) — and `by_placement` in the click report says whether it converts. It renders
non-contextual, so the heading names the destination's partners instead of inviting the
reader to "keep exploring" a place the article was never about. Narrowing the module list to
`["activities", "transport", "connectivity"]` is a one-line change in
`apps/web/lib/guide-affiliate.ts`, which is where both rules live.

### Partner buttons at the end of a travel article

`components/guides/article.tsx` ends a published article with the same
`DestinationAffiliateOptions` panel the destination services page uses, labelled
`placement="guide"`, when all three hold: the article has a `destination_id` (Kyoto folds
into `osaka-kyoto`), at least one of its topics maps to a partner module, and the notice
has not expired. The mapping is the explicit allowlist in `apps/web/lib/guide-affiliate.ts`:
`connectivity → connectivity`, `hotel → hotel`, `transport → transport`, `deal → flight`,
and `itinerary/season/family/nature/culture/viewpoint/beach → activities`. Entry rules,
packing, budget, etiquette, safety, food, shopping and nightlife map to nothing on purpose:
a flight button under a safety article is the non-contextual placement the catalog rules
avoid, and the reader is one click from the all-modules city page.

The panel renders nothing until the API says so: the `guide` surface must be enabled in
the catalog's `affiliate_placements` (off by default) and a verified destination offer
must exist for that destination and module. The disclosure comes with the options, so an
article never shows a partner link without it.

### Partner buttons placed by the editor (`offer` blocks)

An `offer` block — `{module, destination_id?, heading?}` — puts the same panel, for one
module, next to the paragraph that earned it: the "how to buy the ticket" section gets the
transport button, the theme-park day gets the activities button. Which brands show is still
the catalog's decision (an approved, verified destination offer for that destination and
module, the surface enabled); the block only says where and for which module.

- `destination_id` overrides the article's own, which is what lets a cross-destination
  notice ("autumn leaves in Tokyo and Kyoto", `destination_id` null, so no end panel) point
  each section at its city. Kyoto folds into `osaka-kyoto` on the reader's side exactly as
  the end panel does, and a city not in `PUBLIC_DESTINATIONS` draws nothing.
- The write path enforces what the model cannot: at most three per article
  (`422 guide_offer_limit`), a block on a cross-destination article must name its city
  (`guide_offer_destination_required`), and the city must exist in the catalog
  (`guide_offer_destination_unknown`). `_validate_document` runs on create, new
  translation, draft save, publish and restore — publish re-checks because the article's
  destination may have been cleared since the draft was saved — and never on withdrawal.
  The rules sit in `admin_service`, not on the pydantic model, because that model also
  validates every stored revision on the public read path, where a retired destination must
  degrade to "no button" rather than a 500.
- The reader's side: a module the editor placed mid-article is left out of the end panel,
  so the same button never appears twice; one line of disclosure sits under the hero
  whenever the body carries a block (the end panel still carries its own); expiry drops
  every button, inline ones included. The admin preview shows a placeholder where the
  buttons will go and never fetches offers.

### Per-locale hreflang

Publication is per locale, so the root layout's all-five alternate set would advertise
translations that do not exist. The article page overrides `alternates.languages` with
exactly the locales the API reports as published, and offers `x-default` only when English
is among them. A locale that was never written renders a "not in your language" page,
`noindex`, listing the languages that do exist.

### Navigation

`/guides` and `/life` are both in `primaryNavLinks` with **no feature flag**, and the header
renders both outside the three mutually exclusive navigation modes. Adding a section to
`primaryNavLinks` alone would make it invisible whenever discovery or community mode is on —
the defect `2026-09-11-no-sign-in-entry-in-discovery` records.
`components/guides-navigation.test.tsx` holds that line for both, in all three modes. The
phone header gets its own icon per section in the discovery branch, which returns before the
menu sheet is rendered. The bottom tab bar is deliberately left alone.

`primaryNavLinks` also feeds two community surfaces (`community/explore.tsx`,
`community/home.tsx`) that frame it as 旅行工具, so both filter `life` out.

The back office registration is the same shape and worth reading together with it: the
sidebar and the layout guard both read the API's `NAVIGATION_REGISTRY`, and a row in the web
`fallbackAdminNavigation` alone reaches neither (see the paragraph above the route table).
Its label comes from `admin.navigation.guides`, which names both sections now that one
editor serves both.

### Caching

The loaders are `cache: "no-store"` with a 3-second abort and React `cache()` for
per-request dedupe. `docs/seo.md` asks moderated listings to stay uncached, and a
five-minute window in which a withdrawn fare notice is still live is exactly what the
publication gate exists to prevent.

## Still open

The sitemap wiring and the `攻略` relabel both landed in PR #404, together with the footer and
destination-page links. Between #398 and the visibility work the back-office entry itself was
unreachable in production: `/admin/guides` was in the web fallback navigation but not in
`NAVIGATION_REGISTRY`, so the layout answered "forbidden". The frozen `lastmod` was the
last API-side defect and is fixed by `modified_at` (see Publication).

Two remain, both filed while the lifestyle section was planned:

- `tasks/open/2026-09-12-guide-topic-admin-crud.md` — a topic still needs a seed migration,
  which contradicts what this file and `GuideTopic`'s own docstring promise.
- `tasks/open/2026-09-12-content-link-block-sponsored.md` — a `link` block accepts any
  http(s) host with any query string and renders without `sponsored`/`nofollow`, so an
  editor pasting a tracked URL into the body produces an undisclosed, untracked affiliate
  link. More likely now that a non-travel section invites outbound links.

Both sections share one 1,000-row sitemap budget, newest first, with no per-section cap
(`SITEMAP_LIMIT`, `SITEMAP_GUIDE_ENTRY_LIMIT`). That is 2% of Google's per-file limit and
about 200 articles across five locales; an evicted article stays indexable, just
unadvertised. Worth splitting only if the combined count approaches ~800.
