# Hotspot themes and first-party introductions

A hotspot keeps its single `category` (culture, food, nature, beach, family, viewpoint,
shopping, nightlife) and gains any number of **themes** on top of it:

- a **season** it is known for — 賞櫻, 賞楓, 滑雪, 花火, 燈飾, 賞雪 — with the months that
  apply, so the explorer can mark what is in season and the planner can pull seasonal
  spots when a trip's dates fall inside the window;
- a **shop type** — 藥妝, 電器, 百貨, Outlet, 伴手禮, 二手古著, 動漫周邊, 商店街／市場 — on
  `category = "shopping"` hotspots, which is how dedicated stores (a drugstore, an
  electronics chain, an outlet mall) join the catalog without a second directory.

Themes are orthogonal to `category`: a temple is `culture` *and* 賞櫻; a shopping street is
`shopping` *and* 燈飾. The single `category` still drives the card accent and the planner's
interest quota; themes add the second axis the product asked for.

## Data

| Table | Purpose |
| --- | --- |
| `hotspot_themes` | The taxonomy: `slug`, `kind` (`season` or `shop`), one label per site locale in `names_json`, the default `months_json` of a season theme, `display_order`, `is_active`, `source` (`seed` or `admin`). |
| `hotspot_theme_links` | One theme on one hotspot. `months_json` overrides the theme's months for this hotspot (Sapporo's sakura is May, Honshu's is March–April). `source` says who put it there: `seed`, `admin` or `ai`. `is_active = false` is an administrator's tombstone. |
| `hotspot_intros` | One first-party introduction per hotspot per locale (`body`, `review_status`, `source` `ai` or `manual`, the drafting `ai_provider`/`ai_model`, reviewer fields, `metadata_json`). Readers only see `approved` rows. |
| `hotspot_intro_runs` | One AI drafting job per hotspot, the shape of `hotspot_guide_ai_search_runs` without the search-only columns and with Gemini allowed. |

All four tables are created by migration `0050_hotspot_themes_intros`; the JSON columns
are PostgreSQL `json` like every other JSON column in `app/models.py` (nothing is filtered
inside them in SQL).

### Months

A season theme carries a default month list (`hotspot_themes.months_json`, e.g. `[3, 4]`
for sakura, `[11, 12, 1, 2]` for illuminations — lists may wrap the year). A link may
override it with its own list; the public payload always shows the **effective** months,
so consumers never need to know which one applied. Shop themes carry no months.

### Who owns a link

Three sources may attach a theme, and the sync that runs on every collect run must not
undo the other two:

- `seed` links come from `apps/api/app/hotspots/theme_bootstrap.json` and follow the
  file exactly: created when a pair appears, months and note refreshed, deleted when the
  pair leaves the file.
- `admin` and `ai` links are never created, changed or removed by the sync.
- When an administrator removes a seeded pair, the row stays as a tombstone
  (`is_active = false`, `source = 'admin'`), so the next sync sees the pair exists and
  does not bring it back. Deactivating a theme (`hotspot_themes.is_active = false`)
  hides it from the filter, the facets and every card; the seed sync never reactivates it.

## Seeding

- `apps/api/app/hotspots/theme_catalog.py` lists the 14 themes (`THEME_SEEDS`) with five
  locale labels each and validates itself on import, like `foods/category_catalog.py`.
- `apps/api/app/hotspots/theme_bootstrap.json` lists which hotspot carries which theme:

  ```json
  {"slug": "deep-cts-q1298335", "themes": ["sakura"], "months": {"sakura": [5]}}
  ```

  `slug` is the **resolved** catalog slug (explicit `slug`, a `LEGACY_SLUGS` entry, or
  `wikidata-<qid>`). `app.hotspots.themes` validates every row on import — an unknown
  slug, an unknown theme, months on a shop theme, or a shop theme on a hotspot whose
  category is not `shopping` fails the import, on purpose.
- `sync_hotspot_themes(session)` runs inside `collect_hotspots()` right after the catalog
  and food seeds, so every collect run keeps links in step with the file. For a one-off
  back-fill without a collect run: `cd apps/api && uv run python -m app.hotspots.themes`.

Seed coverage in the first version is uneven by design: sakura and autumn leaves cover
Japan and Korea well; skiing has only the two Sapporo-area mountains the catalog holds;
outlet malls, drugstore chains and electronics stores arrive with the dedicated-store seed
batch (a separate task, gated on coordinate verification).

## Public API

- `GET /hotspots/rankings?theme=<slug>` — single-select, like `category`. The slug is
  looked up among active themes (administrators add themes at runtime); an unknown or
  deactivated slug is `422 unsupported_theme`.
- Every ranking item carries `themes`, in catalog order (seasons first, then shop types,
  each by `display_order`), names localised by `X-Travel-Locale` exactly like `area.name`
  (zh-CN falls back to the Traditional label, then English):

  ```json
  "themes": [{"slug": "sakura", "kind": "season", "name": "賞櫻", "months": [3, 4]}]
  ```

- `GET /hotspots/facets` gains `themes`: every active theme, zero counts included, with
  the public hotspot count under the same conditions as the other facets:

  ```json
  "themes": [{"slug": "sakura", "kind": "season", "name": "賞櫻", "months": [3, 4], "count": 33}]
  ```

- `GET /hotspots/for-planner` recommendations carry `themes` as a list of slugs.

Theme labels never enter the web message catalogs; the explorer renders `name` from the
payload and formats months with `Intl.DateTimeFormat`.

## Planner seam

`_collect_ranked(..., theme=)` pages one ranking filtered by a theme, and every
`ItineraryHotspot` (and therefore every planner candidate) carries `themes` as slugs. The
traveller-facing preference (`shop_themes` on `SearchPreferences`, the store-type chips on
the trip form, and the seasonal boost from the trip's months) is a separate task built on
this seam.

## First-party introductions (contract)

The persistence, the review endpoints and the AI drafting job are separate tasks; the
tables exist so the migration ships once. The contract they build on:

- One row per (hotspot, locale); `review_status` is the row's state. A draft arrives as
  `pending`; only `approved` bodies reach the public payload, in the request locale with
  zh-CN ⇄ zh-TW as the only fallback (an English reader never gets Japanese prose).
- The generator writes through `app.hotspots.intros.upsert_hotspot_intro_draft(...)`,
  which never silently replaces an `approved` body (it keeps the previous text in
  `metadata_json["previous_body"]` when explicitly told to replace).
- `hotspot_intro_runs` records each job with the admin's idempotency key, the vendor and
  model used, and a `result_json` of what landed, what was kept and what was rejected.

## Follow-ups filed from this work

- Four seeds carry the wrong category `shopping` (榴岡公園, 廣島城, 嚴島神社, 八公山); their
  season links are in place, the category fix belongs to the catalog task.
- `hotspot_guide_ai_search_runs.provider` has a CHECK without `gemini`, so selecting Gemini
  for guide search fails on insert; `hotspot_intro_runs` allows it from the start.
