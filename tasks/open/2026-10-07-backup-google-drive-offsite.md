---
id: 2026-10-07-backup-google-drive-offsite
title: Copy the nightly backups to Google Drive through an rclone crypt remote
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-07T00:00:00Z
completed_at:
branch:
depends_on:
  - 2026-10-07-backup-nightly-verified-dumps
scope:
  - ops/backup/offsite.py
  - ops/backup/test_offsite.py
  - ops/backup/rclone.conf.example
  - ops/backup/README.md
  - docs/ops/backup-restore-runbook.md
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

- [ ] `rclone` installed on the host from its own apt repository or the pinned release
      binary (version written in README). `rclone.conf` at `/etc/travel-scanner/rclone.conf`
      (root, 0600): a `drive` remote using the owner's own OAuth client ID, scope
      `drive.file`, token obtained with `rclone authorize "drive"` on the owner's machine
      and pasted once; a `crypt` remote wrapping it (`filename_encryption = standard`,
      `directory_name_encryption = true`) with its two passwords also stored in the owner's
      password manager. `ops/backup/rclone.conf.example` shows the shape without secrets.
- [ ] `ops/backup/offsite.py`, called by `backup.py` after a successful local run (or
      standalone with a run directory): `rclone copy` of the run directory to
      `crypt:mokaair/<host>/nightly/<ts>/` with `--drive-chunk-size 64M`, retries and
      `--checksum`; the config bundle is streamed through `rclone rcat` from the temporary
      directory so it never touches `/var/backups`; `manifest.json` is uploaded last and a
      remote `latest.json` is rewritten only after the whole run is verified with
      `rclone check`.
- [ ] Media: `video_media` and `video_work/*/upload/final.mp4` (or whatever the
      measurement in the nightly task supports within the Drive quota) go to
      `crypt:mokaair/<host>/media/` with `rclone sync --backup-dir` so a deleted file is
      kept 30 days rather than dropped. `BACKUP_MEDIA_PATHS` in `backup.env` lists them;
      empty disables.
- [ ] Remote retention: `nightly/` keeps 30 daily runs and the first run of each month for
      12 months (`rclone delete --min-age` plus a kept list in `latest.json`), applied only
      after the new run is verified.
- [ ] `docs/ops/backup-restore-runbook.md`: from a blank machine, install rclone, restore
      `rclone.conf` from the password manager, `rclone ls crypt:`, pull one run, verify
      hashes against `manifest.json`, `pg_restore` into a throwaway `postgres:17` container
      on a private port, count rows in `guides`, `food_merchants` and `users`, then destroy
      the container. Also the config bundle restore and what in it must be rotated after a
      compromise.
- [ ] The first restore drill done and dated in this task's Notes, with the sizes and the
      time each step took.
- [ ] `last.json` gains `offsite`: last successful upload time, remote path, bytes.

## Steps

- [ ] Owner decisions first (plan, section 三, items 7–11): account and quota, which
      media, passphrase custody, AI account tokens, retention and drill cadence.
- [ ] Create the OAuth client in the owner's Google Cloud project (Drive API enabled,
      desktop client), run `rclone authorize` on the owner's machine, build the two remotes
      on the host, `rclone lsd crypt:` works.
- [ ] `offsite.py` with a fake runner in tests (no network); README section; call from
      `backup.py`.
- [ ] First upload by hand, `rclone check`, then the drill.

## How to verify

```bash
python -m unittest discover -s ops/backup -v
rclone --config /etc/travel-scanner/rclone.conf check /var/backups/travel-scanner/nightly/<ts> crypt:mokaair/<host>/nightly/<ts>
```

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
