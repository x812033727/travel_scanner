---
id: 2026-10-08-pin-what-the-rebased-branch-dropped
title: Pin what the rebased branch dropped: one paid speech POST, a dry run's picture check, the limiter's 503, a refused submission; two client tests off the real clock
status: done
priority: P3
area: tools
owner: claude-happy-carson
claimed_at: 2026-10-08T02:25:17Z
created_at: 2026-10-08T02:24:32Z
completed_at: 2026-10-08T02:29:04Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - tools/video/automation/client.test.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/tts/client.test.mjs
  - apps/api/tests/test_video_speech.py
---

# Pin what the rebased branch dropped: one paid speech POST, a dry run's picture check, the limiter's 503, a refused submission; two client tests off the real clock

## Why

#1361 and #1364 closed several of the same board tickets on their own branches. #1364 landed
first, and #1361 was rebased onto main (2026-10-08) keeping only its own tickets, so its
versions of the shared ones were dropped. An overlap comparison (one agent per ticket, each gap
checked by a skeptic) found a few things #1361's tests pinned that main's tests do not, and one
of main's tests that fails under load:

- `client.test.mjs`: two pending-writer cases spend a 40 ms poll budget in real time
  (`budget - Math.max(waited, Date.now() - started)`), so an event loop stalled for 40 ms takes
  their second look-up away. Measured under load: 4 to 13 of 40 concurrent runs failed, and 3 of
  150 single runs beside a full `test:tools` (`gets` 1 instead of 2, or `why` still
  請求過於頻繁).
- A durable submission the rate limit refuses all round is sent the client's attempts (4) under
  one key and no more: nothing on main counts the POSTs (a mutation that drops the cap passes).
- `clips --dry-run` refuses a changed selected start or end picture before it reads the month's
  seconds: main checks it before the dry run, but no test runs a dry run on a changed picture.
- A paid speech call answered 503 `rate_limit_unavailable` on every try stops after five, as a
  service away with the API's sentence, which `flow.mjs` `everyones()` reads as everyone's.
- The Azure provider sends a request that was never sent or whose answer was lost exactly once:
  main's provider test does not count requests.

Main's code already behaves right in every case; only the tests are missing or fragile.

## Definition of done

- [x] The two pending-writer client cases spend their budget in the client's fake sleeps and
      pass under load.
- [x] Each pin above fails when the behaviour it pins is removed.

## Steps

- [x] `client.test.mjs`: `recovered` on a 3 s budget of 1 s fake waits (three look-ups); `cut` on
      a 25 s budget whose first look-up takes 5 real ms, which is what the second gets; the
      refused submission counts four POSTs under one key.
- [x] `clips.test.mjs`: dry-run rows (start and end) in the changed-picture test.
- [x] `tts/client.test.mjs`: the limiter away on every try, for the four paid calls.
- [x] `test_video_speech.py`: `_raising` records the requests, and the provider test asserts one.

## How to verify

```bash
node --test tools/video/automation/client.test.mjs tools/video/tts/client.test.mjs tools/video/media/clips.test.mjs
cd apps/api && uv run pytest tests/test_video_speech.py -k never_sent_from_one_whose_answer
```

## Notes

- 2026-10-08 (claude-happy-carson): done in #1361.
  - Load: the two client cases ran 40 at once on 4 cores, and none of the 40 failed.
  - Mutations (each made its pin fail, then was reverted):
    - `clips.mjs` skips the picture gate on `--dry-run`;
    - `client.mjs` drops `failures >= attempts`;
    - `tts/client.mjs` drops the 503 from `NEVER_RAN`;
    - `azure.py` sends a silent second POST after a read timeout.
- Gaps the same comparison found that are more than a test are filed:
  2026-10-08-a-document-line-whose-planner-request,
  2026-10-08-a-storyboard-s-kept-shot-still and 2026-10-08-a-narration-retake-that-exits-4.
- Left as they are, on purpose:
  - Main keeps a narration retake's round spent when a STOP ends it before any request was
    answered; #1361 gave it back.
  - Main's pending-writer line does not tell a look-up that failed from a submission the server
    never confirmed. The line is less specific, not wrong.
