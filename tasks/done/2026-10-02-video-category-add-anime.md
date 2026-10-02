---
id: 2026-10-02-video-category-add-anime
title: Video category: add anime (動漫)
status: done
priority: P2
area: api
owner: claude-opus-5-5-magical-ptolemy
claimed_at: 2026-10-02T00:26:35Z
created_at: 2026-10-02T00:26:33Z
completed_at: 2026-10-02T00:44:09Z
branch: claude/magical-ptolemy-7ivtcd
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/migrations/versions/0119_video_category_anime.py
  - apps/api/tests/test_migration_0116_video_project_category.py
  - apps/api/tests/test_migration_0119_video_category_anime.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - docs/videos/HANDS-OFF.md
---

# Video category: add anime (動漫)

## Why

The owner asked for one more video category: anime (動漫). The review page on
/admin/videos filters and files videos by `category`, one of a fixed list kept in
`apps/api/app/models.py`, `tools/video/core/schema.mjs`, the web list and the
`ck_video_project_category` check (migration 0116); there was no code for anime.

## Definition of done

- [x] `anime` is a valid category in the model, the API schema, the database check,
      the video tools' `video.json` schema and the admin list's filter and picker.
- [x] The category has a label in all five locales (zh-TW 動漫).

## Steps

- [x] Add `anime` to `VIDEO_CATEGORIES` (models, schemas, web, tools) and HANDS-OFF.md.
- [x] Migration 0118 rebuilds `ck_video_project_category` with the new code; the
      downgrade unfiles anime videos first (category back to NULL).
- [x] Five-locale labels.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_migration_0116_video_project_category.py tests/test_migration_0119_video_category_anime.py tests/test_video_reviews.py -q
npm run check:i18n && npm run typecheck:web && npm run test:tools
```

## Notes

0116 keeps its own ten-code list frozen: it already ran on the host, so the new code
goes through a new migration that drops and recreates the check under its name, as
0117 rebuilt the stage-prompt checks.
