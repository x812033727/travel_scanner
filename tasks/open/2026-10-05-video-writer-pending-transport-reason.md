---
id: 2026-10-05-video-writer-pending-transport-reason
title: Surface durable writer polling failures in pending status
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T13:02:39Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Surface durable writer polling failures in pending status

## Why

The durable writer client retains its request key and includes the last receipt
read error in RUN_PENDING.message. Automation drops that message and reports only
"writer is still running". A completed backend job whose GET receives HTTP 429
therefore looks like model execution is still running, hiding the actual
temporary transport throttle from the operator.

## Definition of done

- [ ] A pending writer whose receipt read was rate-limited or unavailable reports
      that saved cause, without claiming the model is still executing.
- [ ] A genuinely queued/running receipt still has a clear pending message.
- [ ] Preserve the same request key, receipt, retry/STOP/drop/budget policy and
      current round/lane behavior; a diagnostic change must not create another run.

## Steps

- [ ] Check current scopes/PRs and claim before editing the two automation paths.
- [ ] Preserve the bounded client explanation in Automation's pending report.
- [ ] Add a transport-failure control and an ordinary pending-receipt control.

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
