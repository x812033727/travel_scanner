---
id: 2026-09-09-planner-calm-editing
title: Calm daily timeline and safe explicit planner editing
status: review
priority: P1
area: web
owner: codex-planner-calm
claimed_at: 2026-09-09T00:53:02Z
created_at: 2026-09-09T00:52:55Z
completed_at:
branch: codex/planner-calm-editing
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/itinerary-place-browser.tsx
  - apps/web/components/itinerary-place-browser.test.tsx
  - apps/web/components/place-picker.tsx
  - apps/web/components/place-picker.test.tsx
  - apps/web/components/planner
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/components/route-timeline-link.tsx
  - apps/web/components/route-timeline-link.test.tsx
  - apps/web/components/system-itinerary-card.tsx
  - apps/web/components/system-itinerary-card.test.tsx
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-types.test.ts
  - apps/web/lib/planner-copy.ts
  - apps/web/lib/planner-copy.test.ts
  - apps/web/app/globals.css
  - apps/web/e2e/planner-calm.spec.ts
  - apps/web/e2e/navigation.spec.ts
  - apps/web/e2e/planner-premium.spec.ts
  - apps/web/e2e/trip-stay-areas.spec.ts
  - apps/web/e2e/stay22-maps.spec.ts
  - apps/web/e2e/full-stack.spec.ts
  - apps/web/e2e/readability.spec.ts
  - .github/workflows/planner-premium.yml
  - apps/api/app/trips/router.py
  - apps/api/app/trips/schedule.py
  - apps/api/app/trips/route_planner.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_trip_route_planner.py
  - apps/api/tests/test_trip_schedule.py
  - apps/api/tests/test_day_timeline_contract.py
  - apps/api/tests/test_trip_create_replay.py
  - apps/api/tests/test_trip_preferences.py
  - docs/planner-calm-editing.md
---

# Calm daily timeline and safe explicit planner editing

## Why

The prior planner hid useful stops behind empty system anchors and warnings. Editors wrote on blur or selection, so users could lose place identity or misunderstand what was saved. Creation retries could lose their identity on refresh. Deliver a simpler daily timeline with explicit, recoverable editing and matching schedule projection.

## Definition of done

- [x] Actual stops lead the daily timeline; empty system data is retained in optional arrangements.
- [x] Cancel/search supersession cannot change formal place IDs, coordinates or routes.
- [x] Notes, time and preference edits use explicit Save/Cancel and retain failed drafts.
- [x] Route requests and route application require separate explicit actions.
- [x] Creation refresh/retry preserves the request/key and rejects payload conflicts.
- [ ] API/Web/build/browser/CI validation is green and evidence is recorded.
- [x] PR is available for review; merge/deploy remain separately authorized.

## Steps

- [x] Isolated branch from current main; preserve concurrent homepage/navigation work.
- [x] Implement shared timeline projection and draft workflows with focused regressions.
- [x] Adapt browser fixtures to select/draft/save instead of auto-write.
- [ ] Complete integrated validation, rebase, PR and CI checks.

## How to verify

See `docs/planner-calm-editing.md` for commands and behavioural acceptance. Local browser data is intercepted or isolated; production Tokyo trips are read-only and were not mutated.

## Notes

- Default-buffer mismatch reproduced: no saved day settings caused backend zero-buffer versus UI ten-minute estimates. Both now use the configured default.
- Missing-coordinate barriers must preserve downstream provider route identity while withholding invented absolute times and conflicts.
- Local Windows validation uses a fresh `uv sync --frozen` venv; the unrelated POSIX deployment-center module is run by Linux CI. PostgreSQL-only cases need CI.
- Discovery owner handed back `planner-premium.spec.ts` after PR #372; retain its disabled discovery-status fixture when rebasing.
- No production writes, provider searches, merge or deployment authorized in this task.
- PR: https://github.com/x812033727/travel_scanner/pull/373 (no auto-merge).
- Frozen post-rebase local API: 2,057 passed / 126 skipped; Ruff and MyPy (275 files) passed. Windows-only exclusion is deployment-center; Linux/PostgreSQL run in CI.
- Production build passed (252 generated pages). Calm mobile/draft browser tests 8/8, planner contrast 8/8, route/premium flows 20/20, stay-area/Stay22 five-locale tests 14/14 passed.
- CI initially caught legacy date-summary and empty-hotel selectors; adapted to the actual new controls without changing write/identity assertions. Full-stack and final-head CI are being rerun.
- Concurrent local Next dev compilation corrupted a generated validator. Its cache was moved recoverably to the local Temp folder, not user source; production build then passed.
- Pre-footer-fix head 5d51d539 passed PR CI: API 2,307 passed / 5 skipped, Web 1,138 passed, general browser 282 passed, planner browser 30 passed, containers/migration and full-stack smoke. The duplicate push run needed a retry for unrelated community offline reconnection.
- Final screenshot review found the mobile creation CTA behind global navigation. Creation now has its own fixed footer; production build and both desktop/mobile creation tests passed, including in-viewport and unobscured hit-target assertions at 390 by 844. Final-head CI is rerun after this fix.
