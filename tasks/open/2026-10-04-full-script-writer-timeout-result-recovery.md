---
id: 2026-10-04-full-script-writer-timeout-result-recovery
title: Recover full-script writer results after gateway timeout
status: in-progress
priority: P1
area: api
owner: codex-video-recovery-20261004
claimed_at: 2026-10-04T06:01:48Z
created_at: 2026-10-04T05:49:34Z
completed_at:
branch: codex/video-pipeline-recovery-20261004
depends_on: []
scope:
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/run_jobs.py
  - apps/api/tests/test_video_stage_jobs.py
  - apps/api/migrations/versions/0123_video_stage_jobs.py
  - apps/api/tests/test_migration_0123_video_stage_jobs.py
  - apps/web/app/api/video/automation/run/route.ts
  - apps/web/app/api/video/automation/run/jobs/route.ts
  - apps/web/app/api/video/automation/run/jobs/[id]/route.ts
  - apps/web/app/api/video/automation/run/jobs/route.test.ts
  - tools/video/automation/client.test.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/automation.test.mjs
  - docker-compose.prod.yml
  - docs/videos/AUTOMATION.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - tools/video/automation/client.mjs
  - tools/video/automation/flow.mjs
---

# Recover full-script writer results after gateway timeout

## Why

The production worker loses full-script writer responses at the 295-second web
relay deadline, although the subscription model successfully finishes on the
server several minutes later. The existing language-unit fix bounds translation
work but does not bound a whole-script writer call. A successful `video_ai_runs`
row records usage rather than recoverable response text, so owner retries can
repeat work while the video never receives a script.

Read-only production evidence on 2026-10-04 at approximately 05:46 UTC, live
repository HEAD `d038b035e3f4d78263c9d64bca791fa0ba18ee56`: five worker states were
blocked on `writer may have run on the server without its answer reaching the
worker (HTTP 504: no answer within the deadline)`.

## Definition of done

- [ ] A full-script writer that outlives the HTTP deadline can deliver its exact
      completed answer through a durable receipt/result or another bounded,
      resumable contract, without repeating the model request.
- [ ] Retry/reconnect checks the existing request identity and completed result
      before quota checks or a new model dispatch; authorization and input/source
      hashes prevent adoption of another video's or stale answer.
- [ ] An API/host crash after dispatch remains explicitly uncertain if execution
      cannot be proven; no automatic paid retries or fabricated recovery.
- [ ] The worker saves the recovered script, resumes fact checking and reports
      the current stage; `status=ok` alone never counts as worker delivery.

## Steps

- [ ] Freshly collision-check and claim the required API, migration, client and
      worker paths. Scope any selected migration and additional tests before edits.
- [ ] Choose a result-preserving contract for whole-script writing and review
      atomic dispatch, completion, polling and crash behavior independently.
- [ ] Add timeout, reconnect, concurrent submit, stale-input, authorization and
      uncertain-crash tests that prove one model operation and exact result reuse.
- [ ] Verify a source-bound completed script through the actual worker transport
      after the ordinary relay deadline, then check persisted downstream progress.

## Implementation notes

Implemented the additive receipt table, isolated RQ worker, bounded BFF submit/poll
routes and source-bound worker journal. Output adoption is tied to saved artifact
hashes before another lint correction starts. Independent review also covered
cross-day/shared-lexicon drift, exact late-result reuse before an owner retry, model
aliases, per-video STOP, dropped projects and settings changes before dispatch.
Focused client/store tests: 28 passed. Backend tests: 71 passed, 3 PostgreSQL-only
skipped; STOP checks: 5 passed. Real Automation transport fixtures recover a saved
writer after a simulated 650-second completion and calendar-day change, then
verify the script; an initial-script/lint-fix restart leaves no stale receipt.

No production deployment, paid retry, media enablement or upload was performed.
The five older lost synchronous answers were never persisted and cannot be
recovered by the new table; they still require an explicit owner retry decision.

Collision audit: the only open PR was #1201 (unrelated news publication); the
older overlapping video claims already landed through #978, #962, #999, #1172
and #1182. Their relevant worktrees had no edits in these paths. The three
recovery tickets share this branch/owner; forced claims bypassed stale board
scopes after this check, without changing another owner's task.

## How to verify

Run focused API/job and worker client/automation tests, then required API/web/tool
checks. Simulate a writer completing after 295 seconds and a disconnected caller;
resume must fetch the exact retained result with a single upstream model run.
Production recovery requires its own authorized operation and current hashes.

## Notes

- Affected states: `cloudflare-auto-router-who-measured-savings`,
  `cloudflare-workers-per-worker-permissions-ai-agent`,
  `threads-parental-supervision-apac-four-settings`, `ai-term-temperature`,
  `ai-term-knowledge-cutoff`.
- Recent successful calls in `video_ai_runs` for the first three took 530033,
  461253 and 642180 ms respectively. Other attempts took 579073 and 665707 ms.
  These are server completion/usage records, not recoverable script delivery.
- `apps/web/app/api/video/automation/run/route.ts` keeps `RUN_TIMEOUT_MS=295000`;
  raising it alone does not resolve both fetch-header and public proxy limits.
- `apps/api/app/video_automation/ai.py` commits usage/error metadata, then returns
  answer text without retaining it. The currently lost answers cannot be
  retrospectively recovered from that usage table.
- `2026-09-29-prevent-lost-long-running-language-stages` is complete for bounded
  language units and uncertain-result protection. This is a distinct remaining
  whole-script result-recovery gap, not a reversal of that completed fix.
- `2026-10-02-stop-repeating-lost-stage-answers-outside` covers other callers'
  repeated uncertain operations; coordinate rather than duplicate that scope.
- Filed open/unclaimed from diagnosis. No production setting, service, model call,
  owner approval, upload or publication was changed or retried in this audit.
