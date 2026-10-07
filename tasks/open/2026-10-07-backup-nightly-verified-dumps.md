---
id: 2026-10-07-backup-nightly-verified-dumps
title: Nightly verified PostgreSQL dumps and a config bundle on the production host
status: in-progress
priority: P1
area: ops
owner: claude-fable-5-1-backup
claimed_at: 2026-10-07T01:26:45Z
created_at: 2026-10-07T00:00:00Z
completed_at:
branch: claude/auto-deploy-cloud-backup-hylcsz
depends_on: []
scope:
  - ops/backup
---

# Nightly verified PostgreSQL dumps and a config bundle on the production host

## Why

The production database holds every article, merchant, hotspot, community post, video job
and admin setting, and the only dumps of it are the ones `/root/deploy-travel-scanner.sh`
takes when an incoming commit touches `migrations/`, left in `/root` on the same disk. The
deployment agent's verified backups (`/var/backups/travel-scanner`, seven retained) only
exist when that agent is used, and it is off. Nothing backs up the files that are not in
git: `/root/travel_scanner/.env`, `/etc/travel-scanner/*.env`, `/etc/mokaair-uploader/`,
the nginx site file, `/etc/letsencrypt`, the installed systemd units, and the deploy script
itself. Inventory and decisions: `docs/ops/auto-deploy-and-cloud-backup-plan.md`.

This task is the local layer. The Google Drive copy is
`2026-10-07-backup-google-drive-offsite`, which needs these files to exist first.

## Definition of done

- [ ] `ops/backup/backup.py` (standard library, tests run on Windows through a fake
      runner) with `run`, `run --dry-run` and `status`. One run, under
      `/var/backups/travel-scanner/nightly/<UTC ts>/`:
      1. `pg_dump -Fc` through `docker compose -f docker-compose.prod.yml exec -T postgres`
         (user, database and the `--profile` flags as the host script uses them),
         verified with `pg_restore --list`, hashed with SHA-256; a dump that fails
         verification is deleted and the run fails.
      2. Any `/root/travel_scanner_predeploy_*.dump` newer than the previous run is copied
         in, verified and hashed the same way (they are the dumps taken right before a
         migration).
      3. A config bundle `config.tar` of the paths listed in `ops/backup/manifest-paths.txt`
         (the files above plus `/etc/systemd/system/travel-scanner-*` and
         `/etc/systemd/system/mokaair-*`), built in a private temporary directory, hashed,
         and **never left on disk unencrypted**: this task keeps it only for the duration
         of the run and hands it to the offsite step; until that task lands, the bundle is
         encrypted locally with `age` (recipient from the env file) or not kept.
      4. Optional `redis` `BGSAVE` and `dump.rdb` copy when `BACKUP_INCLUDE_REDIS=true`
         (default false; the queue is rebuilt, not restored).
      5. `manifest.json`: host, start and end time, live git SHA, `alembic current`,
         PostgreSQL version, and for every file its name, size and SHA-256.
- [ ] Local retention: the newest 7 nightly directories are kept, older ones removed after
      a successful run, never before.
- [ ] `/var/lib/travel-scanner-backup/last.json`: the last successful run's time, path,
      sizes and duration, and the last failure's time and reason. Nothing secret.
- [ ] Config from `/etc/travel-scanner/backup.env` (root, 0600): `BACKUP_INCLUDE_REDIS`,
      `BACKUP_LOCAL_RETENTION` (7), `BACKUP_AGE_RECIPIENT` (optional until the offsite task).
- [ ] `travel-scanner-backup.service` (`Type=oneshot`, root) and
      `travel-scanner-backup.timer` (daily, `Asia/Taipei` low-traffic hour, the exact minute
      chosen on the host), `install.sh` copying the module to
      `/opt/travel-scanner-backup/` and creating directories and the env file from
      `backup.env.example`, timer not enabled by the installer.
- [ ] A run must not take the deploy lock or stop a deploy: it reads the database through
      `pg_dump` only. It refuses to start while `/var/lock/travel-scanner-deploy.lock` is
      held (a deploy is restarting postgres) and retries at the next timer firing.
- [ ] Tests for the run order, the verification failure path, retention, `last.json`,
      the predeploy sweep and the dry run. `README.md` with install, what is backed up and
      what is not, how to read `last.json` and the logs, and how to restore one dump into a
      disposable container (the full drill is in the offsite task).

## Steps

- [ ] First, on the host, measure before writing retention rules:
      `select pg_database_size('travel_scanner')`, `du -sh` of each named volume
      (`docker volume inspect` for the mountpoints), and `df -h /`. Write the numbers in
      Notes; they decide the Drive quota question in the plan.
- [ ] Module, units, installer, env example, README, tests.
- [ ] Install on the host, run `run --dry-run`, then one real `run` by hand, then enable
      the timer with the owner present. Record the first run's duration and sizes here.

## How to verify

```bash
python -m unittest discover -s ops/backup -v
bash -n ops/backup/install.sh
```

On the host after the first run: the directory holds the dump, `manifest.json` and the
hashes match `sha256sum`; `pg_restore --list` on the dump exits 0 (the command is in
`ops/deployer/README.md`, "Verify a manual backup on the host").

## Notes

- The deploy script backing up before **every** deploy (not only migrations) would be a
  one-line call to this module from `/root/deploy-travel-scanner.sh`. That script is not in
  git and changing it needs the owner (skill `deploy`, rule 6), so it is a Notes item, not
  a checkbox.
- The paths in `manifest-paths.txt` contain secrets. The tar never lands in `/var/backups`
  unencrypted; the test asserts the bundle is built under a `mkdtemp` directory with mode
  0700 and removed in `finally`.
- `/var/backups/travel-scanner` is owned by `travel-deployer` (deployer installer). This
  timer runs as root and writes to `nightly/` under it; keep the directory mode 0750.
- Media volumes (`video_media`, `video_work`, `video_reviews`) are not in this task: they
  are large and partly regenerable; the offsite task decides which of them to copy after
  the measurement above.
