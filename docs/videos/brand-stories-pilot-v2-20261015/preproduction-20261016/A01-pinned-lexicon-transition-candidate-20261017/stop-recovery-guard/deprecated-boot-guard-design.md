# SUPERSEDED — original A01 round 12 boot-hook/SIGSTOP design

This historical candidate is retained for comparison only. Its file list and
hashes are obsolete, and its site-wide Docker boot dependency was removed from
the current package. Do not install or execute anything described below. See
`README.md` in this directory for the current one-off container candidate.

# A01 round 12: STOP recovery design and candidate package

This is a **read-only host assessment and local candidate**, not an installed
production guard. It does not authorize production host writes or model calls.

## Current host evidence

Read from `hostinger2` on 2026-10-17 using `docker inspect`, `stat`, `findmnt`,
`systemctl show` and `ps` only:

| Item | Observation |
| --- | --- |
| Video work | named volume `travel_scanner_video_work`, host mount `/var/lib/docker/volumes/travel_scanner_video_work/_data`, ext4 on `/dev/sda1`; available before `dockerd` |
| A01 STOP | `.../_data/story-rolling-suitcase-v2/STOP` existed, regular mode 0600, 186 bytes; the distinct global `.../_data/STOP` was absent |
| Main worker | `video-worker` running, volume RW, restart `unless-stopped` |
| Model worker | `video-ai-worker` running independently, same volume RO, restart `unless-stopped`; `ai.py` checks project STOP before durable model dispatch |
| Boot | Docker service/socket enabled; systemd 259; Docker root `/var/lib/docker`, `live_restore=false` |
| Auto | `worker.sh` loops `node tools/video/cli.mjs auto`; blocked A01 remains held unless owner retry is recorded while project STOP is absent; a dead LEASE can be reclaimed |

## Recommended bounded host guard

1. Install an idempotent Python restore helper and a systemd one-shot unit with
   `Before=docker.service`, `RequiredBy=docker.service`, and mount dependency for
   the exact volume path. `RequiredBy` is important: `WantedBy` orders it at boot
   but would still let Docker start if the armed restore failed. The volume is a
   host ext4 directory, so helper does not require Docker to read it.
2. Before removing A01's project STOP, persist a marker in the exact release
   directory and a hard link to the original STOP in the same volume, with file
   and directory `fsync`. The current JS driver still verifies and temporarily
   unlinks its own STOP; host helper `lift` is an alternative, **not an additional
   command** for that driver. Host helper `restore` is safe to run repeatedly and
   never overwrites an existing STOP.
3. Run each exact A01 phase under a systemd service with `ExecStopPost=... restore`.
   The phase runner must hold the four deployment locks, its own release hold and
   the A01 project LEASE. It may only issue the driver's pending guard receipt
   after verifying the installed unit, marker, container IDs/policies, phase and
   source hashes.
4. Docker's container restart can race `ExecStopPost` on a **container kill**. Thus,
   while STOP is lifted, temporarily set `restart=no` on the two exact pinned
   video worker container IDs and read them back. Restore the original
   `unless-stopped` policies only after STOP is present and A01 paid jobs settle.
   This affects the two video workers' crash recovery, not the API/web services.
5. If a durable AI job remains queued/running or becomes uncertain, restore STOP
   but keep the marker, release hold and `restart=no`; do not run the next phase,
   clear hold, or pay again on a new key. Read the job and audit receipts first.
   Once a phase is fully settled, restore policies, disarm marker; next phase
   repeats a fresh preflight. Keep the round's deployment hold through final phase.

**Residual concurrency risk:** an existing auto process can receive a new owner
retry in the small interval between the reviewer LEASE dying and `ExecStopPost`
restoring STOP. There is no existing persistent auto-only project hold. `status=blocked`
and LEASE make the ordinary current path safe, but a concurrent retry cannot be
excluded by the host guard alone. An application-level `MANUAL_REVIEW_HOLD` file
checked by `flow.mjs` `movable` and blocked retry would close that gap while leaving
direct `advanceStory` available. It requires a separate claimed task/PR, tests,
CI, merge and deployment, with no migration. Existing `policy_hold`, `dropped_at`
and global automation disable are not equivalents: the current
`review-round12-104.mjs` requires `settings.enabled===true`, and the durable AI
dispatcher in `apps/api/app/video_automation/ai.py` checks the saved `enabled`
value. During a host-only review window the operator must not press A01 Retry
or issue an owner retry by API; a retry observed is a stop condition. A
speculative `SIGSTOP` of
`worker.sh`/auto/Shorts was not adopted: child processes and PIDs move, and it may
freeze unrelated film work or a Shorts call. It needs disposable-container proof
and its own operations review.

## Candidate and checks

Package: `C:/Users/x8120/.codex/worktrees/a01-branch-sync/travel_scanㄐ/docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-pinned-lexicon-transition-candidate-20261017/stop-recovery-guard/`.

| File | SHA-256 |
| --- | --- |
| `a01_stop_guard.py` | `2556BFDBA4BBDA0B61C73A48D2B107BAD953721ABA405C9EB09B64DEFD0A62E6` |
| `install-host-guard.sh` | `DAF566E8329881E677A4B659F6784E7A83496AF0900D9F6FD5EE43686AD293FB` |
| `mokaair-a01-review@.service.template` | `6FFFF72143A9710879F76BDD718500DDC56CB8DBF89284B8ADA3B32CD9EE2FA5` |
| `mokaair-a01-stop-restore.service` | `802B0A205E1C3EB0CE5F1D0779072CAC635B7A21D17259F8918FEE91B7613C1C` |
| `test_a01_stop_guard.py` | `798B61A4325467B9B45EB9B84536A8683BF2EEFC309F5DD83E7310F94A369D23` |

Local checks: `python -m unittest -v test_a01_stop_guard.py` passed 5 cases
with one Windows symlink test skipped; Git Bash `bash -n install-host-guard.sh`
passed; `git diff --check` passed for tracked files. WSL Linux test failed
before Python started due `Wsl/Service/CreateInstance/CreateVm/0x800705b4`.
Systemd unit and Linux `fsync` behavior remain untested locally. No production
write, unit installation, STOP lift, container policy change or paid call was made.

## Approval, fault tests and rollback

The repository's `prod-host-ops` and `deploy` rules require explicit site-owner
approval for host writes and script installation. Approval should identify this
reviewed package/hash, the unit installation and fail-closed Docker dependency,
the exact two temporary restart-policy changes, and one bounded A01 phase. It
should acknowledge that an armed restore failure can stop all Docker services
at next boot and that a worker crash leaves unrelated video work waiting.

Test in a disposable Linux VM/container first: arm/lift/restore across separate
processes; kill a no-model systemd runner MainPID to prove `ExecStopPost`; kill
both disposable workers under `restart=no` to prove no auto restart; simulate
boot order and STOP restoration before Docker; test missing volume fails closed.
On production, a non-paid dry run can verify unit dependencies and `restore`
while STOP already exists. Do **not** kill a paid run or reboot the live host
for testing. A real reboot test needs a separate maintenance authorization.

Rollback before STOP lift: leave STOP in place, restore both recorded container
policies, disarm marker, verify jobs, then clear only the run's own release hold.
After a lift or uncertain model state: restore STOP first; keep marker/hold and
restart `no` until the job receipt and audit are reconciled; then restore policies
and disarm. Uninstall the boot unit only after STOP exists, marker is gone, and
the Docker dependency can be removed safely.

Primary runtime references: [Docker restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/), [Docker container update](https://docs.docker.com/reference/cli/docker/container/update/), [systemd unit ordering](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html), [systemd service hooks](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).
