---
id: 2026-09-09-clarify-stay22-module-switch
title: Clarify the modular hotel affiliate switch and original-channel fallback
status: in-progress
priority: P1
area: web
owner: codex-stay22-module
claimed_at: 2026-09-09T13:15:13Z
created_at: 2026-09-09T13:15:12Z
completed_at:
branch: codex/stay22-modular-toggle
depends_on: []
scope:
  - apps/web/components/travel-services/stay22-admin.tsx
  - apps/web/components/travel-services/stay22-admin.test.tsx
  - docs/stay22-module-switch.md
  - .github/workflows/ci.yml
---

# Clarify the modular hotel affiliate switch and original-channel fallback

## Why

The user requested a modular on/off switch, supplied an actual Stay22 Hub Script
and explicitly accepted its seven-platform LinkSwap, Spark and Nova scope. Existing
Allez is already a separately validated native clickout module, so distinguish it
from browser Script execution rather than imply the three OTA boxes control LMA.

## Definition of done

- [x] The admin sees saved mode separately from unsaved preview and can disable without losing settings.
- [x] Allez and full Script modes have accurate scope, LMA ID validation and five-language explanations.
- [x] Save failures preserve form and confirmed mode; admin never executes the third-party Script.

## Steps

- [x] Inspect actual Hub details and editing restrictions in Chrome; user approved full scope.
- [x] Add mode, Script ID, preserved settings and explicit document lifecycle explanation.
- [ ] Validate UI, document separate native/Script contracts and hand over the feature PR.

## How to verify

Vitest stay22-admin tests, TypeScript, ESLint, i18n, production Next build and
browser fixtures. Root isolation and backend config/options each have their own
claimed task; no real Stay22 traffic or booking is generated in CI.

## Notes

Hub ID supplied by the user: 6aa15a455ff1d17f658d1692, domain mokaair.com.
Hub showed Inactive, seven platforms plus Spark/Nova enabled and no self-service
switch for excluding providers/features (must contact Stay22). The user accepted
that full scope. Reading Hub or showing enabled config is not proof of tracking.
The previous d9ef8fcd first-click fix is live; this new Script work is not merged or
deployed. Canonical dirty checkout remains untouched.

Admin focused tests: 10 passed before final explanatory copy additions. Full
ESLint, i18n, 27 tooling tests, Ruff, mypy (291 files) and final production Next
build (267 routes including regenerated TypeScript route types) passed. CI now
includes the isolated full Script browser suite. Full local Vitest was stopped
under host memory pressure; do not report it as completed.
