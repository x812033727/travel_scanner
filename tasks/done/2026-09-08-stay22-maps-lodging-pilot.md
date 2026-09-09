---
id: 2026-09-08-stay22-maps-lodging-pilot
title: Stay22 Maps lodging pilot
status: done
priority: P2
area: web
owner: codex-stay22
claimed_at: 2026-09-08T08:53:58Z
created_at: 2026-09-08T08:51:18Z
completed_at: 2026-09-08T21:22:51Z
branch: codex/stay22-maps-pilot
depends_on: []
scope:
  - apps/web/components/stay22-map-panel.tsx
  - apps/web/components/stay22-map-panel.test.tsx
  - apps/web/components/stay-area-flow.tsx
  - apps/web/components/stay-area-flow.test.tsx
  - apps/web/lib/stay22.ts
  - apps/web/lib/stay22.test.ts
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/web/lib/stay22-copy.ts
  - apps/web/lib/stay22-messages
  - apps/api/app/trips/stay_router.py
  - apps/api/tests/test_stay22_context.py
  - apps/web/e2e/stay22-maps.spec.ts
  - docs/stay22-maps.md
---

# Stay22 Maps lodging pilot

## Why

The owner approved a Tokyo/Taipei Stay22 Maps pilot after configuring AID mokaair
in the Hub. Add external accommodation browsing without LMA, rewriting existing
affiliate links, importing provider prices, or pretending a map choice reserves a hotel.

## Definition of done

- [x] Authenticated lodging flow exposes a Tokyo/Taipei click-to-load map with actual dates and party.
- [x] Only public catalog centers and minimal search fields leave the site after explicit consent.
- [x] Invalid/missing dates or guests are disclosed, not fabricated; nonpilot destinations stay unchanged.
- [x] Existing hotel selection and partner links remain intact, with five-language and mobile coverage.
- [x] Focused checks, full relevant Web/API checks and CI passed; PR #368 merged under separate authorization.

## Steps

- [x] Add authenticated map context, URL contract, isolated copy catalogs, UI and CSP.
- [x] Validate URL guards, interaction/privacy, five locales and browser behavior.

## How to verify

Run ruff/mypy/focused API tests, Web lint/typecheck/Vitest/build, i18n/tasks/tools
checks, and desktop/390px Playwright. Open lodging, choose an area, explicitly load
the map; confirm no Stay22 request before load and no trip mutation from map controls.

## Notes

2026-09-09 handoff: GitHub confirms #368 merged as 7d20ffbbd8e1e4b32eaa1917c5b15ed5d7611919 on 2026-09-08. The subsequent authorized deployment and opt-in map smoke completed in the owner thread. This closes the stale task claim; the new planner task preserves the map privacy and click-to-load contract.

Isolated branch from origin/main 200e46e, rebased onto e8afbc8 after PR #366 merged.
Only the generated task board conflicted; regenerated with tasks.mjs.
Shared checkout is untouched. The broad
merchant-style-discovery messages scope remains active; use feature-scoped JSON
catalogs, following lib/itinerary-copy.ts, instead of force-claiming shared messages.
Official integration: https://dev.stay22.com/docs/maps/quick-start and parameters.
Hub reference maps: Tokyo 6a9fc9c810fb99ee3ecce832; Taipei 6a9fca1610fb99ee3ecceac0.
Production trip embeds are dynamic /embed/gm URLs with AID mokaair, not static Hub dates.

Local verification: 61 focused API tests (38 new), 47 focused Web tests; Ruff,
258-file mypy, Web ESLint/typecheck, i18n/tasks and production build passed.
Five 390px browser locale tests passed with explicit external-frame fixtures;
Full Web suite: 836 passed; tools: 27 passed. Expanded browser run: 14 passed,
including five locales at 390px, desktop 1280px, and original hotel selection.
API retry excluding only the Windows-incompatible deployment test: 1774 passed,
111 skipped (PostgreSQL/Redis/S3 integration is covered on Linux CI), one existing
AsyncMock warning. Full API Ruff and mypy passed.
Full API collection on Windows hits the existing deployment_agent UnixStreamServer
import error; retrying with only tests/test_deployment_center.py excluded. Full
Linux API, PostgreSQL/migrations, containers and full-stack smoke remain CI gates.
Both CI runs on original head a743e2b passed all four jobs:
https://github.com/x812033727/travel_scanner/actions/runs/34208972546 and
https://github.com/x812033727/travel_scanner/actions/runs/34208908746.
PR https://github.com/x812033727/travel_scanner/pull/368 awaits fresh-head checks
after rebase. No merge or deployment authorization; post-deployment real widget
inventory smoke remains required. Independent API/UI contract review found no blocker.
