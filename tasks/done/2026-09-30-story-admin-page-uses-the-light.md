---
id: 2026-09-30-story-admin-page-uses-the-light
title: Story admin page uses the light series read
status: done
priority: P2
area: web
owner: claude-opus-5-5-story-light-web
claimed_at: 2026-10-01T03:39:08Z
created_at: 2026-09-30T04:21:19Z
completed_at: 2026-10-01T03:56:10Z
branch: claude/story-admin-light-read
depends_on:
  - 2026-09-28-video-story-light-series-read
scope:
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
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

- [x] While the page shows a story series, its minute-by-minute read is the `?beats=summary`
      one; the list, filters, publishing slots and states look the same as before.
- [x] Opening a story's plan reads that story from `/episodes/{number}` and shows the whole
      plan (question, chapters, facts, sources, caveats, takeaway), with a loading and an
      error state; closing and reopening does not need a new read unless the list changed.
- [x] Drama series (long and one-off) keep the whole read: their episodes' beats are the
      chapter outlines the page shows.

## Steps

- [x] The series read lives in `admin-video-series.tsx` (`refreshed = api<Series>(...)`, the
      one that sets `storySlug`), not in the stories component: decide how the story view asks
      for `?beats=summary` (for example, read with it once `storySlug.current` is known to be a
      story, since the first read cannot know the kind).
- [x] `StoryPlan` fetches `/admin/video-automation/series/{slug}/episodes/{number}` and renders
      the answer's `beats`.
- [x] Update `admin-video-stories.test.tsx` for the two reads.

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
- Claimed with `--force` (2026-10-01): the overlaps were stale claims whose work is on main —
  `2026-09-27-video-drama-room-withdraw-a-one` (PR #870, merged 2026-09-28; `withdraw_series` is in
  `series.py`) and the two `codex-ten-drama` tickets (PR #978, merged). No open PR touches these files.
- Scope also adds `apps/web/messages/*/admin.json`: the plan's loading and error lines are new copy
  (`admin.videoStories.plan.loading`, `plan.loadError`), in all five locales. The retry button reuses
  `admin.videoSeries.retry`. No key was renamed, so no owner override is orphaned.
- No BFF route is needed: `lib/api.ts` sends every admin call through the catch-all
  `apps/web/app/api/travel/[...path]/route.ts`, which forwards any path and its query string, so
  both `?beats=summary` and `/episodes/{number}` already reach the API.
- How the light read is asked for (`admin-video-series.tsx`, `SeriesPage.load`): the first read is
  whole, since it cannot know the kind; once it said `kind: "story"` (`storySlug.current === slug`,
  the same ref that already skipped the compilation read) every later read — the minute refresh and
  the reload after any action — adds `?beats=summary`. A drama series never sets the ref, so it is
  always read whole. Opening a story series therefore costs one whole read, then light ones.
- The plan (`useStoryPlan` in `admin-video-stories.tsx`): the opened story's episode is read from
  `/episodes/{number}`; the answer is kept per episode number under a key made of the story's light
  row without its `video` (title, logline, status, dates, the summary beats) plus a counter this
  page's import bumps. Closing and reopening reuses it; a row that changed (skipped, restored,
  renamed, renumbered) or an import from this page reads it again. An import by someone else that
  rewrites only a plan's chapters is not seen until the page is reloaded — the light read carries
  nothing that says a plan changed (episode `updated_at` is not in `SeriesEpisodeOut`). A plan whose
  row the filters hide is not read. Loading shows `plan.loading`; a failure shows the server's
  message with a retry.
- Verified: the three new/changed vitest cases fail with the old components and pass with the new
  ones; the drama case passes both ways (it guards the whole read). Not checked on a local stack with
  the real backlog. Needs the API from PR #1026 deployed: an older API ignores `beats=summary` (the
  page still works, just whole) but answers 404 for `/episodes/{number}`, which shows as the plan's
  error state.
