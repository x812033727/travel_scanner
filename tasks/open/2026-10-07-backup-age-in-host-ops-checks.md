---
id: 2026-10-07-backup-age-in-host-ops-checks
title: Show the age of the last backup in host checks and warn when it is stale
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-07T00:00:00Z
completed_at:
branch:
depends_on:
  - 2026-10-07-backup-nightly-verified-dumps
scope:
  - ops/backup/status.sh
  - .agents/skills/prod-host-ops
  - .claude/skills/prod-host-ops
---

# Show the age of the last backup in host checks and warn when it is stale

## Why

A nightly timer that silently stopped is worse than none, because everyone believes it is
running. The deploy preflight and the host-ops skill are the two places an agent or the
owner already looks at the host; the last backup's age belongs there, with a clear line
when it is older than 36 hours or the last run failed.

## Definition of done

- [ ] `ops/backup/status.sh`: prints `last success <ISO> (<n>h ago) size <..> offsite
      <ISO|never>` from `/var/lib/travel-scanner-backup/last.json`, `BACKUP STALE: ...`
      when older than 36 hours, `BACKUP FAILED: <reason>` when the last run failed, and
      the timer's `systemctl is-enabled`/`is-active` state. Exit 1 on stale or failed so a
      cron or a check can use it.
- [ ] Skill `prod-host-ops` has a "備份" section: the timer, `status.sh`, where the runs
      and `last.json` are, what to do on `BACKUP STALE` (journal of the service, disk, the
      deploy lock, rclone token expiry), and that a restore follows
      `docs/ops/backup-restore-runbook.md`. Byte-identical under `.claude/skills`.
- [ ] `host-preflight.sh` prints the `status.sh` line in a `-- backups --` section. That
      script is in `2026-10-07-autodeploy-rollout-and-skill-docs`'s scope; add the two
      lines there if it is still open, otherwise claim them here by widening this scope.

## Steps

- [ ] Wait for the nightly task's `last.json` format.
- [ ] `status.sh`, skill section, `npm run test:tools`.
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
