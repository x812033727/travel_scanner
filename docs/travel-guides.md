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
link — including the validator that rejects HTML and control characters. Articles add
`sources`: an optional list of `{title, https url, checked_on}`, because a notice that
states a fare or a rule should be able to say where it read it.

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
  edited and republished.

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
tightened for one surface cannot quietly miss the other.

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
article never shows a partner link without it. The in-article `offer` block that would let
an editor place a button mid-text is `tasks/open/2026-09-12-guide-offer-content-block.md`.

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
`NAVIGATION_REGISTRY`, so the layout answered "forbidden". What is left is one API-side
defect: `published_at` records the first publication only, so a corrected notice keeps its
original `lastmod` and tells Google nothing changed. `tasks/open/2026-09-11-guide-lastmod-republication.md` holds the fix, which reads the
currently published revision's timestamp instead of unfreezing the column the list orders by.

Two more, both filed while the lifestyle section was planned:

- `tasks/open/2026-09-12-guide-topic-admin-crud.md` — a topic still needs a seed migration,
  which contradicts what this file and `GuideTopic`'s own docstring promise.
- `tasks/open/2026-09-12-content-link-block-sponsored.md` — a `link` block accepts any
  http(s) host with any query string and renders without `sponsored`/`nofollow`, so an
  editor pasting a tracked URL into the body produces an undisclosed, untracked affiliate
  link. More likely now that a non-travel section invites outbound links.

Both sections share one 1,000-row sitemap budget, newest first, with no per-section cap
(`SITEMAP_LIMIT`, `SITEMAP_GUIDE_ENTRY_LIMIT`). That is 2% of Google's per-file limit and
about 200 articles across five locales; an evicted article stays indexable, just
unadvertised. Worth splitting only if the combined count approaches ~800, and worth
coordinating with the lastmod task, which is already editing `SitemapEntry`.
