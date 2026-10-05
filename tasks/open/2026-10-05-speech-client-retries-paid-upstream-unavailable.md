---
id: 2026-10-05-speech-client-retries-paid-upstream-unavailable
title: Speech client retries a paid upstream_unavailable once the lost-answer routes are live
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T07:42:22Z
completed_at:
branch:
depends_on:
  - 2026-10-05-speech-routes-lost-paid-answer
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - docs/videos/imported-long-languages/speech-journal.test.mjs
---

# Speech client retries a paid upstream_unavailable once the lost-answer routes are live

## Why

Since 2026-10-05-speech-routes-lost-paid-answer, the three paid speech routes
(`apps/web/app/api/video/speech/route.ts`, `.../transcribe/route.ts`, `.../judge/route.ts`) answer
504 `video_speech_answer_lost` when the API took the request and its answer never came back (the
180 s deadline passed, or the connection dropped mid-way), and keep 502 `upstream_unavailable`
for an API they never reached (`SPEECH_LOST` in `apps/web/app/api/video/speech/forward.ts`).

`tools/video/tts/client.mjs` still treats a paid POST's 502 `upstream_unavailable` as uncertain
(`SPEECH_UNCERTAIN`, exit 3, sent once), because a host from before that change answers the 502
for both cases. So an API restart while the web container is up (a deploy that lands during a
speech request) still blocks the video for the owner (`tools/video/automation/flow.mjs` blocks on
`video_speech_uncertain`) where the request never reached the API and could be sent again.

## Definition of done

- [ ] The production host serves the web change before the client change merges: the deployed
  commit contains the pull request of 2026-10-05-speech-routes-lost-paid-answer.
- [ ] A paid POST (speech, speech/transcribe, speech/judge) that gets the route's 502
  `upstream_unavailable` is sent again within the bounded attempts, and one that gets 504
  `video_speech_answer_lost` (or any other unlisted 5xx) is still sent once and stops as
  `SPEECH_UNCERTAIN`.

## Steps

- [ ] Check the deployed commit (skill `deploy` records it; `git merge-base --is-ancestor <PR merge
  commit> <deployed commit>`). If the web change is not live, stop here.
- [ ] Add `upstream_unavailable` to `SETTLED_CODES` in `tools/video/tts/client.mjs`, and rewrite the
  comment above it (it says why the code is not there yet). Decide whether to settle only the
  route's own 502: `speech-journal.test.mjs` feeds a 503 `upstream_unavailable`, which no speech
  route answers.
- [ ] In `tools/video/tts/client.test.mjs`, move "the web route's 502" from the lost list of the
  first test to the settled list of the third; keep "the web route's lost answer" (504
  `video_speech_answer_lost`) in the lost list.
- [ ] Update the `upstream_unavailable` case and its comment in
  `docs/videos/imported-long-languages/speech-journal.test.mjs` to match.

## How to verify

From the root: `node --test tools/video/tts/client.test.mjs
docs/videos/imported-long-languages/speech-journal.test.mjs` (fake transports only, nothing paid).
`npm run test:tools` runs the first file; nothing in CI runs the second.

## Notes

- Split from 2026-10-05-speech-routes-lost-paid-answer: the client half of its second
  Definition-of-done item, which waits for a deploy. That ticket's pull request already pins the
  other half (504 `video_speech_answer_lost` is uncertain) in `client.test.mjs`.
- The order is the point: this change on a client that meets a host from before the routes'
  change would send a paid request whose answer was lost again (the old host answers 502
  `upstream_unavailable` for that). The owner's local CLI can be newer than the host.
- Not done, if the order ever becomes a problem (a host rolled back past the change): the routes
  could mark their never-reached 502 (a field in the problem body) so the client settles only a
  marked one and needs no deploy order. That touches `forward.ts`, which every video route shares.
- The automation client's `SETTLED_RUN_CODES` holds `upstream_unavailable` only because its run
  route passes `RUN_LOST`; the automation judge routes have their own ticket
  (2026-10-05-let-the-judge-routes-tell-a, filed in PR #1237).
