---
id: 2026-10-05-speech-client-retries-paid-upstream-unavailable
title: Speech client retries a paid upstream_unavailable once the lost-answer routes are live
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-speech-client-upstream-unavailable
claimed_at: 2026-10-05T12:31:13Z
created_at: 2026-10-05T07:42:22Z
completed_at:
branch: claude/speech-client-upstream-unavailable
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

- [x] The production host serves the web change before the client change merges: the deployed
  commit contains the pull request of 2026-10-05-speech-routes-lost-paid-answer.
- [x] A paid POST (speech, speech/transcribe, speech/judge) that gets the route's 502
  `upstream_unavailable` is sent again within the bounded attempts, and one that gets 504
  `video_speech_answer_lost` (or any other unlisted 5xx) is still sent once and stops as
  `SPEECH_UNCERTAIN`.

## Steps

- [x] Check the deployed commit (skill `deploy` records it; `git merge-base --is-ancestor <PR merge
  commit> <deployed commit>`). If the web change is not live, stop here.
- [x] Add `upstream_unavailable` to `SETTLED_CODES` in `tools/video/tts/client.mjs`, and rewrite the
  comment above it (it says why the code is not there yet). Decide whether to settle only the
  route's own 502: `speech-journal.test.mjs` feeds a 503 `upstream_unavailable`, which no speech
  route answers.
- [x] In `tools/video/tts/client.test.mjs`, move "the web route's 502" from the lost list of the
  first test to the settled list of the third; keep "the web route's lost answer" (504
  `video_speech_answer_lost`) in the lost list.
- [x] Update the `upstream_unavailable` case and its comment in
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

### Done 2026-10-05 (claude-opus-5-5-speech-client-upstream-unavailable)

- Deploy order. The routes' change was PR #1265. That PR was closed without merging and landed
  inside train #1272, squash `2e301aba3568f4a3f6f7994c484af06625c33c84`. #1235's client half is
  `50fbb9b00`. The coordinator deployed `c12e159d012265ee431dc68cc3bacd4851279245` to production on
  2026-10-05 12:07:49–12:08:43Z. Its host-verify run read live head c12e159d0 and passed
  `web-speech-answer-lost`, so the web image contains `video_speech_answer_lost`. Both
  `git merge-base --is-ancestor 2e301aba3 c12e159d0` and
  `git merge-base --is-ancestor 50fbb9b00 c12e159d0` exit 0. This agent did not contact the host.
  It read the coordinator's deploy record and host-verify output.
- Decision: settle only the route's own 502, not every `upstream_unavailable`. `client.mjs` keeps
  `SETTLED_CODES` as the API's own codes. It adds `NEVER_REACHED = { status: 502, code:
  "upstream_unavailable" }` and a `settled(status, code)` helper used by the paid 5xx check. No
  speech route answers that code with another status (`forward.ts` is the only producer under
  `/api/video/speech`), so a 503 `upstream_unavailable` stays `SPEECH_UNCERTAIN`. The comment above
  says why, and says that a host from before #1272 would make the resend unsafe.
- `client.test.mjs`. The route's 502 moved from the lost list to the settled list, with one retry
  and a 1 s wait. The lost list keeps 504 `video_speech_answer_lost` and gains a 503
  `upstream_unavailable`. "A settled failure that does not clear" now also pins a 502
  `upstream_unavailable` that never clears: 5 attempts, then `upstream_unavailable`, who `service`.
- `speech-journal.test.mjs`. The 503 case stays `SPEECH_UNCERTAIN`. A new 502 case shows the
  native client asking again, and the journal answering that second POST with its local 409
  `video_speech_result_held`. That is one POST, the entry is `unknown`, and who is `service`. The
  journal still never resends. Letting it release the route's 502 is filed as
  2026-10-05-speech-journal-releases-never-reached-502.
- Mutation checks, run against both test files. With main's `client.mjs`, 4 tests fail (the new 502
  cases). With a status-blind variant that settles any `upstream_unavailable`, 3 fail (the 503
  cases). The real change passes 67/67.
- The claim needed `--force`. The scope overlaps the stale claim
  2026-09-29-resume-imported-long-video-languages (codex-video-stall-followthrough, claimed
  2026-10-04T10:51Z, branch `codex/video-approved-final-languages-20261004` not on the remote). No
  open PR touches the three paths.
