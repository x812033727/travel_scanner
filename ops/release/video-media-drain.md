# Host-only API media drain candidate

**Status: offline candidate; production installation and deployment HOLD.** This
is an incremental guard for the one-shot `/root/deploy-travel-scanner.sh` after
#1527's video AI stage guard. It has not been installed or run on production.
Auto-deploy calls the same host script if its timer is enabled; staged release
drivers and the optional deployment-agent path need their own review.

## Why a second guard is needed

`apps/api/app/video_media/jobs.py` commits `status='queued'` before calling a
generation vendor from an API request. A queued row can therefore mean a paid
call is running. A GET of that same row can also dispatch it later. Its Redis
job lock expires after 240 seconds while configured submit/fetch timeouts may
reach 280 seconds; absence of the lock or `vendor_ref` is not no-charge proof.
Media judge and locate calls have no media-job row at all. A check at the
beginning of a deployment cannot cover a request admitted during the build.

The exact live queued row at 2026-10-16 08:26 UTC was
`b721a65d-8c8d-4ae8-834c-391cfc267a6f`: non-pilot Suncatcher `h-planet`
keyframe, MiniMax `image-01`, queued since 2026-10-12 04:17:49 UTC, one
attempt, zero polls, no vendor_ref/idempotency/receipt and no Redis media
lock at that read. The old HTTP process is gone; a later GET could dispatch.
Task `2026-10-16-reconcile-suncatcher-queued-media-job-before` owns its
read-only investigation and later owner-approved disposition. This guard
refuses it; it does not change, delete or retry it.

## Order and failure behavior

Under the existing deploy flock, the incrementally patched script performs:

1. After checkout update, `video_media_drain.sh --precheck` reads queued
   count and media Redis locks, checks exactly one running API with the reviewed
   Uvicorn command and reviewed 0.52.4, one-worker, auto-lifespan, unbounded
   graceful-shutdown settings. It also requires a readable `json-file` Docker
   log before stopping the API. Any refusal
   restores the old checkout without stopping the API. The known queued row
   therefore blocks with the public site still served.
2. `compose build` prepares the target images while old containers keep
   running. A build failure restores the checkout before any managed stop.
3. #1527 warmly drains `video-ai-worker`; the media helper immediately
   rechecks queued jobs/locks and then sends **one** `SIGTERM` to the API with
   `docker container stop --timeout=-1`. Uvicorn stops admitting new requests
   and waits for its accepted HTTP tasks to finish. Docker cannot escalate to
   SIGKILL by a default deadline. A pending marker is created before the
   signal and survives an error or interrupted deploy shell.
4. Uvicorn 0.52.4 re-raises SIGTERM after its graceful shutdown, so the helper
   requires exit 143 with no OOM **and** the exact `Application shutdown
   complete.` and `Finished server process [1]` log lines, in that order,
   from the same container after the recorded nanosecond stop timestamp. It
   retries read-only log inspection for up to four seconds to allow log flush;
   missing or unreadable completion evidence retains the pending marker. It
   then reads queued jobs and Redis locks again. A new queued request arriving
   after either earlier check is thus either durably resolved during graceful
   shutdown or causes a hard refusal. A clean normal drain writes an
   exact-deployment nonce/SHA/container receipt.
5. `compose up --no-build -d` uses the already built images. Rollback rebuilds
   the original checkout before either guarded rollback stop, then drains
   the AI worker and API again. A zero API container is accepted only for a
   rollback with the successful normal drain receipt from the same deployment.

A post-signal refusal, including a late/missing Docker completion log, can
leave the API stopped and the website unhealthy.
That is deliberate fail-closed behavior when the outcome of a paid request
cannot be established. The script must not automatically restart or send a
second TERM. Inspect the marker, exact container and API logs, queued row,
Redis locks, worker run, vendor and budget receipts; obtain an owner-approved
resolution before clearing the marker or restoring the service. An external
watchdog must not use `docker kill`, `compose up` or `--ignore-hold` as a timeout
recovery. A hung HTTP request causes an indefinite wait rather than a forced
kill; operators may investigate without interrupting that connection.

The API currently runs `uvicorn app.main:app --host 0.0.0.0 --port 8000`,
Uvicorn 0.52.4. The pinned local source has
`timeout_graceful_shutdown=None`, one worker and auto lifespan. Its SIGTERM
path closes listeners and waits for existing tasks before logging lifespan
and server completion, then re-raises the signal. The helper refuses changed
command/version/settings or unreadable logs before stopping the API.
`--timeout=-1` is passed explicitly to Docker.

## Other deployment holds

This is **only an API media request guard**. Compose also recreates the
shell/Node `video-worker`. Its PID 1 shell traps TERM by exiting 143 while a
foreground `auto` run and Shorts knock may still have paid speech, media,
review or other vendor units. STOP checks are cooperative and its Compose
service has no stop grace period. Check exact LEASE, STOP, run, receipt and
paid-call state, and solve task
`2026-10-16-warm-drain-video-worker-paid-units` before any paid-video
deployment. A clean API media drain alone does not authorize one. Manual
`docker compose run`, direct API processes and the separately implemented
staged/deployment-agent paths are not covered by the host-only helper.

## Install and verification boundary

`video_media_host_patch.py` accepts only the already patched #1527 host
script and the independently reviewed #1527 helper SHA
`6ea459ddb128fecb4a90ff1d0028046b8d477a58454f25d37286ea045284e2a5`.
It also pins the new media helper's SHA-256
`12aebe004394b7aa756f67e0d778296311e8c2bf1d44f91abb45a9f94149bf29`
before installation. It requires
the host script's fresh exact SHA-256 and mode 0700,
takes the deploy flock, saves a byte-identical backup, checks both shell files
with `bash -n`, installs the media helper and patched script atomically, then
reads back. A failed install restores the exact original script under the
same lock. The #1527 host installation must finish and be read back first;
never run both installers concurrently. A script drift requires a new review.

No local test is a live authorization. Before installation or deployment,
obtain the owner's explicit approval for exact reviewed bytes and the
co-deployed main SHA, recheck current host hold/locks/timer/worker/DB and
backup state, and reconcile the queued Suncatcher job. A deployment must
also pass the independent `video-worker` paid-unit gate and post-deploy
readback. The task and PR remain draft while those conditions are unmet.

Offline checks: `bash -n ops/release/video_media_drain.sh`, `python3 -m
unittest discover -s ops/release -p test_video_media_drain.py -v` on Linux,
`python -m unittest discover -s ops/release -p test_video_stage_drain.py -v`,
Ruff, `npm run check:tasks`, and a synthetic two-anchor render comparison.
