---
id: 2026-10-07-the-automation-and-shorts-clients-hold
title: The automation and Shorts clients hold a paid request the limiter refused (503 rate_limit_unavailable) as uncertain
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T06:41:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/shorts/site.mjs
  - tools/video/shorts/shorts.test.mjs
---

# The automation and Shorts clients hold a paid request the limiter refused (503 rate_limit_unavailable) as uncertain

## Why

The API's limiter refuses a request it cannot count with 503 `rate_limit_unavailable`
(`apps/api/app/infra.py` `enforce_named_rate_limit`, in the video tool token's dependency, before
any route body runs): nothing reached a model, Jev or any vendor. The speech client treats it as
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

- [ ] A paid stage run, Jev judgement or Shorts judgement answered 503 `rate_limit_unavailable`
      is retried like the rate limit and, when the tries run out, is trouble that passes (the
      worker defers; `everyones()` already counts the sentence as everyone's), never uncertain.
- [ ] The code on any other status stays uncertain, as in `tools/video/tts/client.mjs`
      (`LIMITER_AWAY`).

## Steps

- [ ] Mirror `LIMITER_AWAY` from `tools/video/tts/client.mjs` in both clients, with a test per
      paid call that a 503 with the code is retried and a 502 with it is still uncertain.

## How to verify

`node --test tools/video/automation/client.test.mjs tools/video/shorts/shorts.test.mjs`

## Notes

- Filed 2026-10-07 by claude-opus-5-5-limiter while doing the speech client's half.
