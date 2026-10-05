---
id: 2026-10-05-speech-routes-lost-paid-answer
title: Speech routes answer a lost paid answer apart from an unreachable API
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-10-05T00:38:51Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/api/video/speech/route.ts
  - apps/web/app/api/video/speech/transcribe/route.ts
  - apps/web/app/api/video/speech/judge/route.ts
  - apps/web/app/api/video/speech/route.test.ts
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

- [ ] The three paid speech routes answer a lost answer with their own code (for example 504
  `video_speech_answer_lost`), and keep 502 `upstream_unavailable` for an API never reached.
- [ ] Once that is deployed, the client retries a paid POST's `upstream_unavailable` again and
  treats the new code as uncertain; a client that meets an older server stays safe.

## Steps

- [ ] Add the `LostAnswer` to the three routes and route tests for a refused connection
  (502 upstream_unavailable) and a timed-out or dropped answer (the new code).
- [ ] Decide the rollout: the owner's local CLI can be newer than the host, so the client side
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
