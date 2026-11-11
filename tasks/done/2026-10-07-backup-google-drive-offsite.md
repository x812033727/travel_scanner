---
id: 2026-10-07-backup-google-drive-offsite
title: Copy the nightly backups to Google Drive through an rclone crypt remote
status: done
priority: P1
area: ops
owner: claude-opus-5-5
claimed_at: 2026-11-11T00:46:09Z
created_at: 2026-10-07T00:00:00Z
completed_at: 2026-11-11T00:54:38Z
branch:
depends_on:
  - 2026-10-07-backup-nightly-verified-dumps
scope:
  - ops/backup/offsite.py
  - ops/backup/test_offsite.py
  - ops/backup/rclone.conf.example
  - ops/backup/README.md
  - docs/ops/backup-restore-runbook.md
  - ops/backup/install.sh
  - ops/backup/test_backup.py
  - ops/backup/backup.env.example
  - ops/backup/travel-scanner-offsite.service
  - ops/backup/travel-scanner-offsite.timer
---

# Copy the nightly backups to Google Drive through an rclone crypt remote

## Why

A backup on the same disk as the database is not a backup against the disk. The owner
wants the things that need backing up in Google Drive. Everything that leaves the host
(database dumps, the config and secrets bundle, selected video media) is encrypted on the
host first, so Drive only ever stores ciphertext; the mechanism and the reasons for
rclone over a hand-written Drive client, OAuth over a service account, and a `crypt`
remote over per-file encryption are in `docs/ops/auto-deploy-and-cloud-backup-plan.md`.

## Definition of done

Rewritten 2026-11-11 after the owner's decision (Notes): no `crypt` remote, the video backup
remote instead. The original items are kept, struck out where the decision replaced them.

- [x] ~~rclone from apt and an own OAuth client with a `crypt` remote~~ → rclone v1.74.4 from
      `travel-scanner-video-worker:local`, remote `videobackup` (rooted at `AI/備份`, config
      `/etc/travel-scanner/rclone-videos`), target `videobackup:主機/資料庫/nightly`.
- [x] `ops/backup/offsite.py` with `ops/backup/test_offsite.py` (11 tests, fake runner): every
      complete local run Drive lacks, oldest first; `rclone copy` without `manifest.json`, then
      `manifest.json`; `rclone check --one-way`; a run counts as on Drive only with its manifest.
      Started by its own `travel-scanner-offsite.timer` (21:47 UTC, 90 min after the backup)
      instead of being called from `backup.py`, so a failed upload never fails the local backup.
- [x] Remote retention: newest `OFFSITE_RETENTION` (14) run folders, older ones `purge`d only
      after every upload of the run is verified (Drive trash keeps them 30 days).
      ~~30 daily + 12 monthly~~: 14 is what the owner was offered on 2026-11-10.
- [x] `last.json` gains `offsite` and `offsite_failure`.
- [x] Restore steps in `ops/backup/README.md` ("Offsite copy" and "Restoring one dump");
      ~~a separate `docs/ops/backup-restore-runbook.md`~~ not written.
- [x] First restore drill done (Notes).
- [ ] ~~Media to `crypt:.../media/`~~: out of this task. Video files go to `AI/備份/AI劇/` by the
      sessions since 2026-11-10 (`docs/videos/AI-DRAMA-DRIVE.md`); the host volumes are a
      separate plan.

## Notes


- Why not a service account: files it uploads into "My Drive" have no storage quota and
  fail; only a Workspace shared drive works with one. Why `drive.file`: rclone only needs
  to see what it created. Why the owner's own client ID: rclone's shared one is rate
  limited for everyone.
- Losing the `crypt` passwords loses every backup. The password manager copy is a
  definition-of-done item, not advice.
- Google Drive rate limits uploads of many small files; the run directory is a handful of
  files, media is where `--transfers` and `--tpslimit` matter.
- Do not sync `video_work` wholesale: it holds every lane's intermediate renders.

- 2026-11-11, owner (claude-opus-5-5 session): asked to 「先做每日資料庫異地備份」, and chose
  **不加密，直接傳** over the recommended rclone crypt, knowing the dumps hold member emails and
  password hashes and that the `videobackup` token has full Drive scope.
- 2026-11-11 on the host: `ops/backup` installed from `origin/main` (it had never been installed;
  no timer existed). First run `20261111T000844Z`: 637 MB dump + three predeploy dumps swept,
  2.4 GB, 141 s. `travel-scanner-backup.timer` enabled (20:17 UTC). `offsite.py` installed from
  this branch, first upload 2.4 GB in 38 s, `rclone check` 0 differences; a second run uploads
  nothing; `travel-scanner-offsite.timer` enabled (21:47 UTC). Reinstall from main after merge:
  `sudo bash ops/backup/install.sh`.
- Restore drill 2026-11-11: the dump pulled back from Drive in 11 s, SHA-256 matches the
  manifest, `pg_restore --create` into a throwaway `postgres:17-alpine` in 124 s;
  `food_merchants` 511 and `users` 2, the same as production at that moment. There is no
  `guides` table in production any more; count a table that exists when repeating the drill.
- The config bundle is still not kept: `BACKUP_AGE_RECIPIENT` is empty, so `.env`, nginx and
  Let's Encrypt are in no backup. Needs the owner's age public key (identity stays off the host).
- Found while testing: `test_backup.py::test_status_verdicts` built `Paths` with the host
  defaults, so on the host (once `backup.env` existed) it took a real backup. Fixed: every path
  in the temp dir. The stray run it made was deleted.
