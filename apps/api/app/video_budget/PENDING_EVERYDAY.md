# Everyday-story paid admission

The owner approved a USD 25 **whole-film ceiling** for C03–C07, C10 and C15.
This code does not activate a paid route for any of them. The API and current
local TTS, media and automation clients return `video_budget_preproduction_hold`
before dispatch. A new client paired with an older API is also held locally.

This guard creates no account and changes no migration. C03–C06 used paid
providers before a per-film ledger existed; their unresolved historical
exposure is treated as the full USD 25 ceiling, with **zero newly spendable
balance**. C07, C10 and C15 also have no account. Even a mistakenly inserted
account cannot bypass any of these seven API holds.

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
