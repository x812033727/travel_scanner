---
id: 2026-10-05-narration-review-after-check-audio-owner
title: Worker sends narration for review after check-audio stopped for the owner
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T00:39:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
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

- [ ] A `check-audio` exit 3 blocks the video with its last line as the reason (as `media()`
  does), and nothing is pushed for review in that round.
- [ ] Exit 0, 1 and 4 behave as before.

## Steps

- [ ] Handle `check.code === 3` (and any code other than 0, 1 and 4) before `review-push`.
- [ ] A flow test whose runner answers `check-audio` with exit 3 and asserts the block and that
  `review-push` was not run.

## How to verify

`node --test tools/video/automation/automation.test.mjs`, then `npm run test:tools`.
`flow.mjs` is bound by the long-form duration receipt: run
`node tools/video/long-form/cli.mjs check` and report its stale list; do not edit
`docs/videos/long-form/review.json` yourself.

## Notes

- The relevant lines are the end of `narration()`: `if (check.code === 4) return this.later(...)`
  followed directly by `run(ctx, ["review-push", ...])`.
