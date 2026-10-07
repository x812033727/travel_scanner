# Nightly verified backups

Until this directory existed, the production database was dumped only by the deploy script
and only when a migration was about to run, onto the same disk, and nothing backed up the
host files that are not in git. `backup.py run`, started by `travel-scanner-backup.timer`
once a night, writes one directory per run under `/var/backups/travel-scanner/nightly/`,
verifies everything it wrote, and records the result in `/var/lib/travel-scanner-backup/last.json`.
The copy to Google Drive is the next task (`offsite.py`, the plan in
`docs/ops/auto-deploy-and-cloud-backup-plan.md`); it reads complete run directories only.

## One run

| Step | What | Fails the run when |
| --- | --- | --- |
| lock | `flock -n /var/lock/travel-scanner-deploy.lock`: a deploy may be restarting postgres | held: the run is **skipped** (exit 3, `last_skipped`), the next night tries again |
| manifest facts | live git SHA, `alembic_version`, `SELECT version()` | any cannot be read |
| dump | `pg_dump -Fc` through `docker compose exec -T postgres` into `travel-scanner-<ts>-<sha12>.dump`, then `pg_restore --list` on the file, then SHA-256 | empty, or `pg_restore --list` rejects it |
| predeploy sweep | every `/root/travel_scanner_predeploy_*.dump` newer than the last successful run (the deploy script's pre-migration dumps), copied in, listed and hashed; the originals stay | one does not list |
| config bundle | the paths in `manifest-paths.txt` that exist, as a tar in a private `mkdtemp` (0700), encrypted with `age -r BACKUP_AGE_RECIPIENT` to `config.tar.age`; the plain tar is removed in `finally` and never written under `/var/backups`. Without a recipient the bundle is **not kept** | `age` fails |
| redis | `redis-cli SAVE` and a copy of `dump.rdb`, only with `BACKUP_INCLUDE_REDIS=true` | the copy is empty |
| manifest | `manifest.json`: host, times, git SHA, alembic revision, PostgreSQL version, every file's name, kind, size and SHA-256, the config paths included and missing | |
| commit | the directory is `<ts>.partial` until here and is renamed to `<ts>` | |
| retention | the newest `BACKUP_LOCAL_RETENTION` complete runs stay, older ones go; `.partial` directories older than a day go too. Only after a success | |

A failed run removes its partial directory, records `last_failure` (stage and reason) and
exits 1; the previous complete runs are untouched.

## Files on the host

| Path | What |
| --- | --- |
| `/opt/travel-scanner-backup/backup.py`, `status.sh`, `manifest-paths.txt`, `README.md` | Copied by `install.sh`; upgrading is `sudo bash ops/backup/install.sh` from a reviewed checkout |
| `/etc/travel-scanner/backup.env` (root, 0600) | `BACKUP_LOCAL_RETENTION`, `BACKUP_AGE_RECIPIENT`, `BACKUP_INCLUDE_REDIS`; read on every run |
| `/var/backups/travel-scanner/nightly/<ts>/` (0700) | One complete run: the dump(s), `config.tar.age`, optional `redis.rdb`, `manifest.json` |
| `/var/lib/travel-scanner-backup/last.json` | `last_success` (time, path, seconds, bytes, file names, git SHA, alembic revision), `last_failure` (time, stage, reason), `last_skipped`. Never a secret |
| `/etc/systemd/system/travel-scanner-backup.{service,timer}` | `Type=oneshot`, daily at 20:17 UTC (04:17 Asia/Taipei), `Persistent=true`, idle I/O priority |

`manifest-paths.txt` is the list of what a rebuilt host needs and git does not have: the
runtime `.env`, `/etc/travel-scanner`, the uploader secrets, the nginx site and project
files, Let's Encrypt, the deploy script itself (it is not in git), the installed systemd
units and the rclone config of the offsite task. A missing path is listed under
`config.missing` in the manifest, not an error, so the list can name files that are not on
every host yet.

## Install and first run

```bash
sudo apt install age                               # once; the installer says so when it is missing
sudo bash ops/backup/install.sh                    # copies files, installs units, does not enable
sudo vi /etc/travel-scanner/backup.env             # BACKUP_AGE_RECIPIENT=age1...
sudo python3 /opt/travel-scanner-backup/backup.py run --dry-run
sudo python3 /opt/travel-scanner-backup/backup.py run
sudo python3 /opt/travel-scanner-backup/backup.py status
sudo systemctl enable --now travel-scanner-backup.timer
```

The age key pair: `age-keygen -o mokaair-backup.key` on the owner's machine, the `age1...`
public key into `backup.env`, the identity file into the password manager. The host never
holds the identity, so a copy of the host cannot decrypt its own config bundle; losing the
identity loses every config bundle, which is why the password manager copy is a
definition-of-done item in the task, not advice.

Before the first run, measure what the retention and the Drive quota have to hold:

```bash
docker compose -f /root/travel_scanner/docker-compose.prod.yml exec -T postgres \
  psql -U travel -d travel_scanner -Atc "select pg_size_pretty(pg_database_size('travel_scanner'))"
df -h /var/backups
```

## Reading it

```bash
bash /opt/travel-scanner-backup/status.sh                   # timer state + the lines below; exit 1 when failed, never run, or > 36 h old
sudo python3 /opt/travel-scanner-backup/backup.py status   # the same without the timer lines
journalctl -u travel-scanner-backup --since -2d
ls -la /var/backups/travel-scanner/nightly/
```

Each run prints one line per step and ends with `done: <dir> (<n> files, <bytes>, <s>)` or
`failed: <stage>: <reason>`. Exit codes: 0 success, 1 failure, 2 configuration error, 3 skipped
because the deploy lock was held.

## Restoring one dump

Never over production. Into a throwaway container on a private port:

```bash
run=/var/backups/travel-scanner/nightly/<ts>
sha256sum -c <(python3 -c "import json,sys; [print(f['sha256'], ' $run/' + f['name']) for f in json.load(open('$run/manifest.json'))['files']]")
docker run -d --name restore-drill -e POSTGRES_PASSWORD=<disposable-password> -p 127.0.0.1:55432:5432 postgres:17-alpine
docker exec -i restore-drill pg_restore -U postgres -d postgres --create --no-owner < "$run"/travel-scanner-*.dump
docker exec restore-drill psql -U postgres -d travel_scanner -Atc "select count(*) from guides"
docker rm -f restore-drill
```

The full drill from a blank machine, with the offsite copy and the config bundle
(`age -d -i mokaair-backup.key config.tar.age | tar -t`), is `docs/ops/backup-restore-runbook.md`,
written by the offsite task.

## Tests

```bash
python -m unittest discover -s ops/backup -v
```

A temporary directory stands in for the host and a fake runner for every command (pg_dump
writes bytes to the output path, `age` writes the encrypted file); nothing needs root, Docker
or `age`, and the tests run on Windows. Standard library only, no `fcntl`, Python 3.11 or newer.
