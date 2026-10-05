---
id: 2026-10-04-prevent-automatic-retries-of-paid-video
title: Prevent automatic retries of paid video judge requests
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-automation-judge-paid-retries
claimed_at: 2026-10-05T00:13:32Z
created_at: 2026-10-04T16:08:05Z
completed_at:
branch: claude/automation-judge-paid-retries
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/qa/qa.test.mjs
---

# Prevent automatic retries of paid video judge requests

## Why

The automation client's model runs distinguish an uncertain paid outcome from a request that never reached the server. Its judgePolicy and judgeOutline methods call the same request helper without the paid flag, so thrown fetch errors and general 5xx answers can trigger another paid judge POST. The policy and outline endpoints consume one Jev call before asking the provider. Losing an answer can therefore consume the quota again. This is a source finding, not evidence of an observed duplicate charge.

## Definition of done

- [x] Policy and outline judge calls are never blindly resubmitted after an ambiguous transport or response-body failure.
- [x] Definitive never-sent and server-settled failures retain bounded recovery, and read-only GETs remain retryable.
- [x] Any persisted or reused answer stays bound to the exact request, current stance and applicable question set; a failed verdict is preserved unchanged.

## Steps

- [x] Audit every cost-bearing automation method and its request flags, including response-body failures and gateway errors.
- [x] Add uncertainty handling or source-bound reconciliation without changing models, budgets, approvals or global settings.
- [x] Add fake lost-after-send and lost-response-body tests proving at most one paid POST for an uncertain input, plus safe-recovery controls.

## How to verify

Run `node --test tools/video/automation/client.test.mjs` and relevant QA caller tests. Use fake transports; do not reproduce an ambiguous outcome against a paid provider. Assert that the judge methods retain the original returned answer and that an unknown outcome cannot be retried by the same caller.

## Notes

- `tools/video/automation/client.mjs:87` defaults request paid=false; judgePolicy at267 and judgeOutline at274 omit that option. The protections for model stage runs do not establish protection for these judge methods.
- `apps/api/app/video_automation/judge.py:571-588` consumes the Jev quota before asking; judge_policy at628-653 and judge_outline at592-605 use that path.
- The separate paid speech ticket covers `tools/video/tts/client.mjs`, a different transport. Keep these fixes independently scoped.
- During this LLM continuation, only private normal-CLI transport guards are being prepared. Shared automation code is unchanged; no duplicate quota consumption is claimed.
- 2026-10-05 (claude-opus-5-5-automation-judge-paid-retries): `judgePolicy` and `judgeOutline` now
  call `request(..., JUDGE)`: `paid: true` with a judge-only settled set. A thrown fetch error that is
  not a never-sent connection code, a 200 whose body cannot be read, and any 5xx outside the set
  throw `RUN_UNCERTAIN` (who `service`, message "Jev may have run, so it is not sent again") after
  exactly one POST and no sleep. The callers already handle it: `review/sync.mjs judgeOutline` returns
  `later`, and `qa/cli.mjs policyItem` fails the item with exit 4 (external).
- The settled set for judges is only `video_judge_upstream_failed`, the API's own 502 once its Jev
  call failed. The triage plan assumed the stage-run set already covered it; it does not
  (`video_ai_upstream_failed` is a different code). The stage-run set's `upstream_unavailable` is
  deliberately left out: the judge web routes pass no `lost` answer to `forwardToSpeech`, so their
  502 `upstream_unavailable` also follows a request the API took and lost. Follow-up
  2026-10-05-let-the-judge-routes-tell-a gives the routes a lost-answer code so that 502 can be
  retried again. 429s (`rate_limit_exceeded`, `jev_budget_exhausted`) and the never-sent codes keep
  their bounded retries. Stage runs keep `SETTLED_RUN_CODES` and their message unchanged; the
  existing stage-run tests now also pin "the model may have run".
- Audit of the other client methods (step 1): only `run` (stage runs, already `paid`, writer runs
  durable) and the two judges reach a paid model or Jev call. Every other POST/PUT (`report`,
  `submit`, drama-request start/done, series docs/episodes/recap/done, `messageAnswer`, compilation
  start/done, the Shorts plan/topics/report/start/done) is a database write in
  `apps/api/app/video_automation/admin_api.py`, `video_reviews/admin_api.py` or
  `video_shorts/admin_automation_api.py` with no provider call, and every GET stays retryable. The
  new client tests pin a GET `reviews` after a 500 and a `submit` after a dropped connection.
- DoD 3: the client persists and reuses no judge answer; it returns the JSON exactly as the site
  sent it. The tests compare a failed verdict (`passed: false`) for each judge with `deepEqual`
  after a retried never-sent or settled failure, and check that the retry sends the same body.
- "Cannot be retried by the same caller": within one call, the loop never sends the POST again.
  Across worker rounds, `flow.mjs submitOutline` and the QA ask again next round; that per-round,
  per-path state is the second DoD item of 2026-10-02-stop-repeating-lost-stage-answers-outside
  (receipt-bound files, not done here).
- Scope: added `tools/video/qa/qa.test.mjs`. Its "judge being unreachable" case threw a bare
  `TypeError("fetch failed")` with no `cause`, which the paid path rightly reads as possibly sent.
  It now throws a never-sent ECONNREFUSED (still "cannot reach …"), and a new case checks that a
  dropped connection (UND_ERR_SOCKET) sends one judge POST and fails the item. That file is bound to
  `docs/videos/long-form/review.json`, so `cli.mjs check` lists it as stale until an independent
  reviewer adds an increment.
- Not changed here: `tools/video/shorts/site.mjs` has its own unprotected `judgePolicy` (follow-up
  2026-10-05-stop-the-shorts-client-from-resending). Jev's own internal retry loop inside one API
  call is 2026-10-04-jev-provider-uncertain-retries; if that work makes an uncertain Jev outcome a
  `JevError`, `admin_api.py` should answer it with its own code, not `video_judge_upstream_failed`,
  or this client would still retry it as settled.
