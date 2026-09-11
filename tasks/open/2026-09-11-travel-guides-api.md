---
id: 2026-09-11-travel-guides-api
title: Travel guides content API and schema
status: in-progress
priority: P1
area: api
owner: claude-opus-5-guides
claimed_at: 2026-09-11T12:59:36Z
created_at: 2026-09-11T12:37:41Z
completed_at:
branch: claude/travel-info-guide-section-4ulqsj
depends_on: []
scope:
  - apps/api/app/guides
  - apps/api/migrations/versions/0072_travel_guides.py
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/auth/service.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_migration.py
  - docs/travel-guides.md
  - apps/api/app/i18n.py
---

# Travel guides content API and schema

## Why

The owner wants one place for every piece of travel intel and every guide, written by the
team. The site has nowhere to put that today:

- `/explore` (discovery) stores no content of its own. It aggregates already-approved
  catalog rows, **external** article and YouTube references (`HotspotGuide`,
  `app/models.py:1544`) and community stories. It is `noindex` and gated by
  `DISCOVERY_ENABLED`.
- `/destinations/{id}` renders from the source-controlled destination catalog, not from
  anything an editor can write.
- `site_pages` is a four-slug legal CMS, not an article store.

So this adds a first-party article system: draft, version, publish per locale, withdraw.

## Definition of done

- [x] An administrator with the `content` role can create an article, save drafts, publish
      one locale, withdraw it and restore an earlier revision.
- [x] A reader sees only what is published **in their own locale**. No language fallback,
      no draft leak, and a damaged published pointer is a 503, never the draft.
- [x] Time-sensitive intel carries `valid_until`. An expired notice keeps its URL (so
      existing links do not 404) but leaves the listings and the sitemap.
- [x] `GET /guides/sitemap` gives the web layer publication-aware enumeration, which
      `docs/seo.md:61` records as missing.
- [x] Revision history cannot be rewritten, enforced by a database trigger on both
      PostgreSQL and SQLite.

## Steps

- [x] `app/guides/models.py`: five tables; identity and taxonomy separate from the
      per-locale draft/publication row.
- [x] `migrations/versions/0072_travel_guides.py` with fresh-database guards, the
      append-only trigger, and the topic vocabulary seeded (topics only, never an article).
- [x] `app/guides/schemas.py` importing the `site_pages` block union rather than copying
      its link validator.
- [x] `app/guides/publication.py`: one definition of "public in this locale", shared by the
      list, the article and the sitemap.
- [x] `app/guides/service.py` (public reads) and `app/guides/admin_service.py` (authoring).
- [x] `app/guides/router.py`, wired in `main.py`; `/admin/guides` mapped to
      `content.read`/`content.manage` in `auth/service.py`.
- [x] `tests/test_guides.py` and `tests/test_guides_migration.py`.

## How to verify

```bash
cd apps/api
uv run ruff check . && uv run mypy app
uv run pytest tests/test_guides.py tests/test_guides_migration.py -q
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_guides.py tests/test_guides_migration.py -q
uv run pytest -q          # 3,177 passed / 203 skipped at the time of writing
```

## Notes

**Declared scope overlap — `apps/api/app/i18n.py`.** `tests/test_error_localization.py`
requires every error code raised outside an `admin`/`deployments` path to carry a sentence
in all five locales, and that table only works in `app/i18n.py`: the test imports
`app.i18n` alone, so a merge performed from a feature module would not have run when the
test runs standalone. The public surface was first reduced from 13 codes to 2 by splitting
authoring into `app/guides/admin_service.py`; the remaining two
(`guide_article_unavailable`, `guide_cursor_invalid`) are appended as `_GUIDE_ERRORS` in
the same style as `_SITE_PAGE_ERRORS` and `_SAVED_FLOW_ERRORS`. `claim` refused this scope
because `2026-09-09-frontend-flow-saved-api` and `2026-09-11-food-reservation-platforms`
hold the same file, so it was taken with `--force` and declared here rather than edited
undeclared. The change is a ten-line append at the end of the file; if it does conflict,
keep both feature blocks.

**Things that cost time, so the next agent does not repeat them:**

- `default=uuid4` on a column is applied at INSERT, so `article.id` is `None` while you are
  still building the child row. Assign the id explicitly when one object needs another's.
- The session keeps instances across commit (`expire_on_commit=False`) and the writes are
  conditional UPDATEs the ORM never sees, so every read-back after a write needs
  `.execution_options(populate_existing=True)` or it echoes the superseded version.
- `AdminAuditLog.target` is `String(128)` and a slug may be 120 characters, so the audit
  target is keyed by article id, not slug. It also survives a rename.
- The append-only trigger lives in the migration, so `tests/test_guides.py` (which builds
  tables with `Base.metadata.create_all`) cannot see it. That assertion belongs in
  `tests/test_guides_migration.py`, which runs the real migration.
- Seven topic slugs are shared verbatim with `app/discovery/taxonomy.py`. A test asserts
  the labels stay byte-identical, because nothing else stops two tables drifting.

**Not in this task:** the `/guides` web pages, the admin panel, navigation entries, the
sitemap wiring and the `攻略` relabel in `apps/web/lib/discovery-copy.ts`.
