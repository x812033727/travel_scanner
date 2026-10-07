---
id: 2026-10-06-tts-and-a-narration-retake-that
title: tts and a narration retake that exit 4 block the video instead of waiting
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-tts-defer
claimed_at: 2026-10-07T06:02:08Z
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

- [x] A `tts` or a retake that exits 4 defers the video with the command's last line, and one that
      says the trouble is everyone's never blocks it; exit 3 (the owner's) and the other codes
      block as today.
- [x] A paid speech request whose answer was lost (exit 3 with `SPEECH_UNCERTAIN`) still stops the
      video for the owner: nothing here may send it again.

## Steps

- [x] `advance()` and `narration()`: `code === 4` goes to
      `defer(state, line, { what: "tts", everyone: Boolean(everyones(result.out)) })` before the
      block for any other code. Check what a retake that stopped halfway leaves on disk first:
      `retakeStopped` exists because takes changed by a retake no longer match `timeline.json`,
      and a retake that exits 4 after some lines is in the same position.
- [x] Tests in `automation.test.mjs` on the `narrationGate` fixture: a tts and a retake that exit
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
- 2026-10-07 (claude-opus-5-5-tts-defer). `flow.mjs`:
  - `advance()`: a tts that exits 4 is deferred as `${slug}: tts could not finish (<last line>)`,
    with `what: "tts"` and `everyone` from `everyones(result.out)`. Its takes so far are cached and
    the next tts goes on from them.
  - Why that cannot trip the guard before tts: the guard's `resumed` case needs the same script with
    bound evidence, where every take is current, so that tts has nothing to synthesize and cannot
    exit 4 with takes changed.
  - `narration()`: a retake, or a retake after a rewrite, that exits 4 goes through `retakeStopped`
    with defer's options (`retakeWait`): `what: "tts"`, and `everyone` from its output. That
    function records the takes the retake made (`stopped_retake`), so the next round's plain tts
    binds them as it does after a STOP, instead of blocking on "audio evidence no longer matches".
    A STOP keeps its `backoffMs: 0`; exit 4 waits and doubles like any deferral.
  - The resume line now reads "narration synthesized from the takes of the retake that stopped
    halfway", since a service as well as a STOP file can end one.
- Tests (`automation.test.mjs`), each failing on the old code:
  - tts exit 4 with the rate limit's sentence, and with the month's characters spent: eight
    rounds, never blocked, `defer_shared` 8, then synthesized.
  - With a vendor's line: blocked at the seventh try as `deferred:tts`.
  - A retake that exits 4 after one take: recorded, deferred, bound, checked, and no line retaken
    twice.
  - A retake that exits 4 before its first take: recorded nothing, counted.
  - Also pinned (passes on both versions): tts exit 3 (a revoked token, a lost paid answer) and
    exit 2 still block at once.
