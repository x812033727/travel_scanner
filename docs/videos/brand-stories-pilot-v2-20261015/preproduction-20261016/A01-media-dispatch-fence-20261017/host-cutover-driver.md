# Exact-job host cutover driver

## Global paid-intake gate candidate: production HOLD

The local candidate now makes the API read `video_work/.a01-paid-intake/marker.json`
on every paid media POST and active-job GET. A missing, malformed, symlinked or
non-root-owned marker returns `video_media_cutover_paused` (423). The only
pre-cutover open state is an explicitly installed `BOOTSTRAP_ALLOW` marker.
Writing the no-clobber, durable `armed.json` first immediately invalidates that
state; an interval between that write and an atomic `PAUSED_ALL` replacement
also returns 423. `PAUSED_ALL` rejects every slug. `ALLOW_A01_ONLY` accepts
only `story-rolling-suitcase-v2` while the exact Suncatcher Redis nonce still
has its pinned hash and no expiry. In `PAUSED_ALL` and `ALLOW_A01_ONLY`, removing
or corrupting either file closes the gate. Never remove `armed.json`: it is the
no-return proof against a stale bootstrap marker. The global marker lives outside `.ops` because the existing exact-job
installer refuses a pre-existing `.ops` parent.

This is **not an executable production cutover**. There is no reviewed host
installer for the bootstrap/armed/paused files, no old-API live 423 proof, and
the current driver still raises `b25_producer_proof_missing` before writing.
The presently deployed old API does not read this marker. A separate initial
deployment of gate-aware API code with a preinstalled bootstrap marker is
required; only after verifying its exact container/image and source hashes may
the plan be regenerated with that API as `old_live_sha`. The plan requires a
different `target_sha`. The old API must then prove `PAUSED_ALL` on the live
image/clip/music, judge/locate and active-GET routes before SIGTERM. A 423
response proves a fresh request was refused; it does not prove that a request
which passed `BOOTSTRAP_ALLOW` earlier has finished. Wait for graceful old-API
exit before the database/Redis snapshot. Keep the armed file and pause marker
through deploy; check new API source hashes, image/container identity, and live
423 responses before any handoff.

Before changing to `ALLOW_A01_ONLY`, a reviewed root-only transition must
recheck that the old API cannot run, the new API has the exact target image and
source hashes, the marker/armed bytes and owner/mode are pinned, and the Redis
nonce and watcher are still owned. Repeat those checks at every A01 handoff
checkpoint. The API cannot infer its Git SHA from the existing stock deploy:
Compose's `RELEASE_SHA` defaults to `local`, and stock rollback rebuilds under
the same environment. The environment tag alone is not source proof. An early
`ALLOW_A01_ONLY` marker on the preliminary API is therefore unsafe and a STOP.
No general `ALLOW_ALL` state exists after arming; restoration for other videos
needs a separate reviewed release and host action.

`host-cutover-driver.py` is a root-host, dry-run-by-default implementation of
the ordered cutover in this directory's `README.md`. It is **not approved or
installed on production**. The current exact-one preflight must stop while
the unrelated B25 MiniMax stream has a queued/running media job. A brief gap
between its paid jobs can make an instantaneous exact-one query pass, so apply
also requires authoritative proof that the B25 producer has completed or is
durably paused and cannot queue another job. That control is not yet verified;
the current package remains blocked for production. The current `--apply`
path explicitly stops with `b25_producer_proof_missing` before any host write;
that stop may be removed only with a reviewed authoritative proof. An independent
review, a merged target commit, fresh host evidence and site-owner approval
naming the exact plan SHA and API outage are required before `--apply`.

The driver accepts a root-owned private JSON plan. It refuses missing or extra
fields. `schema_version` is `1`; `pr_head`, `target_sha` and `old_live_sha` are
full lowercase commit hashes. `release_dir` is exactly
`/root/mokaair-a01-media-fence-<12 lowercase hex>` and is already root-owned
mode 0700. `require_autodeploy_absent` must be `true`: the autodeploy timer
and its service must both be `LoadState=not-found`, `ActiveState=inactive`, with
no pending job. The `pins` object
contains full 64-character Docker IDs for `old_api_id`, `redis_id`, and
`worker_id`; their `sha256:<64hex>` image IDs; exact Docker volume names and
mount paths `redis_volume`, `redis_mount`, `video_work_mount`; a SHA-256 of
the **effective** API/worker `REDIS_URL` under `api_redis_url_sha256`; and the
byte SHA-256 of `/root/travel_scanner/.env` under `host_env_sha256`. The driver
compares those hashes without logging values. `pr_head` records approval
provenance only: the deploy target is `target_sha`, which may differ after
squash merge. Target blobs and a fast-forward from `old_live_sha` are checked
directly. The `source_sha256` object
pins these exact filenames:

The URL hash is only a byte-identity pin. Before stopping the old API, the
driver also opens each running API and video worker's effective `REDIS_URL`
inside that container and compares its read-only Redis server run ID to the
pinned Redis container's run ID; `CLIENT INFO` must show logical DB 0. It
repeats this for the replacement API. The URL, password and connection errors
are never written to argv, receipts or logs.

| Staged in `release_dir` | Outside `release_dir` |
| --- | --- |
| `host-cutover-driver.py`, `host-cutover-driver.deploy-wrapper.sh`, `dispatch_fence_cutover.py`, `install-marker.sh`, `monitor-lock.sh`, `manifest.json`, `hold.py`, `incoming-docker-compose.prod.yml` | `/root/deploy-travel-scanner.sh`; `jobs.py`, `admin_api.py`, `cutover_intake.py`, `dispatch_fence.py` and `dispatch_fence_cli.py` blobs in `target_sha` |

The staged sources must be root-owned, regular, not group/world-writable and
match the plan hashes. `manifest.json` must have the compiled SHA
`6d6a64a88f066ce62d3ccf2145ab59e052dee0bf76e4da7b68385d93ea6827a5`.
The host deploy script must be the reviewed patched SHA
`836b953610b4ae17eda6d2056efb1f633827db620d0eb43934312cc19d8ac9c6`;
the current live script SHA `c8bb3559f6b7e25e11c3bdf207c2f8dabd28835119c78494b3c9ad8bb75bd64f`
fails closed. The incoming Compose file must equal the `target_sha` Git blob, and its Redis
service/volume plus API Redis URL must equal the live deployment. The target
commit must already be present locally for `git show`, and `origin/main` must
equal it; the driver never fetches or merges Git itself.

**Before merging the target PR to main**, read both
`travel-scanner-autodeploy.timer` and `travel-scanner-autodeploy.service` with
`systemctl show <unit> -p LoadState -p ActiveState -p Job`; require `not-found`,
`inactive`, and no job for each, plus no alternative scheduler invoking the
stock deploy script. Repeat immediately after merge and before driver preflight.
A loaded timer is a STOP: pausing it only after merge would leave a dispatch
window. The installer and driver independently enforce the exact unit absence.

Review the plan and calculate its SHA-256 **after** all values are filled. A
dry-run is a read-only preflight (`GIT_OPTIONAL_LOCKS=0` for Git reads); its
JSON reports `production_ready=false` even if the snapshot checks pass. It does
not invoke the stock script, whose
own `--dry-run` fetches Git and writes a log. It does not acquire locks,
create a hold, stop containers, set Redis keys or install a marker:

```bash
python3 /root/mokaair-a01-media-fence-<sha12>/host-cutover-driver.py \
  --plan /root/mokaair-a01-media-fence-<sha12>/plan.json \
  --expected-plan-sha256 <reviewed 64-character plan SHA>
```

The apply mode refuses a shell invocation. After the named owner approval,
the reviewed driver is launched as a **transient host systemd unit** so an SSH
disconnect does not interrupt it. This is a review template, not an instruction
to run before the approval and action-time dry-run:

```bash
systemd-run --unit=a01-media-cutover-driver \
  --property=Type=exec --property=Restart=no \
  --property=KillMode=process --property=TimeoutStopSec=infinity \
  /usr/bin/python3 /root/mokaair-a01-media-fence-<sha12>/host-cutover-driver.py \
  --plan /root/mokaair-a01-media-fence-<sha12>/plan.json \
  --expected-plan-sha256 <reviewed 64-character plan SHA> --apply
```

The driver takes all four release flocks and uses the repository's hash-pinned
`hold.py` while they remain open. Before creating the hold, it reruns the
**full** preflight under those locks, including the no-existing-hold and
release-state checks. It fsyncs the hold and parent directory,
then rechecks both autodeploy units are absent before draining the old API. It
keeps the same hold from first acquisition through stock deploy and A01
handoff. The helper source must be mode 0644. Before the API stop, the driver
copies that exact file into the pinned worker and reads back its SHA through
the worker's default UID, proving it can execute there. A copy or readability
failure leaves the old API running and the hold in place. It waits indefinitely for `docker stop
--signal=SIGTERM --timeout=-1` on the **pinned old API ID**. Every 30 seconds
the root-private event log records that the graceful stop is still waiting.
An observer can read the unit, hold, old API status and event log; **do not
SIGKILL** a slow stop. Only after its exact exit does the driver use the
reviewed helper in the pinned `video-ai-worker` to `SET NX` a no-expiry exact
job lock and obtain same-connection `WAITAOF` proof. An ambiguous helper result
leaves the private receipt and hold for recovery. There is no automatic retry.
If staging fails, inspect the exact `/tmp/a01-media-cutover-<sha12>.py` path in
the pinned worker before any later attempt; do not overwrite or retry blindly.

The host watcher is a transient unit named
`a01-media-dispatch-fence-watch.service`, with exact `ExecStart`:

```text
/bin/bash /root/mokaair-a01-media-fence-<sha12>/monitor-lock.sh --receipt /root/mokaair-a01-media-fence-<sha12>/nonce-receipt.json --redis-container-id <pinned full Redis ID>
```

The driver pins the watcher script bytes, `systemctl show -p ExecStart --value`
string, MainPID, fresh root-private heartbeat, and actual Redis nonce/TTL. It
retains the watcher and nonce through the stock deploy and A01
handoff. After the new API's held-mode fence check, it writes a root-private
`handoff.json` containing no nonce and exact receipt/heartbeat and hold
identity/hash fields. The A01 R9 guard must adopt and verify that **same** hold
through every A01 phase and exact-job retirement; its current listener needs
the separately reviewed adoption change before cutover. The stock wrapper receives
`--ignore-hold`, `--no-rollback`, the exact expected hold, main, `.env`, and rendered Redis URL
SHA values. The patched stock script checks the hold SHA under its deploy
flock before bypassing it. No failure path automatically rebuilds the old unfenced API. The driver
never invokes `release` or a provider.

On failure before or during stock deploy, the same cutover hold remains. After
the stock script exits, the driver reacquires all four flocks and verifies the
unchanged hold bytes; it never clears or replaces that hold. The nonce remains
regardless. A hung stock deploy or driver/systemd failure requires inspection
of the hold, nonce and watcher before any API action. Do not clear a hold,
delete a marker, remove a
nonce or restart the old API simply to make A01 proceed.

## Separate stock script patch

`host-cutover-driver.deploy-guard.py` transforms only the fresh LF-only
13,617-byte live capture with SHA
`c8bb3559f6b7e25e11c3bdf207c2f8dabd28835119c78494b3c9ad8bb75bd64f`.
The resulting exact candidate is `host-cutover-driver.deploy-patched.sh` at
SHA `836b953610b4ae17eda6d2056efb1f633827db620d0eb43934312cc19d8ac9c6`;
`host-cutover-driver.expected-main-env.patch` shows the changes. After the
script's own fetch, it compares the fetched SHA and uses that immutable SHA
for the survey and merge. It snapshots the approved `.env` into a private
0600 `/run` file, passes it to Compose as both `--env-file` and
`RUNTIME_ENV_FILE`, and checks its hash for every Compose call. Before either
normal or rollback `compose up`, it hashes the rendered API and Redis-using
service URLs without printing them. The cutover itself passes `--no-rollback`.
With `--expected-hold-sha256`, the stock script also verifies the exact A01
hold under its deploy lock and refuses an unrelated pending staged release.
This flag requires all three other immutable pins and `--ignore-hold`.

The private `.env` snapshot is created at one exact
`/run/mokaair-a01-deploy-env.XXXXXXXX` path, root-owned mode 0600. Its normal
EXIT trap removes it. After a SIGKILL, do not delete candidates by a glob:
first prove the stock deploy process and any rollback are terminal, identify
each exact path, verify root ownership/mode and the approved `.env` hash
without printing contents, verify no process has that path open, then use a
separately approved exact-path cleanup and read back its absence. `/run` is
cleared by reboot, but a reboot is not a fence-recovery step.

`host-cutover-driver.install-deploy-guard.py` previews the exact live/candidate
SHA and `bash -n` by default. Its `--apply` path is **not authorized** by this
document: it requires a separate site-owner approval after action-time host
preflight. It takes the four release flocks, refuses an existing hold, loaded
autodeploy timer/tick or active watcher, and creates an exact backup at
`/root/deploy-travel-scanner.sh.a01-before-c8bb3559`, writes a same-directory
temporary file, syntax checks it, atomically replaces the live script, fsyncs
the directory, and reads back the final SHA and mode 0700. It refuses if the live script
no longer matches c8bb3559. `--restore` previews the patched live SHA and
original backup SHA; `--restore --apply` deliberately stops. Restoring the
unguarded script requires a separate approved fence-retirement procedure
proving nonce, marker, queued job, watcher and API state are all reconciled.
Installation and preview do not deploy or call a model.

Offline tests: `python3 host-cutover-driver.test.py -v` on Linux and
`python3 host-cutover-driver.deploy-guard.test.py -v`. They exercise
real disposable flocks/hold files, dry-run, indefinite API stop arguments,
watcher ExecStart matching, private handoff, failure ordering, exact candidate
syntax and no-rollback behavior. They do not simulate a production deploy or
vendor call.
