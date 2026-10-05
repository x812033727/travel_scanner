---
id: 2026-10-05-let-the-judge-routes-tell-a
title: Let the judge routes tell a lost answer from an API they never reached
status: in-progress
priority: P3
area: web
owner: claude-opus-5-5-judge-routes-lost-answer
claimed_at: 2026-10-05T12:27:02Z
created_at: 2026-10-05T00:44:31Z
completed_at:
branch: claude/judge-routes-lost-answer
depends_on: []
scope:
  - apps/web/app/api/video/automation/judge/policy/route.ts
  - apps/web/app/api/video/automation/judge/outline/route.ts
  - apps/web/app/api/video/automation/judge/route.test.ts
  - apps/web/app/api/video/speech/forward.ts
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

- [x] A judge route answers a distinct lost-answer problem (status and code) when its request
  reached the API and no answer came back, and keeps 502 `upstream_unavailable` for an API it
  never reached.
- [ ] The automation client retries a judge's 502 `upstream_unavailable` again, and still treats
  the new lost-answer code as uncertain: at most one paid judge POST per call.

## Steps

- [x] Pass a `LostAnswer` to `forwardToSpeech` in both judge routes; extend
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
- Done (claude-opus-5-5-judge-routes-lost-answer, 2026-10-05): `JUDGE_LOST` (504
  `video_judge_answer_lost`, a Chinese detail like the file's other problems) is defined once in
  `apps/web/app/api/video/speech/forward.ts` beside `SPEECH_LOST` and passed by
  `automation/judge/policy` and `automation/judge/outline`. `forward.ts` was added to the scope for
  that one constant, for the same reason as 2026-10-05-speech-routes-lost-paid-answer: a Next.js
  route file may export only its handlers and route config, so the constant cannot live in one
  judge route and be imported by the other, and two copies would drift. The change only adds an
  export; `forwardToSpeech` is untouched.
- Route tests (`judge/route.test.ts`, 4 new, both routes each): the 180 s deadline (fake timers:
  not aborted at 179,999 ms, 504 at 180,000 ms) and a dropped connection (`UND_ERR_SOCKET`,
  `ECONNRESET`, `UND_ERR_HEADERS_TIMEOUT`) give 504 `video_judge_answer_lost`; a connection never
  made (`ECONNREFUSED`, `ENOTFOUND`, `EAI_AGAIN`, `UND_ERR_CONNECT_TIMEOUT`) gives 502
  `upstream_unavailable`; the API's own 502 `video_judge_upstream_failed` passes through. With the
  outline route's `JUDGE_LOST` removed, the two 504 tests fail (checked).
- Client: `tools/video/automation/client.mjs` already treats the new code as uncertain (a paid 5xx
  whose code is not in `SETTLED_JUDGE_CODES`), so no code-list change was needed for that half.
  `client.test.mjs` now pins it ("the judge route's lost answer", 504, one POST, `RUN_UNCERTAIN`),
  and the comment above `SETTLED_JUDGE_CODES` says why `upstream_unavailable` is not there yet.
- Not done here, split to 2026-10-05-automation-client-retries-a-judge-s: the second step (move
  `upstream_unavailable` into `SETTLED_JUDGE_CODES`, flip "the judge route's 502" to retried) and
  the third (deploy first), i.e. the retry half of the second Definition-of-done item. It needs
  this change live on the production host before it merges. On the host one deploy would ship both
  in order (`up --build -d` builds every image before it recreates any container, and
  `video-worker` `depends_on: web`), but the judge callers also run from local checkouts against
  mokaair.com (`tools/video/qa/cli.mjs`, `tools/video/review/sync.mjs`), and a checkout of a merged
  main that the host has not deployed yet would retry an old route's ambiguous 502. Same rollout as
  the speech routes (2026-10-05-speech-client-retries-paid-upstream-unavailable).
- Codex draft PR #1254 (API) makes the judge endpoints answer 502 `video_judge_outcome_uncertain`
  for a Jev answer that may have been processed; the routes pass the API's own 5xx through
  untouched and the client treats that code as uncertain (not in `SETTLED_JUDGE_CODES`), so the
  two changes do not interact. Nothing under `apps/api` was touched.
- Windows note: with the machine at 100 % CPU (80 node processes), vitest's worker start timed
  out ("Timeout waiting for worker to respond", threads and forks at `--maxWorkers=2`);
  `--maxWorkers=1 --pool=forks` ran fine. The linked node_modules came from a checkout one
  Dependabot bump behind (#1252: next 16.3.7, vitest 5.0.2); CI runs the exact lockfile.
