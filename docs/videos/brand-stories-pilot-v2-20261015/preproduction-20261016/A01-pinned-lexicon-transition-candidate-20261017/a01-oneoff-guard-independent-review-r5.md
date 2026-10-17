# Independent A01 one-off guard review, r5 — 2026-10-17

## Verdict: P1, do not use r5 on production

The exact frozen `stop-recovery-guard/SHA256SUMS.txt` SHA-256 was
`4c0a80aa86d93cc79303eba7c29da7c76c4965fa49356861d0fbfe050dc7a021`.
Its `a01_phase_runner.py` SHA-256 was
`dd89ac57edc68ad55c2e730c7c62e6fef5ee4eba97b55da090aad319cd19dc35`.
I reviewed the post-Compose one-off identity change and independently verified
`sha256sum -c` for every listed file, 27/27 WSL unit tests, `bash -n`, and
Python compilation. A root WSL test run was needed because a separate
disposable install had left `/usr/local/sbin/a01_stop_guard.py` mode 0700;
that file's SHA matched the r5 package.

**P1: real disposable systemd SIGKILL recovery failed.** The Docker 29.1.3
daemon reported an already removed one-off as lowercase
`error: no such object: <full ID>`. `a01_phase_recover.py`'s `absent()` accepts
only uppercase `No such object`/`No such container`, so `ExecStopPost` exited
with status 1 even though it killed the one-off and A01 STOP remained present.
The runner's `oneoff_stopped()` has the same case-sensitive check. Both sites
must accept only an exact, case-insensitive no-such-object/container response
bound to the requested full 64-character ID. A generic Docker error or daemon
outage must never count as absence. Rehash the changed package, rerun unit
tests, then rerun the same real disposable systemd MainPID SIGKILL test and
verify `ExecStopPost=0`, one-off absent/stopped, original STOP hash and inode,
original worker IDs and `restart=no`, and retained hold.

The r5 post-run identity lookup itself resolves one candidate by the exact
custom phase label, then reads back full `.Id`, fixed `.Name`, Compose project,
service, and `oneoff=True` before writing the durable marker. It is a defensive
improvement over reliance on Compose stdout. The earlier apparent blank
Compose stdout was a Windows/WSL quoting error; a real script run returned a
full ID. Docker's `compose ps --all` did include original and one-off, so the
original-container lookup must retain its `oneoff=False` label filter.

No production host write, provider call, or paid phase was performed by this
review. Even after the P1 fix, real disposable daemon-restart/reboot and
STOP-loss fault receipts, action-time production preflight, filled SHA-pinned
manifest, independent review, and named site-owner approval remain gates for
installation, STOP lift, and model work. Privileged root manually starting a
new worker during the maintenance window is outside the host-only guard's
boundary and must be excluded explicitly in operator instructions.
