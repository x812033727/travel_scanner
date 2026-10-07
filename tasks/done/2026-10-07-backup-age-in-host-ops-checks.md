---
id: 2026-10-07-backup-age-in-host-ops-checks
title: Show the age of the last backup in host checks and warn when it is stale
status: done
priority: P2
area: docs
owner: claude-fable-5-1-backup
claimed_at: 2026-10-07T02:05:40Z
created_at: 2026-10-07T00:00:00Z
completed_at: 2026-10-07T02:07:41Z
branch: claude/auto-deploy-cloud-backup-hylcsz
depends_on:
  - 2026-10-07-backup-nightly-verified-dumps
scope:
  - ops/backup/status.sh
  - ops/backup/backup.py
  - ops/backup/test_backup.py
  - ops/backup/install.sh
  - ops/backup/README.md
  - .agents/skills/prod-host-ops
  - .claude/skills/prod-host-ops
  - .agents/skills/deploy/scripts/host-preflight.sh
---

# Show the age of the last backup in host checks and warn when it is stale

## Why

A nightly timer that silently stopped is worse than none, because everyone believes it is
running. The deploy preflight and the host-ops skill are the two places an agent or the
owner already looks at the host; the last backup's age belongs there, with a clear line
when it is older than 36 hours or the last run failed.

## Definition of done

- [x] `ops/backup/status.sh`: prints `last success <ISO> (<n>h ago) size <..> offsite
      <ISO|never>` from `/var/lib/travel-scanner-backup/last.json`, `BACKUP STALE: ...`
      when older than 36 hours, `BACKUP FAILED: <reason>` when the last run failed, and
      the timer's `systemctl is-enabled`/`is-active` state. Exit 1 on stale or failed so a
      cron or a check can use it.
- [x] Skill `prod-host-ops` has a "備份" section: the timer, `status.sh`, where the runs
      and `last.json` are, what to do on `BACKUP STALE` (journal of the service, disk, the
      deploy lock, rclone token expiry), and that a restore follows
      `docs/ops/backup-restore-runbook.md`. Byte-identical under `.claude/skills`.
- [x] `host-preflight.sh` prints the `status.sh` line in a `-- backups --` section. That
      script is in `2026-10-07-autodeploy-rollout-and-skill-docs`'s scope; add the two
      lines there if it is still open, otherwise claim them here by widening this scope.

## Steps

- [x] Wait for the nightly task's `last.json` format.
- [x] `status.sh`, skill section, `npm run test:tools`.
- [ ] Optional, decide with the owner: the same line as a notification once a day through
      the channel chosen for auto deploy (plan, section 三, item 4).

## How to verify

```bash
npm run test:tools
bash -n ops/backup/status.sh
```

On the host: `bash /opt/travel-scanner-backup/status.sh` after a good night prints the
success line and exits 0; stop the timer for two days in a test window and it prints
`BACKUP STALE` and exits 1.

## Notes

- 36 hours covers one missed night plus a late run; a second missed night is always stale.
- 2026-10-07 (claude-fable-5-1-backup): `ops/backup/status.sh` prints the timer's state and
  next run, then delegates to `backup.py status --state-dir` (the flag is the one change to
  `backup.py`, with a test), so the 36-hour rule lives in one place; exit 1 on stale, failed,
  never run or not installed. Exercised against a fresh, a stale-and-failed and a missing
  state. The installer copies it to `/opt/travel-scanner-backup/status.sh`. Skill
  `prod-host-ops` gained row 9, a command line and a "備份" section with the table of what
  each verdict means and what to do; only `SKILL.md` is mirrored. `host-preflight.sh` prints a
  `-- backups --` section that runs the script when installed: the scope was widened to that
  file as the task allowed, since `2026-10-07-autodeploy-rollout-and-skill-docs` (same owner)
  only has host steps left. The optional daily notification waits for the channel decision in
  the plan.
