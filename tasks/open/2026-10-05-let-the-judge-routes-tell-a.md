---
id: 2026-10-05-let-the-judge-routes-tell-a
title: Let the judge routes tell a lost answer from an API they never reached
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-05T00:44:31Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/api/video/automation/judge/policy/route.ts
  - apps/web/app/api/video/automation/judge/outline/route.ts
  - apps/web/app/api/video/automation/judge/route.test.ts
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Let the judge routes tell a lost answer from an API they never reached

## Why

The web routes for Jev's judgements (`apps/web/app/api/video/automation/judge/policy/route.ts` and
`.../outline/route.ts`) call `forwardToSpeech` without a `lost` answer. So when the route took the
worker's request, reached the API and then lost the answer (its 180 s deadline passed, or the API
dropped the connection mid-way), it answers the same 502 `upstream_unavailable` as for an API it
never reached.

The API takes one call off the daily Jev budget before it asks Jev, so the automation client now
treats that ambiguous 502 from a judge route as uncertain (`RUN_UNCERTAIN`) and does not send the
judgement again (2026-10-04-prevent-automatic-retries-of-paid-video). That is the safe reading,
but it also gives up the immediate retry when the API container is only restarting and nothing
was sent: the QA's `policy` item fails, or the outline waits, until the next worker round.

The stage-run route already separates the two cases (`RUN_LOST` in
`apps/web/app/api/video/automation/run/route.ts`).

## Definition of done

- [ ] A judge route answers a distinct lost-answer problem (status and code) when its request
  reached the API and no answer came back, and keeps 502 `upstream_unavailable` for an API it
  never reached.
- [ ] The automation client retries a judge's 502 `upstream_unavailable` again, and still treats
  the new lost-answer code as uncertain: at most one paid judge POST per call.

## Steps

- [ ] Pass a `LostAnswer` to `forwardToSpeech` in both judge routes; extend
  `apps/web/app/api/video/automation/judge/route.test.ts` for a dropped and a never-connected
  upstream.
- [ ] Add `upstream_unavailable` to `SETTLED_JUDGE_CODES` in `tools/video/automation/client.mjs`,
  and change the "the judge route's 502" case in `client.test.mjs` from uncertain to retried, with
  a new case for the lost-answer code.
- [ ] Deploy the web change before the client change, or a client from after it would retry an
  old route's ambiguous 502.

## How to verify

From `apps/web`: `npx vitest run app/api/video/automation/judge/route.test.ts --maxWorkers=2`.
From the root: `node --test tools/video/automation/client.test.mjs tools/video/qa/qa.test.mjs tools/video/review/sync.test.mjs`.
Fake transports only.

## Notes

- Filed from 2026-10-04-prevent-automatic-retries-of-paid-video. Low priority: the judge callers
  (`tools/video/review/sync.mjs`, `tools/video/qa/cli.mjs`) already leave an uncertain judgement
  for the next round, so this only shortens the wait after an API restart.
- The order matters (third step): the client change alone would bring back the blind retry.
