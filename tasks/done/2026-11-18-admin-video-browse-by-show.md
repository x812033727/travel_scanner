---
id: 2026-11-18-admin-video-browse-by-show
title: Browse admin videos by show, series and topic
status: done
priority: P1
area: web
owner: claude-opus-5-5-video-shelf
claimed_at: 2026-11-18T01:50:08Z
created_at: 2026-11-18T01:49:18Z
completed_at: 2026-11-18T07:03:23Z
branch: claude/kind-mccarthy-5m28jo
depends_on: []
scope:
  - apps/web/components/admin-video-stories.test.tsx
  - apps/api/app/video_automation/series.py
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-browser.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/api/app/video_reviews/shelf.py
  - apps/api/app/video_reviews/shelf_cli.py
  - apps/api/migrations/versions/0147_video_project_shelf.py
  - apps/api/tests/test_video_shelf.py
  - apps/api/tests/test_migration_0147_video_project_shelf.py
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/api/app/models.py
  - apps/api/app/cli.py
  - apps/api/tests/test_video_reviews.py
---

# Browse admin videos by show, series and topic

## Why

On /admin/videos the 全部影片 catalog filters by one column, `video_projects.category`. 奇聞檔案局
(curio-*) and 原來如此事務所 (sothatswhy-*) are both `explainer`, and every imported drama
(種田娶妻打天下, its live-action remake, 恁祖媽今年18, 偶的江湖…) is `drama`, so with hundreds of
videos the owner cannot find one show, one drama or one topic (H-歷史懸案, 生物動物與植物…).
The owner asked (2026-11-18) for the two explainer shows to stand on their own, filterable by
their topics, and for the dramas to be switchable one drama at a time.

## Definition of done

- [ ] The catalog's first row of pills is the show: 奇聞檔案局 and 原來如此事務所 on their own, then
      the categories (觀念解說 now holds only the other explainers).
- [ ] Picking 漫劇 (or any show with series) offers a row of its dramas with counts; picking
      奇聞 or 原來 offers a row of their topics with counts.
- [ ] A drama or a topic lists in episode order; the choice lives in the URL; old `?category=`
      links still work.
- [ ] Existing rows are filled by a backfill command run once after deploy.

## Steps

- [x] Migration 0147: nullable `series_key` (indexed) and `topic` on `video_projects`.
- [x] `app/video_reviews/shelf.py`: one function from a project to (series_key, topic), reusing
      `app/video_backup/target.py` (`drama_series`, `SLUG_PREFIXES`, `ai_episode_parts`), called
      wherever slug, category or series_slug is written.
- [x] Backfill CLI `video-shelf-backfill` (dry run by default, `--apply`).
- [x] `GET /admin/videos/browse`: `shelf`, `series`, `topic` filters and facets.
- [x] Web: three rows of pills in `admin-video-browser.tsx`, labels in five locales.

## How to verify

API: `uv run pytest tests/test_video_shelf.py tests/test_video_reviews.py -q`.
Web: `npm run test:web -- admin-video-reviews`. After deploy, on the host:
`docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-shelf-backfill`
then again with `--apply`, and click 奇聞 → H-歷史懸案 and 漫劇 → 恁祖媽今年18 on /admin/videos.

## Notes

- Claimed with `--force` (owner approved, 2026-11-18): ten older in-progress claims from
  2026-10-12 to 2026-11-13 list `apps/web/messages` or the shared API files, which every admin
  change touches.
- The catalog's drama param is `shelf_series`, not `series`: the drama tab already keeps its open
  series under `?series=`. The API param is `series`.
- Backfill is `python -m app.cli video-shelf-backfill` (reports only) then `--apply`, the video
  CLIs' convention, not `--dry-run`.
- Left for later: the two groups above the catalog (ready to upload, needs you) are not filtered.
- The explainer shows have no series row and no `series_slug` in their video.json; the slug
  prefix is the only thing that says which show a video is, which is also what Drive backup uses.
