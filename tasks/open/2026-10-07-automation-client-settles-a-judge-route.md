---
id: 2026-10-07-automation-client-settles-a-judge-route
title: Automation client settles a judge route's upstream_unavailable at any status, not only the route's 502
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T06:41:09Z
completed_at:
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

- [ ] A judgement that gets 502 `upstream_unavailable` is asked again, and one that gets that code
  with any other status is sent once and thrown as `RUN_UNCERTAIN`.

## Steps

- [ ] Settle `upstream_unavailable` only with status 502 for the judge methods, as `site.mjs`
  does, and decide the same for `SETTLED_RUN_CODES`.
- [ ] Add a 503 `upstream_unavailable` row to the lost judgements in `client.test.mjs`.

## How to verify

`node --test tools/video/automation/client.test.mjs`.

## Notes

- Found by the review of `2026-10-05-shorts-client-retries-the-judge-route` (2026-10-07). The
  reviewer traced every source of `upstream_unavailable` on the judge URLs: only the web route's
  connect-time failures answer it, always as 502.
