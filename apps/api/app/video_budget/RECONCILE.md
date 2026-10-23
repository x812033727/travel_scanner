# Pilot budget reconciliation

This is a host-only operator procedure for every budgeted slug in `models.py`. The
ledger counts `reserved` and `uncertain` at their full ceiling until a real provider record
settles the charge or proves no charge. A timeout, failed job, missing output, old age, or
empty wallet screen is not no-charge evidence. Do not manually update the database or
repeat a paid request to test its status.

Run the CLI inside the deployed API container. Inspection is read-only:

```sh
python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2
python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2 --operation-id OP
```

Record the exact slug, operation ID, category, provider, model, ceiling, status, and related
media job ID/status/vendor task reference. Check the provider's task record **and** invoice or
usage ledger for this request. The CLI cannot see provider billing, so it cannot decide whether
the provider charged. Keep the dated invoice row, provider support case, or task-detail export
in the operator's private evidence store. Use its opaque ID as `--evidence-ref`; do not put
API keys, signed URLs, customer data, or the evidence document itself in CLI arguments.

If an exact billed amount is known, first preview and then apply with the same arguments:

```sh
python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2 \
  --operation-id OP --action settle --expected-status uncertain \
  --actual-usd 0.042 --evidence-ref invoice-20261015-row-7
# Review the JSON and provider evidence, then repeat with --apply.
```

If the provider confirms **no task and no charge**, preview and then apply `release`:

```sh
python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2 \
  --operation-id OP --action release --expected-status uncertain \
  --no-charge-reason "provider confirms no task or invoice" \
  --evidence-ref vendor-case-123
# Review the JSON and provider evidence, then repeat with --apply.
```

For a `queued` or `submitted` media job, before either action first pause all clients and
pollers that can advance this job, confirm no API request is still executing it, and use
`--worker-stopped`. The CLI also
checks its Redis execution lock and refuses a present or unavailable lock. Absence of the lock
alone is insufficient because a long request could outlive its lease. A `ready` media job
cannot be released. Applying no-charge marks a linked media job as failed with
`video_media_no_charge_reconciled`; the existing retry path will assign a fresh operation ID.
The old ID stays closed with its evidence, so it cannot dispatch twice. If a late invoice later
shows a charge, settle that closed ID with the new invoice reference and `--expected-status
released`; the original no-charge evidence remains in its release reason.

The separate monthly Redis image/clip/music unit meter keeps its original reservation after a
no-charge reconciliation. This is conservative: a later retry may hit the monthly unit limit
even when the USD ledger has room. Do not reset or decrement that Redis counter by hand; its
repair needs a separate idempotent receipt so a repeated operator command cannot undercount it.

After any `--apply`, rerun inspection and compare the account totals and media state.
`overrun_operations` counts individual charges above their reservation; it can remain zero
when a late invoice makes settled charges plus outstanding holds exceed USD 25. Check
`total_over_limit`, `over_limit_usd`, and `remaining_usd` as well. A settlement above its
reservation is recorded as an overrun and stops new spending; the CLI exits nonzero and
inspection confirms the persisted charge. Any unresolved or unavailable provider evidence
keeps the full hold. No reconciliation action calls a media provider.

Finished-film acceptance requires no unresolved reservations or uncertain operations,
settled total at or below USD 25, `total_over_limit=false`, and a match to the provider's
billing statement for every paid operation. A zero `overrun_operations` count alone is not
evidence that the film stayed within budget.

If a provider invoice contradicts an automatically released operation, this CLI cannot
correct that release. Stop pilot spending and acceptance, retain the invoice, and open a
separate controlled correction. Never ignore a charge because the local row says `released`.

## Everyday-object stories awaiting a ledger

The current guard creates no new account or operation. C03–C06, C07, C10 and
C15 are held for attributed API requests and at the current local paid-client
boundary. Legacy speech clients can omit attribution entirely; the server
cannot infer a C-series slug from such a request. Keep old workers stopped and
verify the current client on every C-series worker before a production rollout.
A provider bill alone does not activate paid work. Any other
`story-everyday-` slug fails closed with
`video_budget_missing_account` until a reviewed migration opens its account:
the local TTS, media and automation clients attribute every slug in the series.

C03–C06 called TTS, transcription, Jev and (C03) media before they had accounts.
Until a future migration seeds a full USD 25 uncertain `pre-ledger-history`
operation for each, they have no newly spendable balance. Their local STOP files
stay under separate owner control. What the local workdirs showed on 2026-10-23
(empty speech journals do not establish the provider's charge or request state):

| Slug | Recorded paid requests | Worst case from the server's per-request ceilings |
| --- | --- | --- |
| `story-everyday-moleskine-c03` | 94 TTS, 94 transcriptions, Jev for 27 lines, plus a media ledger of USD 1.713 (118 MiniMax images, 122 Gemini judges, one Lyria track, 2026-10-21 15:51Z to 2026-10-22 01:50Z) | about USD 113 |
| `story-everyday-bubble-wrap-c04` | One `tts` run refused by Gemini (HTTP 429); no WAV, cache, timeline or media | none recorded |
| `story-everyday-kincho-c05` | 79 TTS, 79 transcriptions, one Jev call (34 lines) | about USD 93.5 |
| `story-everyday-play-doh-c06` | 94 TTS after one 429-refused run, 71 transcriptions from an unfinished `check-audio`, no Jev | about USD 87.5 |

The ceilings are `PILOT_GEMINI_TTS_MAX_USD` (USD 0.151552 per TTS) and, because the
pre-ledger transcription route set no output limit, the full model bound of USD 1.032192
per transcription. Those exceed USD 25, so request counts alone cannot clear the exposure.
Only provider billing can show the actual charge.

Before creating or settling a historical hold, read each provider's usage for its billing project over the
window from the film's first paid call to its STOP. Read AI Studio / Cloud Billing at least
48 hours after the last call, because that bar lags. The window's whole project total is an
upper bound for any single film even when several films shared the key: settling at that
total (plus the film's MiniMax and Jev totals for the same window) over-counts and never
under-counts. Record the evidence in the private store. Only after a separately
reviewed migration has seeded a durable hold may an operator preview settlement
with `reconcile_cli`, using the exact billed upper bound and private evidence
reference as described above. The current guard has no such operation to settle.

The film stays stopped after settlement until the separate account, voice,
model, region and price review lifts its API and client hold. C04's run shows a
provider refusal and no recorded take. A
release with `--no-charge-reason` still needs the provider's usage or invoice for that
window showing no charge, since a refused run alone is not no-charge evidence under the
rules above. Removing a STOP file is a separate owner decision after the readback, and
neither action calls a provider.
