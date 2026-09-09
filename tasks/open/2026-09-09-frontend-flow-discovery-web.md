---
id: 2026-09-09-frontend-flow-discovery-web
title: Editorial discovery and unified collection frontend
status: in-progress
priority: P1
area: web
owner: codex-discovery-flow-web
claimed_at: 2026-09-09T03:36:39Z
created_at: 2026-09-09T03:06:52Z
completed_at:
branch: codex/frontend-explore-flow
depends_on: []
scope:
  - apps/web/components/discovery
  - apps/web/components/saved-items-provider.tsx
  - apps/web/components/saved-items-provider.test.tsx
  - apps/web/lib/discovery.ts
  - apps/web/lib/discovery-copy.ts
  - apps/web/lib/saved-items.ts
  - apps/web/lib/saved-items.test.ts
  - apps/web/lib/frontend-flow-copy.ts
  - apps/web/e2e/discovery.spec.ts
  - apps/web/e2e/discovery-full-stack.spec.ts
---

# Editorial discovery and unified collection frontend

## Why

Make inspiration browsing, saved content and itinerary handoff one coherent flow. The old discovery page repeated the trip search form, hid place facts behind separate pages and exposed two different save systems.

## Definition of done

- [x] Discovery uses five category groups, a compact destination/search toolbar and optional advanced filters, preserving the old homepage when the feature is off.
- [x] Images and titles open a URL-driven accessible detail drawer with current source facts, media and existing hotel booking options.
- [x] One canonical saved key powers one-click save/undo and named-list organization; an auth-return URL only opens confirmation.
- [x] All saved is the default collection view, with server cursor pagination, unavailable tombstones, batch organization/removal and preserved restaurant map links.
- [x] Reads and writes are bound to the active login, old requests are aborted and stale state probes cannot overwrite newer saves or membership refreshes.
- [ ] Root production build and desktop/Pixel 7 acceptance complete with no outstanding blockers.

## Steps

- [x] Coordinate exact discovery category/detail/planning and canonical saved API contracts with backend owners.
- [x] Implement scoped semantic-token CSS and five-language copy without global CSS or shared translation edits.
- [x] Reuse the root-owned TravelPlanAction, existing native dialog, source image authorization, video consent, booking panel and source credits.
- [x] Update existing discovery unit/E2E UI assertions without removing publication/privacy/withdrawal gates.
- [x] Add focused canonical-key, account/late-request, batched-state, URL, save/undo and collection pagination tests.
- [ ] Complete final joint validation and record PR/merge evidence before task closure.

## How to verify

From apps/web: `npx vitest run components/saved-items-provider.test.tsx lib/saved-items.test.ts components/discovery/frontend-flow.test.tsx components/discovery/discovery.test.tsx --maxWorkers=1 --reporter=dot`.

Scoped ESLint: `npx eslint components/discovery components/saved-items-provider.tsx components/saved-items-provider.test.tsx lib/discovery.ts lib/saved-items.ts lib/saved-items.test.ts lib/frontend-flow-copy.ts e2e/discovery.spec.ts e2e/discovery-full-stack.spec.ts`.

Root runs `npm run typecheck:web`, production build and desktop/Pixel 7 Playwright, including the existing discovery and discovery-full-stack suites and new frontend-flow acceptance.

## Notes

- `/saved-items/all` and named lists are account-only and independent of community enrollment. Hotel/service and article/video/guide references are aliases, not duplicate saved rows. Non-restaurant UUID hex normalizes to dashed lowercase; opaque Google Place IDs retain case.
- Save status probes batch up to 100 keys, coalesce sibling-card requests, and carry both mutation generations and per-key probe sequences. They never increment collection mutation revision.
- Each login identity owns its async results and bounded in-memory page snapshots. No browsing history or private content is persisted to browser storage.
- `SavedContentAction({item,returnTo,compact?,resumeEnabled?})` is the integration export. List cards disable resume when a URL detail drawer is present, avoiding duplicate native confirmations. Root owns the matching `TravelPlanAction` planning flow.
- Details render only actual `place_detail_payload` fields. Google weekly text/attribution and durable coordinates are preserved; no fabricated Plus Code, pictures or prices. Existing BookingPanel remains the hotel platform boundary.
- Focused runs before final regression additions passed: discovery 19, new frontend-flow 8, canonical/provider 6. Final aggregate rerun includes the newly added out-of-order membership probe and legacy UUID regressions.
- No source changes outside claimed scope, no source commits or production mutations performed by this agent.
