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

- `apps/api/app/hotspots/shopping_bootstrap.json` holds the 30 dedicated stores the shop
  types needed. Every row's coordinate comes from a public source that names the shop
  itself — a Wikidata item's P625, or an OpenStreetMap object whose name and address are
  the shop's — so the file carries no `curated_coordinate` at all. That rule is not
  ceremony: matching on "nearest coordinate to a remembered guess" first returned
  南大沢駅 for an outlet mall, 三越劇場 for a department store, a tram stop for 狸小路 and
  a temple for 光華商場. Fifteen candidates found no such source and were left out rather
  than placed from memory; they are listed in the follow-up task.

Seed coverage is uneven by design: sakura and autumn leaves cover Japan and Korea well,
and skiing has only the two Sapporo-area mountains the catalog holds. Every shop type now
has at least two stores, outlet malls included — before the dedicated-store batch that
chip existed but returned an empty page.

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

## First-party introductions

A hotspot's "introduction" used to mean a link out to somebody else's article or video
(`hotspot_guides`). This is the other kind: a paragraph Mokaair wrote itself, saying what
the place is and when to go — which is what a shopping row or a seasonal spot actually
needs.

One row per hotspot per locale, and `review_status` is the row's whole state. Everything
lives in `app/hotspots/intros.py`.

### The rule the code is shaped around

**A draft never silently replaces an approved paragraph.** Someone read that text and
said yes to it; a later generation run that overwrote it would undo a review nobody asked
to redo. `upsert_hotspot_intro_draft(...)` therefore:

- inserts as `pending` when nothing is stored;
- replaces a `pending`, `rejected` or `disabled` row and puts it back to `pending`,
  because a fresh draft deserves a fresh look;
- leaves an `approved` row alone and returns `written=False` — unless the caller passes
  `replace_approved=True`, and even then the approved text is kept in
  `metadata_json["previous_body"]` and the row returns to `pending`.

### What a reader sees

Only `approved` rows, in their own language. zh-CN and zh-TW stand in for each other and
nothing else does: an English reader is never shown Japanese prose. The payload carries
the `locale` it actually resolved to, so a page can say which language it is showing.

`intro` rides along on every ranking item (batched, one query per page) and
`GET /hotspots/{hotspot_id}/intro` serves one on its own.

### Endpoints

| Route | Purpose |
| --- | --- |
| `GET /admin/hotspots/intros` | the review queue: filter by status, locale, hotspot, source; carries `status_counts` |
| `POST /admin/hotspots/intros/review` | approve, reject or disable a batch |
| `PATCH /admin/hotspots/intros/{id}` | edit the text or move the status; an edit records who wrote it |
| `GET /admin/hotspots/{hotspot_id}/intros` | five rows, one per locale, so a missing language reads as a gap |
| `POST /admin/hotspots/{hotspot_id}/intros` | type one by hand; approved on arrival, because the author just reviewed it |

### The AI drafting job

`POST /admin/hotspots/{hotspot_id}/intros/generate` (202, `Idempotency-Key` required)
records a `hotspot_intro_runs` row and queues one job on the `hotspot-intros` queue;
`GET /admin/hotspots/intros/runs/{run_id}` reads it back. One model call drafts every
requested locale at once, so the facts stay consistent between languages.

It publishes nothing. Everything it writes goes through `upsert_hotspot_intro_draft`
as `pending`, and by default an approved paragraph is left alone.

Two rules the code enforces rather than merely asks for:

- **The place's own text is never an instruction.** `INTRO_PROMPT` is a constant and
  the attraction travels as JSON values under `payload["attraction"]`. Hotspot names
  come from Wikidata discovery, so they are attacker-shaped input.
- **A prompt is a request; a regex is a rule.** The prompt forbids prices, discounts,
  clock times, opening hours, phone numbers and URLs — and `forbidden_claims()` checks
  the output for them anyway. A rejected draft is reported in the run's `result_json`,
  not stored. `length_ok()` likewise bounds each locale by its own script.

Vendor, model, timeout and budgets come from the `hotspot_intro_ai_*` settings, which
default to the guide search's model for the chosen vendor. Both the run count and the
per-call count are rate-limited through the same daily budget helper the guide search
uses.

`intro_targets(...)` answers which hotspots still need which locales — skipping anything
already `pending` or `approved` — so a bulk pass that is interrupted does not redraft
what already landed.

## Follow-ups filed from this work

- 大阪アメリカ村's `Q4745722` is held by the Okinawa 美國村 seed, whose coordinates point
  at Osaka. `kix-amerikamura` therefore cites the item for its coordinate but leaves
  `wikidata_item_id` null; fixing the Okinawa row frees the id.
- 龍山電子商街 and 三創生活園區 sit a few hundred metres outside every circle in the area
  catalog, so they carry no area. Drawing circles for them moves neighbouring seeds
  between areas, which belongs to the area catalog rather than to a seed batch.
- `hotspot_guide_ai_search_runs.provider` has a CHECK without `gemini`, so selecting Gemini
  for guide search fails on insert; `hotspot_intro_runs` allows it from the start.
