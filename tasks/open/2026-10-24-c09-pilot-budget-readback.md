---
id: 2026-10-24-c09-pilot-budget-readback
title: Read back C09 prior spend and whole-film budget before paid admission
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-24T06:28:22Z
completed_at:
branch: codex/c09-patagonia-script-repair-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09/reviews/budget-readback.md
---

# Read back C09 prior spend and whole-film budget before paid admission

## Why

C09 has a reviewed nonpaid quote in
`docs/videos/story-everyday-patagonia-c09/production-quote.md`, but the repo's
`C_SERIES_PILOT_LIMITS_USD` does not include this slug and the
`story-everyday-` paid route fails closed. The local C09 media workdir and
ledger are absent; that does not prove zero historical spend. Account-side
pricing, prior spend and uncertain requests must be read back before any paid
admission work. The owner approved the exact quote's all-in US$25 cap on
2026-10-24; this approval does not remove the paid hold.

## Definition of done

- [ ] A dated C09-only receipt names the actual provider account/model/region,
      applicable prices, billed prior requests, uncertain requests and the
      resulting remaining whole-film allowance, with source snapshots/IDs.
- [ ] The receipt states whether a durable per-episode US$25 hard stop could
      safely be activated. It does not itself remove any hold or spend money.

## Steps

- [x] Claim only the receipt path through the normal task board; do not force
      claim budget code or reuse another episode's owner approval.
- [ ] Read vendor billing and the persisted C09 budget route without sending a
      paid request; reconcile unknown outcomes at full reserved value.
- [ ] Owner approval of the C09 whole-film quote is documented in
      `docs/videos/story-everyday-patagonia-c09/reviews/owner-paid-pilot-approval-20261024.md`.
      After a reviewed budget-route code change, verify the host readback and
      exact US$25 stop.

## How to verify

Compare the provider billing rows with the receipt's request IDs and amounts;
read back the C09-only budget account and reserved/settled/uncertain totals;
check that a request with insufficient remaining allowance is refused before
provider dispatch. Keep actual paid probes disabled for this ticket.

## Notes

The approved quote caps 67 illustrations, up to 201 image/judge attempts, 77 first
TTS takes plus at most one evidence-backed redo per line, up to 154 ASR checks,
four Jev batches and one Lyria track, all subject to US$25. The US$2.7935
visible media figure includes a Gemini judge *internal estimate*, not a vendor
ceiling. Gemini per-call conservative reservations can exhaust the approved
cap before the quantity maxima. Owner approved the US$25 all-in local pilot
cap, while the single-episode route, account prices, old spend and uncertain
requests remain HOLD. No backend state was read or written in this task update.
