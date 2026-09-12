# 旅遊情報與攻略專區

## What this is, and what it is not

First-party articles written by the team in `/admin/guides`: **情報** (`intel` — time-bound
notices: fare deals, transport changes, entry rules, seasonal events) and **攻略** (`howto`
— evergreen how-to: pre-trip preparation, transfer tutorials, sample itineraries).

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

1. **Kind** — `intel` or `howto`. Fixed, two values, a `CHECK` constraint. It is part of the
   URL, so it must not change once a locale is published.
2. **Destination** — `guide_articles.destination_id`, validated against
   `app/destinations/catalog.py` (the same ids as `/destinations/{id}`). **Nullable**: an
   article like "which Japan Rail Pass to buy" spans cities and must still have a home.
3. **Topics** — many per article, rows in `guide_topics` with one label per locale in
   `names_json`, the shape `HotspotTheme` already uses. An editor can add a topic without a
   deploy and without an i18n catalog change.

Seven topic slugs (`culture`, `nature`, `family`, `nightlife`, `viewpoint`, `food`,
`shopping`, `hotel`, `beach`) are shared verbatim with `app/discovery/taxonomy.py` so a
guide and an attraction that share a subject can find each other later. A test asserts the
labels stay byte-identical; nothing else stops two tables drifting.

## Storage

`site_pages` keys a document by `(slug, locale)` in one table because its slug set is four
fixed values. An article cannot: its slug, kind, destination, topics and validity belong to
the article, not to any one translation, and five copies drift. Hence two layers.

```
guide_articles          identity + taxonomy, language-independent, own `version`
guide_article_locales   one row per translation: version, draft_json, published_version,
                        published_at  (the SitePage role)
guide_article_revisions append-only history, enforced by a database trigger
guide_topics            slug + names_json + display_order + is_active + source
guide_article_topics    join
```

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
GET /api/v1/guides?locale=&kind=&destination=&topic=&cursor=&limit=
GET /api/v1/guides/topics?locale=
GET /api/v1/guides/sitemap
GET /api/v1/guides/{kind}/{slug}?locale=
```

`GET /guides/sitemap` is the publication-aware enumeration `apps/web/app/sitemap.ts` consumes:
one row per published, non-expired article × locale, capped at 1,000 and ordered newest first. The article response carries `published_locales` so the web layer can emit
hreflang for the translations that actually exist.

Admin (`content.manage` for writes):

```
GET    /api/v1/admin/guides                              list + per-locale state
POST   /api/v1/admin/guides                              create + first locale draft
GET    /api/v1/admin/guides/{id}?locale=
PUT    /api/v1/admin/guides/{id}                         taxonomy only
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
/{locale}/guides/{kind}/{slug}        the article
/{locale}/admin/guides                the editor
```

`[kind]` is a dynamic segment holding exactly two literal values; anything else is a 404.
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

### Per-locale hreflang

Publication is per locale, so the root layout's all-five alternate set would advertise
translations that do not exist. The article page overrides `alternates.languages` with
exactly the locales the API reports as published, and offers `x-default` only when English
is among them. A locale that was never written renders a "not in your language" page,
`noindex`, listing the languages that do exist.

### Navigation

`/guides` is in `primaryNavLinks` with **no feature flag**, and the header renders it
outside the three mutually exclusive navigation modes. Adding it to `primaryNavLinks` alone
would make it invisible whenever discovery or community mode is on — the defect
`2026-09-11-no-sign-in-entry-in-discovery` records. `components/guides-navigation.test.tsx`
holds that line. The phone header gets its own entry in the discovery branch, which returns
before the menu sheet is rendered. The bottom tab bar is deliberately left at four tabs.

### Caching

The loaders are `cache: "no-store"` with a 3-second abort and React `cache()` for
per-request dedupe. `docs/seo.md` asks moderated listings to stay uncached, and a
five-minute window in which a withdrawn fare notice is still live is exactly what the
publication gate exists to prevent.

## Still open

The sitemap wiring and the `攻略` relabel both landed in PR #404, together with the footer and
destination-page links. What is left is one API-side defect: `published_at` records the first
publication only, so a corrected notice keeps its original `lastmod` and tells Google nothing
changed. `tasks/open/2026-09-11-guide-lastmod-republication.md` holds the fix, which reads the
currently published revision's timestamp instead of unfreezing the column the list orders by.
