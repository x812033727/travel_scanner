# Calm planner: daily timeline and explicit drafts

## Behaviour

- The daily timeline renders real arrangements first. Unset system flight, hotel and meal rows remain in the database, but are grouped under optional arrangements. Selected places without coordinates stay visible and block adjacency; the planner never silently routes through them.
- `deriveDayTimeline` is the UI projection boundary for rows, optional rows, neighbours, route status, time certainty and counts. Backend filtering, default buffer and unknown-time propagation use matching rules.
- Unknown travel time is not zero. A missing or expired leg leaves downstream flexible times uncertain until an explicit fixed-time anchor. Valid downstream provider route metadata remains available even when its absolute times cannot be projected.
- Stop titles, places, time modes, notes and preferences are drafts. Selection is not insertion. Cancel does not alter IDs, coordinates, routes or formal items. Explicit Save/Join sends the versioned request before updating the timeline.
- Errors retain draft content; version conflicts never perform an unconditional overwrite. Closing or leaving a dirty editor prompts to keep editing or discard. Pending writes cannot be interrupted by the corresponding close/back action.
- Search retains text, source/filter and insertion context. First-party catalog results are primary; provider search is explicit. Escape dismisses suggestions first. Aborted or superseded searches cannot apply a late selection.
- Route mode/buffer selection is local intent only. Query is explicit; selecting an option remains a preview until Apply. Opening the route drawer first flushes earlier timeline changes and validates adjacency. Saved per-leg settings are preserved.
- AI defaults to the current day: arrange places, adjust the existing itinerary, or reorder existing places. Preview precedes apply, with manual/locked/fixed items and existing server usage rules retained. Preview-only copy does not imply that applying AI is free.
- Sorting remains an immediate versioned change with Undo. Maps remain opt-in. Animations respect reduced-motion preferences.

## Safe trip creation

The browser stores an account-scoped draft and an immutable pending request snapshot before sending POST. The pending snapshot includes the original request bytes and idempotency key. A timeout or refresh retries that exact request; editing is locked while its outcome is unknown. Local recovery expires after 23 hours, before the server's 24-hour replay window, and directs the user to My Trips instead of creating another trip.

The API stores a canonical request digest beside the creation idempotency result and in the committed trip metadata. A matching key/body returns the original trip. A matching key with a different body returns `409 trip_create_payload_conflict`. Legacy replay records without a digest fail closed with `trip_create_recovery_required`. The database record closes the commit-to-cache failure window; the user row lock serializes concurrent creation in PostgreSQL. No schema migration or provider contract change is required.

## Verification

All write tests use isolated fixtures or newly registered test users. Existing production Tokyo trips are not modified.

```powershell
npm run check:tasks
npm run check:i18n
npm run lint:web
npm run typecheck:web
npm run test:web -- --pool=threads --maxWorkers=1
npm run build:web
```

From `apps/api`:

```powershell
uv run ruff check .
uv run mypy app
uv run pytest
```

From `apps/web`, use the production build when practical:

```powershell
$env:PLAYWRIGHT_SERVE_BUILD='true'
npx playwright test e2e/planner-calm.spec.ts e2e/planner-premium.spec.ts --workers=1
```

The calm browser suite checks the actual first attraction above the mobile dock at 390×844, no horizontal overflow, draft cancellation with zero writes, failed-save retry and choose-before-join with search restoration. Existing navigation/premium/full-stack suites retain route-apply, creation, manual insertion and persisted-ID assertions under the new explicit controls. The CI matrix additionally supplies Linux, fresh PostgreSQL migrations, containers and unmocked BFF/API smoke journeys.

## Release boundary

This change prepares a PR only. Merge and production deployment need a separate user instruction. No live provider keys, paid route lookups, production itinerary writes or deployment switches are used for local acceptance.
