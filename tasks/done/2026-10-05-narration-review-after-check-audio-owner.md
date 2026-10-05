---
id: 2026-10-05-narration-review-after-check-audio-owner
title: Worker sends narration for review after check-audio stopped for the owner
status: done
priority: P2
area: tools
owner: claude-opus-5-5-tts-client-paid-retries
claimed_at: 2026-10-05T05:09:54Z
created_at: 2026-10-05T00:39:07Z
completed_at: 2026-10-05T05:12:44Z
branch: claude/tts-client-paid-retries
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Worker sends narration for review after check-audio stopped for the owner

## Why

`narration()` in `tools/video/automation/flow.mjs` runs `check-audio`, loops on exit 1
(retakes, rewrites), returns "later" on exit 4, and then runs `review-push --gate audio` for
every other exit code. Exit 3 (the owner's: a revoked token, Gemini key removed, and since
2026-10-04-prevent-paid-speech-retries-after-ambiguous a transcription or Jev judgement whose
paid answer was lost, `video_speech_uncertain`) therefore sends a partly checked narration for
review, and the round reports "narration checked (some lines flagged) and sent for review".
`media()` and the dub path block or give up on exit 3 instead.

Found by reading the code on 2026-10-05; no production run has been seen doing it.

## Definition of done

- [x] A `check-audio` exit 3 blocks the video with its last line as the reason (as `media()`
  does), and nothing is pushed for review in that round.
- [x] Exit 0, 1 and 4 behave as before.

## Steps

- [x] Handle `check.code === 3` (and any code other than 0, 1 and 4) before `review-push`.
- [x] A flow test whose runner answers `check-audio` with exit 3 and asserts the block and that
  `review-push` was not run.

## How to verify

`node --test tools/video/automation/automation.test.mjs`, then `npm run test:tools`.
`flow.mjs` is bound by the long-form duration receipt: run
`node tools/video/long-form/cli.mjs check` and report its stale list; do not edit
`docs/videos/long-form/review.json` yourself.

## Notes

- The relevant lines are the end of `narration()`: `if (check.code === 4) return this.later(...)`
  followed directly by `run(ctx, ["review-push", ...])`.

### 2026-10-05 done (claude-opus-5-5-tts-client-paid-retries, branch claude/tts-client-paid-retries)

- Folded into PR #1235 after its review asked that the PR not merge while this was open: the
  client change made one lost transcription or Jev answer enough to reach it. A primary
  `askJev` in `tools/video/tts/check.mjs` has no try/catch, so the check stopped with
  `review/check.json` holding lines with `match: false` and `noul: null`, which the review card
  would have counted as judged fine.
- `narration()` now blocks on `check.code === 3` with `check-audio needs the owner: <last line>`
  (as `media()` does) and on any other code than 0, 1 and 4 with `check-audio failed: <last two
  lines>`, both before `review-push`. Exit 4 still returns "later"; 0 and 1 still go for review.
- Test in `tools/video/automation/automation.test.mjs` ("a narration check that stops for the
  owner ..."): `check-audio` answers 4 (later, nothing pushed), then 3 with the real client's
  `video_speech_uncertain` line and a half-written check.json (blocked, no `review-push` run, no
  audio review), then 2 after the owner's retry (blocked again), then passes after the second
  retry and is sent for review. Scope widened to that test file.
- Claimed with `--force`: the overlapping claims on `flow.mjs` were all older than 24 hours
  (2026-09-28-drama-listener-stale-check, 2026-09-28-sothatswhy-shorts-from-episode,
  2026-09-30-video-worker-moves-two-videos-at, 2026-10-03-illustrated-slides-round-2-a-family,
  2026-10-03-video-worker-narration-takes-made-stale). Open draft PR #1242
  (2026-10-04-audio-stage-incomplete-exits) changes the same lines: it adds `EXIT.incomplete`
  (6) handled as "later". Whichever lands second must keep that line before the new
  "any other code" block, or a STOP would block the video.
- `flow.mjs` and `automation.test.mjs` are bound by the long-form duration receipt; the receipt
  increment is left to the independent reviewer.
