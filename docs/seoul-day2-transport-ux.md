# Seoul transport settings and readable directions

## Reproduction and scope

On 2026-09-10, real Chrome interaction with the deployed Seoul itinerary's
second day reproduced these problems:

- Unqueried connectors showed approximate 15/20-minute journeys, but querying
  transit returned an ODsay configuration warning and no applicable route.
- The route panel mixed transport settings, map display and external navigation;
  an unavailable mode ended at a disabled apply button.
- Manual input started with an arbitrary 20 minutes. Buffer settings and the
  detailed steps were unnecessarily difficult to find.

The investigation did not rearrange the user's sights, save fabricated routes,
enable providers, change credentials or deploy an application version. Actual
query/apply/reload UX verification uses a clearly labelled, private loopback
fixture itinerary, not the user's production data.

## Evidence, not a coverage assumption

The production Google Routes key was already configured; ODsay was not.
The Korean country rule selected only ODsay and never attempted Google.

Two bounded, normally metered requests were made for the same public Seoul
hotel-to-museum endpoints: one duration-only authorization probe, then one
detailed request. The probe returned HTTP 200 with a route. The detailed request
successfully normalized walking, bus, boarding/alighting stops, direction, stop
count and timestamps. No raw provider response or private trip/account ID is
stored in this document or the checked-in synthetic fixtures.

The detailed request used the trip's future local departure time and returned
`schedule_mode=preview` after the existing same-weekday/time mapping. It is
evidence that this route was available at the tested reference time, **not** a
guarantee of nationwide coverage or the future trip's actual timetable.

## Behavior after the change

- KR transit selects configured ODsay, otherwise configured Google Routes.
  This is a configuration fallback, not a new cross-provider paid retry loop.
- Monthly metering, verified Google ID isolation, cache keys, future-date
  warnings and preview/apply authorization remain in the existing services.
- KR walking remains external/manual; driving remains NAVER. Displaying a map
  does not establish a usable travel duration.
- Navigation metadata describes whether the mode can be queried without making
  a paid request or exposing keys. An empty query is not reported as a coverage
  prohibition.
- Route settings expose the extra buffer directly. Successful queries show
  expanded boarding, transfer, alighting and walking steps before the map.
  One result does not need a separate large selection card. Explicit query
  completion focuses the detail region without smooth motion.
- Provider, manual and unqueried timings are distinct. A blank manual input
  requires the user to enter a positive duration. Korean unqueried walking does
  not derive a fake following start time.
- External navigation remains optional when a real in-app route exists. An
  unavailable mode offers external navigation and manual time, without a fake
  apply action. Map expansion and map-provider switching do not query routes.

## Verification boundaries

Backend fixtures exercise provider selection/normalization, metering, identity
isolation, future-date preview, read-only navigation, user isolation and existing
preview/apply/background behavior. Frontend tests exercise explicit querying,
step readability, buffer persistence, manual input, focus, unavailable modes and
map independence. Browser fixtures are synthetic and do not establish coverage.

Local Chrome verified a 23-minute synthetic route plus a 15-minute extra buffer:
the following activity changed to 09:38 only after apply and survived reload.
Production remained unmodified, with its unqueried routes still unqueried.

Validation completed on 2026-09-10:

- Ruff and mypy for the changed routing/API modules: pass.
- Primary routing/provider/navigation pytest suite: 136 passed. Independent
  background/preview/apply review suite: 123 passed (overlapping tests; do not add
  these counts together).
- Five web component/type suites: 181 passed; the final extra unavailable-mode
  regression brings the panel/card subset to 53 passing tests.
- Full web ESLint, TypeScript and i18n (five locales, 25 namespaces): pass.
- Korea Playwright suite: six passing cases across desktop Chromium and Pixel 7,
  with no fixture-context console errors, unexpected first-party errors, external
  provider requests or horizontal overflow.
- Next.js production build: pass, including TypeScript and 272 generated pages.
- Final real Chrome view: detailed list receives focus after query and has no
  horizontal overflow. Its only captured error was a browser wallet extension,
  not a first-party error. Earlier hot-reload/diagnostic issues were rechecked in
  a fresh tab; no claim is made that a dev-server session can never become stale.

These are targeted tests, not a run of the entire monorepo or a new production
PostgreSQL/Redis deployment. No schema migration is required by this change.

This change needs a separately authorized merge/deployment before it affects
the live Seoul itinerary. After deployment, re-query its transit route and check
the actual returned steps and preview warning before applying.
