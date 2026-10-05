---
id: 2026-10-05-speech-routes-lost-paid-answer
title: Speech routes answer a lost paid answer apart from an unreachable API
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5-speech-routes-lost-answer
claimed_at: 2026-10-05T07:20:47Z
created_at: 2026-10-05T00:38:51Z
completed_at:
branch: claude/speech-routes-lost-answer
depends_on: []
scope:
  - apps/web/app/api/video/speech/route.ts
  - apps/web/app/api/video/speech/transcribe/route.ts
  - apps/web/app/api/video/speech/judge/route.ts
  - apps/web/app/api/video/speech/route.test.ts
  - apps/web/app/api/video/speech/forward.ts
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# Speech routes answer a lost paid answer apart from an unreachable API

## Why

`apps/web/app/api/video/speech/forward.ts` answers 502 `upstream_unavailable` both when it could
not connect to the API (nothing ran) and when the API was reached but its answer never came back
(the 180 s deadline passed, or the connection dropped mid-way: the API may have synthesized and
been charged). `forwardToSpeech` already takes a `LostAnswer` for that second case, and
`automation/run/route.ts` passes one (`RUN_LOST`), but the three paid speech routes (`speech`,
`speech/transcribe`, `speech/judge`) pass none.

So `tools/video/tts/client.mjs` cannot tell the two apart and, since
2026-10-04-prevent-paid-speech-retries-after-ambiguous, treats a 502 `upstream_unavailable`
after a paid POST as uncertain (exit 3, a person reconciles). An API restart while the web
container is up therefore blocks the video for the owner (narration, a dub, its retake or its
check: `tools/video/automation/flow.mjs` blocks on `video_speech_uncertain`) where the request
could safely have been retried. A deploy that lands during a speech request does this.

## Definition of done

- [x] The three paid speech routes answer a lost answer with their own code (for example 504
  `video_speech_answer_lost`), and keep 502 `upstream_unavailable` for an API never reached.
- [ ] Once that is deployed, the client retries a paid POST's `upstream_unavailable` again and
  treats the new code as uncertain; a client that meets an older server stays safe.

## Steps

- [x] Add the `LostAnswer` to the three routes and route tests for a refused connection
  (502 upstream_unavailable) and a timed-out or dropped answer (the new code).
- [x] Decide the rollout: the owner's local CLI can be newer than the host, so the client side
  should only move `upstream_unavailable` into `SETTLED_CODES` after the web change is live
  (for example by a separate PR after the deploy).

## How to verify

From `apps/web`: `npx vitest run app/api/video/speech/route.test.ts --maxWorkers=2` and
`npx eslint app/api/video/speech`; from the root `npm run typecheck:web` and
`node --test tools/video/tts/client.test.mjs`.

## Notes

- Found while classifying the speech client's paid retries (2026-10-05). The automation
  client's `SETTLED_RUN_CODES` contains `upstream_unavailable` only because its route passes
  `RUN_LOST`; do not copy that into the speech client before this ticket lands.
- Done (claude-opus-5-5-speech-routes-lost-answer, 2026-10-05): `SPEECH_LOST` (504
  `video_speech_answer_lost`, a Chinese detail like the file's other problems) is defined once in
  `apps/web/app/api/video/speech/forward.ts` and passed by `speech`, `speech/transcribe` and
  `speech/judge`; `speech/status` (a GET, nothing billed) keeps the 502 for a lost answer.
  `forward.ts` was added to the scope for that one constant: a Next.js route file may export only
  its handlers and route config, so the constant cannot live in `speech/route.ts` and be imported
  by the other two, and three copies would drift. Every video route imports `forward.ts`; the
  change only adds an export, `forwardToSpeech` is untouched.
- Route tests (`route.test.ts`, 4 new): for each paid route, the 180 s deadline (fake timers:
  not aborted at 179,999 ms, 504 at 180,000 ms), a dropped connection (`UND_ERR_SOCKET`,
  `ECONNRESET`, `UND_ERR_HEADERS_TIMEOUT`) gives 504 `video_speech_answer_lost`; a connection
  never made (`ECONNREFUSED`, `ENOTFOUND`, `EAI_AGAIN`, `UND_ERR_CONNECT_TIMEOUT`) gives 502
  `upstream_unavailable`; the API's own 502 `video_speech_upstream_failed` passes through; the
  status GET still answers 502 for a dropped connection.
- Client: `tools/video/tts/client.mjs` already treats the new code as uncertain (a paid 5xx whose
  code is not in `SETTLED_CODES`), so no code-list change was needed. `client.test.mjs` now pins
  it ("the web route's lost answer", 504, sent once, `SPEECH_UNCERTAIN`), and the comment above
  `SETTLED_CODES` says why `upstream_unavailable` is not there yet.
- Rollout decided: the client moves `upstream_unavailable` into `SETTLED_CODES` in a separate
  change after this one is deployed, because the owner's CLI can be newer than the host and an
  older host answers that 502 for a lost answer too. That is the client half of the second
  Definition-of-done item, left unticked here and split to
  2026-10-05-speech-client-retries-paid-upstream-unavailable (it needs the deploy, which this
  change cannot do). That ticket also records an alternative that would not need the order.
- Windows note: under a loaded machine (CPU 100 %, 37 node processes) vitest's `threads` pool
  timed out starting its first worker ("Timeout waiting for worker to respond") for any single
  file; `--pool=forks` ran the same files fine.
