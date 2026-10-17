# One exact media dispatch fence: review and cutover plan

Status: **the API fence and [single-host cutover driver](host-cutover-driver.md)
are prepared locally for independent review; no production action performed.**
The sequence below is the driver's contract, not separate PuTTY commands:
separate SSH calls cannot retain four lock file descriptors or prove the
`hold.py` precondition. Production still requires a named site-owner approval
for the exact PR/SHA, host script installation, durable Redis nonce, temporary
API outage and marker write, plus fresh action-time host evidence. The driver
refuses while another queued/submitted media job exists; the 2026-10-17 B25
MiniMax image stream currently makes that condition fail. A brief gap between
B25 jobs can make a single database count appear clear, so the current
`--apply` path also stops with `b25_producer_proof_missing` before any host
write. Production needs separately reviewed, authoritative proof that the B25
producer has completed or is durably paused. Do not use a prior A01
paid-production approval to stop an unrelated API or write this marker.

## Scope and invariant

The sole target is `b721a65d-8c8d-4ae8-834c-391cfc267a6f`, slug
`google-project-suncatcher-prototype-what-it-tests`, request hash
`52b39c04a45f39b4101bcd7e401c31cd0e6083f3c8390b729afd2a83569379e6`,
kind `image`, provider `minimax`, model `image-01`. The 2026-10-17 15:45:32Z
read-only snapshot showed `queued`, `attempts=1`, `polls=0`, and null
`vendor_ref`/`submitted_at`. Recheck this whole tuple immediately before action.
This task does not call MiniMax, retry or fail the job, alter its database row,
create A01 media, or infer that no earlier vendor charge occurred.

The new API compiles the ID and tuple. For that ID, both direct GET advancement
and repeated POST refuse **before** any provider call or database transition.
A matching regular on-volume manifest gives `video_media_dispatch_fenced` (423);
a missing, malformed or mismatched manifest gives
`video_media_dispatch_fence_invalid` (503). Both leave the row unchanged.
Other IDs follow the existing code. Deleting the marker cannot resume this ID;
removal needs a separate reviewed code change and owner decision.

The candidate `manifest.json` SHA-256 is
`6d6a64a88f066ce62d3ccf2145ab59e052dee0bf76e4da7b68385d93ea6827a5`.
The API already mounts `travel_scanner_video_work` read-only at
`/var/lib/mokaair/video-work`; the marker path is
`/var/lib/mokaair/video-work/.ops/media-dispatch-fences/b721a65d-8c8d-4ae8-834c-391cfc267a6f.json`.
The API runs as UID 10001, so new parent directories must be mode 0755 and the
marker mode 0644. `install-marker.sh` refuses pre-existing parents/marker,
symlinks, volume/mount drift, and candidate-hash drift; its default is dry-run.
It creates and fsyncs new directory entries, file data and the marker directory
before bounded `O_NOFOLLOW` readback. A partial install is a stop for review,
not a reason to loosen permissions or overwrite.

## Why a deploy alone is unsafe

The old API does not read the marker. A queued database status does not rule
out an in-flight `_submit` call. The old `advance_job` also deletes its short
Redis lock unconditionally in `finally`; an operator must **first** let the
old API exit gracefully, then acquire a durable, non-expiring exact-job nonce.
A fixed 280-second wait is insufficient: an HTTP timeout may cover individual
operations, and the old call could outlive its original 240-second lock. A
new marker or Redis lock while the old API still runs is no proof of safety.

The production stock deploy stops `video-ai-worker` during its final drain.
Therefore the nonce watcher must run on the **host**, not in that worker. The
watcher pins the live Compose Redis container ID each loop and checks the exact
nonce and no-expiry TTL. A missing heartbeat, watcher death, Redis replacement,
or Redis URL drift is a STOP. The cutover disables stock automatic rollback to
the old API, which has no compiled fence. Any later recovery or rollback needs
a separate approved procedure while the hold and nonce remain in place.

## Required action-time preflight

1. Pin the proposed PR head, reviewed source hashes, green CI, current `main`,
   deployed SHA, exact API and Redis full Docker IDs/images, exact database row,
   active queued/submitted media count, Redis key absence, volume mountpoint,
   current API port 8090 owner, auto timer and deploy state. Recheck that the
   video-work volume is still mounted read-only in the API and API UID can
   traverse the proposed mode 0755 parents. A second active media job or
   changed tuple is a stop, not an exemption. The normal production preflight
   must show no other paid work, stage marker, deploy lock or hold.
   Query the exact Compose Redis with `CONFIG GET appendonly appendfsync
   maxmemory-policy maxmemory`: require `appendonly=yes`, an AOF fsync policy
   at least as strong as `everysec`, and `maxmemory-policy=noeviction`.
   Record the returned values and Redis data-volume identity. A Redis setting
   mismatch is a stop even if a subsequent `WAITAOF` returns an acknowledgement.
   Diff the reviewed incoming `docker compose -f docker-compose.prod.yml config`
   against the deployed Compose Redis service, data volume and API `REDIS_URL`
   target. Any Redis service, volume or connection-target change is a stop
   before starting the cutover. Repeat the full preflight under all four locks
   before creating the hold.
2. Review `/root/deploy-travel-scanner.sh` at its current SHA, especially the
   one-shot lock/hold checks, pinned target and environment guards, and drain
   hooks. Review
   `ops/release/README.md` and the `deploy` and `prod-host-ops` skills. Do not
   remove an existing hold or disable a timer by assumption. Obtain the site
   owner's **specific** approval for this SHA, brief API outage, marker and
   Redis writes, and deploy. This cutover uses `--no-rollback`; any failure
   recovery or later old-code rollback requires a separate owner decision.
3. Stage these reviewed scripts and `manifest.json` to private host storage;
   compare complete source hashes there, with no shell interpolation of the
   receipt's secret nonce. `install-marker.sh --expected-mountpoint <freshly
   inspected Docker mountpoint>` must print only the intended target/hash in
   dry-run. A previously existing `.ops` or marker stops the one-off installer
   for inspection; never `chmod` existing content.

## Bounded cutover sequence

All steps require one approved host driver with an audit log that omits the
nonce. The four locks are `/var/lock/travel-scanner-deploy.lock`,
`/root/mokaair-deploy.lock`, `/run/mokaair-manual-deploy.lock`, and
`/run/travel-scanner-deployer/deploy.lock`. `ops/release/hold.py` requires all
four. The hold is `/root/travel-scanner-deploy.hold`; after a full preflight
under all four locks, acquire it with a unique cutover release directory and
pinned target SHA using `hold.py`, then verify its exact bytes. Keep this
**same hold continuously** through deploy, verification and A01 handoff. Keep
the four lock file descriptors through marker installation, release them only
for stock deploy, then reacquire all four for verification. Loss of driver/SSH
while waiting means stop, leave the hold, and re-audit.

1. Under all four locks and the hold, recheck no old in-flight paid work and
   the exact old API container ID/image. Do not bypass the hold when stopping
   the API. Copy the mode 0644, hash-checked `dispatch_fence_cutover.py` into
   the pinned non-API Python worker and read its hash through the worker's
   default UID **before** stopping the old API. Gracefully stop **that ID
   only** with `docker container stop --signal=SIGTERM
   --timeout=-1 <old-full-API-ID>`. `-1` waits indefinitely for graceful exit;
   never substitute a finite SIGKILL timeout. A hang is a stop; leave hold and
   Redis untouched. An external observer may declare an operational timeout
   from the driver's status, hold and old container, but must not SIGKILL the
   stop or API. The driver remains parked for manual review, retaining its
   locks and hold. Verify the same ID now has `Running=false`, `PID=0`, no
   other Compose API container and no listener on 127.0.0.1:8090. Confirm the
   exact DB row is still queued with null vendor reference/submission time and
   no exact Redis lock. A stopped container alone does not establish whether
   an earlier provider charge happened.
2. After the old API exits, verify the pinned non-API worker still uses the
   pinned Redis service, then invoke the staged helper's
   `acquire --receipt-file /tmp/a01-media-cutover-<unique>.json`; it first
   creates a private 0600 fsynced receipt, then `SET NX` with no expiry,
   `WAITAOF 1 0 10000` on the **same dedicated Redis connection**, and
   compares exact nonce plus `TTL=-1`. Require local fsync ack `1` and
   `durable=true`; a timeout/unknown result may leave the key present and is
   a stop requiring private receipt recovery, never a blind retry or delete.
   The command prints only nonce SHA, not the nonce. Copy the receipt without
   printing it into `/root/mokaair-a01-media-fence-<12-hex>/nonce-receipt.json`
   with root-owned mode 0700 parent and 0600 file. Verify both modes and guard
   the receipt from logs. Do not run `watch` in `video-ai-worker`, which deploy stops.
3. Start `monitor-lock.sh --receipt <root-only-host-receipt>
   --redis-container-id <pinned-64-character-ID>` as supervised **host
   service** `a01-media-dispatch-fence-watch.service` (approved `systemd-run
   --unit=a01-media-dispatch-fence-watch`, with exact command, PID, active
   state and journal recorded), never as an SSH
   child or inside an application container. Prove its first fresh heartbeat
   at `/run/a01-media-dispatch-fence/heartbeat.json` and that the service
   remains active. The heartbeat is root-owned mode 0600 under a root-owned
   0700 directory and records `schema_version=1`, exact `job_id`, full
   `redis_container_id`, `checked_at_utc`, positive `checks`, `nonce_sha256`,
   `owned=true`, `no_expiry=true`; it refreshes after each successful two-second
   check. Require age at most 15 seconds at every A01 guard checkpoint.
   It verifies Compose resolves to this exact
   Redis ID, the ID is the sole running Redis service, and the nonce stays
   intact without expiry every two seconds. Keep this watcher running through
   the whole deploy and A01 handoff; heartbeat/service loss is a
   stop for A01 even though the durable nonce may remain in Redis. A host
   reboot or Redis restart requires fresh Compose ID, AOF configuration,
   exact receipt nonce/TTL readback and a newly supervised watcher before
   any A01 action. Never infer persistence solely from the old receipt.
4. With old API stopped, nonce durable and watched, and all four locks/hold
   still owned, run `install-marker.sh --expected-mountpoint <same-mount>
   --apply`. Require `O_NOFOLLOW` regular-file/hash readback, new parents
   0755 and marker 0644. Read back the marker as UID 10001 using a disposable
   read-only mount or the later new API container; do not restart the old API
   for this test. Recheck DB row, nonce ownership and watcher heartbeat.
5. Reverify the exact hold, nonce, marker and watcher, then release the four
   lock file descriptors while **retaining the same hold**. Run the reviewed
   background stock-deploy wrapper with `--ignore-hold --no-rollback` and
   exact expected main SHA, `.env` SHA, rendered Redis URL SHA and hold SHA.
   The patched stock script verifies the hold bytes under its deploy lock
   before bypassing that one hold. Wait for the wrapper's **terminal exit**.
   A new paid job, deploy drift, unexpected container replacement or watcher
   failure aborts A01. Do not use a second deploy entry point. A deploy
   failure leaves the old unfenced API stopped, with the same hold and nonce;
   there is no automatic old-code rollback. Treat the brief API outage as
   planned and visible.
6. After stock deploy exits, reacquire **all four locks** and verify the
   **original exact hold** (release directory, owner, creation time and raw
   hash) before trusting any API receipt. A lock conflict or changed hold is
   a stop; retain the nonce. Under these locks,
   repin the Compose API and Redis full IDs/images, API port owner, deployed
   SHA, exact DB row, active-media count, marker and host watcher. Pin the
   **new** running API full container ID/image and verify health, deployed
   SHA and UID 10001 marker read access. In that exact API container,
   run `python -m app.video_media.dispatch_fence_cli check --job-id
   b721a65d-8c8d-4ae8-834c-391cfc267a6f --expect-operator-lock`.
   This read-only held-mode receipt must show `enforced=true`, exact tuple,
   `active_media_count=1`, marker SHA, source hashes, and
   `media_lock_absent=false`; held mode **does not** verify nonce ownership.
   Separately `inspect` the private receipt through the helper, compare the
   nonce hash, and ensure the host watcher still observes the same Redis ID.
   If any check fails, keep the nonce and original hold; do not call A01.
7. **Keep the durable nonce.** Record the held-mode API receipt plus the
   private host nonce-ownership/readback receipt and exact hold identity/hash
   in the handoff. Release the four locks but **keep the same hold**, nonce,
   watcher and receipt through every A01 phase. The A01 R9 guard must first
   receive its separately reviewed hold-adoption change and then independently
   verify that same hold, held-mode CLI receipt, actual nonce/TTL, Redis ID,
   API ID/image and source hashes at each checkpoint. Until then A01 is
   blocked. No direct GET job poll is a substitute. Hold and nonce retirement
   need a separate owner-approved procedure; do not clear either as part of
   this cutover.

The CLI never calls `advance_job` or a vendor. `propose` prints the canonical
candidate JSON for the current DB row; `validate --manifest <file>` compares
a candidate read-only; `check` inspects the installed marker/DB/Redis lock.
Success exits 0, mismatch/marker/lock exits 3 with a reason, unavailable
DB/Redis exits 4. The **held-mode** check JSON fields are `schema_version=1`,
`enforced=true`, `fence_sha256`, `fence_path`, `media_lock_absent=false`,
`operator_lock_expected=true`, `active_media_count=1`, `job` with exact
`id/slug/request_hash/kind/provider/model/status/vendor_ref/submitted_at`, and
`code` with `jobs_sha256/dispatch_fence_sha256`. Held mode checks only Redis
key presence; the private receipt and host watcher separately prove nonce
ownership. A normal `check` requires absent lock and is **not** the A01
cutover receipt while the durable nonce remains.

**Stop and recovery:** On every failure, leave this cutover's one root hold in
place. If stock deploy was launched, wait for its terminal status and reacquire
all four locks before inspecting the exact hold, API, marker, nonce receipt and
watcher. Its `--no-rollback` setting prevents automatic restart of the old
unfenced API. The non-expiring exact Redis nonce remains through failed
new-code proof; neither a transient watcher failure nor a missing API receipt
authorizes deleting it. If a later separately approved recovery would run
pre-fence code, keep that API stopped until the same exact nonce is durably
proved against the pinned Redis DB and the continuous hold is verified. The
new compiled API still refuses this ID even if Redis fails, but A01 guard
waits for fresh held-mode and nonce-owner receipts. Do not delete a stuck key,
marker or hold to make a guard pass. Resolve the live state and charge
uncertainty under a separate owner-approved recovery plan.

Docker documents [indefinite `stop --timeout=-1`](https://docs.docker.com/reference/cli/docker/container/stop/)
and [manual stop with `unless-stopped`](https://docs.docker.com/engine/containers/start-containers-automatically/).
Redis documents the [same-connection `WAITAOF` acknowledgement](https://redis.io/docs/latest/commands/waitaof/).
These are protocol assumptions; action-time container and Redis behavior
must still be read back.
