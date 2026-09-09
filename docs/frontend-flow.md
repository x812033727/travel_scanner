# Explore → Saved → My trips

This change is based on main `7cee8650` (calm planner #373). It does not replace the itinerary editor, change providers, activate paid queries, or publish content. Merge, deployment and production flags need separate approval.

## User flow

- Discovery ON: four destinations on desktop/mobile: Explore, Saved, My trips, My. My contains account, appearance/language/text size and secondary travel tools/admin access.
- Homepage/explore show compact editorial content, search and destination/category filters. Advanced filters are optional. `content=kind:UUID` is a shareable, history-aware drawer; closing returns to the same filter and loaded results.
- `/search/new` reuses the existing recommendation/search workbench with basic fields and optional preferences. `/#trip-search` forwards there only when discovery is enabled. Neither route automatically requests a quote.
- Public detail reads only approved stored content and existing valid place-cache projections. Videos load on click; hotel booking options keep the existing verified Klook/Stay22/platform flows.
- Save once to All saved; organize later. Named-list removal/deletion preserves the base save; global unsave removes all own memberships. Unavailable content remains removable without revealing its previous title/media.
- Planning reads current content capability and trip versions. Destination IDs match across locales. Only one same-destination trip is preselected; food requires an actual restaurant and meal, hotels explicitly confirm the all-days replacement.
- Creating a trip keeps the existing draft/request snapshot/idempotency implementation. A 24-hour account-bound session reference returns to the original content for confirmation; it never auto-adds. Sign-in cancellation, reload and deep links are read/confirmation-only.
- An uncertain hotspot/meal POST is not blindly retried: the user is directed to inspect the trip. Hotel retries reuse the original server-supported idempotency key/body/version.

## API and storage

- Discovery `category=all|hotspots|foods|hotels|guides` intersects the legacy `type` before pagination; cursors bind to filters. Detail adds an optional public `detail` projection, never raw review/private/provider records.
- `GET /saved-items/all`: cursor-paginated cross-source union, optional type/destination/collection, stable canonical deduplication; no 100-item truncation. `POST /saved-items/states`: at most 100 exact keys per batch.
- `PUT/DELETE /saved-items/{type}/{id}`: five legacy favorites plus guide/post; hotel aliases service, article/video aliases guide. Restaurant Place IDs remain opaque and case-sensitive. Collection mutations reuse the same transaction service.
- Private caches are login-identity scoped. Responses from prior logins are ignored/aborted; optional `expected_user_id` on mutations protects account-switch races. BFF same-origin writes/no-store remain unchanged.
- Migration `0067_collection_inbox` adds nullable inbox system role and a per-owner unique partial index. First guide save atomically creates a private inbox. GET never creates/backfills one; ordinary collections are not moved or deleted. Inbox does not count against named-list quota or the 500-item named-list limit; it has a separate 10,000-item safety ceiling. Collection target storage expands to 255 to preserve the existing Place ID maximum.

## Verification and release

New tests cover category/detail policy, 551+ saved rows and cursor deduplication, inbox races/migration, hidden content, source aliases, collection preservation, stale identity/probe responses, explicit trip confirmation and uncertain mutation recovery.

`travel-discovery.yml` runs isolated PostgreSQL/Redis/Mailpit, guarded synthetic fixture seeding and desktop/Pixel 7 browser flows. The new end-to-end path checks public reading → real login → save → organize → existing creation form → return for explicit add → persisted trip/collection. The community service is disabled for that flow. No test seeds production.

Browser fixture screenshots are explicitly test-data renders, not evidence of live publishing. The opt-in `FRONTEND_CAPTURE_BASELINE=1` test only reads the public production homepage for before screenshots. `test-results` artifacts stay out of Git.

### Visual and regression evidence

- The public production before captures are `apps/web/test-results/frontend-before/{desktop,pixel7}-production-home.png`: the first screen is dominated by the date form.
- The discovery acceptance artifact contains `after-home-{locale}.png` and `after-explore-dark-large-{locale}.png` for desktop and Pixel 7 across all five locales. They are synthetic content fixtures with no invented attraction photos. At standard text size the first card title is in the viewport; large/dark/reduced-motion views have no horizontal overflow.
- Manual inspection of the Traditional Chinese captures confirmed compact search/category/destination controls, readable semantic dark surfaces and four direct bottom destinations. Reading-drawer Escape and focused creation-page navigation have dedicated regressions after the initial browser run exposed issues.
- Full-stack acceptance uses ordinary email verification and sign-in with community disabled. It checks explicit save, list organization, destination/date entry in the existing creation form, calendar auto-close, confirmation after return, persisted trip dates/content, reload and base-save preservation after list deletion.
- Local focused checks include 12 dialog/navigation, 41 metadata, 30 legacy frontend and 13 planning tests, plus the complete API suite (Windows cannot run the Linux `fcntl` module). PostgreSQL migrations/concurrency and full-suite Linux/browser results are recorded in [PR #374 checks](https://github.com/x812033727/travel_scanner/pull/374/checks); pending runs are not counted as passes.

After authorized deployment, verify discovery ON/community OFF, ordinary public reading and private saved state with a real browser. Do not infer retention improvement from passing tests; reuse existing first-party events without new cross-day tracking.
