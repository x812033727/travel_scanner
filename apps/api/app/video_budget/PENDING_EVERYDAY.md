# Everyday-story paid admission

The owner approved a USD 25 **whole-film ceiling** for C03–C07, C10 and C15.
This code does not activate a paid route for any of them. The API rejects
attributed requests and queued subscription-model stages, and current local TTS,
media and automation clients return
`video_budget_preproduction_hold` before dispatch for every `story-everyday-*`
slug. A new client paired with an older API is also held locally.

The speech API still accepts requests that omit both `video_slug` and
`operation_id` for existing non-series workflows. An old TTS/ASR/Jev client
that omits both fields cannot be identified as C-series by the server. Before
deploying or treating this as a production stop, verify that every old C-series
worker is stopped and cannot restart with its old client; confirm that the
current client is installed on every permitted C-series worker. Do not use an
unattributed request to test a held film. Binding paid requests to an
authenticated project identity belongs in the later activation review.

This guard creates no account and changes no migration. C03–C06 used paid
providers before a per-film ledger existed; their unresolved historical
exposure is treated as the full USD 25 ceiling, with **zero newly spendable
balance**. C07, C10 and C15 also have no account. Even a mistakenly inserted
account cannot bypass any of these seven API holds. Other everyday stories have
no paid account and receive the same API and local preproduction hold.

Before a later reviewed activation change removes a hold:

1. Read back the exact narration voice, model, supplier account, region,
   published and account-specific prices, billable units, and bounded retake
   allowance. Reserve the worst payable amount for each TTS, ASR, Jev, image,
   music and text operation under one film ledger.
2. Reconcile C03–C06 historical exposure against provider billing, or retain
   a durable full USD 25 hold in the future migration. A shared delayed project
   total may be used only as a conservative per-film upper bound, never guessed
   into smaller allocations.
   Confirm C07/C10/C15 have no earlier unrecorded charge.
3. Add and verify one separate account per slug in a later migration. Seed
   C03–C06 with full uncertain `pre-ledger-history` operations unless provider
   evidence already establishes an exact safe amount. Keep existing operations
   and account limits. Review the application rollback path before deployment.
4. Read back stable operation IDs, reservations, uncertain holds, settled
   charges, remaining balance, and the supplier's separate available balance.
   A new attempt must never erase an earlier hold.
5. Only then remove the client and API admission holds in a reviewed change.
   After actual narration, measure the body after the intro at **at least 480
   seconds** before buying illustrations; verify the finished illustration
   share separately.

A later migration would change the Alembic head. The current API image does not
recognize that future head as a rollback state. Deploy a reviewed compatibility
release and pass a real PostgreSQL/Compose rollback check before that migration.
This document, a green PR, or account creation alone does not authorize a
provider call, STOP removal, upload, or publication.

## C03 Moleskine activation (owner decision 2026-10-24)

The owner closed C03's pre-ledger exposure at the **full USD 25 ceiling** instead of
reconciling provider billing, and activated the film for the work that finishes it:
one narration line (`c031202`), its transcription and judge, then the unpaid clips,
assembly, captions, QA and packaging. Concretely:

- `ACTIVATED_STORY_SLUGS` (API `models.py`, local `pending-pilot-budget.mjs`) removes
  C03 from the admission hold in the API and in the TTS, media and automation clients.
  C04–C07, C10 and C15 and every other `story-everyday-*` slug stay held exactly as above.
- On the host, after deployment, the 0138 `pre-ledger-history` row is settled with
  `reconcile_cli --action settle --expected-status uncertain --actual-usd 25
  --evidence-ref owner-decision-20261024-c03-full-ceiling`. Only that exact settlement
  (full ceiling, that receipt) is excluded from C03's balance; an uncertain row or any
  other settlement still counts in full, so C03 stays exhausted until it is applied.
  The row is never deleted: rollback verification and every readback still see it, and
  `summary`/`inspect` report it as `historical_closed_usd`.
- The USD 25 ceiling therefore guards C03's post-activation work only. The owner accepted
  that the film's all-in cost is the closed historical exposure plus that work.

## Story remakes (owner decision 2026-10-26)

The 2026-10-25 remakes are new films under new slugs (`story-everyday-*-remake-20261025`).
None of them has paid history, so none needs a `pre-ledger-history` hold, and none
borrows the original slug's account: an original's held or exhausted account stays
exactly as above.

- **C11 UCC remake** (`story-everyday-ucc-c11-remake-20261025`): the owner approved a
  USD 25 whole-film ceiling and about ten minutes. 0140 creates its account
  (`video_pilot_budget_0140_owned`), and `ACTIVATED_STORY_SLUGS` (API `models.py`,
  local `pending-pilot-budget.mjs`) admits it. `REMAKE_PILOT_LIMITS_USD` holds its
  ceiling apart from `C_SERIES_PILOT_LIMITS_USD`, whose exact set the 0138 and 0139
  rollback readbacks still expect. The 0139 compatibility image (#1870) holds it.
- **C14, C03, C04, C06, C05, C08 remakes**: the owner asked for them next under the same
  terms. The 0140 image (#1875) accepts the additive 0141 contract of their six USD 25
  accounts (`migration_guard._verify_reviewed_0141`) and keeps them held. 0141 creates the
  accounts (`video_pilot_budget_0141_owned`) and `BATCH_REMAKE_SLUGS` activates them, in
  the release after the 0140 image is deployed.

Before the first paid call of each remake, report its narration characters, image count
and the total to the owner, then read back `reconcile_cli` / `inspect` for its account.
