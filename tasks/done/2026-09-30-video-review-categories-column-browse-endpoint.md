---
id: 2026-09-30-video-review-categories-column-browse-endpoint
title: Video review categories: column, browse endpoint and pipeline report
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-30T10:00:15Z
created_at: 2026-09-30T09:58:47Z
completed_at: 2026-09-30T10:34:07Z
branch: claude/nifty-heisenberg-0ldw0i
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/migrations/versions/0116_video_project_category.py
  - apps/api/tests/test_migration_0116_video_project_category.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/import/import.mjs
  - tools/video/import/import.test.mjs
  - docs/videos/HANDS-OFF.md
---

# Video review categories: column, browse endpoint and pipeline report

## Why

`/admin/videos` mixes AI-term explainers, news pieces, tutorials, comparisons and brand stories in
one list with nothing to tell them apart, and the list has no way to narrow or search: it reads
`GET /admin/videos?shorts=exclude` once (capped at 200, silently) and groups everything in the
browser. The owner asked for content categories and a list that stays usable as the videos grow.
This is the API half: the column, the catalog endpoint, and the pipeline entries that already send
a category (schema, story, import).

## Definition of done

- [x] `video_projects.category` exists (migration 0116), one of eight codes or NULL, guarded by
      `ck_video_project_category`; the migration files `ai-news-*` sources and `ai-term-*` slugs.
- [x] A report (`ProjectIn.category`) fills only an unfiled video; the owner's choice
      (`PUT /admin/videos/{slug}/category`, `video_category_set` audit) sticks and can go back to null.
- [x] `GET /admin/videos/browse` pages the tutorials with `category` (incl. `none`), `state`
      (working/published/dropped), `q` and returns the counts behind every filter value.
- [x] `GET /admin/videos` keeps its shape; the worker and the other tabs are untouched.
- [x] `video.json` accepts `category`; brand stories carry `story`; `import` takes `meta.category`.
- [x] docs/videos/HANDS-OFF.md §影片分類 describes who files a video and how the list reads.

## Steps

- [x] Model, migration 0116 and its test (offline SQL, guards, PostgreSQL temp table).
- [x] Schemas: `VideoCategory`, `CategoryIn`, `ProjectPage` with facets.
- [x] Service: `browse_projects`, `set_category`, `_listing_statement` / `_summaries` shared with `list_projects`.
- [x] Router: `/browse` before `/{slug}`, `PUT /{slug}/category`; unit and integration tests.
- [x] tools/video: schema, story, import (+ tests); HANDS-OFF.md.

## How to verify

```bash
cd apps/api && uv run alembic heads && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0116_video_project_category.py tests/test_video_reviews_integration.py -q
npm run test:tools
```
After deploy: `alembic current` is 0116; `SELECT category, count(*) FROM video_projects GROUP BY 1`
shows the `ai-news` / `ai-terms` rows filed and the rest NULL.

## Notes

- The worker's `report()` in `tools/video/automation/flow.mjs` and `review-push` in
  `tools/video/review/sync.mjs` do not send `category` yet: both files were held by other active
  tickets when this one was claimed, so that part is `2026-09-30-video-worker-and-review-push-report`.
  Until it lands, a worker-made tutorial is filed by the owner on the page (or by the migration's rules).
- The backfill deliberately does not read the guide's `kind`: `intel`/`howto` are the travel
  section and `life` mixes AI news with everyday pieces, so it would mislabel most rows.
- The backfill compares with `substr()` rather than `LIKE`, so the offline SQL has no `%` to escape,
  and renders its constants inline (`literal_binds`) so `alembic upgrade --sql` is runnable as written.
- Full API suite (5132) and the two PostgreSQL integration files ran green locally against a
  throwaway Postgres 16; `test_admin_users_integration` needs Redis and was not run here.
