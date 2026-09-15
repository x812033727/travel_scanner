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

Since `0076_guide_topic_hierarchy` topics are **two levels deep**: a lifestyle parent such as
`ai` holds sub-topics such as `ai-terms` (`guide_topics.parent_id`, nullable, SET NULL on
delete; a parent never has a parent, which `admin_service` and the seed enforce rather than
a CHECK). An article may carry the parent, the child or both; `?topic=<parent>` lists the
children's articles too (`taxonomy.topic_ids_including_children`), and `GET /guides/topics`
returns each topic's `parent`, its hub lead (`descriptions_json`, per locale) and how many
articles each locale publishes under it (`count`, `counts`; a parent counts the distinct
union of itself and its children). `tutorial` is deliberately not a parent: it marks the
format of most lifestyle articles, not their subject. The travel vocabulary stays one level;
its second axis is the destination, grouped by country (`?country=japan`, mapped to the
catalog's cities by `service.destinations_in_country`, and `GET /guides/destinations` for
the hub's country groups). Three slugs are refused as article slugs -- `topics`, `series`,
`search` -- because the web routes own those path segments. The vocabulary, the rules that
re-file existing packs (`app/guides/retopic.py`) and the phases that build on this live in
[`docs/article-architecture.md`](article-architecture.md).

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
link — including the validator that rejects HTML and control characters, and adds five of
its own in `app/guides/schemas.py` (`GuideBlock`): `image`, `table`, `callout`, `offer` and
`partner_link`.
They are guide-only on purpose: the legal pages keep the four-block `ContentBlock`, so their
editor never meets a block it has no fields for. An article may also carry a `hero`
(`GuideDocument.hero`, optional so every revision written before it validates), which is
the picture at the top of the page, on the listing cards and on the share card.

- `image` / `hero` — `src` must match `/guides/<slug>/<name>.(webp|jpg|png|svg)`, a path
  under the web app's own `public/`, never a URL: an article's own pictures can never come
  from a third party, and the files ship and review with the code. (Since 2026-09-13 an
  article page *can* make third-party requests, but only for Google's ad tag, and only when
  the owner has switched advertising on — see "Advertising" below. Nothing in an article's
  content can introduce one.)
  The hero is raster only (`jpg|png|webp`), because social crawlers do not render SVG.
  `width`/`height` are stored so the browser reserves the box before the bytes arrive.
  `credit` is `{author, license, source_url?}`; the web renders "圖片：author (licence)",
  linking the author to the source page and a Creative Commons licence to its deed.
- `table` — `header` (1–6 cells) and rectangular `rows` (≤30), each cell plain text.
- `callout` — `tone` (`tip`/`warning`/`info`), optional `title`, `text`.
- `offer` — see "Partner buttons" below.
- `partner_link` — see "Partner links" below.

Articles add `sources`: an optional list of `{title, https url, checked_on}`, because a
notice that states a fare or a rule should be able to say where it read it.

No ordinary URL in an article may be a tracked one: a `link` block, a source or an image
credit whose URL carries affiliate tracking or is a short link is refused on every write
with `422 content_link_affiliate` (`affiliate_marker` in `app/affiliates/content_links.py`).
The partner-link block is the one way a paid link reaches a reader, because it is the one
place that discloses it, qualifies it and counts it. The managed legal pages refuse the same
URLs in `app/site_pages/service.py`.

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
`expired: true`. It leaves the listings and the sitemap, which is where "current" is what a
reader expects. Publishing something that is *already* expired is refused rather than
creating an invisible page.

**The reader is never shown a date.** `valid_until` and `published_at` are editorial and
operational fields: they decide what is listed, what the sitemap carries and what the
`Article` JSON-LD reports, and neither is drawn on a card or an article. There is no
"published on", no "applies until" and no expiry banner — a notice that is still correct
should not be aged by a date stamp, and an expired one is already handled by leaving the
listings. What `expired: true` still changes on the page is one thing: it drops every
partner button (see Partner buttons). The reader-facing date that survives is "更新日期",
and only once `modified_at` is later than the first publication.

## Permissions

`/admin/guides` maps to `content.read` / `content.manage` in `_admin_path_capability`
(`app/auth/service.py`), so the existing `content` admin role can write guides with no new
capability. This matters: `_admin_path_capability` falls through to `roles.manage` — owner
only — for any path it does not recognise.

## Endpoints

Public, all `Cache-Control: no-store` (the web layer does the caching):

```
GET /api/v1/guides?locale=&kind=&section=&destination=&country=&topic=&cursor=&limit=
GET /api/v1/guides/topics?locale=&section=          parents then children, with per-locale counts
GET /api/v1/guides/destinations?locale=&section=    destinations with a published article, by country
GET /api/v1/guides/series?locale=                   every registered series hub published in the locale
GET /api/v1/guides/sitemap?section=&locale=&cursor=&limit=   one child sitemap's rows, paged
GET /api/v1/guides/sitemap/summary                  published rows per kind and locale
GET /api/v1/guides/series/{series_slug}?locale=
GET /api/v1/guides/{kind}/{slug}?locale=
POST /api/v1/guides/{kind}/{slug}/partner-links/{key}/click?locale=   count one partner-link click, 204
```

`section` expands to the kinds it covers and composes with `kind` as an intersection. An
empty intersection (`?section=life&kind=intel`) returns an empty list rather than an
unfiltered one — the natural "skip the filter when the tuple is empty" refactor is what
would leak lifestyle articles into a travel-scoped response. The keyset cursor encodes only
`published_at` and the slug, so a cursor minted on one section is accepted on the other;
harmless, because the section predicate is re-applied to every page. `topic` names a parent
or a sub-topic and an unknown slug answers an empty list; `country` is a catalog country in
URL form (`japan`, `south-korea`) and an unknown one answers an empty list too.

`GET /guides/series` reads `app/guides/series_registry.json`, the one list of series and
tutorial hubs across the three mechanisms that hold one (the `series_data` catalogues, the
web's Gemini projection, the editorial catalogues under `docs/`): a row names the hub
article and the sub-topic a series belongs to, and the row shows in a locale only while
that hub article is published there.

`GET /guides/sitemap` is the publication-aware enumeration `apps/web/app/sitemap.ts` consumes:
one row per published, non-expired article × locale, newest first, with the slug and the
locale as tiebreakers so rows published in the same second page cleanly. `section` and
`locale` narrow it to one child sitemap, `limit` (default and maximum 1,000) is the page and
`next_cursor` the keyset to follow; a call without parameters still answers the newest
thousand rows in one page, as it did before paging. Each row names every locale its article
is published in (`locales`), which is what lets a one-language child carry the article's
full hreflang set. `GET /guides/sitemap/summary` counts published rows per kind and locale
for the sitemap index and the section hubs. The article response carries
`published_locales` so the web layer can emit hreflang for the translations that actually
exist.

Admin (`content.manage` for writes):

```
GET    /api/v1/admin/guides?status=&kind=&destination=&topic=&q=&page=&limit=
                                                         list + per-locale state, total/pages,
                                                         status and kind facets
POST   /api/v1/admin/guides                              create + first locale draft
POST   /api/v1/admin/guides/batch                        hide or unhide up to 100 articles
GET    /api/v1/admin/guides/partners                     the partner programs a partner link may use
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

Fifty launch articles with heroes, diagrams, tables and partner blocks are not something to
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

Producing a pack is tooled too, since the third batch rewrote the same scratchpad script for
the third time: `app/guides/pack_ingest.py`, run as `uv run python -m app.guides.pack_cli`.
`ingest --from <workdir> --slug <slug>` turns a writing agent's workspace (`pack.json`,
`diagram-N.svg`, a `hero.svg` or an `images.json` naming Commons files, `notes.md`) into the
pack and its pictures — validating with `ArticlePack` and the write path's own rules, rendering
`hero.svg` with headless Chromium, fetching photographs through the Commons API with the licence
gate, writing sizes and credits — and writes nothing if anything is wrong. `lint [--kind life]
[--render-dir …] [--catalogue …]` runs the rules below over the packs that ship, renders every
SVG to PNG for the reviewer's eyes, and compares a series catalogue with the packs.
`tests/test_guides_content_pack.py` holds every `life` pack to its errors; the travel packs
predate it and were reviewed by hand (running `lint` over them shows what that review let
through: a few 14 px labels and diagram numbers the non-zh-TW texts do not carry). The
生活分享 AI series is planned in `docs/life-ai-series.md`, and its writing brief is
`docs/life-ai-series-brief.md`.

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
  go in the caption. Every fare, time or date printed on a diagram must appear in the
  article's own verified text (a number the article does not carry is not drawn), and no
  label is smaller than 15 px so the figure stays legible on a phone. The second and third
  batches' diagrams were drawn by the writing agents from the same brief; the review checked
  both rules mechanically, then rendered every SVG to PNG (headless Edge) and looked at it,
  because an agent cannot see its own layout: labels crossing their own route lines, text
  running out of a box and labels piled on each other all passed the mechanical checks.
- `alt` describes the picture; it does not repeat the caption. The hero is a photograph,
  not a diagram, because it doubles as the share card.
- A 生活分享 article about software has no photograph to take. Its hero is then a self-drawn
  illustration — `hero.svg`, committed next to it — rendered to `hero.jpg` by
  `python -m app.guides.pack_cli ingest`, or a Commons photograph of generic hardware (a
  keyboard, a phone in a hand, a desk) under the same licences. A product's logo, wordmark,
  icon, mascot or interface screenshot never appears in a hero, a diagram or an inline photo:
  trademarks and interface copyright are not ours to license, so the product is named in
  plain text. An illustration hero carries at most one short line of text, because the fonts
  of the machine that rendered it decide its look; labels belong on the diagram, which stays
  SVG and renders in the reader's own fonts.

Partner buttons:

1. At most three `offer` blocks per article, placed after the paragraph that creates the
   intent (buying the ticket, the theme-park day, the day trip), never before the first
   level-2 heading. One disclosure line appears under the hero whenever the body carries one.
2. Topics with no honest module (entry, packing, budget, etiquette, safety, food, shopping,
   nightlife) get no end panel; an `offer` block there must be about that section itself
   (airport transport at the end of an entry-rules notice is fine; a shopping notice gets none).
3. Nothing on an expired notice — the renderer already enforces it.
4. The end panel skips modules already placed inline, so a button never shows twice.
5. Which article converts is read from `affiliate_clicks` once
   `2026-09-12-attribute-affiliate-clicks-to-the-guide` lands; revisit placements after a month.

Partner links (non-travel programs, mostly in 生活分享):

1. Only where the article actually uses the product — the tutorial that deploys to a VPS links
   the host it deploys to, the reading list links the book. At most three per article.
2. Paste the link the affiliate program's own dashboard generates. Customer referral codes
   (Hostinger's `REFERRALCODE`, for one) are refused, because their terms keep them off
   websites; resale, account-sharing or API relay services are never linked at all.
3. The disclosure line and the badge beside each link are automatic; do not write a second
   one into the body, and do not put a product's logo in the hero.

Text:

- Every fare, duration and rule is checked against an official page on the day of writing
  and cited in `sources` with `checked_on`; a number the official page does not confirm is
  not written ("以官網為準" instead). Prices stay in the local currency.
- A pack may carry several locales of one article (the Taiwan batch has `en`, `ja`, `ko`,
  `zh-CN`, created in that order). Each locale is written for its own readers rather than
  translated: entry rules, payment habits and language support differ by passport and home
  market, so each locale checks those facts itself and may cite different sources. Images,
  offer blocks and block order stay the same across locales; one diagram with Traditional
  Chinese and English labels serves them all.
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
back into this site opens in the same tab. A `link` block in the body is an ordinary
editorial anchor (`noopener noreferrer`, no `sponsored`): affiliate URLs never get that far,
because the write path refuses them. The renderer draws only a `link` block as a link, so a
block it does not know — a partner link, or something a newer API sends — draws nothing
instead of falling through to the link branch.

### What a travel article looks like

Header (kind, city, title, description, then the update date and reading time — no
publication date, see Expiry is not withdrawal) → hero with
its credit → one line of disclosure, only when the body itself carries partner buttons or
partner links →
a table of contents once there are three level-2 headings (`section-N` anchors the renderer
numbers across the whole body) → the body in slices around each `offer` and `partner_link`
block → the end
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

### Partner links (`partner_link` blocks)

Travel offers cover the travel half of an article. A tutorial about an AI tool earns from
something else — the host a project is deployed to, a book, a course, a software plan — and
a `partner_link` block, `{partner, url, label, note?}`, is how that link gets into the body.
It is allowed in every kind; the registry holds no travel brand, so it opens no way around
the catalog's approval of travel offers.

- **The registry is code.** `CONTENT_PARTNERS` in `app/affiliates/content_links.py` names
  each program's code, display name, category (`hosting`, `books`, `courses`, `software`),
  the hosts its links may use, the query keys or path prefixes that mark its tracked links,
  and any query keys its own terms keep off websites, with the reason. Hostinger and
  博客來 are listed today. Adding a program is one entry plus a test run of
  `tests/test_guide_partner_links.py`; list the network's tracking domain too when its links
  go through one.
- **Write path.** `_validate_document` refuses more than three (`422
  guide_partner_link_limit`), an unknown program (`partner_link_unknown`), a URL on another
  host (`partner_link_host`, subdomains match, lookalike suffixes do not) and a forbidden
  link (`partner_link_forbidden`, e.g. Hostinger's customer-referral `REFERRALCODE`). The
  model itself only checks shape (an https URL, a code-shaped partner), so a program removed
  from the registry leaves old revisions readable.
- **Read path.** `public_article` resolves the blocks against the registry on every request
  and returns `partner_links: [{key, partner, display_name, url}]`, empty under an expired
  notice. The web draws a block only when an entry matches its partner and URL, so removing
  a program takes its links off every article at the next deploy without editing one.
  `key` is the first 16 hex characters of the URL's SHA-256: stable across reordering and
  republication, and nothing a reader cannot already see.
- **The link.** `components/guides/partner-link.tsx` draws a direct anchor to the partner's
  URL with `target="_blank" rel="sponsored noopener"` and
  `referrerPolicy="strict-origin-when-cross-origin"`, a badge ("合作連結", "広告", "광고")
  and the partner's name beside it, and the article's disclosure line — worded for buying or
  subscribing, `guides.partnerDisclosure` — above the first one. It is deliberately not the
  same-origin clickout travel offers use: that is a 303 with `Referrer-Policy: no-referrer`,
  and Hostinger's affiliate agreement forbids cloaking that hides the traffic source.
- **Counting.** The click also sends a keepalive `fetch` POST to
  `/api/travel/guides/{kind}/{slug}/partner-links/{key}/click?locale=`, which never delays
  the navigation and whose failure nobody sees. `fetch`, not `sendBeacon`: a beacon's
  `Origin` follows the page's referrer policy and the BFF refuses a write without one. The
  endpoint rate-limits per IP (60 a minute, failing closed), looks the link up in the
  currently published translation — never trusting the request for a partner or URL — and
  writes one `affiliate_clicks` row with no identity: `partner` and `brand` are the program
  code, `module` its category, `placement` `life` or `guide`, `sub_id`
  `cnt_<category>_<locale>_<placement>` (stored only, never sent), `destination_summary` the
  article slug until `2026-09-12-attribute-affiliate-clicks-to-the-guide` adds a column, and
  `status='clicked'` because nothing was redirected. Drafts, hidden or expired articles,
  other locales and unknown keys answer 404 and write nothing. The count is a floor: a
  reader without JavaScript or with a blocker follows the link uncounted.
- **Editor.** The block's program list comes from `GET /admin/guides/partners`; without it
  the editor offers no partner-link block. The preview shows a placeholder, never the link,
  and a block whose program has left the registry keeps showing that code rather than
  silently switching to another program.

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

One remains of the two filed while the lifestyle section was planned:

- `tasks/open/2026-09-12-guide-topic-admin-crud.md` — a topic still needs a seed migration,
  which contradicts what this file and `GuideTopic`'s own docstring promise.

The other, a `link` block that published tracked URLs undisclosed and uncounted, was closed
by the partner-link work: tracked ordinary URLs are refused on write and paid links have a
block of their own (see "Partner links").

The sitemap is an index over one child per section and locale (`docs/seo.md`), each child
holding up to 5,000 (article, locale) rows read from `GET /guides/sitemap` in pages; the
shared 1,000-row budget the two sections used to compete for is gone. `pack_cli lint` warns
per child at 4,000 rows (`SITEMAP_WARN_ROWS`), naming the child, so the next split -- most
likely `life-zh-TW`, which carries the bulk of the lifestyle section -- is planned before a
row is evicted rather than after.

## Advertising

Article pages — and only article pages — can carry Google AdSense: up to three in-article
units, plus whatever overlay formats (anchor, vignette, Multiplex) the AdSense account's Auto
ads settings turn on for the same tag. Everything about it is off by default;
`docs/adsense-feasibility.md` is the full evaluation and records the owner's decisions.

- **Where.** `/{locale}/guides/{intel,howto}/{slug}` and `/{locale}/life/{slug}`, decided by
  `isAdsenseArticlePath` (`apps/web/lib/adsense.ts`). Hubs and listings are "no content"
  screens outside zh-TW, `/share/{token}` has its secret in the URL, and community, account
  and trip pages are private — none of them may ever carry a slot.
- **When.** All four must hold: the host is the production origin, the request carries
  neither `DNT: 1` nor `Sec-GPC: 1`, the back-office `adsense` card is on with a valid
  publisher id and slot id (`GET /api/v1/ads/config`), and the article is genuinely
  published in this locale. Otherwise the page renders no slot and no reserved space, and
  the browser makes no request to Google.
  That last condition is checked in the layout, not only in the page: an article-shaped URL
  whose article is missing, unpublished or untranslated renders the "article unavailable"
  screen, and the layout decides whether to load the tag before the page gets to say so.
  Advertising on a no-content screen is exactly what the programme policies forbid.
  `getGuideArticle` is React-cached, so the layout and the page share one read.
- **What.** In-article units, all sharing the one configured slot id, placed by
  `adsensePlacements` (`apps/web/lib/adsense.ts`):
  - The first is no earlier than after the first level-2 heading and its first paragraph,
    so never above the hero (the LCP element). A hero is optional and is most of what
    separates the headline from the first section, so an article without one needs
    `MIN_BLOCKS_BEFORE_WITHOUT_HERO` of body above it instead — otherwise the ad can be the
    first thing in the opening viewport.
  - Every unit keeps `AD_CLEARANCE_BLOCKS` of body between itself and any `offer` or
    `partner_link` block on either side, and before the end of the body, where the automatic
    partner panel follows. The placement policies forbid an ad beside an interactive element,
    and those partner buttons and links are the revenue it must not eat; an ad beside a
    partner link would also blur which of the two is the site's own recommendation.
  - A unit only follows a paragraph or a list, never a heading, an image or a table.
  - `MIN_BLOCKS_AFTER` blocks must follow the first unit, so a short article gets none;
    units are `MIN_BLOCKS_BETWEEN` blocks apart, one per `BLOCKS_PER_AD` blocks of body, at
    most `MAX_ADS`.
  - The first unit requests its ad on mount; the others wait until they are within about a
    screen of the viewport (`ArticleAdSlot`'s `lazy`). A unit Google leaves unfilled
    (`data-ad-status="unfilled"`) collapses instead of keeping an empty reserved box.
- **Overlay formats.** Anchor, vignette and Multiplex come from the AdSense account's Auto
  ads settings, not from this code; in-page Auto ads stay off there because they could land
  beside a partner button and reserve no space. The tag is only loaded on article pages, so
  nothing else can show them. An anchor sits above everything, so `AnchorAdOffset`
  (`apps/web/components/ads/anchor-ad-offset.tsx`) measures how much of the top or bottom
  edge it covers — from geometry, not the tag's undocumented attributes — and `globals.css`
  moves the mobile bottom navigation, the sticky header and the page's bottom padding out
  of its way.
- **Personalisation.** Non-personalised ads unless `adsense_cmp_enabled` says a
  Google-certified consent message ("Privacy & messaging") is published in the AdSense
  account; then the reader's own answer decides, and the tag loads and shows that message
  itself for the EEA, the UK and Switzerland. Nothing extra is loaded for readers elsewhere,
  and a DNT/GPC browser sees no advertising and therefore no consent message at all. The flag
  is the only thing that may allow personalisation: forcing `requestNonPersonalizedAds`
  alongside a published message would override whatever the reader chose.
- **Document boundary.** The two article routes live under `app/(ads-public)/`, a second root
  layout. Next.js performs a complete document navigation across that boundary, so the ad
  runtime is discarded before a reader reaches their account or a trip — removing a React
  `<Script>` could not do that (`docs/stay22-module-switch.md:41-62`). The same layout omits
  the two providers that fetch `/auth/me`, so no answer about the reader exists in a document
  Google's tag can read. The cost is a full page load on hub → article navigation, paid
  whether or not advertising is on.
- **CSP.** `proxy.ts` emits the relaxed, AdSense-compatible policy only for a request that
  could actually be served an ad; every other response keeps the strict policy unchanged,
  byte for byte (`lib/csp.test.ts` pins it in full). The proxy and the renderer share one
  gate, `adsenseRequestGate`, so they cannot drift apart — they used to decide separately,
  and the proxy's half was the looser: a DNT request got a loosened policy for ad code it was
  never going to receive. The one condition the proxy still cannot apply is whether the
  article exists, which needs an API read it cannot afford per request; such a page carries
  no ad code either way.
- **ads.txt.** `apps/web/public/ads.txt` is a build-time file naming one publisher id, while
  the id itself is back-office configuration. Changing the id therefore also means changing
  that file and redeploying, or Google treats the inventory as unauthorised —
  `2026-09-13-adsense-ads-txt-drift` is the ticket to remove that footgun.
- **Query strings.** With advertising on, an article URL carrying a query redirects to the
  clean path before the document loads, because the ad tag can read `location.href` for
  itself. The cost is that `utm_*` and `gclid` do not survive to an article page while
  advertising is on, so first-party campaign attribution and the paid-traffic measurement in
  `2026-09-13-google-ads-conversion-measurement` would both need this relaxed first. It is
  one condition in `app/(ads-public)/[locale]/layout.tsx` if the owner decides the trade is
  the wrong way round.

## Article inline links and code (2026-09-14)

Article-only `rich_paragraph` stores 1–80 text/link children and preserves meaningful spaces between them; a link uses the existing ordinary URL validator and affiliate checks. The public renderer keeps same-site links in the current tab. `code` stores literal code (up to 24,000 characters), an optional language and filename, preserving indentation and line endings after CRLF normalization. It renders escaped text with a copy button; no evaluation or Markdown/HTML execution occurs. Both blocks round-trip through the existing admin draft, preview, publication and pack import paths. Existing paragraph/list/heading documents remain readable.

The Gemini directory and all article navigation share `apps/web/lib/guide-series.json`; publication of the hub gates its site entry. See [the series maintenance and release procedure](gemini-series/README.md). No series database table or new article URL scheme is introduced.
