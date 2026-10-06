---
id: 2026-10-05-public-video-library-at-videos-with
title: Public video library at /videos with article embeds
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-10-05T03:47:13Z
created_at: 2026-10-05T02:52:27Z
completed_at: 2026-10-06T13:35:07Z
branch: claude/determined-clarke-1laipc
depends_on: []
scope:
  - apps/api/app/video_reviews/public_api.py
  - apps/api/app/main.py
  - apps/api/tests/test_public_videos.py
  - apps/web/app/[locale]/videos
  - apps/web/lib/videos.ts
  - apps/web/lib/videos.server.ts
  - apps/web/components/videos
  - apps/web/components/guides/article-page.tsx
  - tools/e2e-runtime-api.mjs
---

# Public video library at /videos with article embeds

## Why

The site makes YouTube videos (tools/video, /admin/videos) but readers could not find them
anywhere on it: no listing page, no link from the article a video retells. The owner asked
for a front end where articles and videos are both easy to find.

## Definition of done

- [x] `GET /api/v1/videos` lists only published videos: a YouTube id, a
      `youtube_publish_at` in the past, and not dropped. It is newest first with keyset
      paging, filters by `kind` (long or shorts), `category` and `guide` (an article slug),
      and sends no admin fields.
- [x] `/videos` shows long or Shorts tabs, the categories that have something, and cards
      that load the youtube-nocookie player only on press, each linking to its article.
      Filtered or paged views are `noindex`.
- [x] An article page shows the videos whose `source_guide` is that article, above the
      related articles.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_public_videos.py -q
npm run test:web -- videos
npx playwright test e2e/site-navigation.spec.ts   # the library case
```

## Notes

- A video uploaded private or unlisted has no `youtube_publish_at`, so it is never listed.
  The cost: a video the owner made public by hand in Studio, without the site's schedule,
  does not appear either. If that becomes common, record a publish time when the sync sees
  `privacyStatus == "public"`.
- `source_guide` is linked only while that article is active (the API joins
  `guide_articles`), so a retired article never becomes a dead link.
