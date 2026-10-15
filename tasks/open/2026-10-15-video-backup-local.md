---
id: 2026-10-15-video-backup-local
title: Back up locally produced videos to the Drive folder
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-15T02:14:12Z
completed_at:
branch:
depends_on:
  - 2026-10-15-video-backup-host-setup
scope:
  - tools/video/backup-local.mjs
  - tools/video/backup-local.test.mjs
---

# Back up locally produced videos to the Drive folder

## Why

Some productions (for example the Hailuo drama work) live on the owner's PC under
`~/mokaair-work`, not on the host. They should land in the same `AI/備份/<series>/<ep>/`
layout through Google Drive for desktop. Design: `docs/videos/BACKUP.md` (本機製作的影片).

## Definition of done

- [ ] `node tools/video/backup-local.mjs <slug>` copies the tier's files into
      `$VIDEO_BACKUP_LOCAL_ROOT` (default `G:\我的雲端硬碟`) + the configured path +
      the resolved folder, writes the same `backup.json`, and reports to the API.
- [ ] It refuses to say "done" until DriveFS shows no pending uploads for those files and
      sizes match; it never deletes the local source.
- [ ] Dry-run flag prints the plan.

## How to verify

```bash
node --test tools/video/backup-local.test.mjs
```

## Notes

- Reuse the file-list and folder logic from `tools/video/automation/backup.mjs` rather than
  copying it.
