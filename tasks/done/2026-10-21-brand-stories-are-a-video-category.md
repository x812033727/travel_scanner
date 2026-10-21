---
id: 2026-10-21-brand-stories-are-a-video-category
title: "Brand stories are a video category: no daily count, titles tagged on the way out"
status: done
priority: P2
area: api
owner: claude-opus-5-5-story-category
claimed_at: 2026-10-21T05:50:07Z
created_at: 2026-10-21T05:49:07Z
completed_at: 2026-10-21T06:31:05Z
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/stories.py
  - apps/api/app/video_automation/story_cli.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/cli.py
  - apps/api/app/video_youtube/requests.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/tests/test_video_story.py
  - apps/api/tests/test_video_story_admin.py
  - apps/api/tests/test_video_story_redo.py
  - apps/api/tests/test_video_youtube_story_title.py
  - apps/api/tests/test_video_youtube_sync.py
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
  - docs/videos/STORY.md
  - .agents/skills/youtube-video/references/story.md
---

# Brand stories are a video category: no daily count, titles tagged on the way out

## Why

The owner said on 2026-10-21 (重新整理品牌故事類別): a brand story is a video category like
觀念解說, not something the worker starts in order within a daily count, so the daily count and
the automatic pacing around it go. Every brand story's title must also carry 「｜品牌故事」,
before the captions tag 「｜CC字幕」, on YouTube. The worker adds both when it packages a video
(#1617), but packages made before that, and titles the owner retypes on the card, still go out
without the story tag.

## Definition of done

- [x] A story series has no daily count: the worker never holds a story for the day's count or for
      the upload buffer; only a paused series and the drama-wide in-flight and monthly limits hold.
- [x] /admin/videos 品牌故事 has no per-day control, and the import form asks for none.
- [x] A story plan or import file no longer needs `series.episodes_per_day` (one that has it still
      imports; the value is ignored).
- [x] Every title the site sends YouTube for a video in the `story` category ends with
      「…｜品牌故事｜CC字幕」 (per language), whatever package or card text it came from.

## Notes

- The `video_drama_series.episodes_per_day` column stays, unread; dropping it is a later migration.
- Ticket 2026-09-28-video-story-rollout (每天一支七天，再調成每天兩支) no longer applies.
- Claimed with `--force` over stale claims on the same shared files (the board's 2026-09/10
  story, language and Studio-link tickets); none of their work was touched.
- The publishing slots (12:00 and 20:00 Taipei) are still suggested beside a story ready to
  upload on /admin/videos: that is the upload schedule, not production, and was left as it is.
- The site adds the story tag in `requests.captioned(..., story=True)` from the video's category
  (`sync.Package.story`), for both the API upload and the VPS Studio uploader. A title already
  on YouTube takes it the next time the site sends that video's details; the channel-wide
  `video-youtube-caption-titles` retitle still adds only the captions tag.
