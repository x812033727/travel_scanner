---
id: 2026-10-15-video-backup-web
title: Backup location card and backup status in the video admin
status: done
priority: P1
area: web
owner: claude-festive-archimedes
claimed_at: 2026-10-19T17:11:48Z
created_at: 2026-10-15T02:14:02Z
completed_at: 2026-10-19T17:29:22Z
branch: claude/festive-archimedes-9ntb36
depends_on:
  - 2026-10-15-video-backup-api
scope:
  - apps/web/components/admin-video-backup.tsx
  - apps/web/components/admin-video-backup.test.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/lib/video-backup-copy.ts
  - apps/web/lib/video-backup-messages
---

# Backup location card and backup status in the video admin

## Why

The owner sets where uploaded videos are backed up (`G:\我的雲端硬碟\AI\備份\` on their PC,
`AI/備份` in Drive) and needs to see whether each video is safely in Drive before the host
deletes it. Design: `docs/videos/BACKUP.md`.

## Definition of done

- [x] A "備份位置" card in `/admin/videos?tab=settings#video-backup-settings`, built like
      the VPS uploader card: enable toggle, path field (accepts the local `G:` path or the
      Drive path and shows the normalised result), default tier explanation, per-series tier
      overrides and folder names, a "測試" button that shows the worker's result and free
      space when it arrives. Read-only for reviewers without `settings.manage`.
- [x] ~~The ready card and project detail show the backup state~~ The backup card lists every
      video that is not completely in Drive (all of them with "show every video"), with its
      state: done (time, size, folder), pending, overdue, failed (reason), blocked by quota,
      partial (missing files), not queued, series off. The chip on each video's own card is
      `2026-10-19-show-each-video-s-drive-backup` (its files are held; see Notes).
- [x] All strings in every locale, in a feature catalog (`lib/video-backup-messages`), not
      `apps/web/messages` (held; see Notes).

## Steps

- [x] Card component and wiring into `admin-video-settings.tsx`.
- [x] ~~Status chip in `admin-video-reviews.tsx`~~ moved to the follow-up task.
- [x] Messages for all locales.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- A path outside the host's lock is rejected by the API; show its message as is.

- Done 2026-10-19 (claude-festive-archimedes). `components/admin-video-backup.tsx` exports
  `VideoBackupCard`, mounted at the end of `AdminVideoSettings` so it shows under both
  sections, with anchor `#video-backup-settings`. It reads `GET /admin/video-backup/settings`
  and `/status` (`?all=true` on "show every video"), saves only changed fields with
  `expected_updated_at`, and requests a test with `POST /admin/video-backup/test`.
- The card's first block answers the owner's question in one sentence ("all N uploaded videos
  are completely backed up in AI/備份", or "X of N are not yet; the host keeps their files").
- The path preview runs the API's normaliser rule in the browser (`drivePath`); the API stays
  the authority and its refusal (outside the lock, `..`) is shown as it comes.
- `apps/web/messages/*/admin.json` and `admin-video-reviews.tsx` were held by
  `2026-10-12-let-managers-link-a-private-studio` and `2026-10-19-imported-video-languages-eight`,
  so the copy lives in `lib/video-backup-messages/` like `lib/video-vps-messages/`. check:i18n
  does not read these catalogs; the card's test asserts key and `{name}` parity across the five.
- `admin-video-settings.test.tsx`'s fake site now answers the backup routes, and its
  "已儲存" assertions name the saved status, since the card adds statuses of its own.
- Drive's root folder name in `drivePath` is written as `\u` escapes: check:i18n reads the raw
  source for Han characters.
