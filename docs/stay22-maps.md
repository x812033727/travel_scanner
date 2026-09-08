# Stay22 Maps lodging pilot

## Boundary

Tokyo (`tokyo` / `JP` / `NRT`) and Taipei (`taipei` / `TW` / `TPE`) only.
This is an external accommodation map, **not** a hotel-price API, booking engine,
or source of permanent hotel/itinerary data. No LMA, LinkSwap, Spark, Nova,
global link rewriting, or automatic popups are installed. Existing hotel search,
manual lodging selection, Travelpayouts and other configured partner actions remain.

The owner configured Stay22 AID `mokaair` on 2026-09-08. This is a public affiliate
identifier, not a secret or API key. Hub reference maps:

- Tokyo: <https://www.stay22.com/embed/6a9fc9c810fb99ee3ecce832>
- Taipei: <https://www.stay22.com/embed/6a9fca1610fb99ee3ecceac0>

The application uses the documented dynamic `/embed/gm` URL so actual saved trip
dates, party and chosen public catalog area can be passed instead of static Hub
event settings. A map can open from the initial lodging-area view **without**
calling the hotel quote provider. Choosing an area still runs the existing quote
workflow and requires fresh consent for the changed map center.

## Data and privacy

The existing owner-only `GET /trips/{id}/stay-areas` adds optional `map_context`;
old responses and nonpilot cities simply omit the UI. It contains canonical
destination identity, original untruncated dates, validated saved-search party
(or trip party when no saved search exists), and TWD. No new route, migration,
provider call, quota charge, or browser credential is introduced.

Before explicit load there is no Stay22 frame, script, preload or connection.
Browser DNT/GPC disables map entry. Consent is in memory only and resets when the
context changes or the lodging panel closes. Closing removes the iframe and returns
focus. External links are deliberate user clicks with `noopener noreferrer`.

Only fixed query keys are constructed: affiliate and static per-city campaign,
public catalog coordinates, valid dates, valid adult/child/room counts, and visual
options. Never pass private trip IDs/names/notes/items/coordinates or access tokens.
`referrerPolicy=no-referrer` prevents leaking the private trip URL. The iframe is
sandboxed without permission to navigate its parent; user-initiated booking popups
remain possible. CSP adds only `https://www.stay22.com` to `frame-src`, not parent
script/connect domains. Existing strict CSP remains Report-Only.

The displayed consent/disclosure states that Stay22 and its providers receive search
and device/network information and may use cookies. Their current policy is linked.
The site owner's broader legal-policy task remains separate; this does not assert
that the existing placeholder privacy page is complete.

## Honest search behavior

- Real future dates are preserved, including stays longer than the existing
  provider's 14-night cap. Invalid, incomplete, equal/reversed or past dates are
  omitted together, with an instruction to choose them in the map.
- Adults, children and rooms remain distinct; incomplete/invalid party is omitted
  rather than guessed. Child ages are not sent; the booking platform must confirm them.
- Currency is TWD, consistent with existing lodging comparison. Price display is
  nightly, not a guarantee about taxes, fees or availability.
- Map choices cannot reserve a room, update the itinerary, or overwrite its budget.
  Users can return to the existing manual lodging flow after identifying a hotel.
- Outer copy covers all five locales. Stay22's own language/currency controls remain
  visible; we do not invent an undocumented `lang` mapping or promise five-language
  completeness inside a third-party iframe.
- A persistent new-tab fallback remains available. Iframe `load` does not prove
  provider inventory availability. A slow/error notice and manual reload are offered;
  there are no automatic retries and no inspection/scraping of cross-origin content.

## Rollout and validation

Feature files are `stay22-map-panel`, `lib/stay22` and feature-scoped JSON copy
catalogs (following the existing itinerary-copy pattern to avoid shared active
message scopes). Tests check five-language key/placeholder parity separately.

Run API Ruff/mypy/tests, Web lint/typecheck/Vitest/build, i18n/tasks/tools checks,
and `playwright test stay22-maps.spec.ts`. Browser tests use an explicitly labeled
external-frame fixture, not live affiliate clicks. Check 390px containment, 44px
controls, keyboard load/close, no pre-consent requests and no trip writes.

After explicit merge/deployment approval, smoke-test a real signed-in Tokyo and
Taipei trip: open lodging, load map, check destination/date/guest controls and real
inventory, then close it. Verify original hotel selection and partner clickouts.
No test bookings. Disable the pilot by removing the panel integration or setting
the backend pilot context to null; no persistent trip data requires cleanup.

Official references (checked 2026-09-08):
- <https://dev.stay22.com/docs/maps/quick-start>
- <https://dev.stay22.com/docs/maps/parameters>
- <https://dev.stay22.com/docs/maps/troubleshooting>
- <https://www.stay22.com/privacy>
