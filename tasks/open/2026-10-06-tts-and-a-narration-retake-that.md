---
id: 2026-10-06-tts-and-a-narration-retake-that
title: tts and a narration retake that exit 4 block the video instead of waiting
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-06T15:42:27Z
completed_at:
branch:
depends_on:
  - 2026-10-06-a-failing-video-is-deferred
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# tts and a narration retake that exit 4 block the video instead of waiting

## Why

Every other command the worker runs for a video treats exit 4 (a service away, a budget spent, a
rate limit) as trouble that passes: the video is deferred (`flow.mjs` `defer`), and since the
repair of PR #1342 a deferral whose output says the trouble is everyone's (`everyones`: the
month's speech characters spent, the API's rate limit, Jev's daily calls) never counts toward a
block. Two calls were left out, and they still block the video at once, one owner retry each:

- `advance()`, the narration stage: `if (result.code !== 0) return this.block(state, "tts failed: …")`
  after the STOP-file case, so a `tts` that exits 4 is a block.
- `narration()`, the retakes: `if (redo.code !== 0) return this.block(state, "retake failed: …")`,
  and the same for the retake after a rewrite.

This is what blocked `openai-agent-posted-53-user-images` on 2026-10-04 with
`tts failed: 請求過於頻繁，請稍後再試` (`2026-10-05-a-burst-of-narration-lines-trips`, which
fixes the client's wait and leaves this side as it is). The speech budget of the month running out
blocks every video that reaches its narration the same way, and each stays blocked into the next
month.

Read in the code while the second review of PR #1342 was being answered. Older than that pull
request, and not one of its findings.

## Definition of done

- [ ] A `tts` or a retake that exits 4 defers the video with the command's last line, and one that
      says the trouble is everyone's never blocks it; exit 3 (the owner's) and the other codes
      block as today.
- [ ] A paid speech request whose answer was lost (exit 3 with `SPEECH_UNCERTAIN`) still stops the
      video for the owner: nothing here may send it again.

## Steps

- [ ] `advance()` and `narration()`: `code === 4` goes to
      `defer(state, line, { what: "tts", everyone: Boolean(everyones(result.out)) })` before the
      block for any other code. Check what a retake that stopped halfway leaves on disk first:
      `retakeStopped` exists because takes changed by a retake no longer match `timeline.json`,
      and a retake that exits 4 after some lines is in the same position.
- [ ] Tests in `automation.test.mjs` on the `narrationGate` fixture: a tts and a retake that exit
      4 with the rate limit's sentence, eight rounds, never blocked; with a vendor's line, blocked
      at the seventh.

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs
```

## Notes

- `flow.mjs` and `automation.test.mjs` are bound by the duration-review receipt
  (`docs/videos/long-form/review.json`): a change there needs the independent re-bind.
- `everyones()` reads the server's wording because the commands print the detail and not the code;
  its table is in `flow.mjs` beside `EVERYONE_CODES`.
