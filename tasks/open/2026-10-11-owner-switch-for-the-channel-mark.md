---
id: 2026-10-11-owner-switch-for-the-channel-mark
title: Owner switch for the channel mark on the admin videos page
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-11T16:48:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/web/components/admin-video-settings.tsx
  - tools/video/core/watermark.mjs
  - tools/video/automation/flow.mjs
---

# Owner switch for the channel mark on the admin videos page

## Why

Every video drawn for the first time now carries the channel mark (docs/videos/WATERMARK.md).
Which mark is a constant in tools/video/core/watermark.mjs (`CURRENT_WATERMARK`), and there is
no way for the owner to turn it off, for the channel or for one video, short of a code change.

It was left out of the first change on purpose: a setting on /admin/videos goes through
files the duration receipt binds (the video_automation models and schemas, the five
admin.json files, tools/video/core/schema.mjs for a video.json key, automation/flow.mjs for
`settle()`), and the owner had asked for the mark, not for a switch.

## Definition of done

- [ ] The owner has said whether a switch is wanted, and at which level (channel, format, video).
- [ ] If wanted: the setting reaches `selectWatermarkForRender`, a video that turns it off is
      drawn with the old brand word, and a video already pinned keeps its mark.

## Steps

- [ ] Ask the owner.
- [ ] Follow the `slides_music_track` precedent: migration, model, schema, admin field in five
      locales, `settle()` writing a video.json key, schema.mjs accepting it.
- [ ] Have the duration receipt re-issued by an independent reviewer.

## How to verify

Render a stand-in video with the setting off and on; read `frames/manifest.json`.

## Notes

- A per-video opt-out needs no setting if a disabled pin is enough: `watermark.json` could say
  `{ "schema_version": 1, "enabled": false }`, as branding.json does.
