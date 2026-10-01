---
id: 2026-09-30-story-admin-page-uses-the-light
title: Story admin page uses the light series read
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-30T04:21:19Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-light-series-read
scope:
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-stories.test.tsx
---

# Story admin page uses the light series read

## Why

The brand-story page on `/admin/videos` (`apps/web/components/admin-video-stories.tsx`)
shows a hundred stories from one read of `GET /admin/video-automation/series/{slug}`, and
that read carries every story's whole plan in `beats` (chapters, facts to check, sources,
the reviewer's caveats). With the real 100-story backlog it is 1,197,209 bytes, re-read
every minute while the page is open. The list only needs each story's `id`, `category`,
`region`, `subject` and `publish`; the whole plan is needed only for the one story the owner
opens (`?story=A01`, the `StoryPlan` panel).

Ticket `2026-09-28-video-story-light-series-read` added the API for this:

- `GET /admin/video-automation/series/{slug}?beats=summary` answers the same `SeriesOut`,
  but each episode's `beats` keeps only `id`, `category`, `region`, `subject`, `publish`
  (58,767 bytes for the real 100-story backlog, no videos yet). Without the parameter, or
  with `beats=full`, the read is whole, as before.
- `GET /admin/video-automation/series/{slug}/episodes/{number}` (`content.read`) answers one
  `SeriesEpisodeOut` with its whole `beats` and its `video`, exactly as the whole series read
  carries that episode.

## Definition of done

- [ ] While the page shows a story series, its minute-by-minute read is the `?beats=summary`
      one; the list, filters, publishing slots and states look the same as before.
- [ ] Opening a story's plan reads that story from `/episodes/{number}` and shows the whole
      plan (question, chapters, facts, sources, caveats, takeaway), with a loading and an
      error state; closing and reopening does not need a new read unless the list changed.
- [ ] Drama series (long and one-off) keep the whole read: their episodes' beats are the
      chapter outlines the page shows.

## Steps

- [ ] The series read lives in `admin-video-series.tsx` (`refreshed = api<Series>(...)`, the
      one that sets `storySlug`), not in the stories component: decide how the story view asks
      for `?beats=summary` (for example, read with it once `storySlug.current` is known to be a
      story, since the first read cannot know the kind).
- [ ] `StoryPlan` fetches `/admin/video-automation/series/{slug}/episodes/{number}` and renders
      the answer's `beats`.
- [ ] Update `admin-video-stories.test.tsx` for the two reads.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web -- components/admin-video-stories.test.tsx
```

Then on a local stack with the real backlog imported, the network tab shows the minute
read at `?beats=summary` (under 150 KB) and one `/episodes/{n}` read when a plan opens.

## Notes

- Scope adds `admin-video-series.tsx` (where the series is fetched) and the component's test
  to the one file this ticket was filed with.
- Each episode's `video` (a `ProjectSummary`, about 1–3 KB) stays in the light read; once a
  hundred stories all have videos the light read grows by roughly that much per story. If it
  passes 150 KB then, trimming `video` in summary mode is an API follow-up, not this ticket.
