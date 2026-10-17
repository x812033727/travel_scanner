# Independent A01 STOP recovery guard review — 2026-10-17

Scope: static/read-only production design review of `stop-recovery-guard/` in this candidate. No host write or paid call. The phase runner had not been frozen for review when this report was written. This is **not approval to install or run**.

## Decision

**Do not lift the A01 project STOP with the current package.** The hard-link/marker sequence is a reasonable crash-recovery foundation, but the package does not yet give a strict live-worker exclusion guarantee. The phase service is only a template, and Linux/systemd fault behavior has not been tested in a disposable environment. A narrow application-level A01 manual-review hold is the preferable production gate. A process-level quiescence alternative requires a separately reviewed and tested supervisor.

## Findings

### P1 — Already-running auto worker can process owner Retry while STOP is absent

`README.md:25-51` correctly admits this race. `restart=no` protects against container restart; it does not pause the existing `video-worker`. The API accepts an A01 Retry while its DB stage is blocked (`apps/api/app/video_reviews/admin_service.py:2141-2165`). The auto worker skips a retry only while the project STOP exists, then tries to acquire the project LEASE (`tools/video/automation/flow.mjs:1532-1555`). If the review process/LEASE dies, a retry and auto tick could run between STOP loss and systemd `ExecStopPost` restoration. No code in this package prevents that. An app-level marker checked by every A01 auto path or a verified frozen auto process is needed before STOP lift.

### P1 — Missing marker can make boot restoration succeed with STOP absent

`a01_stop_guard.py:123-127` returns `unarmed; no action` solely because `a01-stop-recovery-armed.json` is missing. If its `/root` release directory or marker disappears while A01 STOP is absent, `mokaair-a01-stop-restore.service` succeeds and the `RequiredBy=docker.service` dependency allows Docker to start video containers without A01 STOP. `arm()` fsyncs the marker (`:99-108`), so ordinary power loss is addressed; deletion or path loss remains fail-open. While this temporary boot unit is installed, conservatively restore or create A01 STOP on every Docker startup, or at least treat a held link with no marker as armed and refuse boot when both marker and STOP are absent.

### P1 — Runtime restore failure leaves live auto worker unfenced

`a01_stop_guard.py:123-144` can fail to create STOP (I/O error, ENOSPC, unexpected symlink). The phase template calls it in `ExecStopPost` (`mokaair-a01-review@.service.template:12`), but a failure only fails that service; the existing `video-worker` remains running. A `restart=no` Docker policy does not stop that running process. If the helper cannot restore STOP, recovery must keep the auto process stopped or stop exact pinned video containers. The current candidate has no such fallback. The README itself says strict concurrent Retry protection needs an app marker (`README.md:45-51`).

### P1 — Installer can leave a site-wide boot dependency after partial failure

`install-host-guard.sh:33-45` copies the helper and unit, runs verification, enables the unit against `docker.service`, then checks whether Docker requires it. No rollback/backups/readback are performed if later steps fail. The dependency can block **all** Docker-backed site services if the restore helper fails at boot (`mokaair-a01-stop-restore.service:13-16`; README:148-154). Make installation transactional or provide an independently reviewed rollback that preserves an armed marker; verify copied bytes, unit graph and a no-marker one-shot before any STOP lift. The site-wide availability tradeoff needs explicit site-owner approval.

### P2 — The supervised phase has not been installed or tested

`mokaair-a01-review@.service.template:8-12` points to a future `run-reviewed-a01-round12-phase.sh`. `install-host-guard.sh` installs only the boot unit, not this phase unit. Official systemd documentation says `ExecStopPost` runs after abnormal exit, but no evidence yet proves this template was installed, launched, and fault-tested with the actual runner. Review the frozen runner and exact unit together; test SIGKILL and partial-start behavior in disposable Linux/systemd before production.

### P2 — Linux-specific durability/systemd tests are missing

Local `python -m unittest discover -s stop-recovery-guard -p test_a01_stop_guard.py -v` passed 5 tests and skipped the symlink test on Windows; Bash syntax and Python compilation passed. These tests do not exercise `_sync_dir()` on Linux, systemd ordering, crash after each arm/lift/finish write, or Docker restart policy behavior. Do not promote local tests to a production reboot guarantee.

### P2 — `finish()` does not enforce its stated external prerequisites

`a01_stop_guard.py:147-156` only requires marker and some regular STOP before deleting marker/held link; it does not prove that STOP is the original durable file, that both pinned Docker policies were restored, or that A01 jobs are reconciled. The README delegates those checks to a future runner (`:110-130`). The runner must perform and durably record them before `finish()`; otherwise a caller can disarm crash protection early.

## Alternative assessed: moving A01 work directory under `.manual_review/`

This would hide A01 from immediate-child auto enumeration (`tools/video/automation/flow.mjs:240-246`), and a DB Retry would wait. It is **not compatible with this reviewed round** without redesign:

- The round-12 driver hard-codes canonical `/var/lib/mokaair/video-work/story-rolling-suitcase-v2` (`review-round12-104.mjs:19-33`), while the API stage dispatcher checks project STOP only at that canonical slug path (`apps/api/app/video_automation/ai.py:72-74` and `docker-compose.prod.yml:267`). Merely setting `VIDEO_WORKDIR` does not redirect both.
- The admin producer read reports `not_adopted` while the canonical directory is absent (`apps/api/app/video_reviews/producer_state.py:39-51`), changing owner-visible behavior.
- Durable stage adoption stores absolute artifact paths (`tools/video/automation/run-receipts.mjs:208-223`), and this pilot verifier expects canonical absolute paths (`inspect-review-progress.mjs:84-86`). Relocating back makes hidden-path proofs point at vanished paths; accepting them would require explicit relocation evidence and a new independent audit design.

Reject the rename workaround for this phase.

## Process-level quiescence assessment

A host supervisor could freeze only the exact `worker.sh` parent shell and its `node tools/video/cli.mjs auto` child while leaving the separate Shorts knocker alive; a fresh `docker exec` review process is outside that child tree. Before STOP removal it would have to pin container ID, host PIDs, `/proc` start ticks and ancestry; freeze parent first, then auto/descendants, iterate until the process tree is stable, read back each `T` state, and prove no foreign LEASE or paid job. On exit, `ExecStopPost` must restore and fsync A01 STOP **before** signaling `SIGCONT`; any restore failure must leave auto frozen and the two video containers at `restart=no`. Persist recovery identities before signaling and disposable-test SIGKILL/container death/reboot. None of this exists or is tested in the current package. The app-level A01 hold has a much smaller operational scope.

## Positive observations and sources

- `arm()` writes and fsyncs the marker while original STOP still exists, hard-links STOP within the same video-work directory, then fsyncs that directory before a later lift (`a01_stop_guard.py:90-108`). A crash between marker and link leaves original STOP in place; a crash after lift can relink the held inode.
- The boot unit combines `RequiredBy=docker.service` with `Before=docker.service`, and `RequiresMountsFor` pins filesystem ordering. This is the right dependency shape if the dependency is accepted and installed correctly. Official systemd unit/service documentation: https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml and https://github.com/systemd/systemd/blob/main/man/systemd.service.xml .
- Docker documents that `docker update --restart=no` takes effect immediately and prevents automatic container restart: https://docs.docker.com/reference/cli/docker/container/update/ and https://docs.docker.com/engine/containers/start-containers-automatically/ . It does not quiesce an already-running process.

## Required authorization

The prior A01 US$25 paid-cap and narrow manuscript-review-receipt approval do not authorize this new host change. The repo `prod-host-ops` and `deploy` skills require a fresh named site-owner approval for installing/enabling the systemd Docker dependency, changing and restoring exact pinned restart policies for `video-worker` and `video-ai-worker`, temporarily lifting A01 STOP, and running the exact bounded phase driver. A worker/host failure or project-data drift must stop for reconciliation without fabricating an editorial PASS.
