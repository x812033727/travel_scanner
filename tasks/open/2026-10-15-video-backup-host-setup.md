---
id: 2026-10-15-video-backup-host-setup
title: Connect the video backup rclone remote on the host and run the first backup
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-15T02:14:07Z
completed_at:
branch:
depends_on:
  - 2026-10-15-video-backup-worker
  - 2026-10-15-video-backup-web
scope:
  - ops/video/rclone-videos.conf.example
  - ops/backup/manifest-paths.txt
  - docs/videos/BACKUP.md
---

# Connect the video backup rclone remote on the host and run the first backup

## Why

The code from the worker and web tasks does nothing until the host has a Drive remote
locked to the owner's `AI/備份` folder. Design: `docs/videos/BACKUP.md`.

## Definition of done

- [ ] Owner: Drive API enabled in their Google Cloud project, a desktop OAuth client,
      `rclone authorize "drive"` with scope `drive` run on their PC, token pasted once.
      The `AI/備份` folder ID read from its Drive URL.
- [ ] `/etc/travel-scanner/rclone-videos.conf` (root, 0600): remote `videobackup`,
      `type = drive`, `scope = drive`, the owner's `client_id`/`client_secret`,
      `root_folder_id = <AI/備份 id>`. `ops/video/rclone-videos.conf.example` shows the
      shape without secrets; `ops/backup/manifest-paths.txt` lists the file.
- [ ] `rclone lsd videobackup:` lists only the contents of `AI/備份`.
- [ ] Backup enabled in the admin card, test passes, the first video backed up and visible
      in `G:\我的雲端硬碟\AI\備份\<series>\` on the owner's PC; `rclone check` clean.
- [ ] Measured sizes (basic and full, one each) written into BACKUP.md's 空間 section;
      the owner told the projected monthly use so they can choose a Drive plan.

## Steps

- [ ] Owner steps above (they run `rclone authorize`; the token is theirs to paste).
- [ ] Config, deploy with the `deploy` skill, enable, test, watch one round.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec video-worker rclone lsd videobackup:
docker compose -f docker-compose.prod.yml exec video-worker rclone about videobackup:
```

## Notes

- Plan A (owner 2026-10-15): full `drive` scope is safe enough only because
  `root_folder_id` confines rclone; never remove that line.
- Separate from `2026-10-07-backup-google-drive-offsite` (encrypted disaster backups); the
  two remotes and config files stay apart.
