# Independent A01 one-off guard review, r6 — 2026-10-17

## Verdict

**Conditional code and component-fault PASS; production use remains gated.**
Frozen `stop-recovery-guard/SHA256SUMS.txt` SHA-256:
`f97000ac5352ce2a499eb9e05abc0a72ba2fdf266e6a4f99d7964d992574e9fe`.
I independently verified all listed hashes, 30/30 WSL Linux unit tests,
`bash -n` and Python compilation. The disposable `/usr/local/sbin`
`a01_stop_guard.py` and `a01_phase_recover.py` were root-only during my test;
their hashes matched this exact package, so I ran the tests as root. No
production host write or provider call was part of this review.

R5's P1 was fixed in both recovery and normal runner readback. R6
`a01_phase_recover.absent()` accepts an exact, case-insensitive Docker
`no such object/container: <full ID>` response. It rejects another ID and a
generic Docker error. `a01_phase_runner.oneoff_stopped()` reuses the same
function. A missing one-off after `--rm` is therefore proven without treating
a daemon outage as absence.

## Disposable evidence reviewed

- Docker 29.1.3/Compose 2.40.3 labelled one-off: `oneoff=True`,
  `AutoRemove=true`, `restart=no`, with a full 64-character ID. Compose
  `ps --all` returns both original and one-off; r6 original lookup uses
  `oneoff=False`. See `fault-lab/compose-semantics-20261017.md`.
- Baseline Type=exec MainPID SIGKILL using the exact R6 `ExecStopPost`:
  `ExecStopPost status=0`; one-off stop logged before STOP readback; label
  scan empty; STOP hash/inode intact. `Result=signal` is expected for the
  deliberate SIGKILL. See `fault-lab/sigkill-baseline-pass-20261017.md`.
- Truncated one-off marker: fixed label fallback killed and removed the
  one-off, STOP remained, and `ExecStopPost status=1` retained failure for
  reconciliation. See `fault-lab/sigkill-corrupt-marker-20261017.md`.
- Missing one-off marker: the fixed label fallback killed and removed the
  one-off; `ExecStopPost status=0`, STOP remained and label scan was empty.
  See `fault-lab/sigkill-missing-marker-pass-20261017.md`.
- After exact guard `arm`/`lift`, while project STOP was absent: MainPID
  SIGKILL led to one-off stop **before** original STOP hardlink restore,
  `ExecStopPost status=0`, no labelled one-off, unchanged STOP SHA/inode,
  original auto stopped with `restart=no`, AI worker running with
  `restart=no`. See `fault-lab/sigkill-lifted-stop-pass-20261017.md`.
- Disposable Docker daemon restart with project STOP lifted: both originals
  had `restart=no`, remained stopped after restart, the AutoRemove one-off
  disappeared, and the held original STOP inode survived. The operator's
  exact guard restore relinked the original SHA/inode **before** any worker
  start. See `fault-lab/daemon-restart-pass-20261017.md`. This used a script
  rather than the full phase unit, so it proves the Docker policy/recovery
  component, not systemd reaction to a daemon restart during a real phase.

These are provider-free WSL lab receipts using a custom test unit and inert
containers. They exercise the exact recovery and STOP guard, but not the full
production runner, site/API/DB preflight, real image mounts/network, or a paid
dispatch. The earlier apparent empty Compose stdout was a Windows/WSL
one-liner quoting mistake; a real script returned a full ID. R6 also resolves
the created one-off by exact name, project/service/`oneoff=True` labels and
full ID instead of trusting stdout.

## Gates still open

1. The disposable full VM reboot with `restart=no` originals, one-off and
   lifted STOP remains open. Require STOP restore/readback **before** any video
   container is restarted. The tested SIGKILL recovery sequences finished
   within the 90-second recovery window; daemon-unavailable systemd behavior
   remains an availability test.
2. The supplied phase manifest has blank pins and `fault_test_allowed=false`;
   it cannot run as-is. The whole archive/host/one-off tree and phase source
   pins must be filled and verified. The isolated no-model `validate` on the
   live host is a bounded write and needs its own exact owner approval after
   action-time host preflight. Require successful terminal systemd invocation,
   `ExecStopPost=0`, source/link receipt, STOP and one-off readback before
   contemplating a paid phase.
3. The normal runner's global STOP drain, worker stop/start, Docker policy
   changes, release hold and paid call still require named owner approval.
   A first model dispatch is uncertain after timeout or signal even when the
   one-off is stopped; reconcile stage jobs, audit chain and budget before
   any retry. Keep the US$25 cap and phase-specific authorization explicit.
4. This host-only fence covers ordinary auto selection, UI Retry, automatic
   container restarts and host reboot. An out-of-band privileged root manual
   `docker compose up/start/restart` can bypass it and must be prohibited for
   the maintenance window. The original video-worker/Shorts is paused during
   a phase, and AI worker crash restart is disabled until reconciliation.

This review does not claim A01 manuscript approval, completed video, or
permission to start production. The earlier r4 and r5 review reports are
historical snapshots; r5 was blocked by the now-fixed lowercase Docker error.
