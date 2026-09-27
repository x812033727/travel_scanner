---
id: 2026-09-27-video-binge-web
title: Video binge W5: one-button form, series cards, compilation download, routes and strings
status: done
priority: P1
area: web
owner: claude-fable
claimed_at: 2026-09-27T12:04:47Z
created_at: 2026-09-27T11:43:46Z
completed_at: 2026-09-27T12:39:41Z
branch: claude/keen-hamilton-plu6kp
depends_on:
  - 2026-09-27-video-binge-api
scope:
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-drama-settings.tsx
  - apps/web/app/api/admin-video-download
  - apps/web/app/api/video/automation/series
  - apps/web/messages
  - apps/web/components/admin-video-drama-settings.test.tsx
---

# Video binge W5: one-button form, series cards, compilation download, routes and strings

## Why

The owner wants one button that starts a whole binge series (docs/videos/BINGE.md): pick a
genre, a lead, a length and a visual tier and let the worker do the rest. The series tab only
had the classic form (slug, title, premise, chapter shape), the series cards did not show the
binge fields or the compilation's progress, a compilation's 1080p cut had no way off the host
without SSH, the worker had no route for the compilation job, and the drama settings page had
no field for `series_max_in_flight` although the API now allows up to 6.

## Definition of done

- [x] A 「一鍵開拍」 form above the classic one: six genre cards, the lead, an optional premise
      (required for `custom`), total minutes (30–480, default 120), minutes per episode (2–4),
      three visual-tier cards (default `hybrid`), the style preset and a note. It posts the
      binge fields with `hands_off: true` and `compilation: true` and no slug, title or shape.
- [x] A live quote from `GET /admin/video-automation/series/binge-quote` beside the form:
      episodes, chapters, clip seconds, images, US$ and one line per monthly budget, red with
      「先到設定分頁調高」 when the month cannot cover it. The button stays enabled: the worker
      waits on a 429, it does not break.
- [x] Series cards and the series page show the genre, tier, 「免關卡」 and the compilation
      state (waiting, queued, making, done); the series page has the 「合集」 block with the
      compilation project's step, an open link, the 1080p download when `download_available`,
      a 「做合集」 action for a finished series and a 「免關卡」 switch that patches `hands_off`.
- [x] A compilation's ready card and video page carry 「下載 1080p 成片」 through the BFF
      route `apps/web/app/api/admin-video-download/[slug]` (streams, forwards Range and
      Content-Disposition, 30 s header deadline); the drama-settings page has
      `series_max_in_flight` with a maximum of 6.
- [x] Worker routes `…/series/[slug]/compilation/start` and `…/done` forward to the API like
      the sibling series routes; strings in all five locales; vitest on each component and route.

## Steps

- [x] Routes and their tests.
- [x] Review card, reviews page, drama settings.
- [x] Series component: form, quote, cards, series page compilation block, doc notes.
- [x] Five locales; `lint:web`, `typecheck:web`, `check:i18n`, `test:web`.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-series.test.tsx components/admin-video-reviews.test.tsx components/admin-video-drama-settings.test.tsx app/api/admin-video-download app/api/video/automation/series
```
On the site: 漫劇 tab → the form → 一鍵開拍; the new series appears with 「免關卡」 and 「合集：等每一集做完」.

## Notes

- 2026-09-27: done on `claude/keen-hamilton-plu6kp` with the other binge tickets. The form
  sends `target_minutes` for the minutes per episode (the API's existing name) and
  `total_minutes` for the whole; the API derives `planned_episodes` and
  `episodes_per_chapter` (`binge_shape`).
- The quote is keyed by the request it answers, so a slow earlier answer never overwrites a
  newer one (the `react-hooks/set-state-in-effect` rule shaped this).
- The tutorial list on `/admin/videos` still filters `format === "drama"`, so a compilation
  is reached from the series page's 「合集」 block, the drama tab's ready card and the video
  page, not from the tutorial group.
- `DramaSettings` lives in `admin-video-settings.tsx` (out of scope), so the drama-settings
  component types `series_max_in_flight` locally; fold it into `DramaSettings` when that file
  is next touched.
