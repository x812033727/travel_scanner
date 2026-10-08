---
id: 2026-10-07-automation-client-settles-a-judge-route
title: Automation client settles a judge route's upstream_unavailable at any status, not only the route's 502
status: done
priority: P3
area: tools
owner: claude-opus-5-5-judge-502
claimed_at: 2026-10-07T08:40:02Z
created_at: 2026-10-07T06:41:09Z
completed_at: 2026-10-07T09:20:01Z
branch:
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Automation client settles a judge route's upstream_unavailable at any status, not only the route's 502

## Why

`tools/video/automation/client.mjs` lets a paid Jev judgement (`judgePolicy`, `judgeOutline`) be
sent again when its 5xx code is in `SETTLED_JUDGE_CODES`, and that set holds
`upstream_unavailable` whatever the status. Only the judge routes' 502 with that code means an API
they never reached (`apps/web/app/api/video/speech/forward.ts`). The speech client
(`tools/video/tts/client.mjs` `NEVER_REACHED`) and, since 2026-10-07, the Shorts client
(`tools/video/shorts/site.mjs`) settle only the 502.

No route answers the code with another status today, so this is defence in depth. A future 503 or
504 `upstream_unavailable` would make a judgement that may have run be paid for a second time.
Stage runs (`SETTLED_RUN_CODES`) share the same pattern; check whether the same reasoning applies
there.

## Definition of done

- [x] A judgement that gets 502 `upstream_unavailable` is asked again, and one that gets that code
  with any other status is sent once and thrown as `RUN_UNCERTAIN`.

## Steps

- [x] Settle `upstream_unavailable` only with status 502 for the judge methods, as `site.mjs`
  does, and decide the same for `SETTLED_RUN_CODES`.
- [x] Add a 503 `upstream_unavailable` row to the lost judgements in `client.test.mjs`.

## How to verify

`node --test tools/video/automation/client.test.mjs`.

## Notes

- Found by the review of `2026-10-05-shorts-client-retries-the-judge-route` (2026-10-07). The
  reviewer traced every source of `upstream_unavailable` on the judge URLs: only the web route's
  connect-time failures answer it, always as 502.
- 2026-10-07 (claude-opus-5-5-judge-502). `client.mjs` settles `upstream_unavailable` for a paid
  request only with status 502 (`NEVER_RAN`, `settles()`), as `tts/client.mjs` and
  `shorts/site.mjs` do. It is out of both `SETTLED_JUDGE_CODES` and `SETTLED_RUN_CODES`.
- Stage runs: the same reasoning applies. `automation/run` goes through the same
  `forwardToSpeech` as the judge routes, with its own lost answer (`RUN_LOST`, 504
  `video_ai_run_uncertain`). The forwarder answers `upstream_unavailable` only as 502, for a
  connect-time failure. No API module answers the code (`grep` over `apps/api/app`).
- Unchanged: the GETs and the review submit still retry any 5xx, and the job lookups read their
  status directly (`settledLookup`).
- Tests: `client.test.mjs` gains a 503 and a 504 `upstream_unavailable` row in both the stage-run
  and the judgement lost tables. These are sent once and thrown as `RUN_UNCERTAIN`, with no wait.
  The 502 rows that are asked again stay. The new rows fail on the old code. Each of two
  mutations (the code at any status; any 502) fails a test.
- Review (2026-10-07, two lenses, each finding verified): no defect in the change. It traced
  every source of `upstream_unavailable` on these routes: the forwarder answers it only for
  connect-phase errors, the API never does, and nginx and Next.js add no code. It also traced
  every caller of the changed error (flow, review sync, QA, Shorts). It found, and this task
  takes, an older should-fix in the same scope:
  - The API's 503 `rate_limit_unavailable` blocked a stage run for the owner (`RUN_UNCERTAIN`,
    `uncertain:<stage>`), though nothing had run. Redis could not count the call, and
    `enforce_named_rate_limit` runs in `video_tool` and first in the run and judge handlers,
    before any model or Jev call. It is now in `NEVER_RAN` with its 503 only, so it is asked
    again within the attempts, and then deferred as everyone's trouble (flow.mjs
    `EVERYONE_CODES` already lists it).
  - Tests: a settled row for it in the stage-run and judgement tables. The stage-run lost table
    gains a 502 with a code that settles nothing (the gap that let "any 502" pass there) and the
    rate-limiter code at another status. Mutations (no rate-limiter pair, the code at any
    status, any 502) each fail two tests.
- Filed from the review:
  - `2026-10-07-the-speech-and-shorts-clients-hold`: `tts/client.mjs` and `shorts/site.mjs`
    hold the same 503 as uncertain.
  - `2026-10-07-a-paid-media-judge-or-locate-call`: the media forwarder answers a lost
    judge or locate answer as its 502, which the media client sends again.
