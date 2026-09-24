---
id: 2026-09-24-take-payment-for-the-usage-packs
title: Take payment for the usage packs
status: blocked
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-24T00:30:24Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/usage
  - apps/web/app/[locale]/pricing
---

# Take payment for the usage packs

## Why

The site already sells nothing it could sell. The usage-pack ledger is complete: packages
TRIAL_3 (free), PACK_10 NT$199, PACK_30 NT$499 and PACK_100 NT$1,299 are seeded in
`apps/api/app/usage/service.py:51-112`, each with `purchasable: False`, and the pricing page
shows a disabled 購買即將開放 button (`apps/web/app/[locale]/pricing/page.tsx:57`). Top-ups
happen only through the CLI, via `grant_package` (`usage/service.py:360`), which is idempotent
on `external_reference`: exactly the hook a payment webhook needs.

What is missing is a payment provider, and the choice is the owner's
(`docs/monetization-alternatives.md`, decision D4). Stripe does not open accounts in Taiwan.
Local gateways (ECPay 綠界, NewebPay 藍新, TapPay) and whether an individual without a
business registration may use them, and what e-invoice duty follows, were **not verified**
on 2026-09-24 and are a question for the owner and an accountant.

**Blocked on D4.** It is also premature: the pack only has value to people who come back to
the planner, and nothing measures that yet.

## Definition of done

- [ ] The owner has chosen a provider and settled the invoicing question; both are in Notes.
- [ ] A signed-in user can buy a pack; the provider's confirmed callback grants it through
      `grant_package` exactly once, however many times the callback arrives.
- [ ] A failed, cancelled or refunded payment grants nothing or reverses the grant.

## Steps

- [ ] Owner: provider account, business and invoice question.
- [ ] Callback endpoint that verifies the provider's signature before anything else, then
      calls `grant_package` with the provider's transaction id as `external_reference`.
- [ ] Flip `purchasable` for the packs being sold; enable the pricing button.
- [ ] Legal pages: refund terms, payment processor in the privacy policy (five locales).

## How to verify

```bash
cd apps/api && uv run pytest tests -q -k usage
```

With the provider's sandbox: buy PACK_10, replay the callback twice, balance goes up by 10 once.

## Notes

- Related: `2026-09-14-preview-never-charged` decides what an itinerary preview costs;
  settle it before anything is sold.
