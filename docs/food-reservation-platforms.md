# Independent merchant reservation reviews

## Administrator workflow

Open **Food → Catalog → Merchants → Edit**, then **Reservation platforms**.

1. Choose a platform. The country recommendation is a suggestion, not a restriction.
2. Open the actual venue page and compare its branch name/address with official merchant evidence. Search snippets, platform homepages, and branch-selection pages are insufficient.
3. Enter the precise URL, optional verified language URLs, outcome, and review note.
4. Choose **Save reservation platform only**. This issues one platform PUT, not the merchant PATCH. Merchant names, addresses, coordinates, sources, dish relations, activation, and merchant approval are not part of that payload.
5. Switch providers to review another platform. Each has a separate saved outcome and draft. Disabling one does not disable the other platforms or merchant.

The ordinary merchant save no longer implicitly saves a platform draft. A newly created merchant must first be saved to obtain its ID. Platform drafts stay in the editor while switching providers, after failures, and after saving merchant details. Closing with unsaved platform drafts requires explicit discard confirmation. Drafts are page-local, not persistent browser storage.

Concurrent edits use `expected_checked_at`. A stale edit returns `reservation_platform_version_conflict` (409). Reload the saved platform state while retaining the draft, compare the latest values, explicitly confirm reuse of the draft, and save again. A branch already assigned to a different merchant instead returns `reservation_platform_url_conflict`; reloading cannot resolve a wrong merchant identity.

## Supported platforms

The shared known-provider catalog contains TableCheck, Catchtable Global, EZTABLE, Chope, OpenRice, Hungry Hub, PasGo, inline, Maifood, SevenRooms, 一休, My Concierge Japan, 食べログ, ホットペッパーグルメ, ぐるなび, AutoReserve, and 네이버 예약. Existing reviewed links remain supported. No arbitrary provider or user-supplied host is accepted.

New supported precise routes include TableCheck's locale/venue/reserve/message and reserve/landing paths, inline's two venue identifiers, Maifood's brand/branch path, SevenRooms' reservation and venue-scoped booking paths, Ikyu's restaurant ID, and My Concierge's restaurant page. Maifood `/branches` is not accepted as a precise branch. Both old and new TableCheck paths are recognized as the same venue identity.

Japan and Korea were added in 2026-09 because the country defaults covered almost none of their merchants. Tabelog is a restaurant number under a prefecture and two area codes, optionally behind one of its own language directories (`en`, `tw`, `cn`, `kr`, `th`), which map onto the site locales; the bare path is Japanese. Hot Pepper is one fixed-width `strJ` shop code. Gurunavi keeps its Japanese site on `r.gnavi.co.jp/{shop}` and its international site on `gurunavi.com/{language}/{shop}/rst`, and a route from one host is never accepted on the other. AutoReserve is a locale plus a twenty-character restaurant ID, whose case is significant. Naver is a business ID under its own category number; the category is not part of the branch identity, so the same business stays one identity across categories and across the mobile host. A Catchtable venue ID's dot segment may start with an underscore (`hani._.noodle`); the ID as a whole still has to start alphanumeric, and an empty dot segment is still rejected.

Recognizing a Japanese or Korean route does not mean the shop takes bookings there. All four Japanese platforms show other restaurants' reservation badges on a shop page — Tabelog and Hot Pepper in the area carousel, Gurunavi in a loyalty-points banner on every page — so a review has to look at the page's own booking control. `docs/catalog-content-reviews/2026-09-12-japan-platforms.md` records which marker identifies it on each platform.

HTTPS, exact provider hosts and explicit venue routes are required. Credentials, ports, fragments, traversal, encoded separators, redirect parameters, and generic search/list pages are rejected. Only inline's supported language query is retained. Localized URLs must identify the same branch; a URL whose explicit language contradicts its assigned locale is rejected. Unknown language is not guessed from a creator's country or platform default.

This validates route structure and administrator evidence, not availability or successful online booking. It does not fetch external sites when saving or click through a booking flow. Public actions continue to say “View reservation information”; unavailable outcomes never produce public reservation buttons.

## API and compatibility

- `GET /admin/foods/merchants` adds `available_platforms` (`provider`, `label`) and each merchant's independently ordered `platform_links`.
- `GET /admin/foods/merchants/{id}/platform-links` is an authenticated read-only refresh for the platform editor.
- `PUT /admin/foods/merchants/{id}/platform-link` retains its isolated one-provider semantics and audit record. `expected_checked_at: null` asserts a new row; a timestamp asserts the last-seen review. Omission is accepted only for legacy client compatibility.
- `platform_link` remains a deterministic compatibility projection: country-recommended saved row first, otherwise first provider in sorted order. It is not a second authoritative store.
- Country defaults remain available to existing seeds. Verified supported platforms are no longer hidden merely because the merchant is in another country.
- PostgreSQL row locks protect same-merchant updates. A transaction advisory lock and normalized provider/branch identity check prevent concurrent same-branch aliases from being assigned to different merchants; existing database URL uniqueness remains in place.
- Normal authentication, suspended/revoked session checks, content-management capability requirements and audit logging remain in effect. The read-only endpoint requires the corresponding content-read capability.

The existing `food_merchant_platform_links` table already supports multiple providers per merchant. No migration, existing value deletion, paid API, production catalog approval, or deployment is included in this change.

## Verification

```text
cd apps/api
uv run pytest tests/test_food_platform_links.py tests/test_reservation_platform_auth.py -q
uv run ruff check app tests
cd ../..
npm run check:i18n
npm run typecheck:web
npm run lint:web
npm run test:web
npm run build:web
cd apps/web
npx playwright test e2e/food-map-reservations.spec.ts e2e/food-reservation-platforms.spec.ts
```

The dedicated Food map and reservations CI workflow runs the browser checks against the production build. New browser fixtures cover five languages, 320/390/1280-pixel widths, light/dark themes, independent saves, preserved merchant/platform drafts, multiple providers, separate disabling, and explicit stale-review recovery. Fixtures do not contact production or submit reservations. PostgreSQL integration tests run in the existing API CI job with `RUN_INTEGRATION_TESTS=1`; SQLite-only checks do not substitute for PostgreSQL locking coverage.

Catalog enrichment remains separate: enabling more provider types does not mean all public merchants have been researched, approved, or supplied with reservation links.
