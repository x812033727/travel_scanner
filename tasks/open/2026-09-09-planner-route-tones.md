---
id: 2026-09-09-planner-route-tones
title: Route apply state regression and semantic itinerary tones
status: in-progress
priority: P1
area: web
owner: codex
claimed_at: 2026-09-09T03:38:23Z
created_at: 2026-09-09T03:36:20Z
completed_at:
branch: codex/planner-route-tones
depends_on: []
scope:
  - .github/workflows/planner-premium.yml
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/components/route-map.tsx
  - apps/web/components/route-map.test.tsx
  - apps/web/components/system-itinerary-card.tsx
  - apps/web/components/system-itinerary-card.test.tsx
  - apps/web/components/planner/optional-stop.tsx
  - apps/web/components/planner/optional-stop.test.tsx
  - apps/web/components/planner/stop-tone.ts
  - apps/web/components/planner/stop-tone.module.css
  - apps/web/components/planner/route-panel.module.css
  - apps/web/e2e/planner-route-tones.spec.ts
  - apps/web/e2e/full-stack.spec.ts
  - apps/web/messages/en/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
---

# Route apply state regression and semantic itinerary tones

## Why

Applying a mode/buffer change from daily route settings can remount the drawer with old entry overrides and hide the saved route. Explicit querying also exposed repetitive idle warnings. Hotel, lunch and dinner summaries lose semantic color in both themes.

## Definition of done

- [x] Applied route stays selected after version updates; preview/apply remain explicit.
- [x] Idle/loading/preview/applied/stale/external/error states are truthful and concise.
- [x] Selected path availability controls schematic map messaging.
- [x] Hotel blue, lunch amber and dinner violet work in collapsed, expanded and optional rows in both themes.
- [ ] Five locales, accessible contrast/targets and mobile layout pass regression validation.
- [ ] PR created with checks; do not merge or deploy without later authorization.

## Steps

- [x] Parent route synchronization and integration regression.
- [x] Route panel/map state and scoped layout.
- [x] Shared role tones and system-card semantics.
- [ ] Browser fixtures, full Web checks and CI smoke.

## How to verify

Run lint:web, check:i18n, typecheck:web, Vitest single worker, production build, focused Playwright and CI full-stack smoke. Reproduce transit/10 -> walk/15 -> query -> apply -> new version in an isolated fixture; never write to the existing production Tokyo trip.

## Notes

Base origin/main 7cee8650. Prior PR #373 closure cherry-picked to release its owned scope. No API, schema, provider keys, globals.css, new-trip-form or navigation changes. Merchant-style owner released five trips locales via ebd94ce (cherry-picked ee850491) before they were added to this claim. Root owns trip-editor/E2E/task; delegates own distinct components.

Regression evidence: provider/manual daily-entry apply both failed selected mode after version increment before the parent fix and passed after it (2 tests). Initial focused run 126 passed/4 failed: three new assertions accidentally matched a hidden zero-minute buffer option and one retained old hotel help text; assertions corrected without changing product guarantees. Read-only cross-review caught valid late-reservation conflict routes being filtered; provider/manual/estimated provenance now preserved with five new regression cases.

Local lint and production Turbopack build/TypeScript/252 pages passed. First two CI Planner UX runs passed including all five locales, themes and route apply; screenshots exposed initial 62dvh route sheet concealing map, so the route now opts into existing defaultExpanded and tests require visible/unoccluded map and instruction. Full-stack smoke first runs failed only a selector matching both new collapsed role badge and expanded hotel label; narrowed to existing systemCards. Final CI and local full Vitest still pending; do not claim final acceptance yet.

At c75fa588 CI full Web Vitest and full-stack smoke passed. The complete local Vitest stalled after an unrelated admin async timeout on the busy shared host; stopped only its verified owned process and rely on the isolated CI full-suite result. New browser tests initially stopped before collection because ESM JSON imports needed attributes; corrected and collection passed. Desktop navigation tests exposed legacy align-items:start collapsing the newer flex inline-size container to 2px; a real Chromium exact-styles reproduction confirmed align-items:stretch restores width and hit-testing. Added 1280px narrow-drawer pointer regression alongside 390/920px. Palette review also restored grid centering for timeline markers. Final head browser acceptance remains pending.
