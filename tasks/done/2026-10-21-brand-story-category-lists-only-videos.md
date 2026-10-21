---
id: 2026-10-21-brand-story-category-lists-only-videos
title: Brand story category lists only videos; its series move to Drama
status: done
priority: P2
area: web
owner: claude-opus-5-5-story-category
claimed_at: 2026-10-21T09:06:54Z
created_at: 2026-10-21T09:04:53Z
completed_at: 2026-10-21T09:06:59Z
branch:
depends_on: []
scope:
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
---

# Brand story category lists only videos; its series move to Drama

## Why

The owner on 2026-10-21, after #1645: the Videos tab's 品牌故事 category still opened with the
story series cards (「同時進行 1／1」「現在不開新故事」) and the import; 觀念解說 shows only its
videos. Chose: list only the videos, move the series to the Drama tab.

## Definition of done

- [x] /admin/videos 品牌故事 category shows only the video list, like 觀念解說.
- [x] The story series cards, their pages and the import are under the Drama tab, beside the
      explainer requests; a story series opens there.
- [x] An old `?story_series=` bookmark on the Videos tab goes to `?tab=drama&series=`.

## Notes

- The drama series page reads a story series' compilations once on its first read, before it
  knows the kind; that is the page's existing behaviour.
