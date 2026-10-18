---
id: 2026-10-15-video-backup-web
title: Backup location card and backup status in the video admin
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-10-15T02:14:02Z
completed_at:
branch:
depends_on:
  - 2026-10-15-video-backup-api
scope:
  - apps/web/components/admin-video-backup.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/messages
---

# Backup location card and backup status in the video admin

## Why

The owner sets where uploaded videos are backed up (`G:\我的雲端硬碟\AI\備份\` on their PC,
`AI/備份` in Drive) and needs to see whether each video is safely in Drive before the host
deletes it. Design: `docs/videos/BACKUP.md`.

## Definition of done

- [ ] A "備份位置" card in `/admin/videos?tab=settings#video-backup-settings`, built like
      the VPS uploader card: enable toggle, path field (accepts the local `G:` path or the
      Drive path and shows the normalised result), default tier explanation, per-series tier
      overrides and folder names, a "測試" button that shows the worker's result and free
      space when it arrives. Read-only for reviewers without `settings.manage`.
- [ ] The ready card and project detail show the backup state: done (time, size, folder),
      pending, failed (reason), blocked by quota, partial (missing files).
- [ ] All strings in every locale's messages.

## Steps

- [ ] Card component and wiring into `admin-video-settings.tsx`.
- [ ] Status chip in `admin-video-reviews.tsx`.
- [ ] Messages for all locales.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- A path outside the host's lock is rejected by the API; show its message as is.
