---
id: 2026-10-05-stop-the-shorts-client-from-resending
title: Stop the Shorts client from resending a judge policy request after a lost answer
status: done
priority: P1
area: tools
owner: claude-opus-5-5-shorts-client-no-resend
claimed_at: 2026-10-05T12:27:46Z
created_at: 2026-10-05T00:44:19Z
completed_at: 2026-10-05T12:38:21Z
branch: claude/shorts-client-no-resend
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

- [x] A Shorts policy judgement that was sent and lost its answer is not sent again by the same
  call; the QA's `policy` item says the outcome is unknown instead.
- [x] A request that never reached a server (ECONNREFUSED, ENOTFOUND, EAI_AGAIN, EHOSTUNREACH,
  ENETUNREACH, UND_ERR_CONNECT_TIMEOUT), the API's own 502 `video_judge_upstream_failed` and a 429
  are still tried again as before; the other requests (settings, videos, reviews, uploads) keep
  their retries.
- [x] The verdict that does come back is returned unchanged, a failed one included.

## Steps

- [x] Mirror `tools/video/automation/client.mjs`: a `paid` option on `request()` with the never-sent
  connection codes and a settled set holding only `video_judge_upstream_failed`; only
  `judgePolicy` passes it.
- [x] Decide what `SiteError` code the lost answer carries (reuse `video_ai_run_uncertain` so a
  reader sees the same code in both tools) and check that `tools/video/shorts/qa.mjs` `failing()`
  reports it as a failed item without retrying.
- [x] Add `tools/video/shorts/site.test.mjs` with a fake fetch: a reset after sending, a broken 200
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
- 2026-10-05 (claude-opus-5-5-shorts-client-no-resend): `siteClient.request` takes a `paid`
  option, as in `tools/video/automation/client.mjs`; only `judgePolicy` passes it. A paid request
  is sent again only after a never-sent connection error (the same six codes, read from
  `error.cause.code` as undici throws them), a 429 (any code, `jev_budget_exhausted` included,
  as the automation client does) or the API's own 502 `video_judge_upstream_failed`. Any other
  thrown fetch error, a 200 whose body cannot be read, or any other 5xx (a 500 without a code, a
  gateway's 504 page, the judge route's 502 `upstream_unavailable`) throws a `SiteError` with code
  `video_ai_run_uncertain` (imported as `RUN_UNCERTAIN` from the automation client, no import
  cycle), `who: 'service'`, the response's status (0 for a thrown error), and a message ending
  "Jev may have judged it, so the outcome is unknown and it is not sent again". 4xx refusals were
  already thrown after one request and still are.
- `qa.mjs` needed no change: `failing()` turns the throw into `item('policy', false, message)`, so
  the policy item reads that message; `site.test.mjs` runs `runQa` with the real client and a reset
  after sending and sees one POST and that detail. The lab round (`tools/video/shorts/lab.mjs`
  `qa()`) does not rewrite for a failed `policy` item (it is not in `QA_FIXES`), so the Short goes
  to the owner; a rewrite for another item runs a new QA on a new script, which asks Jev again by
  design.
- The new tests fail on origin/main's `site.mjs` (2 of 5: the lost-answer cases and the QA item)
  and pass with the change; the never-sent, settled, refusal and other-route cases pass on both,
  so they guard the retries that must stay.
