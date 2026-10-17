# A01 one-off guard fault tests

**Plan with disposable test receipts; no production phase has started.** Provider-free WSL Docker 29.1.3/Compose 2.40.3/systemd 259 tests confirmed one-off labels, `restart=no`/AutoRemove, MainPID SIGKILL recovery with STOP present or lifted, malformed and missing marker recovery, and Docker daemon restart. Exact receipts are under `C:/Users/x8120/.codex/captures/A01-20261017-afternoon-fe35369c/fault-lab/`. The full phase runner and paid path have not been exercised end to end. Run any further fault injection on an isolated Linux VM with a disposable A01 work volume, sanitized site and database, and **no provider keys**. A production no-model `fault-test` would still create a container and marker, so it requires a separate site-owner approval and action-time pins.

## Disposable baseline

Keep the production package's hardcoded paths and checks intact. In the disposable VM, create a **synthetic** checkout at `/root/travel_scanner`, the same named video volumes and the same A01 STOP path, plus a local fake site/database with a blocked A01 row, equal Retry IDs, no live jobs/leases and a US$25 budget. Do not copy production credentials or use a real provider endpoint. Build or load VM-local `:local` images; the VM's full image IDs and container IDs will differ from production. Install the exact reviewed helpers/unit there, stage the reviewed archive, and fill a VM-specific copy of `a01-phase-manifest.json` with that VM's actual HEAD, STOP, container, image and installed-file hashes. Keep source/file hashes tied to the reviewed archive. Set `fault_test_allowed=true` **only in that disposable manifest**. If the synthetic site/budget preconditions cannot be built, run only component tests and report that the full systemd/Compose fault test remains unproven; do not weaken production checks with a test-path environment override. Record before every injection:

```bash
sha256sum /var/lib/docker/volumes/travel_scanner_video_work/_data/story-rolling-suitcase-v2/STOP
stat -c '%d:%i:%a' /var/lib/docker/volumes/travel_scanner_video_work/_data/story-rolling-suitcase-v2/STOP
docker inspect --format '{{.Id}} {{.State.Running}} {{.HostConfig.RestartPolicy.Name}} {{.Image}}' <original-video-worker-id> <original-video-ai-worker-id>
docker ps -a --no-trunc --filter label=mokaair.a01.round12
```

Verify no stage/media job, project LEASE, release hold or deploy lock is present. The site A01 row must be blocked and Retry request/ack IDs equal. If any baseline differs, stop the test.

## No-model systemd MainPID SIGKILL

1. On the **disposable VM**, run `systemctl start --no-block mokaair-a01-review@fault-test.service`. The mode only creates a labelled `sleep infinity` one-off, writes its ID marker, logs `A01_FAULT_TEST_READY`, then blocks. It does not invoke a review driver, lift STOP, change either original worker policy or call a model.
2. Read `journalctl -u mokaair-a01-review@fault-test.service -n 30 --no-pager` and the fixed Docker label. Require exactly one full one-off ID, `restart=no`, `AutoRemove=true`, and the original STOP and two original container states/policies identical to baseline.
3. Run `systemctl kill --signal=SIGKILL --kill-who=main mokaair-a01-review@fault-test.service`. Read `systemctl show ... -p ActiveState -p Result -p ExecMainStatus -p ExecStopPost`; wait for the unit to settle. Do not issue another start. Require the journal to show `A01_ONEOFF_STOPPED` before `A01 STOP already present`, and the labelled container to be stopped/removed. Require STOP SHA and inode unchanged and the two original IDs/states/restart policies unchanged. Require recovery to finish within `TimeoutStopSec=90s` on this Docker version; a timeout is a failed test.
4. Repeat after truncating **only the disposable** `a01-round12-oneoff.json` after `A01_FAULT_TEST_READY`, before MainPID SIGKILL. The label fallback must still kill the one-off and restore/read back STOP; the unit must report failure because the marker is corrupt. Repeat with the marker absent.
5. Reconcile the deliberately retained marker under the test lock; verify no labelled one-off or job, then remove only this test marker. Restore `fault_test_allowed=false` and verify the manifest hash changes. No paid phase is run.

## Paid-path checkpoint injections without provider calls

Use a **disposable copy** of the runner and a mocked direct driver which only writes a synthetic audit receipt. Disable all provider credentials at the network and environment layers. Never inject faults into the production candidate or a real paid phase. At each checkpoint below, kill the disposable unit MainPID with SIGKILL and record `ExecStopPost`, STOP, one-off labels, original worker state/policy, global STOP, hold, jobs and budget:

| Checkpoint | Expected result |
| --- | --- |
| During exclusive marker write, before full JSON/fsync | Label fallback kills a created one-off; STOP remains/restores; malformed marker makes unit fail. |
| After temporary global STOP, while auto Node or Shorts is still running | Runner waits and **does not** stop original worker. If it does not drain in 120s, unit fails, leaves global STOP and hold, project STOP remains. |
| After original worker is stopped, before one-off creation | Original remains stopped with restart=no; project STOP remains; no labelled one-off or model call. |
| After one-off is pinned, before `arm` | One-off is killed by `ExecStopPost`; project STOP remains; original remains stopped. |
| After `arm`, while mock driver has removed project STOP | One-off is killed/proved absent **before** original STOP is relinked; original stays stopped with restart=no; hold remains. |
| After synthetic dispatch receipt but before runner reconciliation | Do not retry; retain hold/restart=no until job, budget and audit result are inspected. |

For every injection, a Docker daemon error must **not** be accepted as proof that the one-off stopped. Recovery must still attempt STOP restoration and fail; never start the original auto worker. Test a slow/hung Docker command as an availability fault and verify a human can restore STOP and reconcile before any video restart.

## Daemon restart and boot-start audit

The disposable Docker daemon restart was run with both originals at `restart=no`, original auto stopped, an `AutoRemove=true`/`restart=no` labelled one-off, and project STOP lifted. Both originals remained stopped/no and the one-off disappeared; the held inode restored the original STOP before any video container restart. See `fault-lab/daemon-restart-pass-20261017.md` in the capture directory above. A full shared WSL reboot is optional: its ARM/WSL boot configuration would not establish how the production x86 host starts services. The distinct reboot risk is a systemd unit, timer, cron or cloud-init hook that manually starts video Compose outside Docker's restart policy. Before production use, perform a fresh **read-only** inventory of those boot starters; any video startup path not already covered requires a design change or a separate fence. Forbid out-of-band root `docker compose up/start/restart` for the maintenance window. An isolated VM reboot remains useful if a production-like boot fixture becomes available; do not reboot production or shared WSL merely to satisfy this plan.

## Promotion gate

Record Docker, Compose, systemd versions, exact package SHA, test logs, STOP SHA/inode, full container IDs/image IDs/restart policies, one-off label inventory, job/budget snapshots and elapsed recovery time. Require the accepted daemon-restart receipt and fresh production boot-start inventory; document the untested full reboot as a residual rather than claiming it passed. Independent review must accept the receipts and a new action-time production preflight before any site-owner approval request for installation, `validate`, fault-test, or a paid phase. No production reboot or paid phase is part of this fault plan.
