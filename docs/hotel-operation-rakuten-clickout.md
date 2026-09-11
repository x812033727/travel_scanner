# Hotel operating dates, Rakuten Japan and resilient booking handoff

## Scope and release boundary

Built from `origin/main` d0ec33ee in isolated branch
`codex/hotel-operation-rakuten-clickout`. Existing shared-checkout changes and
production moderation states are untouched. This PR does not approve the four
held Kyoto hotels, add hotels, activate an affiliate agreement, or deploy.

## Operating rules

`facts.hotel_operating_rules` is optional JSON, so existing rows need no database
migration. Set null to explicitly remove a rule using the normal versioned admin
edit and review workflow. New or changed catalog content still needs its normal
approval. The rules are not live availability or guaranteed room inventory.

```json
{
  "unavailable_stays": [{
    "start_date": "2027-01-14",
    "end_date": "2027-01-15",
    "reason": "Example only: source-backed conservative maintenance exclusion",
    "source_url": "https://hotel.example.com/operating-notice"
  }],
  "last_checkout_date": "2027-05-09",
  "last_checkout_reason": "Example only: source-confirmed final checkout",
  "last_checkout_source_url": "https://hotel.example.com/final-checkout"
}
```

The example is a synthetic schema illustration, not an approved hotel policy.
Periods are accommodation nights `[start_date, end_date)`: checkout on the first
excluded night is allowed; check-in on the end date is allowed unless another
restriction applies. The final-checkout date permits checkout on that date, not
another night's stay. Partial daytime closures must be explained explicitly;
conservative nightly exclusions must not be described as full-day shutdowns.

Each restriction needs a valid ISO calendar date, nonempty reason and public
HTTPS non-map source. Overlapping/duplicate ranges, malformed dates and partial
cutoff records are rejected. Raw malformed persisted rules fail closed. After
the final-checkout date starts in the hotel's destination timezone, the hotel
is removed from eligible public products without destroying historical records.

Guards run before selecting/replaying a hotel, quote quota/provider work,
DNS/affiliate resolution or redirects. Trip recommendations filter dates and
existing selections report availability against current trip dates. Legacy
date-less booking links and Stay22 raw-anchor exports cannot bypass restrictions.
Do not treat editing an existing trip's dates or AI schedule as a new confirmed
hotel reservation; those existing trip contracts are not changed here.

Restricted hotels must supply dates at the first-party booking panel. All
restricted stored booking URLs must be date-free: an opaque query is rejected,
not stripped (it might identify another property). An existing affiliate offer
with opaque query parameters cannot override caller dates; where allowed, use
the separately verified clean direct URL. This can temporarily disable links
whose identity depends on query parameters until explicitly reviewed.

## Admin and public interaction

The admin date fields edit the same product JSON draft. Save uses its existing
version; failed or conflicting saves keep the draft. There is no bulk approval
or direct publication action in these new controls. Public booking panels show
source-backed restrictions and block conflicting dates without navigation.
The BFF recognizes only three allowlisted operating error codes, renders local
five-language messages, preserves request IDs and removes ineffective retry for
date conflicts. It never renders upstream traces.

Stay22's script-enabled public document must not collect private trip dates or
mount account-aware booking UI. A restricted hotel links via a native full-page
navigation to `/[locale]/hotels/<id>`, a first-party booking page under the
ordinary root layout. Its read-only `GET /travel-services/<id>/booking-details`
reuses catalog eligibility and serialization, independent of the Discovery
switch. This discards the vendor document before the booking/date flow. A
policy change after page load similarly offers this first-party entry instead of
an endless failed raw-link retry.

## Rakuten Japan

The ordinary hotel link validator accepts only exact HTTPS
`travel.rakuten.co.jp/HOTEL/<positive numeric ID>/<same ID>.html` pages, without
query parameters. Search/list/map paths, alternate hosts, mismatched IDs and
redirect parameters fail. Japan and Global IDs have separate namespaces; no
conversion or cross-market guessing is performed. Japanese-market pages may
legitimately identify hotels in Taiwan or Korea, but the destination is unchanged
and a human must still verify the precise property.

The affiliate allowlist is unchanged. Japan targets do not match existing
affiliate offers and are excluded from raw anchors handed to Stay22's script.
Use the first-party direct POST instead; this is not an assertion that Rakuten
Japan affiliate/API support was approved.

## Browser diagnosis and fallback

On 2026-09-11, a fresh Chrome tab at the production Taipei Zhongshan catalog
opened amba's Trip.com button in a new tab at the precise hotel path
`/hotels/taipei-hotel-detail-1917532/amba-taipei-zhongshan/`. In the prior in-app
browser reproduction the same native POST produced no observable new tab. This
does not establish a provider/backend outage or certify booking inventory.
The external page subsequently redirected to Trip.com sign-in, with that same
hotel in its `backurl`. No login was attempted in this diagnostic tab and the
external booking flow is not claimed verified.

Preserve native POST + `_blank` + `noopener`. Only after an actual submission
attempt show "Not opened? Continue in this tab" for that platform. The fallback
uses `formTarget="_self"`, current validated fields and the same BFF endpoint;
no automatic retry, AJAX redirect, `window.open`, guessed URL or personal dates
in query strings. The external redirect still enforces no-referrer. Browsers
without a new-tab issue retain the original workflow.

## Validation and production follow-up

Local results (2026-09-11, PR #389): API full suite 2,955 passed / 161 skipped;
subsequent final hotel-boundary regression 273 passed / 2 skipped. Full API Ruff
and Mypy (303 files), Web lint/typecheck/i18n, 27 tool tests and the final
production build including the independent hotel route pass. The first full
single-worker Web run finished with 1,918 passed, three timeouts in unchanged
new-trip-form / destination landing tests and one admin-test worker-start
timeout. Isolated reruns of all three affected files passed (48 tests); this is
not a claim that the original full run was green. Both booking browser suites
passed all 60 desktop/mobile tests against local fixtures, including same-tab
POST and SDK-document isolation with Discovery disabled. Final-head PR CI is
required for PostgreSQL, the full Web suite, containers and full-stack evidence;
its live checks are the release gate, not these local rerun results.

- API: `uv run ruff check .`, `uv run mypy app`, `uv run pytest -q`.
- Web: lint, typecheck, i18n, single-worker Vitest, production build.
- Browser: `stay22-allez.spec.ts` and `stay22-script.spec.ts`, desktop Chromium
  and mobile Chromium; only local fixture booking responses, no real orders.
- CI: PostgreSQL upgrades, API integration, production containers and full-stack
  smoke. Local Docker is unavailable; those checks are not claimed locally.

After explicit merge/deploy authorization, refresh each held hotel's official
operating notice, enter its exact conservative policy, reverify platform identity
and complete normal approval individually. Check Booking.com, Trip.com, Agoda,
Expedia and Rakuten only where a genuine reviewed property page exists. Never
fabricate a platform page or approve solely to lower the pending counter.
