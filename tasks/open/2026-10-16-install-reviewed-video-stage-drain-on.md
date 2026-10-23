---
id: 2026-10-16-install-reviewed-video-stage-drain-on
title: Install reviewed video stage drain on production and verify
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-16T07:43:50Z
completed_at:
branch:
depends_on: []
scope:
  - ops/release
---

# Install reviewed video stage drain on production and verify

## Why

The 2026-10-16 incident showed that a paid video stage can start after an early
deployment preflight and be abandoned when the host-only deploy script recreates
`video-ai-worker`. The independently reviewed repository candidate in
`ops/release/` adds a final warm-drain guard before the normal and rollback
`compose up`, but no helper or host-script patch has been installed on production.
The live deployment race therefore remains until a separately approved install
and post-deploy readback complete. See the incident ticket
`2026-10-16-deploy-can-interrupt-a-video-stage` and its draft PR.

## Definition of done

- [ ] The exact reviewed helper and host-only script patch are installed after
      owner approval, current CI, and a fresh host preflight; file hashes,
      original backup, mode, lock and hook positions read back as intended.
- [ ] A separately approved deployment demonstrates warm drain at the last
      recreation boundary, with no in-flight paid stage interrupted or resent;
      compare worker/RQ/DB rows and operation receipts before and after.
- [ ] Normal failure and rollback paths are reconciled from exact evidence;
      any unresolved marker or uncertain result remains held for owner action.

## Steps

- [ ] Confirm the guard PR is merged and deployed only under its own approval;
      recheck the live host-only script SHA/mode and both compose anchors. If the
      2026-10-16 SHA has drifted, stop and independently review a new patch.
- [ ] Check deploy hold, staged releases, flock, disk, one expected worker
      process, RQ jobs, DB `video_stage_jobs` statuses and no active paid stage
      at the intended install/deploy boundary. Confirm the current auto timer
      installation state rather than assuming the repository design is live.
- [ ] With explicit host-write approval, use the reviewed pinned-SHA installer
      under the deployment lock; read back helper, patched host script and mode.
- [ ] On a later separately authorized deployment, read back health, exact
      worker container and exit/restart state, RQ registry, DB stage rows and
      unchanged paid-operation receipts. Keep failed/unknown work unretried.

## How to verify

Use the installation and rollback plan in `ops/release/README.md`. Compare
`sha256sum` of `/root/deploy-travel-scanner.sh` against the fresh baseline
before installation and the reviewed render after, plus `stat` mode/owner and
`bash -n` for helper and host script. Read the deploy log for both guard sites,
check `docker compose ... ps video-ai-worker`, its PID1 command, RQ registry and
the exact SQL status cohort before/after. Require post-deploy health/migration
checks and a persisted no-resend audit; a green CI or successful installer alone
does not close this task.

## Notes

The read-only host baseline on 2026-10-16 had
`/root/deploy-travel-scanner.sh` SHA-256
`c6e69658cd22351008a179389e807304cb284052136b3aaf1522ffb281a39370`,
mode 0700, root:root; the independently reviewed offline patched render was
`c8bb3559f6b7e25e11c3bdf207c2f8dabd28835119c78494b3c9ad8bb75bd64f`.
These are pinning evidence, not permission to install after drift. The auto
timer was not installed on this production host at that check; the repo's
90-minute timeout and paused receipt tests do not establish a live timer.
No host write, paid retry, worker restart or deployment was part of the guard
code PR.
