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
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
---

# Show brand story planning and script intake beside finished-video progress

## Why

The C01–C20 planning intake and ten eligible script sources have been saved to the
video backend, but the admin series card still shows `0/20`. That number is
`episodes_done / planned_episodes` in `admin-video-series.tsx`; it counts finished
videos and remains correct. The card has no separate preproduction signal, so
an owner reading it cannot see the persisted plan and script-source intake.

## Definition of done

- [ ] The C-series admin card shows separately labeled counts for persisted plans
      and eligible script sources or review state, from backend readback rather than
      hard-coded repository numbers.
- [ ] `episodes_done / planned_episodes` continues to mean finished videos. The
      existing `0/20` stays visible until actual videos finish; preproduction counts
      never advance that metric.
- [ ] The labels distinguish imported source, script review and completed film,
      including missing or partial intake, without implying upload or publication.

## Steps

- [ ] Confirm the authoritative backend rows for the 20 plans and ten script sources
      against `docs/videos/brand-stories-everyday-reversals-20261020/stories.json`
      and `approved-scripts.json`; do not infer state from the files alone.
- [ ] Add a read-only series summary for preproduction intake and render it in the
      admin series list/detail card with localized labels.
- [ ] Test full, partial and absent intake and retain the finished-video progress
      assertion. Coordinate existing claims before editing any scoped file.

## How to verify

Run the focused API series tests, `admin-video-series.test.tsx`, i18n checks,
and read back the C-series card in admin. It should show the separately labeled
20/20 plan and ten script-source intake while finished videos still read 0/20.

## Notes

Filed 2026-10-23 during C-series closeout. The current UI uses
`t("progress", { done: each.episodes_done, total: each.planned_episodes })` near
`apps/web/components/admin-video-series.tsx:584` and similarly near line 829.
This ticket is a later UI/API improvement; it does not authorize changing the
backend's finished-video metric, uploading, publishing or paid generation.
