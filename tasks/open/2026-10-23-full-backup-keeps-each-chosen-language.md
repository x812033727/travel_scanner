---
id: 2026-10-23-full-backup-keeps-each-chosen-language
title: Full backup keeps each chosen language's unpackaged dub track and thumbnail
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-23T07:22:06Z
created_at: 2026-10-23T07:21:52Z
completed_at:
branch: claude/manual-multilingual-audio-upload-2f97b6
depends_on: []
scope:
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - docs/videos/BACKUP.md
  - apps/api/app/video_backup/target.py
  - apps/api/app/video_backup/admin_settings.py
  - apps/api/app/video_backup/schemas.py
  - apps/api/tests/test_video_backup.py
  - apps/web/components/admin-video-backup.tsx
  - apps/web/components/admin-video-backup.test.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/lib/video-backup-messages
---

# Full backup keeps each chosen language's unpackaged dub track and thumbnail

## Why

The Drive backup copies the upload package only. A dub the worker gave up on never enters the
package, and the tidy later deletes the track from the work directory, so it is lost. On
2026-10-23 the owner wanted to upload the A4 episode's (`story-adapt-a4-paper-size`) other
languages by hand: all eight dubs had been given up (`dubs/<locale>/skipped.json`), en/pt/th/vi
tracks still sat in the work directory, and Drive had none. The owner asked that the full
backup hold every chosen language's voice track and thumbnail.

## Definition of done

- [x] The full tier copies, for each locale with `dub` ticked in `languages.json`, a work-dir
  track `dubs/<locale>.(m4a|mp3|wav)` the package lacks, to `dubs/未進上傳包/<file>`.
- [x] The full tier copies `thumbnails/<locale>.jpg` for each locale with any part ticked when
  the package has none. The basic tier is unchanged.
- [x] The site never counts an unpackaged track as a packaged dub (`contentsOf`).
- [x] Every backed-up video defaults to the full tier (owner, 2026-10-23: 如果有備份的都要完整備份);
  a series set to basic or off in the settings still wins. `FULL_CATEGORIES` and the settings
  view's `full_categories` are gone; the card's help text says so in five locales.
- [x] A work directory made by hand, with `upload/final.mp4` and no `auto.json`
  (`openai-devday-2026-recap`, `free-vs-paid-ai-plans-2026`), is backed up too; before, the
  round skipped any directory without `auto.json`, so these two were never queued.
- [ ] Deployed, and a full-tier video with an unpackaged track shows it in Drive.

## How to verify

`node --test tools/video/automation/backup.test.mjs` (the new planFiles test). Two tests in the
file fail on Windows before and after this change (staging folder); they pass on Linux CI.

## Notes

- A done backup whose plan grows is no longer `stillCovered`, so the tidy holds the work files
  and the round copies the new ones before the tracks are cleared.
- `story-adapt-a4-paper-size`'s backup was tier `basic`: `brand-stories-adapt` was not in the
  settings' tiers, and the old default gave non-drama categories basic. With the full default,
  every unset series (it and the other brand-story adaptations) is re-queued at full after deploy.
- API: `uv run pytest tests/test_video_backup.py` (44 pass). Web: vitest on the two card tests.
