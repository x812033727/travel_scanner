# Hotel discovery first-click fix

## Observed cause

Production at `a8be96cd` returned 422 for the first hotel booking POST from the
Discovery card (`placement=discovery`). The retry page silently dropped that entry
label, and the otherwise identical next POST returned 303. Three matching pairs
were observed in the existing API logs without generating new affiliate clicks.

This was an entry-contract mismatch, not a proven DNS, timeout or authentication
problem. The exact-hotel route, nearby affiliate route and Stay22 campaign builder
now share one finite backend placement definition. The frontend booking panel and
error-retry page share their typed placement list, including `discovery`.

Unknown/private placement labels are still rejected. Existing affiliate priority,
URL/review/DNS safety, CSRF checks, no-referrer external redirects, form conditions
and privacy rules are unchanged. No migration, catalog approval, provider enablement
or production deployment is included.

## Platform visibility is separate

The two reported hotel cards currently expose only official-site options. Read-only
production inspection showed Allez disabled with an empty enabled-platform list.
An AID cannot create a hotel's missing or ineligible exact OTA URL. Platform options
still require a reviewed current link and a permitted channel; do not fabricate a
Booking/Agoda/Expedia URL or silently enable an affiliate to fix this submission bug.

## Verification

- Relevant backend suites: 259 passed, including first-POST 303 for official and
  Stay22 across all six public placements, existing-affiliate priority, nearby
  offers, rejection of invalid labels, and public-only campaign fields.
- Focused frontend/BFF suites: 46 passed, including placement/body preservation and
  a single upstream call for a valid redirect.
- Browser acceptance covers the actual Discovery card/detail/panel path for
  official, Booking, Agoda and Expedia, plus both destination and Discovery retries.
  Success destinations are isolated HTML fixtures; real BFF recovery deliberately
  receives 404 from the local upstream. This is not real OTA/commission verification.
- ESLint, TypeScript, five-locale validation and production Next.js build passed.
- All 20 Chromium browser cases passed across desktop and Pixel 7 (one worker,
  production build on port 3312). The four platform first-click scenarios have no
  page errors or horizontal overflow. The browser fixtures made no external calls.
- Repository task tooling: 15 tests passed. Full Linux CI, PostgreSQL/Redis and
  existing unmocked journeys are reported on PR #382, independently of local tests.

The user's Chrome connection disappeared during browser-tool initialization. The
production log pairs establish the reported failure; isolated Chromium acceptance
does not claim a manual Chrome or live-provider verification.

## Authorized rollout follow-up (2026-09-09)

After the user's explicit merge/deployment approval, PR #382 passed all 12 push/PR
checks and was squash-merged as `d9ef8fcd3565ae3ddd02751d334e662e20412a99`.
The production build uses a clean archive in an isolated release; activation is
gated on the merged main CI, a verified PostgreSQL backup and health checks.

The user additionally requested Booking.com through Stay22. Using their already
authenticated Chrome admin session, only Allez and Booking.com were enabled:
configuration version 7, AID `mokaair`, platforms `["booking"]`. Agoda and Expedia
remain outside Stay22. This was a separate audited settings operation, not a
catalog approval or part of the source-code fix. The existing readiness report
listed 57 Booking links capable of Stay22, 25 missing and 3 requiring review.

Chrome then showed the Tokyo Station Hotel's Booking.com button with the Stay22
disclosure without opening a map; the public API reports `affiliate_channel=stay22`.
The panel had no horizontal overflow (512px content and scroll width) or first-party
console error. Unrelated wallet-extension injection errors were not app errors.
No external affiliate click, booking, commission or Hub attribution was verified.
The two originally reported hotels still have only approved official-site URLs;
enabling a channel does not create their missing Booking links.

Merged-main CI run 34354259218 and both browser workflows subsequently passed.
Deployment of `d9ef8fcd` succeeded from
`/root/mokaair-release-d9ef8fcd-deQy9sRl` after a 14,981,622-byte protected custom
PostgreSQL backup and successful `pg_restore --list`. All eight application services
run that SHA with zero restarts; three consecutive health checks passed, the public
homepage returned 200 and schema remained `0068_admin_operations_center`. Runtime
environment contents/permissions, data-container IDs/mounts and approved Booking
configuration were preserved. No rollback was required.

Three bounded first-party discovery POSTs now returned 303: Ginza Premier official,
Otemachi official and Tokyo Station Hotel Booking. The latter points to
`www.stay22.com/allez/booking` with `aid=mokaair` and the exact encoded original
Booking property URL. Redirects were not followed; these calls created only local
click audit records, not externally verified tracking or bookings. `no-store` passed.
The strict `no-referrer` wire assertion did NOT pass: an older global Next header
overrides it with `strict-origin-when-cross-origin`. This pre-existing issue is
tracked separately in `2026-09-09-preserve-clickout-referrer-policy`; do not report
all privacy-header assertions as passing.
