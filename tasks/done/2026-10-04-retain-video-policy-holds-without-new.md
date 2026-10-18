---
id: 2026-10-04-retain-video-policy-holds-without-new
title: Retain deterministic video policy holds without creating new writer jobs
status: done
priority: P1
area: tools
owner: claude-opus-5-5-policy-holds
claimed_at: 2026-10-07T01:03:55Z
created_at: 2026-10-04T17:53:20Z
completed_at: 2026-10-07T01:05:23Z
branch: claude/sharp-bardeen-ob6fn9
depends_on:
  - 2026-10-03-video-worker-narration-takes-made-stale
  - 2026-09-30-video-worker-moves-two-videos-at
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Retain deterministic video policy holds without creating new writer jobs

## Why

At 2026-10-04 17:29-17:42 UTC, video-ai failed_job_count increased from
58 to 62. A bounded read-only reconciliation identifies all four new jobs as
ai-agent-travel-booking-instinct / writer, rejected with
video_ai_drama_disabled (409). Their database dispatched_at fields are null;
the worker log, raw failed registry and database UUIDs match exactly. Planned
Claude Code/Opus fields do not mean a model request occurred. These failures
are unrelated to Cloudflare/Grok language results or the bounded media repair.

The native client does not classify video_ai_drama_disabled as an owner hold.
durableRun.completed() removes every failed local receipt through
removeFailed(), which unlinks its journal. A later round can therefore prepare
a different request_key and submit another job under the unchanged policy.
This is a settled policy rejection, distinct from lost/uncertain paid answers,
translation checkpoint adoption and atomic producer exclusion.

## Definition of done

- [x] A deterministic drama-disabled writer result persists its original
      receipt, request_key, input/source identities and exact error across
      repeated rounds and process restarts. Unchanged policy causes zero new
      job POSTs and zero model dispatches.
- [x] The affected project reports its actual policy hold to the backend and
      is skipped until an authorized resume is validated. Failure to report
      cannot trigger a new writer job or starve other eligible videos.
- [x] Resume checks fresh source, owner/retry acknowledgement, selected policy
      and STOP/drop state; merely having an old retry or changing provider/model
      cannot bypass a still-disabled feature. Preserve previous receipts by
      archiving rather than deleting them when a resume is actually allowed.
- [x] Successful/pending/uncertain paid results retain their existing recovery
      and adoption contracts. No bulk conversion of unrelated failures to a
      retryable state and no fake source, approval or listening acceptance.
- [x] Keep drama, Shorts, uploader, budgets and provider settings unchanged.
      Validate and independently review before any production use.

## Steps

- [x] Recheck official main, branches, worktrees and active claims. Obtain the
      dependent flow owners' handoff before changing their scope; do not force
      claim, release their tasks or edit the frozen PR1210 recovery runtime.
- [x] Distinguish settled policy holds from a failure that permits a genuinely
      authorized new operation. Keep exact negative receipts durably bound.
- [x] Integrate a project-local hold/report/resume path and test it through
      the real native Automation/client, without live paid endpoints.

## How to verify

Use counting fetch with the actual native client and persisted work directory.
Return a complete failed writer receipt with video_ai_drama_disabled and null
dispatched_at, then repeat in the same process and after restart. Count job POSTs
and compare request keys and preserved bytes. Test a blocked-report transport
failure and another eligible project, stale retry acknowledgements, unchanged
disabled policy, source/settings drift, STOP/drop and an authorized later resume.
Include successful/pending/uncertain receipt regression cases. Run affected
client/receipt/Automation tests and the complete tools suite with compatible Node.

## Notes

Four exact database job IDs:

- bdb4e66c-d3c1-4294-95ee-8d1474beb202, failed at 17:31:36.492666Z.
- 16ed2b44-c693-479d-a5a2-ce82cc4edd71, failed at 17:33:10.612485Z.
- c466f471-b8d4-4c64-a57f-d3ff49d1f050, failed at 17:38:20.870598Z.
- 86d2a3ed-c732-40b3-9c0e-be00e0b51b97, failed at 17:40:28.616114Z.

Bounded deployed proof: temporary
mokaair-video-ai-failed-four-attribution-20261004-1742-compact.json,
8,943 bytes, SHA-256
0b59880b78475da43a3fd5b744ce2821297dbdedbc355f2af689c353aaff48bd.
Raw failed-registry proof SHA-256
172831d9909c6b817f2f0f287e7ac5636e796f45e62a42116a7e14239cb4b59c.
Registry scores are expiry timestamps; failure times come from the actual
ended_at fields and matching database rows. No job/status API, queue cleanup,
requeue, provider request, production write or feature activation was performed.

The existing native-language-durable-units-and-progress ticket concerns paid
translation/review checkpoint adoption and pending fairness. The existing
native-video-project-stop-and-producer-exclusion ticket concerns STOP and shared
mutation ownership. This ticket records the separate deterministic failed-job
lifecycle and its backend-visible project hold; coordinate their shared scopes.
It remains unclaimed while the dependent flow scopes are held.

An offline diagnostic also reproduced this through the actual native client
in two independent Node processes with identical synthetic source. Both complete
queued/failed wire pairs pass StageJobOut validation. The two processes issued
two mock job POSTs with different request keys, removed both failed receipts and
reported who=service. Real network/provider calls were zero. This is a failing
behavior reproduction, not a completed fix or production acceptance.
Temporary result mokaair-drama-off-writer-client-poc-20261004-result.json,
SHA-256 b0328276f972bfa194297d94c1808c2e8e2a1d862a04bb9d19bf2b0345ac64ee;
diagnostic script SHA-256
26508f27d2a78ca48de6efbe07694ad16f27feaf5cf2c40da9e166df787fb9d8.

### 2026-10-07 結案（claude-opus-5-5-policy-holds）

Implemented by PR #1274 (`af07dbc0`, 2026-10-05, "recover news/video stall handling"), which
never closed this ticket. No new code was needed; each box maps to a test on main:

- Receipt kept across rounds and restart, zero new POSTs: `run-receipts.mjs` `hold()` /
  `policy_rejection`, `removeFailed()` refuses a policy hold; client.test "a settled policy
  refusal survives repeated rounds and client restarts without another job POST" (both the
  failed-job and direct-409 shapes); automation.test "the native worker retains a disabled
  writer receipt, reports its hold and never dispatches or buys a second job across restart".
- Project-local hold, report failure does not buy a job or starve others: automation.test
  "a policy hold survives failed reporting and restart, while another project advances…".
- Resume guards (new owner request id, fresh enabled route or corrected format, STOP, source
  drift, drop, format mismatch; archive not delete): client.test "policy retry requires a fresh
  enabled route…", "a verified undispatched slides repair may resume…", "a mixed legacy set of
  policy holds cannot be partly archived…"; automation.test "policy retries respect project
  STOP, source drift and owner drops…", "an authorized policy retry sends the current source
  format once…"; run-receipts.test "settled policy refusals cannot be deleted or archived
  without fresh validated owner authority".
- Successful/pending/uncertain contracts unchanged: the rest of the three suites.

Run on main `b884e22e`: `node --test` over run-receipts, client and automation tests, 214 pass,
0 fail. Not verified from here: production `failed_job_count` no longer growing for
`video_ai_drama_disabled` writer jobs since #1274 was deployed (needs host access).
