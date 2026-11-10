---
id: 2026-10-16-reconcile-suncatcher-queued-media-job-before
title: Reconcile Suncatcher queued media job before deployment
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-16T08:33:05Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/recovery/2026-10-16-suncatcher-queued-media.md
---

# Reconcile Suncatcher queued media job before deployment

## Why

The 2026-10-16 read-only production snapshot found exactly one queued media
job, `b721a65d-8c8d-4ae8-834c-391cfc267a6f`, for the non-pilot video
`google-project-suncatcher-prototype-what-it-tests`: image/keyframe
`h-planet`, MiniMax `image-01`, created 2026-10-12 04:17:49 UTC. It has one
attempt, zero polls, no vendor reference, idempotency key, pilot budget
operation or media receipt; its Redis media lock was absent at 08:26 UTC.
The old HTTP process is gone, but a later GET can dispatch this queued job.
That status is an unknown outcome, not evidence that the vendor was never
called. The media deployment barrier must refuse it without site downtime.

## Definition of done

- [ ] Preserve the exact DB/job and workdir history; obtain independent
      provider/account evidence for whether the 2026-10-12 request was sent,
      charged or produced an asset.
- [ ] Prepare an exact, limited owner decision for the one row. Apply only the
      authorized reconciliation path, then read back DB, budget, audit, workdir
      and provider receipts; never auto-clear or resend to pass deployment.

## Steps

- [ ] Recheck this ID and hash-bearing request fields, API logs, worker run,
      Redis history if retained and vendor history with read-only access.
- [ ] Independently review a no-charge release, billable settlement or
      unresolved hold proposal with exact evidence; seek owner authorization
      for any production write or repeat paid request.
- [ ] Record result in the scoped recovery document and verify no unrelated
      job, A01 budget or paid work changed.

## How to verify

Compare exact before/after job ID, request hash, status, attempts, polls,
vendor_ref and provider statement; report the matching audit/budget operation
or continued hold. A vanished Redis lock is insufficient proof.

## Notes

Filed from the media deploy-barrier investigation. No production mutation,
poll, deletion or vendor call was made. This ticket is independent of A01.
