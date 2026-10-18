---
id: 2026-10-11-a-sent-back-newest-languages-batch
title: A sent-back newest languages batch leaves every part unfinished and the worker re-sending it
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T00:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_youtube/language_package.py
  - tools/video/review/sync.mjs
---

# A sent-back newest languages batch leaves every part unfinished and the worker re-sending it

## Why

Found by the review of `2026-10-10-let-the-owner-re-request-a` (finding
`e2e-made-sent-back-after-pending-card`). When the newest `languages` batch of a video is
sent back and no approved batch stands behind it:

- `language_states()` counts only pending and approved batches, so every chosen part
  reads 尚未完成 again;
- the worker sees the parts as working, builds the same batch, and `submit_review` answers
  with the rejected review for the identical `content_sha256`: no card appears, and the
  worker sends it again every unit;
- `language_package.compose()` and `review-push` both take the newest languages batch by
  `created_at` whatever its status, so YouTube sync refuses the video (「最新語言包尚未核准」).

It predates the dub retry, but the retry makes it reachable on the path the cost sentence
advises: ask for a skipped dub again while the first languages card is still pending (the
new batch supersedes it), then send the new card back. The retry itself now says so in the
cell (`dubRetryMadeSentBackAlone`) and offers no button; nothing gets the video out.

Restoring the superseded review in `decide()` does not work as it is: `submit_review` ends
with `store.keep_only(slug, kept_files(...))` and `kept_files` drops the files of a batch
superseded while pending, and both consumers above would still read the rejected batch as
the newest.

## Definition of done

- [ ] After the owner sends back the newest languages batch, the page says what happens
      next and something on it leads to a new batch (a note acted on, or the previous
      pending batch back with its files).
- [ ] The worker does not re-send a batch the site answers with a rejected review every
      unit; it waits or reports once.
- [ ] YouTube sync reads the newest batch that counts, or says which batch blocks it.

## Steps

- [ ] Decide with the owner what "send back" on a languages card means (redo which part,
      on whose note).
- [ ] `kept_files`, `language_package.py`, `sync.mjs` together; the last two are bound by
      the duration review receipt.

## How to verify

API and automation tests for: a first batch pending, a retry's batch superseding it, the
new card sent back; then the cell, the worker's next unit and `compose()`.

## Notes

- `apps/api/tests/test_video_dub_retry.py` already pins today's state from a pending first
  batch (all parts working, the request stays `made`, the click is 409).
