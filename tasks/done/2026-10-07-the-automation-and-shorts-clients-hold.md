---
id: 2026-10-07-the-automation-and-shorts-clients-hold
title: The automation and Shorts clients hold a paid request the limiter refused (503 rate_limit_unavailable) as uncertain
status: done
priority: P3
area: tools
owner: claude-opus-5-5-limiter2
claimed_at: 2026-10-07T06:44:40Z
created_at: 2026-10-07T06:41:56Z
completed_at: 2026-10-07T06:48:39Z
branch:
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/shorts/site.mjs
  - tools/video/shorts/site.test.mjs
---

# The automation and Shorts clients hold a paid request the limiter refused (503 rate_limit_unavailable) as uncertain

## Why

The API's limiter refuses a request it cannot count with 503 `rate_limit_unavailable`
(`apps/api/app/infra.py` `enforce_named_rate_limit`, in the video tool token's dependency and
again at the top of the stage-run and judge routes, before either asks a model or Jev): nothing
reached a model, Jev or any vendor. The speech client treats it as
settled since 2026-10-07-a-paid-speech-request-the-limiter. Two more clients still hold it as a
paid answer that may have been charged:

- `tools/video/automation/client.mjs` `request()`: a paid stage run or Jev judgement whose 5xx is
  not in `SETTLED_RUN_CODES` / `SETTLED_JUDGE_CODES` throws RUN_UNCERTAIN, so the worker blocks
  the video for the owner (or holds the line) on a refusal that charged nothing. Durable writer
  runs (`durableRun`) are not affected: a failed POST there keeps the request key and reports
  pending.
- `tools/video/shorts/site.mjs` `settledJudge()`: the Shorts judge call, the same way.

Redis blinking on the host is enough to trigger it, for every video that sends a paid request
in that minute.

## Definition of done

- [x] A paid stage run, Jev judgement or Shorts judgement answered 503 `rate_limit_unavailable`
      is retried like the rate limit and, when the tries run out, is trouble that passes (the
      worker defers; `everyones()` already counts the sentence as everyone's), never uncertain.
- [x] The code on any other status stays uncertain, as in `tools/video/tts/client.mjs`
      (`LIMITER_AWAY`).

## Steps

- [x] Mirror `LIMITER_AWAY` from `tools/video/tts/client.mjs` in both clients, with a test per
      paid call that a 503 with the code is retried and a 502 with it is still uncertain.

## How to verify

`node --test tools/video/automation/client.test.mjs tools/video/shorts/site.test.mjs`

## Notes

- Filed 2026-10-07 by claude-opus-5-5-limiter while doing the speech client's half.
- Done 2026-10-07 by claude-opus-5-5-limiter2. Confirmed in `apps/api/app/video_automation/admin_api.py`
  that `run_video_stage`, `judge_video_outline` and `judge_video_policy` call
  `enforce_named_rate_limit` first, after the `video_tool` dependency that does the same, so a 503
  `rate_limit_unavailable` there means no model or Jev was asked. `automation/client.mjs`
  `request()` settles exactly that 503 (`LIMITER_AWAY`, `limiterAway()`, beside the settled code
  sets, for stage runs and Jev alike); `shorts/site.mjs` `settledJudge()` does the same next to
  `NEVER_REACHED`. Both then retry like any settled 5xx; the code on another status stays
  uncertain.
- Tests: a 503 row in the settled tables of the stage run, the Jev judgement
  (`client.test.mjs`) and the Shorts policy judgement (`site.test.mjs`), and a 502 row in each
  lost table. With the change reverted the three settled tests fail; with the status unchecked
  the three lost tests fail. `node --test "tools/video/automation/*.test.mjs"
  "tools/video/shorts/*.test.mjs" "tools/video/qa/*.test.mjs"` 693 pass.
