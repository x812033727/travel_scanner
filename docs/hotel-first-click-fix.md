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
