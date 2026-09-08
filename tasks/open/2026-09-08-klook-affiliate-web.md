---
id: 2026-09-08-klook-affiliate-web
title: Klook affiliate frontend channels and contextual discovery
status: in-progress
priority: P1
area: web
owner: codex-klook-web
claimed_at: 2026-09-08T16:32:56Z
created_at: 2026-09-08T16:32:56Z
completed_at:
branch: codex/klook-product-integration
depends_on: []
scope:
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/admin.test.tsx
  - apps/web/components/travel-services/hotel-admin.test.tsx
  - apps/web/lib/klook-affiliate-copy.ts
  - apps/web/lib/klook-affiliate-messages
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/components/travel-services/catalog.tsx
  - apps/web/components/travel-services/catalog.test.tsx
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
  - apps/web/app/[locale]/destinations/[destinationId]/services/page.tsx
  - apps/web/lib/travel-service-discovery.ts
  - apps/web/lib/travel-service-discovery.test.ts
---

# Klook affiliate frontend channels and contextual discovery

## Why

Existing partner forms assume every brand uses Travelpayouts. Klook direct affiliate approval must remain independent, and reviewed booking/discovery options should be accessible within the existing travel-service catalog without implying pricing API access.

## Definition of done

- [x] Klook direct and Travelpayouts brand evidence, activation and optimistic versions are independent.
- [x] Existing hotel/tour/transfer/esim catalog surfaces contextual reviewed destination discovery without a new intrusive trip panel.
- [x] Direct review can explicitly record browser evidence, scoped to the exact row version; no automatic attestation.
- [x] Focused tests, TypeScript and ESLint pass.
- [ ] Parent completes responsive E2E and overall release validation.

## Steps

- [x] Add independent five-locale copy, channel labels, affiliate ID field and no-pricing-API clarification.
- [x] Filter discovery modules and destinations, normalize Osaka/Kyoto, abort stale requests and separate exact products from destination links.
- [x] Complete unit regressions and hand off tested changes.

## How to verify

`npm exec --workspace apps/web -- vitest run components/travel-services/admin.test.tsx components/travel-services/hotel-admin.test.tsx components/travel-services/catalog.test.tsx components/destination-affiliate-options.test.tsx components/admin-settings-panel.test.tsx lib/travel-service-discovery.test.ts --pool=threads --maxWorkers=1`

`npm run typecheck:web`; focused ESLint on owned TypeScript files. Parent owns `e2e/travel-services.spec.ts` and browser validation.

## Notes

- Channel contract: `travelpayouts | klook_direct`, legacy omission means Travelpayouts. Direct only applies to Klook. Direct create/update omits static tracking URLs.
- Existing six-city product catalog is not broadened. Other public destinations retain category-specific reviewed discovery. Do not modify `stay-area-flow.tsx`, Stay22 files or the old trip affiliate tools panel.
- Source instructions read: root/web AGENTS and task protocol; Next use-client/page docs read from the already installed adjacent worktree while this worktree's dependencies were being installed.
- Final focused Vitest: 84 tests passed across six files. Whole-web TypeScript and focused ESLint (all 13 owned TypeScript files) passed; `git diff --check` passed. No live API, quote, approval, commit or publish calls were made by this subtask.
- Brand selection captures the original row version instead of following later metadata snapshots. Unselected brand editors remain hidden rather than misrepresenting an approved account as pending. Successful writes may update only the selected channel's baseline.
- Osaka/Kyoto trip destinations normalize to one canonical destination; the dual-city destination page displays common discovery only once. `showDestinationDiscovery` defaults true for existing catalog callers.
