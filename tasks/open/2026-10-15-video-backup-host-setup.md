---
id: 2026-10-15-video-backup-host-setup
title: Connect the video backup rclone remote on the host and run the first backup
status: blocked
priority: P1
area: ops
owner: claude-festive-archimedes
claimed_at: 2026-10-19T18:02:34Z
created_at: 2026-10-15T02:14:07Z
completed_at:
branch: claude/festive-archimedes-9ntb36
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
- [ ] `/etc/travel-scanner/rclone-videos/rclone.conf` (uid 1001, 0600, in a 0750 folder of
      the same owner): remote `videobackup`, `type = drive`, `scope = drive`, the owner's
      `client_id`/`client_secret`, `root_folder_id = <AI/備份 id>`.
  - [x] `ops/video/rclone-videos.conf.example` shows the shape without secrets (rclone
        v1.74.4 parses it as written).
  - [x] `ops/backup/manifest-paths.txt` already takes `/etc/travel-scanner` whole, so the new
        folder is in the nightly bundle without a line of its own.
- [ ] `rclone lsd videobackup:` lists only the contents of `AI/備份`.
- [ ] Backup enabled in the admin card, test passes, the first video backed up and visible
      in `G:\我的雲端硬碟\AI\備份\<series>\` on the owner's PC; `rclone check` clean.
- [ ] Measured sizes (basic and full, one each) written into BACKUP.md's 空間 section;
      the owner told the projected monthly use so they can choose a Drive plan.

## Steps

- [x] Owner steps written out in `docs/videos/BACKUP.md` §主機設定, with the Google Cloud
      "Testing" trap (a refresh token there expires after 7 days) and a troubleshooting table.
- [ ] Owner steps (they run `rclone authorize`; the token never goes into a chat).
- [ ] Deploy (#1595 merged 2026-10-19 17:53 UTC; the auto-deploy timer should take it), put
      the file on the host, enable, test, watch one round.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T video-worker sh -c \
  'cp /etc/mokaair/rclone-videos/rclone.conf /tmp/rv.conf && export RCLONE_CONFIG=/tmp/rv.conf && rclone lsd videobackup: && rclone about videobackup:; rm -f /tmp/rv.conf'
```

## Notes

- Plan A (owner 2026-10-15): full `drive` scope is safe enough only because
  `root_folder_id` confines rclone; never remove that line.
- Separate from `2026-10-07-backup-google-drive-offsite` (encrypted disaster backups); the
  two remotes and config files stay apart.
- From the worker task (2026-10-19): the file goes in a folder, not at
  `/etc/travel-scanner/rclone-videos.conf`. Compose mounts `/etc/travel-scanner/rclone-videos/`
  read-only, so put the remote in `/etc/travel-scanner/rclone-videos/rclone.conf`, readable by
  the worker's uid 1001: `install -d -m 0750 -o 1001 -g 1001 /etc/travel-scanner/rclone-videos`,
  then `install -m 0600 -o 1001 -g 1001 rclone.conf /etc/travel-scanner/rclone-videos/`. The
  remote must be named `videobackup` (or set `VIDEO_BACKUP_REMOTE`). `VIDEO_BACKUP_LOCK_PATH` is
  `AI/備份` in compose; change it there if `root_folder_id` points elsewhere. Read the verify
  commands' paths as `/etc/mokaair/rclone-videos/rclone.conf` inside the container
  (`RCLONE_CONFIG=... rclone lsd videobackup:`).
- 2026-10-19 (claude-festive-archimedes): the repository side is done: the config example,
  and BACKUP.md rewritten to what #1595 shipped (state in backup-state.json, the site's own
  count of missing files, the tidy gate, Shorts' folders, the whole upload/ tree) with the
  step-by-step host setup. Blocked on the owner: the Google Cloud client, `rclone authorize`,
  and putting the file on the host (this cloud session has no SSH to the host). The verify
  commands copy the file to /tmp first because the mount is read-only and rclone may write
  a refreshed token back.
