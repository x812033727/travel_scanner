---
id: 2026-10-05-video-writer-pending-transport-reason
title: Surface durable writer polling failures in pending status
status: done
priority: P2
area: tools
owner: claude-opus-5-5-writer-pending
claimed_at: 2026-10-07T06:32:04Z
created_at: 2026-10-05T13:02:39Z
completed_at: 2026-10-07T06:36:41Z
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

### 2026-10-07 done (claude-opus-5-5-writer-pending)

- `client.mjs`: the RUN_PENDING error now carries `polling` (why the last look at the server
  failed: the lookup's 429 detail, a dropped connection, a body cut short) and `receipt_status`
  (what the server last said, null when no job was confirmed). A successful read clears
  `polling`: before, `lastProblem` was kept after a later read said "running", so the message
  could name a 429 the server had since answered. The stale-journal lookup carries its cause the
  same way. The message text is unchanged.
- `flow.mjs` `pendingLine()`: "writer is still running" only when the server last said so;
  "writer's saved run could not be looked up (<cause>); its receipt is checked again next round"
  when the receipt read failed; "writer's request was not confirmed by the server (<cause>); it is
  sent again under the same key next round, which the server takes as the same run" when no job
  was confirmed. The request key, receipt, PENDING_RECHECK_MS wait, STOP, budget and lane
  handling are untouched; only the line changes.
- Tests: `automation.test.mjs` "a writer whose saved receipt cannot be read says why…" (the real
  durable client over the durableJobs fake: running, then finished but every GET 429, then read:
  the same job adopted, one POST; and a POST refused until the next round: one job under one
  key). `client.test.mjs` "a pending writer says why its last look failed, only while it did"
  (a 429 then a running read clears it; an unconfirmed POST has no receipt status). Each fails
  with its piece removed. `node --test "tools/video/automation/*.test.mjs"` 446 pass.
- Left as it is: the owner's retry (`retryRuns`) turns a failed lookup, a 429 included, into
  RUN_UNCERTAIN "could not verify the saved run before owner retry", so a rate limit during the
  owner's retry blocks the video again and the owner retries once more. That is the retry path's
  own policy (it consumes the retry request on anything it cannot verify), not this ticket's.
