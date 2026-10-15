# Pilot budget reconciliation

This is a host-only operator procedure for the four A01/B18 original and v2 slugs. The
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

After any `--apply`, rerun inspection and compare the account totals and media state. A
settlement above the reservation is recorded as an overrun and stops new spending; the CLI
exits nonzero and inspection confirms the persisted charge. Any unresolved or unavailable
provider evidence keeps the full hold. No reconciliation action calls a media provider.
