# C10/C15 whole-film budget admission

C10 OXO and C15 FriXion each have an owner-approved **USD 25 whole-film ceiling**. This
change only makes their paid paths fail closed. It does **not** create a spendable account,
authorize the first speech request, or change the C03–C06 prior-charge hold in PR #1684.

`PENDING_PILOT_LIMITS_USD` records the two approved ceilings separately from
`PILOT_LIMITS_USD`, which lists funded accounts. The API recognizes C10/C15 as pilots
but rejects reservation before dispatch even if somebody mistakenly inserts an account
row. The local TTS, media, and automation clients refuse their paid requests before
contacting the API, protecting a new client paired with an older server that does not
recognize these slugs. No migration seeds C10/C15 accounts in this change.

Before an activation change removes these holds:

1. Read back the exact narration voice, model, supplier account, region, published and
   account-specific prices, billable unit, and bounded re-recording allowance. Reserve
   the worst payable amount for each TTS, ASR, judge, image, music, and text operation.
2. Reconcile or retain full possible charges for C03–C06; do not subtract a shared
   delayed supplier total from a single episode by guesswork. Confirm no earlier C10
   or C15 operation has an unrecorded or unknown charge.
3. Add one migration to seed **separate** USD 25 C10 and C15 accounts, with a reviewed
   upgrade/rollback order. Keep every old operation row and the old pilots' limits.
   Move the slugs into the funded map only after the new account set and migration guard
   can be read back safely on the host.
4. Verify the stable operation IDs, reservations, uncertain holds, settled charges and
   remaining balance across all paid routes. New attempts must not erase earlier holds.
   Verify the supplier's available balance separately from this local ledger.
5. Only then remove the client and API admission holds in a reviewed activation change.
   After actual narration, measure the body after the intro at **at least 480 seconds**
   before buying illustrations; verify the finished illustration share separately.

Until those steps are complete, any paid C10/C15 attempt must stop without a vendor POST.
