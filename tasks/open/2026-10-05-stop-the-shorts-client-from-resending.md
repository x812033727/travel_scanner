---
id: 2026-10-05-stop-the-shorts-client-from-resending
title: Stop the Shorts client from resending a judge policy request after a lost answer
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-05T00:44:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/site.mjs
  - tools/video/shorts/site.test.mjs
---

# Stop the Shorts client from resending a judge policy request after a lost answer

## Why

The Shorts tool talks to the site through its own client, `siteClient` in
`tools/video/shorts/site.mjs`, not through the automation client. Its `judgePolicy`
(`POST automation/judge/policy`, called by `tools/video/shorts/qa.mjs` for the Shorts QA's
`policy` item) uses the generic `request()` loop. That loop sends the same POST again, up to
four times, after any thrown fetch error and after any 5xx or 429.

The server takes one call off the daily Jev budget before it asks Jev
(`apps/api/app/video_automation/judge.py` `_ask`). A Shorts judgement that reached the API and
lost its answer on the way back (a dropped connection, an unreadable body, a gateway's 5xx, or
the judge route's 502 `upstream_unavailable` after the API took the request) can therefore spend
the budget again inside one QA run. The automation client got the same guard in
2026-10-04-prevent-automatic-retries-of-paid-video. This is a source finding: nobody has seen a
duplicate charge.

## Definition of done

- [ ] A Shorts policy judgement that was sent and lost its answer is not sent again by the same
  call; the QA's `policy` item says the outcome is unknown instead.
- [ ] A request that never reached a server (ECONNREFUSED, ENOTFOUND, EAI_AGAIN, EHOSTUNREACH,
  ENETUNREACH, UND_ERR_CONNECT_TIMEOUT), the API's own 502 `video_judge_upstream_failed` and a 429
  are still tried again as before; the other requests (settings, videos, reviews, uploads) keep
  their retries.
- [ ] The verdict that does come back is returned unchanged, a failed one included.

## Steps

- [ ] Mirror `tools/video/automation/client.mjs`: a `paid` option on `request()` with the never-sent
  connection codes and a settled set holding only `video_judge_upstream_failed`; only
  `judgePolicy` passes it.
- [ ] Decide what `SiteError` code the lost answer carries (reuse `video_ai_run_uncertain` so a
  reader sees the same code in both tools) and check that `tools/video/shorts/qa.mjs` `failing()`
  reports it as a failed item without retrying.
- [ ] Add `tools/video/shorts/site.test.mjs` with a fake fetch: a reset after sending, a broken 200
  body, a 504 page and the judge route's 502 each give one POST; ECONNREFUSED,
  `video_judge_upstream_failed` and 429 give two; a GET on a 500 is retried.

## How to verify

`node --test tools/video/shorts/site.test.mjs tools/video/shorts/cut.test.mjs tools/video/shorts/lab.test.mjs tools/video/shorts/pipeline.test.mjs`,
then `npm run test:tools`. Use fake transports only; never reproduce a lost answer against Jev.

## Notes

- Split from 2026-10-04-prevent-automatic-retries-of-paid-video, which fixed the automation client
  only (its scope). `siteClient.request` on origin/main at 2026-10-05: `catch` → sleep and retry;
  `response.status === 429 || >= 500` → sleep and retry.
- `tools/video/shorts/*` is not bound to `docs/videos/long-form/review.json`.
