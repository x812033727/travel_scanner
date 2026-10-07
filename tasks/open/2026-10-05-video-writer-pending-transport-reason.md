---
id: 2026-10-05-video-writer-pending-transport-reason
title: Surface durable writer polling failures in pending status
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-pending-reason
claimed_at: 2026-10-07T15:36:10Z
created_at: 2026-10-05T13:02:39Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Surface durable writer polling failures in pending status

## Why

The durable writer client retains its request key and includes the last receipt
read error in RUN_PENDING.message. Automation drops that message and reports only
"writer is still running". A completed backend job whose GET receives HTTP 429
therefore looks like model execution is still running, hiding the actual
temporary transport throttle from the operator.

## Definition of done

- [x] A pending writer whose receipt read was rate-limited or unavailable reports
      that saved cause, without claiming the model is still executing.
- [x] A genuinely queued/running receipt still has a clear pending message.
- [x] Preserve the same request key, receipt, retry/STOP/drop/budget policy and
      current round/lane behavior; a diagnostic change must not create another run.

## Steps

- [x] Check current scopes/PRs and claim before editing the two automation paths.
- [x] Preserve the bounded client explanation in Automation's pending report.
- [x] Add a transport-failure control and an ordinary pending-receipt control.

## How to verify

Use the real durable client and Automation with fake network responses: a saved
receipt's GET returns 429, then a later round returns the source-bound succeeded
result. Assert the first report retains the polling cause, the same request is
later adopted, and only one POST/model operation occurs. Keep the ordinary
pending case and STOP/per-project isolation checks. Run focused automation tests
and task consistency checks before a PR.

## Notes

- Filed from read-only production diagnosis on deployed d7ae39a2b, 2026-10-05.
- Travel's backend job completed at 12:37:46 UTC. Existing access logs show worker
  GETs at 12:51:19-22 returned 429; the next main opportunity at 12:56:54.677
  returned 200. Its receipt then settled, saved source exactly matched the
  canonical persisted result, and original speech/audio/timeline remained valid.
  This was temporary shared VideoTool 120/min transport throttling, not a proven
  permanent receipt-recovery defect.
- Snapshot 08 and 09 contained identical worker log lines. Do not call such a
  snapshot a new worker pass without timestamp or line-delta evidence.
- An independent in-memory reproduction confirmed the current flow discards
  RUN_PENDING's cause. Existing lost-POST/restart-GET/bounded-poll checks pass 3/3.
  No message fix, limit change, paid retry or deployment is included in this filing.
- 2026-10-07 (claude-opus-5-5-pending-reason). The scope also takes `client.mjs` and
  `client.test.mjs` (neither bound by the duration receipt nor held by another task): half of the
  cause was there.
  - `client.mjs` `durableRun` kept `lastProblem` after a later look-up read the receipt, so the
    RUN_PENDING message could name a 429 though the job was last read as running. A receipt read
    now clears it. The RUN_PENDING error carries the failed look-up's cause as `why` (from the poll
    loop, and from `reconcileStale` when a stale run could not be looked up); a pending job the
    server read as queued or running carries none. The request key, the receipt and every
    retry, STOP, drop and budget path are unchanged: only the message's cause and the new field.
  - `flow.mjs` `stepOnce`: with `why`, the line is "<stage> has not answered yet: the worker's last
    request for its saved receipt failed (<why, at most 160 characters>); it is asked again next
    round", instead of "<stage> is still running"; without it, the line is as before.
  - Tests: `client.test.mjs` (every look-up rate-limited, a look-up rate-limited then read as
    running, a stale run that could not be looked up); `automation.test.mjs`, the ticket's case
    through the real durable client and Automation: running, then the job done and its look-ups
    429 (the line says why), then a later round takes the same job's answer, with one POST and
    the receipt settled. Mutations (the cause kept after a read, no `why` from the poll or the
    stale look-up, flow ignoring it) each fail a test.
