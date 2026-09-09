# Itinerary-first planning workspace

## User flow

1. Pick a city and date range. The name follows the selection until manually edited. Defaults are two adults, no children and one room; preferences are optional.
2. Create a `manual_blank` trip with `routing.auto_compute=false`. Creating a trip never starts AI or live route queries.
3. See the trip header, dates and actual day timeline. Add a place manually or open the AI assistant. Supporting services live under Travel essentials / Trip settings / Share & export.
4. Add several places without closing the picker. Use card More actions for editing, moving across days, locking or undoable deletion. Return to the most recently added card.
5. Preview AI changes or route alternatives before explicitly applying them. Manual, locked and fixed-time items retain the existing backend protections.

## Safety and implementation

- Secondary service components mount only inside the selected tools category. UI navigation is not a reason to charge usage or query paid providers.
- `PlannerOverlay` portals escape transformed layout ancestors, copy only approved theme tokens, have unique ARIA IDs, trap keyboard focus in the topmost layer and restore page scroll/focus. Sheets do not add duplicate route history entries.
- Text adjustments render their diff inside the existing assistant sheet instead of stacking a second dialog. Busy operations prevent switching or closing the parent workflow. Previews do not mutate a trip; existing usage settlement remains server-controlled.
- Metadata PATCH accepts partial `travelers` and `preferences`, validates the merged sections, checks ownership and version, and preserves the source SearchRequest. `search_settings_overrides` identifies explicit overrides for future searches and Stay22 context. Quote-affecting changes invalidate the relevant snapshots, never move itinerary items; blank trips without quotes remain unpriced.
- Settings UI sends only changed keys, preserves legacy/non-preset values, flushes item edits first and does not mark newer local edits persisted because an older metadata request completed.
- Existing daily route preferences, precise POIs, Korean navigation rules, pricing truthfulness, five locales, themes and font sizing remain supported. No new database schema or provider integration is introduced.

## Verification

Focused API and UI regressions exercise partial patches, no-ops, invalid values, ownership/CAS, quote invalidation, preserved source data, continuous additions, panel focus, embedded intent previews, and pending-operation guards.

Playwright uses disposable local fixture trips (not live provider results or production accounts), tests desktop and mobile, and captures `premium-first-screen.png`, `premium-mobile-timeline.png`, `premium-ai-preview.png`, and `premium-single-page-create.png` in test artifacts.

The Windows API suite cannot import the existing Unix-only deployment agent test. Linux CI must verify the complete suite with PostgreSQL/Redis, migrations, container builds and full-stack smoke. Merge and deployment require separate user authorization.

Local verification before the final mainline rebase: 1,009 Web tests in 149 files; 78 desktop/mobile navigation and planner browser scenarios; 27 repository-tool tests; ESLint, TypeScript, five-locale catalog checks and Next.js production build passed. API verification passed 1,854 tests (120 skipped, Unix-only deployment module excluded), followed by 163 focused/adjacent tests after the quote-state edge-case fix. Browser screenshots were inspected at 390px and desktop widths. CI verifies the rebased head, including the real first-party full-stack scenarios.
