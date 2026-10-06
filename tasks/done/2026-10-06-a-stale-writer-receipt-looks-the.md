---
id: 2026-10-06-a-stale-writer-receipt-looks-the
title: A stale writer receipt looks the saved job up and archives it when it is over instead of blocking the video
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T05:56:11Z
created_at: 2026-10-06T05:55:39Z
completed_at: 2026-10-06T15:57:29Z
branch: claude/video-unstuck-stale-receipts
depends_on: []
scope:
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# A stale writer receipt looks the saved job up and archives it when it is over instead of blocking the video

## Why

On the production host (2026-10-06) the video `ai-term-knowledge-cutoff` was blocked with
"writer may have run on the server without its answer reaching the worker (stage inputs
changed while a saved run is unfinished; restore its exact inputs or inspect the receipt
before an owner retry)". The durable writer keeps a journal per request under
`run-receipts/`; `find()` compared every unfinished journal of the same stage and variant
by `unitSource` (everything in the request except `today` and `lexicon`: the whole
instructions text, the fetched source pages, the owner's notes, stance and voice) and
threw `video_ai_receipt_input_changed` when it differed. Every deploy that changes
`prompts.mjs` and every settings edit therefore invalidated the writer journals in flight;
`client.mjs` wrapped the error as RUN_UNCERTAIN and `flow.mjs` blocked the video for the
owner. The owner's retry archived only `uncertain` receipts (or `succeeded` ones when the
reason said inputs changed); a `queued`/`running` journal stayed and the next round
blocked again.

The money (subscription usage) is spent either way. A finished job's stale journal can be
archived on the worker's own authority; only a job still queued/running (wait) or
uncertain (the owner looks) deserves care.

## Definition of done

- [x] A stale journal (same stage/variant, different inputs) is no longer a block by
      itself: `find()` reports it with `stale: true`, and the client reconciles it with the
      server before the current request starts.
- [x] Reconciliation: no receipt → archived, no lookup; saved `failed` → removed; else one
      GET of the job: `succeeded` → archived, `failed` → removed, `queued`/`running` →
      RUN_PENDING (the worker waits a round), `uncertain` → RUN_UNCERTAIN whose message is
      the receipt's own `error_detail` followed by the familiar "inputs changed" sentence
      (the owner looks); a settled 4xx from the lookup (404 `video_ai_job_not_found` after a
      re-pair, 409 `video_ai_job_input_changed`, 400/422) → the journal is archived with a
      reason naming the answer and the new request proceeds; a lookup that fails otherwise
      (5xx, 408, 429, network, a broken body) → RUN_PENDING, never a block.
- [x] The archive written on the worker's authority carries
      `owner_retry: { request_id: null, reason: "inputs changed; the saved run is terminal" }`;
      the journal is moved with the Windows-tolerant rename, never unlinked and rewritten.
- [x] An owner retry on a still-running stale journal throws RUN_PENDING and leaves the
      journal and the retry request in place; a plain failed journal is cleared by it.
- [x] `prepare()` still refuses to create a second journal beside an unreconciled stale one.

## Steps

- [x] `run-receipts.mjs`: `find()` returns `{ file, record, stale: true }` (an exact match
      anywhere in the directory still wins); `prepare()` throws the input-changed error for a
      stale result; `archive()` gains `autoArchive` for a non-adopted success or a journal with
      no receipt and no policy hold; `retryCandidates()` lists plain failed journals.
- [x] `client.mjs`: `fetchJob`/`lookupReceipt` shared by `durableRun`, `retryRuns` and the new
      `reconcileStale`; `run()` reconciles every stale journal before `durableRun`; `retryRuns`
      removes plain failures up front, throws RUN_PENDING on a fresh `queued`/`running`
      status, removes a fresh `failed`, and lets RUN_PENDING through its catch.
- [x] Tests rewritten and added in both suites (see below).

## How to verify

```bash
node --test tools/video/automation/run-receipts.test.mjs tools/video/automation/client.test.mjs
node --test tools/video/automation/automation.test.mjs   # exercises the client through flow.mjs
node tools/video/long-form/cli.mjs check                  # these files are outside the duration receipt
npm run check:tasks
```

Results on Windows (Node 24), after the review round: receipts 18 pass + 1 POSIX-only
skip; client 29 pass; automation 115 pass; long-form check PASS (473 plans); task files
valid.

On the host, after deploy: the blocked video's next round should log "writer is still
running; its saved receipt will be checked next round" (RUN_PENDING) or start the writer
with the current prompt, and `run-receipts/archive/` of that video should hold the old
journal with `owner_retry.request_id: null`. If the stale job's server state is `uncertain`,
the video stays blocked with the same wording as before and the owner's retry clears it.

## Notes

- `flow.mjs` was not edited. Verified path for the retry case: `bookkeeping()` (flow.mjs
  :814) rethrows every non-POLICY_HOLD error from `retryRuns` before it sets
  `state.retry_request_id`; `step()` (:736) turns RUN_PENDING into `later()`, so the retry
  id is not consumed and the next round looks the job up again. For the run path, `stage()`
  (:656) and `move()` (:888) already handle RUN_PENDING via `step()` and RUN_UNCERTAIN via
  `unanswered()`; the stale errors carry `slug` and `stage` for `later()`'s line.
- `prepare()` throws rather than returning a stale entry: a caller that has not reconciled
  must never poll the old job as if it matched the new inputs, nor create a second journal
  beside it. `find()` is the only way to see `stale`.
- `lookupReceipt` classifies its answer once for every caller: 401/403 and owner-coded
  answers are owner errors (the same class every other call raises for a bad token); a
  settled 4xx (400–499 except 401/403/408/429) marks the error `gone: { status, code }`,
  which `reconcileStale` and `retryRuns` turn into `archive(entry, { autoArchive: true,
  gone })` with the reason "the server no longer has this job (404 video_ai_job_not_found)";
  5xx, 408, 429, network and a broken body become RUN_PENDING in the run path and the
  existing "could not verify … retained" RUN_UNCERTAIN in the retry path. Review of the
  first version found that a settled 4xx looped as RUN_PENDING for ever (the same stale
  journal found first every round) — hence this classification. A `RunReceiptError` from
  the lookup's `receive` (mismatched identities) still becomes RUN_UNCERTAIN through the
  existing fail-closed wrapper in `run()`. A policy-held journal whose job is gone is not
  auto-archived: the policy retry is verified by its job, so it stays for the owner.
- `archive()`'s `gone` authorization applies to any saved receipt status (the server's
  answer, not the receipt, is what settles it), never to a policy hold or an adopted
  journal; a journal with no receipt is archived as never dispatched instead. The store
  only checks the shape (integer 4xx status, string code); the client classifies.
- `retryRuns` checks STOP for every candidate before anything is mutated: plain failed
  journals are listed, skipped by the "mixed set with a policy hold" check (so a failure
  beside a policy hold cannot make the policy retry ambiguous), and removed only in the
  second loop after the second STOP check, like every other mutation there.
- The uncertain stale error's message is `${receipt.error_detail}; ${INPUT_CHANGED_MESSAGE}`
  (`why` the same), because `flow.unanswered()` puts the message on the owner's card and the
  real cause (for example the 403 text) matters more than the input-changed sentence; the
  suffix keeps "inputs changed" so a later owner retry still archives on that reason.
- Tests: `run-receipts.test.mjs` — stale find + prepare refusal + reconciled prepare;
  auto-archive authorization (succeeded and never-dispatched yes; running, failed, policy
  hold, adopted no); `retryCandidates` lists plain failures; the archive rename test now
  loops over the owner path and the auto path and checks the moved bytes. `client.test.mjs`
  — succeeded stale journal archived after exactly one GET and one new POST; never-dispatched
  journal archived with no GET; `uncertain` → RUN_UNCERTAIN (who owner, receipt_code);
  502 / network error / half body → RUN_PENDING with the journal byte-identical; running
  stale journal → RUN_PENDING after one GET; lookup 404 / 409 / 422 → archived with the
  answer named and exactly one new POST, 408 / 429 → RUN_PENDING with the journal intact;
  the uncertain message carries the receipt's `error_detail`; `retryRuns` with `queued` →
  RUN_PENDING, journal kept; with a plain `failed` journal under STOP → refused and the
  journal left in place, without STOP → deleted; with a lookup 404 → archived with the
  gone reason; the existing failed-lookup case (:501) unchanged. Store: `gone` archives
  running / uncertain / succeeded receipts, refuses a policy hold, a non-4xx status, a
  missing code or a missing `autoArchive`.
- Windows: the combined run once hit a real transient EPERM on a journal save (the retry
  helper absorbed it, but the test's injected wait list then had seven extra entries). The
  suite passed alone three times in a row and together once more; the same flake class is
  documented in 2026-10-05-windows-stage-receipt-rename.

- 2026-10-06: landed on main as 6d7985fa (PR #1337); closed in the board sweep that carried train #1346's complete PRs.
