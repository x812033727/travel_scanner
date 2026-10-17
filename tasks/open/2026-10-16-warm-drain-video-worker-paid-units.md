---
id: 2026-10-16-warm-drain-video-worker-paid-units
title: Warm-drain video worker paid units before container recreation
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-16T08:27:37Z
completed_at:
branch:
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
