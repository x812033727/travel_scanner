# Evidence-backed hotspot identity editor

This change supplies missing controls in the existing canonical location editor.
It does not moderate a catalog automatically, deploy the application, launch an AI
run, or make a paid provider request. Filling an ID is not proof of its identity.

## Contract

- `/admin/hotspots/candidates` additionally returns `updated_at`.
- The existing `/admin/hotspots/review` accepts single-row `action: update`
  corrections to `category` (the eight existing codes) and a missing
  `wikidata_item_id` (`Q` followed by a positive integer, maximum 32 characters).
- Non-empty existing QIDs cannot be replaced, cleared, or reassigned. Duplicate
  QIDs return 409, including unique-index races. Whitespace-only legacy IDs count
  as missing. Correcting an existing identity requires a separate reviewed process.
- Actual category/QID changes require a nonblank reason. Explicit `reason` on
  every action persists to the record and audit; omission preserves each row's
  existing reason, while explicit `null` remains an intentional clear operation.
  Editing does not change the row's publication status or active flag.
- `expected_updated_at` protects a single-row edit. `expected_updated_ats` maps
  every selected ID to its observed timestamp for approve/reject/disable actions.
  Timestamps must include timezone information. These are optional for old clients,
  but new clients submit them when supplied by the listing API.
- The server locks rows in ID order, refreshes ORM state and checks every supplied
  timestamp before mutations. Stale edits return `409 hotspot_review_conflict`.
  The existing audit gains category/QID/reason before/after values. Existing map,
  coordinate-source, permissions and publication checks remain in effect.

## Interface

The location editor now exposes classification, protected Wikidata identity, and
review rationale/source text. Saving sends changed fields only (coordinates remain
a pair), leaves other map providers intact, and does not approve the record. The
normal moderation toolbar submits a nonblank new rationale, or preserves each
selected record's existing rationale when the toolbar is left blank.

A stale edit retains its draft and disables resubmission until the administrator
explicitly reloads the current record. Discarding a dirty editor requires confirmation;
leaving the browser page warns about unsaved edits. While a request is in flight,
closing/switching records and changing fields are disabled so late responses cannot
overwrite another draft. Editor requests have their own busy lock, independent of
list-filter loading. Workspace navigation and same-tab links share the dirty-draft
confirmation and cannot leave during an editor request. New copy covers all five existing locales. Controls use
the application's semantic colors and touch-sized inputs.

## Verification and boundaries

- Ruff and mypy over the complete API application passed.
- Complete API suite: 2704 passed, 161 skipped; real PostgreSQL concurrency cases
  require `RUN_INTEGRATION_TESTS=1` and were not run locally.
- Focused frontend suite: 17 passed, including delayed success/409 responses,
  immutable existing QIDs, missing/whitespace IDs, partial patches, and draft recovery.
- Complete Web Vitest suite on 2026-09-10: 192 test files and 1540 tests passed
  (exit 0, 550.82 seconds), after the focused test additions were finished.
- Web ESLint passed with `--max-warnings=0`; TypeScript passed with
  `--noEmit --incremental false`; i18n validation passed for 5 locales across
  25 namespaces. All three commands exited 0.
- [Machine-local captured Web validation log](C:/Users/x8120/AppData/Local/Temp/hotspot-review-editor-web-validation-2026-09-10-1025.md)
  records commands, output, versions and unchanged Web source/test hashes.
  These are local checks, not CI, deployment, production UI or live PostgreSQL
  concurrency evidence.
- Production build passed. Browser fixture scenarios passed on desktop Chromium
  and Pixel 7 in both light/dark modes, with reduced motion, explicit conflict
  recovery and reload persistence (4 cases). These are fixtures, not production writes
  or full-stack database evidence.
- Opening the editor does not search Google, call AI or approve any record. No
  credentials, provider configuration, feature flags, migration, or runtime deployment
  are part of this change. Production moderation remains a separately verified operation.

## 2026-09-10 main integration

User separately authorized integration, merge and deployment after PR386 landed.
The merge preserves both Google/NAVER identities and the supplemental review
panel. The previous Korean task owner confirmed that the overlapping admin files
were released; its merged/deployed claim was closed through the task CLI.

Integration review found and fixed saved-rationale erasure during subsequent
approval, unguarded workspace navigation, and a filter-response/pending-save race.
Backend regression was demonstrated first: three omitted-reason cases failed on
old code. Final local API checks pass: Ruff, mypy (301 files), 59 focused tests
(one PostgreSQL skip), and full pytest 2822 passed/161 service-gated skips. One
existing unawaited AsyncMock warning remains in unrelated usage-setting tests.
Alembic has one head, 0070_map_identity_metadata; this PR adds no migration.

Final focused frontend checks pass 31 cases, scoped ESLint and full TypeScript.
Reciprocal Korean map edits, blank-toolbar rationale preservation, cancelled
navigation and delayed saves across filter refreshes have regression coverage.
Full Web suite, production-build/browser checks and fresh CI are release gates,
not inferred from the earlier pre-merge results above. Local staged i18n initially
reported main's already-merged map copy as new against the old branch; the normal
check passed after recording the merge. No i18n checks were disabled or altered.
