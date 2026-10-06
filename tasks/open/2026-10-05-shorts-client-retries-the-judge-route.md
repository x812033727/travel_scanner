---
id: 2026-10-05-shorts-client-retries-the-judge-route
title: Shorts client retries the judge route's never-reached 502 like the automation client
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T23:52:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/site.mjs
  - tools/video/shorts/site.test.mjs
---

# Shorts client retries the judge route's never-reached 502 like the automation client

## Why

The Shorts tool asks Jev for its QA's `policy` item through its own client
(`tools/video/shorts/site.mjs` `judgePolicy`, POST `automation/judge/policy`), not through
`tools/video/automation/client.mjs`. Since 2026-10-05-stop-the-shorts-client-from-resending it is
`paid`: after it was sent, only a 429 or the API's own 502 `video_judge_upstream_failed`
(`SETTLED_JUDGE_CODES`) lets it ask again, and every other 5xx is `RUN_UNCERTAIN`, the judge route's
502 `upstream_unavailable` included.

That 502 now means only an API the route never reached: since 2026-10-05-let-the-judge-routes-tell-a
the judge routes answer a request the API took and whose answer was lost with 504
`video_judge_answer_lost` (`JUDGE_LOST` in `apps/web/app/api/video/speech/forward.ts`), and production
serves that since a9e4c3851 (deployed 2026-10-05 23:13Z). The automation client took this step in
2026-10-05-automation-client-retries-a-judge-s. The Shorts client still fails the `policy` item when
the API container is only restarting, instead of asking again within its bounded attempts.

## Definition of done

- [ ] A Shorts `judgePolicy` that gets the route's 502 `upstream_unavailable` is asked again within
  the client's attempts; one that gets 504 `video_judge_answer_lost`, a 502 with any other code, or
  any other unlisted 5xx is still sent once and thrown as `RUN_UNCERTAIN`.

## Steps

- [ ] Before starting, confirm the deployed commit still contains a9e4c3851 (skill `deploy`), so
  no host answers that 502 for a lost answer.
- [ ] Add `upstream_unavailable` to `SETTLED_JUDGE_CODES` in `tools/video/shorts/site.mjs` and
  rewrite the comment above it, as `tools/video/automation/client.mjs` did.
- [ ] In `tools/video/shorts/site.test.mjs`, move "the judge route's 502" from `LOST` to the settled
  list of "a policy judgement that never reached a server, or that the API settled, is asked again",
  add the route's 504 `video_judge_answer_lost` and a 502 `video_judge_outcome_uncertain` to `LOST`,
  and drop "the judge route's 502" from the lost test's name.

## How to verify

From the root: `node --test tools/video/shorts/site.test.mjs tools/video/shorts/lab.test.mjs` (fake
transports only, nothing paid). Run the new tests against origin/main's `site.mjs` once to see the
settled case fail there.

## Notes

- Filed by claude-opus-5-5-judge-settled-502 while closing
  2026-10-05-automation-client-retries-a-judge-s, whose Notes named this as the next step once
  2026-10-05-stop-the-shorts-client-from-resending landed (it has, in a9e4c3851).
- `video_judge_outcome_uncertain` is the API's 502 for a Jev call whose outcome it cannot tell
  (2026-10-05-jev-judge-endpoints-report-an-uncertain, Codex PR #1254, open on 2026-10-06). It must
  stay outside the settled set.
- `tools/video/shorts/*` is not bound to `docs/videos/long-form/review.json`.
