---
id: 2026-10-23-show-brand-story-preproduction-intake-progress
title: Show brand story planning and script intake beside finished-video progress
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-23T12:15:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_series.py
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
---

# Show brand story planning and script intake beside finished-video progress

## Why

The C01–C20 planning intake and ten eligible script cards have been saved to the
video backend. This `kind=story` series renders in `admin-video-stories.tsx`:
its list card shows status and quota without preproduction intake, and its
detail counts episodes with `status=done` as finished films. The generic
`0/20` progress in `admin-video-series.tsx` belongs to a different series
view. The story UI needs separate persisted plan and script-card signals.

## Definition of done

- [ ] The actual C-series story list and detail show separately labeled counts
      for full persisted plans, live script cards by review state, source Markdown,
      and finished films, from backend readback rather than repository constants.
- [ ] `episodes_done / planned_episodes` and the story detail `done` count
      continue to mean finished films; preproduction counts never advance them.
- [ ] The labels distinguish imported source, script review and completed film,
      including missing or partial intake, without implying upload or publication.

## Steps

- [ ] Read the full stored story plans and only count episodes with valid plan
      identity, chapters and sources. Match each live script-review card to its
      exact series, episode number and project slug; exclude dropped, rejected,
      superseded or mismatched cards. Count original source Markdown separately:
      C03 has an approved legacy card without `source_md`.
- [ ] Render these read-only counters on the `kind=story` list/detail with
      localized labels. Existing series and project detail GETs may be used if
      they meet the predicate; otherwise coordinate the API scope before editing.
- [ ] Test full, partial and absent intake and retain the finished-video progress
      assertion. Coordinate existing claims before editing any scoped file.

## How to verify

Run focused story UI/API tests, `admin-video-stories.test.tsx`, i18n checks,
and read back the C-series card in admin. For current persisted state it should
show 20 full plans, ten live script cards (nine source Markdown plus one C03
legacy card), and zero finished films. A failed backend read must be shown as
unavailable rather than silently counted as zero.

## Notes

Filed 2026-10-23 during C-series closeout; corrected after readback of the
`kind=story` route. The story list is in `admin-video-stories.tsx`, and its
detail computes `done` from episode status. The generic series progress label
does not render this story card. This ticket does not authorize changing the
finished-video metric, uploading, publishing or paid generation.
