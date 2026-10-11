---
id: 2026-10-10-offer-a-setting-for-official-pages
title: Offer a setting for official pages as a video topic source
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-10T09:02:37Z
completed_at:
branch:
depends_on:
  - 2026-10-10-official-pages-the-news-writer-declined
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/topics.py
  - apps/web/components/admin-video-settings-tutorial.tsx
  - docs/videos/AUTOMATION.md
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_automation_topics.py
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Offer a setting for official pages as a video topic source

## Why

Official pages become video topic candidates through a key on each news source
(`video_topics` in `apps/api/app/news_automation/sources.json`). Turning the whole thing
off, or a source on, means editing that file and loading it on the host. The other two
topic sources have a checkbox on `/admin/videos` (`topic_from_site`, `topic_from_search`).

This was left out on purpose on 2026-10-10: a setting needs a migration and changes to
ten files bound by the duration receipt, and the per-source key was enough to ship. Build
it only if the owner asks for one-click control.

## Definition of done

- [ ] The owner has said they want the checkbox. Without that, close this task.
- [ ] `topic_from_official` on the video automation settings, on by default so that the
      per-source keys keep deciding, with a checkbox beside the other two.
- [ ] `gather_topics` honours it and adds the same kind of note as the other two when it
      is off.

## Steps

- [ ] Migration, `models.py`, `schemas.py`, `settings.py`, the settings component, the
      five `admin.json` files, tests.
- [ ] The duration receipt increment for the bound files.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_automation_topics.py tests/test_video_automation_settings.py -q
```

## Notes

- The scope does not name the migration: add its path when the number is known.
  `apps/web/components/admin-video-settings.tsx` is not bound by the receipt but has to
  change: it holds the settings type and the list of keys the tutorial part saves.
- Bound by the receipt among these: `models.py`, `schemas.py`, `settings.py`,
  `test_video_automation_settings.py`, `admin-video-settings-tutorial.tsx` and the five
  `admin.json` files.
