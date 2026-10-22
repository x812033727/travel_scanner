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
branch: claude/video-cloud-backup-issue-48a886
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

- [x] Owner: Drive API enabled in their Google Cloud project, a desktop OAuth client,
      authorized on their PC with scope `drive` (`rclone config create`, 2026-10-22).
      The `AI/備份` folder ID read from its Drive URL.
- [x] `/etc/travel-scanner/rclone-videos/rclone.conf` (uid 1001, 0600, in a 0750 folder of
      the same owner): remote `videobackup`, `type = drive`, `scope = drive`, the owner's
      `client_id`/`client_secret`, `root_folder_id = <AI/備份 id>`.
  - [x] `ops/video/rclone-videos.conf.example` shows the shape without secrets (rclone
        v1.74.4 parses it as written).
  - [x] `ops/backup/manifest-paths.txt` already takes `/etc/travel-scanner` whole, so the new
        folder is in the nightly bundle without a line of its own.
- [x] `rclone lsd videobackup:` lists only the contents of `AI/備份`.
- [ ] Backup enabled in the admin card, test passes, the first video backed up and visible
      in `G:\我的雲端硬碟\AI\備份\<series>\` on the owner's PC; `rclone check` clean.
- [ ] Measured sizes (basic and full, one each) written into BACKUP.md's 空間 section.
      (The plan question is settled: the owner has 5 TiB.)

## Steps

- [x] Owner steps written out in `docs/videos/BACKUP.md` §主機設定, with the Google Cloud
      "Testing" trap (a refresh token there expires after 7 days) and a troubleshooting table.
- [x] Owner steps (2026-10-22; the token never went into a chat).
- [x] Deploy (#1595 is live), put the file on the host. Backups were already enabled in the
      admin card (2026-10-20 00:45Z, every series on the full tier).
- [x] The test answered and one round watched (2026-10-22 01:25Z; since #1660 every round
      backs up, `2026-10-22-back-up-videos-even-when-an`).
- [ ] The first complete backup (with `final.mp4`), checked with `rclone check`, and its size.

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
  the worker's uid 1001 (the `install -o 1001` written here first does not work on the host;
  see 2026-10-22 below and BACKUP.md §主機設定 step 4). The
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
- 2026-10-22 (claude-opus-5-5-video-cloud-backup), with the owner:
  - Google Cloud: reused the YouTube project `mokaair-studio-sync` (already 實際運作中, Drive
    API already enabled) and added a desktop client. Its first secret was pasted into a chat
    by mistake, so the owner added a new one and disabled the old one before authorizing.
  - `rclone config create … --config %USERPROFILE%\rclone-videos.conf` on the owner's PC does
    the authorization and writes the whole file at once, so the token is never copied by hand.
    winget's rclone 1.75.1 (ARM64); the host's 1.74.4 reads the file.
  - `install -o 1001` fails on the host (`invalid user: '1001'`, uutils `install` wants a
    name); `mkdir`/`chown 1001:1001`/`chmod` works. BACKUP.md now says so.
  - Verified from inside video-worker (uid 1001): `lsd` lists only `偶的江湖`,
    `公開影片-20261018-部分備份` and `奇聞檔案局`; `about` says 5 TiB, 4.769 TiB free.
  - After 7 minutes nothing had moved: every round since 2026-10-21 16:43Z ends in the
    site's "instructions：內容太長" before the backup, which ran only after a whole round. The
    last lock report is 2026-10-21 01:00, the owner's test (2026-10-21 01:03) is unanswered,
    and 62 videos on YouTube have no backup record.
  - Left: after #1657 and this branch deploy, check that the lock is reported, the test is
    answered, and the first two videos reach `done`; then measure sizes and close.
- 2026-10-22 results: a round that finished at 01:25Z answered the owner's test ("已在 AI/備份
  寫入並刪除測試檔", success) and backed up the two oldest; #1660 (02:02Z) backs up two a round
  even at the draft cap. By 02:13Z six videos were `partial`, four `pending`, 53 not queued yet.
  All six are old videos the tidy had already cleared: each lacks `final.mp4` (two also a dub),
  13–14 files and about 140 KB each. 28 work folders on the host still hold `upload/final.mp4`,
  so the first complete backup, and the sizes for 空間, come when the queue reaches them.
