---
id: 2026-10-16-warm-drain-video-worker-paid-units
title: Warm-drain video worker paid units before container recreation
status: in-progress
priority: P1
area: ops
owner: codex-video-worker-warm-drain
claimed_at: 2026-10-16T09:00:37Z
created_at: 2026-10-16T08:27:37Z
completed_at:
branch: codex/video-worker-warm-drain-20261016
depends_on: []
scope:
  - ops/video/worker.sh
  - ops/release/video_worker_drain.sh
  - ops/release/test_video_worker_drain.py
  - docs/videos/AUTOMATION.md
---

# Warm-drain video worker paid units before container recreation

## Why

Compose recreates the `video-worker` on every deployment. Its PID 1 is
`ops/video/worker.sh`, a shell loop whose `TERM` trap exits 143 while the
foreground `node tools/video/cli.mjs auto` may be making paid speech, media,
review, or other vendor calls. The Compose service has no grace period and the
worker's STOP is cooperative between units. Draining the separate RQ
`video-ai-worker` (#1527) and gracefully shutting down the API media requests
do not prove this worker's current unit or external result was preserved.

## Definition of done

- [ ] Every deployment path that recreates `video-worker` waits for its current
      paid unit to reach a durable result, or refuses the deployment with an
      unresolved exact run/receipt instead of terminating the unit.
- [ ] A bounded, reviewable restart or owner recovery exists for a failed
      drain; existing media/voice takes and LEASE data are preserved.
- [ ] Production verification compares exact pre/post LEASE, STOP, run,
      vendor and paid-operation receipts without resending an unknown call.

## Steps

- [ ] Inventory each worker paid route and current termination behavior,
      including child Node processes, Shorts knock and manual `exec` sessions.
- [ ] Design a worker-admission stop and warm shutdown across normal and
      rollback Compose replacement, with a crash-persistent hold.
- [ ] Test arrival after preflight, STOP during a paid call, stranded LEASE,
      failed/interrupted drain, rollback and unrelated queued work.
- [ ] Independently review and request separate owner authorization before
      host installation or any production deployment.

## How to verify

Focused process/signal and paid-call mock tests, plus a read-only production
before/after comparison of exact worker container, workdir STOP/LEASE, current
`auto` run, media and speech operation IDs and provider receipts. A green API
media drain alone cannot satisfy this ticket.

## Notes

Filed during the 2026-10-16 media deployment-barrier review. No worker signal,
STOP, LEASE, paid call, host deployment script or production row has been
changed. Until this ticket is solved, overall paid-video deployment is HOLD
even if `video_media_jobs.queued=0` and the API graceful drain passes.

2026-10-16 candidate on `codex/video-worker-warm-drain-20261016`: added a
container-specific `DEPLOY_DRAIN.ready` protocol to `ops/video/worker.sh` and a
host-only helper that refuses legacy images, records a persistent pending marker,
waits for both `auto` and Shorts, rejects active manual exec/unknown processes,
and refuses missing-worker rollback. STOP and media files are preserved; no
production command has run. Independent core review found two safety gaps:
header-only/extra-process `docker top` was accepted, and a manual Shorts
`tick` ignored STOP. This branch now requires a PID tree rooted at the
container's inspected init PID and rejects Shorts tick before POST under
shared STOP/DEPLOY_DRAIN. Their new negative tests are offline only.

The candidate remains **HOLD / not installable**. General
`tools/video/cli.mjs` admission is unimplemented because active tasks
`2026-10-12-play-the-channel-intro-bumper-after` (review) and
`2026-10-14-enforce-usd-25-all-in-cap` (in progress), plus open PR #1454,
touch that file. A manual raw `docker exec` can begin between the helper's
ExecIDs/PID/ready snapshot and TERM; no enforceable host-level freeze exists.
The #1527/#1529 host-only installer anchors have not been patched. The live
old worker lacks protocol 1, so its first upgrade needs a separate reviewed
maintenance path. An isolated Docker/tini smoke must validate the actual
init/PID tree and exit-143 semantics before host installation. Linux CI is
now wired to run the seven fake-Docker/process cases, but results are pending;
Windows unittest skipped them, and local WSL CreateVm timed out. No host
write, worker signal, paid call, merge or deployment has occurred.

Offline host integration plan is tracked in
`2026-10-16-install-video-worker-drain-host-anchors`: only after #1527 then
#1529 installers are reviewed and installed, pin their exact rendered host
script and helper hashes. Insert this helper's `--precheck` before image
prebuild, `--normal` after stage and API media guards have drained but before
normal `compose up --no-build -d`, and `--rollback` after rollback prebuild
and both existing rollback guards but before rollback compose up. Both
anchors must share the deployment nonce, original SHA and receipt path;
unknown anchor counts or changed bytes refuse. This remains a plan, not an
installer or authorization to deploy.
