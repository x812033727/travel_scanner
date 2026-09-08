# Admin domain workspaces

## Boundaries

The primary admin entry points are Overview, Attractions, Food and Hotels.
Operations groups members, analytics, community, AI history, shared partners,
usage and non-hotel travel services. System groups shared provider credentials,
runtime/layout settings, UI text and deployment. Backend capabilities still
control administrator access and deployment visibility.

This change does not publish records, switch providers, enable paid services,
run backfills, change public APIs or require an Alembic migration. Stay22 stays
under its existing settings and publication gates.

| Workspace | `tab` | `section` |
| --- | --- | --- |
| `/admin/hotspots` | `catalog` | `catalog` |
| | `review` | `manual`, `ai` |
| | `places` | `identity`, `google` |
| | `content` | `guides`, `themes`, `intros` |
| | `settings` | none |
| `/admin/foods` | `catalog` | `merchants`, `dishes` |
| | `review` | `merchants`, `dishes`, `ai` |
| | `completion` | `coordinates`, `taxonomy` |
| | `nearby` | `scans`, `sources` |
| | `settings` | none |
| `/admin/hotels` | `catalog` | `catalog` |
| | `review` | `products`, `platforms` |
| | `affiliates` | `products`, `destinations` |
| | `imports` | `import`, `coverage` |
| | `settings` | `catalog`, `providers` |

Each route is locale-prefixed. Manual queues reuse the catalog editor with a
real pending-status API filter. Hotel counts and coverage use only hotel rows.
Restaurant scans remain distinct from curated food merchants.

## One editable owner per setting

`apps/web/lib/admin-settings-ownership.ts` is the executable ownership registry.
Tests require secrets and unknown fields to remain accessible in shared settings.
The UI renders non-owned fields as links, never a second editable credential form.

| Owner | Fields |
| --- | --- |
| Attractions | `layout.hotspots_enabled`; guide backfill scheduling; guide-search and introduction generation enablement, models and domain quotas |
| Food | Google Maps `restaurant_*` configuration: scanning, refresh, batch limits and restaurant budgets |
| Hotels | `runtime.hotel_provider_mode`; Booking Demand hotel configuration and enablement; Travelpayouts hotel target URL; hotel catalog enablement, direct links and quote policies |
| Shared providers | All secrets, shared Google/AI/Amadeus/Travelpayouts configuration and remaining provider fields |
| System / Layout | Remaining runtime / layout fields; unknown fields keep their shared owner |
| Operations / Partners | Shared brand approval; hotel offers link to this one brand editor |

Deep links use `provider` and optional `field`. Hotel provider links also use
`tab=settings&section=providers`. Provider saves send only dirty fields plus the
baseline `expected_updated_at`; omission remains compatible with old clients.
Both existing-row and first-row writes are transaction-serialized. Stale writers
receive 409, retain their draft, and must explicitly reload before retrying.
Credentials remain encrypted/masked and audit records contain field names only.

Settings panels stay mounted across domain tabs. Provider drafts are RAM-only
and tied to the active authenticated session, including safe Back/Forward
restoration; credentials are not written to browser storage. Non-secret hotel
catalog drafts retain their original version in session storage. Leaving via a
link or reloading warns about unsaved changes. Saving one provider does not
discard a different provider's draft.

## API isolation

- `GET /admin/hotels` returns hotel records, review queues and hotel-only coverage.
- `PATCH /admin/hotels/config` applies the versioned hotel subset, preserving
  other service kinds, global publication, cities and Airalo configuration.
  It shares a transaction lock with the compatible global config API.
- Hotel CSV preview and commit reject other kinds and source-key collisions with
  non-hotel records before upserting anything. Product, platform, offer and brand
  approval remain separate gates.
- Catalog AI APIs accept `scope=all|hotspots|foods`. Counts, snapshots, discovery,
  results, apply, resume and history enforce the same scope server-side. Legacy
  requests/runs without scope remain `all`, including their original idempotency
  contract. `/admin/catalog-review` shows history/resume, not a new mixed-run CTA.
- Only one AI run can be active globally; cross-domain contention reports the
  active scope. Usage accounting is still shared.

No hidden coordinate queue or paid-query panel is mounted. Overview and workspace
navigation only load read-only catalog/config metadata; scans, enrichment and
provider tests remain explicit operations.

## Compatibility and verification

Old attraction `#restaurants` / `#sources` links redirect to Food nearby tabs.
Old catalog/content/coordinate hashes and hotel service links remain supported.
The URL adapter preserves unrelated filters and locale, handles encoded queries,
and prevents outgoing or stale React effects from rewriting a newer history entry.

Focused suites cover canonical identity editing, pending filters, scope isolation,
idempotency, hotel imports/config writes, provider ownership/409/draft races,
navigation, five-locale copy and keyboard interaction. PostgreSQL concurrency tests
use disposable schemas and require `RUN_INTEGRATION_TESTS=1`.

Run `npm run lint:web`, `npm run typecheck:web`, `npm run test:web`,
`npm run build:web`, `npm run check:i18n`, `npm run check:tasks`; in `apps/api`,
run `uv run ruff check .`, `uv run mypy app`, `uv run pytest` and
`uv run alembic heads`. Existing CI validates fresh PostgreSQL migrations.

`e2e/admin-domains.spec.ts` runs isolated browser fixtures on desktop and Pixel 7.
`e2e/admin-domains-full-stack.spec.ts` requires `ADMIN_DOMAIN_E2E=1`, a loopback
PostgreSQL/Redis stack and CLI-created fixture administrators. It logs in through
the UI, persists hotel-only settings, reloads and checks unrelated settings plus
food-only AI counts. Reserved admin emails must never use public registration.
Neither suite should be pointed at production for writes.
