---
id: 2026-10-05-automation-client-retries-a-judge-s
title: Automation client retries a judge's upstream_unavailable once the judge lost-answer routes are live
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T12:43:03Z
completed_at:
branch:
depends_on:
  - 2026-10-05-let-the-judge-routes-tell-a
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Automation client retries a judge's upstream_unavailable once the judge lost-answer routes are live

## Why

Since 2026-10-05-let-the-judge-routes-tell-a, the two Jev judgement routes
(`apps/web/app/api/video/automation/judge/policy/route.ts` and `.../outline/route.ts`) answer 504
`video_judge_answer_lost` when the API took the request and its answer never came back (the 180 s
deadline passed, or the connection dropped mid-way), and keep 502 `upstream_unavailable` for an
API they never reached (`JUDGE_LOST` in `apps/web/app/api/video/speech/forward.ts`).

`tools/video/automation/client.mjs` still treats a judge's 502 `upstream_unavailable` as uncertain
(`RUN_UNCERTAIN`, one POST), because a host from before that change answers the 502 for both
cases. So when the API container is only restarting and the judgement never reached it, the QA's
`policy` item fails, or the outline waits, until the next worker round, instead of being asked
again within the call's bounded attempts.

## Definition of done

- [ ] The production host serves the web change before the client change merges: the deployed
  commit contains the pull request of 2026-10-05-let-the-judge-routes-tell-a.
- [ ] A judgement (`judgePolicy`, `judgeOutline`) that gets the route's 502 `upstream_unavailable`
  is asked again within the bounded attempts, and one that gets 504 `video_judge_answer_lost` (or
  any other unlisted 5xx) is still sent once and stops as `RUN_UNCERTAIN`: at most one paid judge
  POST that may have reached Jev per call.

## Steps

- [ ] Check the deployed commit (skill `deploy` records it; `git merge-base --is-ancestor <PR merge
  commit> <deployed commit>`). If the web change is not live, stop here.
- [ ] Add `upstream_unavailable` to `SETTLED_JUDGE_CODES` in `tools/video/automation/client.mjs`
  and rewrite the comment above it (it says why the code is not there yet). It is already in
  `RETRYABLE_CODES`, so it is then retried like a stage run's.
- [ ] In `tools/video/automation/client.test.mjs`, move "the judge route's 502" from the lost list
  of "a Jev judgement sent and left without its answer is not asked again" to the settled list of
  "a Jev judgement that never reached a server, or that the API settled, is asked again"; keep
  "the judge route's lost answer" (504 `video_judge_answer_lost`) in the lost list, and drop "or
  502" from the first test's name.

## How to verify

From the root: `node --test tools/video/automation/client.test.mjs tools/video/qa/qa.test.mjs
tools/video/review/sync.test.mjs` (fake transports only, nothing paid; `npm run test:tools` runs
them too).

## Notes

- Split from 2026-10-05-let-the-judge-routes-tell-a: the client half of its second
  Definition-of-done item and its second and third steps, which wait for a deploy. That ticket's
  pull request already pins the other half (504 `video_judge_answer_lost` is uncertain) in
  `client.test.mjs`.
- The order is the point: this change on a client that meets a host from before the routes' change
  would send a judgement whose answer was lost again (the old host answers 502
  `upstream_unavailable` for that), taking a second call off the daily Jev budget. On the host the
  worker and web ship together (`up --build -d`, `video-worker` `depends_on: web`), but
  `tools/video/qa/cli.mjs` and `tools/video/review/sync.mjs` also run from local checkouts against
  mokaair.com, which can be newer than the host.
- Same rollout as the speech client (2026-10-05-speech-client-retries-paid-upstream-unavailable),
  which records the alternative that would not need the order (a marker on the routes'
  never-reached 502 in `forward.ts`).
- The Shorts tool asks Jev through its own client (`tools/video/shorts/site.mjs` `judgePolicy`);
  2026-10-05-stop-the-shorts-client-from-resending covers it, and once it lands its settled set can
  take the same step after the same deploy.
