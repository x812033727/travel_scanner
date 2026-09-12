---
id: 2026-09-12-affiliate-readiness-matrix
title: Affiliate readiness matrix and per-module status
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T05:36:46Z
created_at: 2026-09-12T05:34:50Z
completed_at: 2026-09-12T12:08:18Z
branch: claude/affiliate-controls-and-guide-cta
depends_on: []
scope:
  - apps/api/app/affiliates/schemas.py
  - apps/api/app/affiliates/router.py
  - apps/api/app/admin/service.py
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_admin_readiness.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
---

# Affiliate readiness matrix and per-module status

## Why

`GET /affiliates/status` existed with no consumer, and `partner_configured` (per partner) and
`partner_supports_module` (per module) disagree on purpose for Klook: an AID alone powers
reviewed catalog offers but none of the generic search or trip buttons. The card showed a
green light while the front end rendered nothing.

## Definition of done

- [x] `AffiliatePartnerStatus.supported_modules` lists the modules a button can render today.
- [x] The affiliate category of `/admin/settings` shows a partner by module matrix above the cards.
- [x] The Klook card says what an AID-only configuration powers and what still needs a template.
- [x] `affiliate_link_cache_ttl_seconds` and `affiliate_clickout_token_ttl_seconds` are editable on
      the Travelpayouts card instead of environment-only.

## Steps

- [x] Schema field, status route, card message, card fields.
- [x] `AffiliateReadinessMatrix` in `admin-settings-panel.tsx`; ASCII headers until keys are free.

## How to verify

```
cd apps/api && uv run pytest tests/test_affiliates.py tests/test_admin_readiness.py tests/test_admin_provider_settings.py -q
cd apps/web && npx vitest run components/admin-settings-panel.test.tsx
```

## Notes

`partner_configured("klook")` deliberately keeps requiring only the AID (catalog offers) and
`partner_supports_module` keeps requiring the template (legacy options); the matrix makes the
difference visible rather than collapsing it.
