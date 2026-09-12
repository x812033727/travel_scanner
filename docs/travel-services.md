# Contextual travel services

## Release boundary

The catalog is off by default. This implementation does not apply brand approvals,
invent inventory, seed fabricated hotels or deploy production configuration. It does
not charge a member's use balance. Partners complete all bookings externally.

Public routes use the authoritative destination catalog at
`/{locale}/destinations/{destination_id}/services`; all 33 current destination IDs
are accepted. The legacy `osaka` and `kyoto` URLs remain compatible and resolve
destination-level offers through `osaka-kyoto`.
Administration: `/{locale}/admin/travel-services`. The planner's four service shortcuts
and existing stay-area flow use the same catalog. Hotspot details link to nearby stays.
Public browsing and clickout are anonymous; saving and selecting require sign-in.

The existing encrypted **API & keys → Travelpayouts** configuration is the network
account. Its token, marker, project ID and enabled flag are reused, never sent to
the browser. No Klook or KKday direct affiliate key is required.

### Read-only account verification, 2026-09-07 09:10 UTC

Project `570089` currently shows 26 available and 20 to unlock. Within this catalog's
brand registry, Klook, KKday, Airalo, Saily, Yesim, GigSky, Kiwitaxi, Welcome Pickups,
GetTransfer.com, intui.travel, Tiqets and WeGoTrip appeared in **Available**, with
Generate link controls. Booking.com, Trip.com, Agoda, Expedia, Viator, GetYourGuide
and Rakuten Travel appeared in **Unlock more**, with the project review notice.
Source: the signed-in [project programs page](https://app.travelpayouts.com/programs?source=570089).
This is a dated observation, not an API entitlement or an evergreen approval seed;
it does not automatically enable any brand. No account settings were changed.

## Operator sequence

### Ordinary hotel booking (no affiliate enrollment)

Hotel catalog browsing, ranking and lodging selection do not require a Travelpayouts
account. `facts.hotel_links` adds reviewed ordinary links independently of affiliate
offers; `direct_hotel_links_enabled` defaults to false. No migration or paid inventory
API is needed. Existing affiliate enrollment and validation rules are unchanged.

1. Import hotel-only CSV rows (omit `brand`/`target_url`/`scope`) without a network
   project. Mixed imports containing affiliate offers still require a project and
   fail before writing any products if it is missing.
2. In the hotel card's **Ordinary hotel booking links** editor, add a provider,
   exact hotel URL and identity evidence URL. `official` requires same-host evidence;
   platform URLs must belong to their registered brand. Do not label an area search,
   platform homepage or another hotel as an exact property. A reviewer must check
   the actual hotel's identity, source permissions and existing precise-map rules.
3. Save, then review/approve. Changes reset the whole product to pending. Approval
   validates public HTTPS DNS and each redirect, with bounded requests and no stored
   page bodies. Cross-host redirects or a different final property path/query fail
   closed; submit the final exact URL with matching evidence instead. Captchas,
   anti-bot responses and unavailable pages are not silently treated as verified.
4. Enable ordinary hotel links plus the hotel category and relevant destinations;
   the public destination page additionally requires `public_enabled`. No production
   flags or products are enabled by deploying this change.
5. Re-review every 30 days. Stale links disappear while lodging selection remains
   available. Disabling a product or the ordinary-link flag revokes clickout.

Example `facts.hotel_links` shape (illustration only; not seeded product data):

```json
[{"provider":"official","url":"https://hotel.example.com/stay","evidence_url":"https://hotel.example.com/location"}]
```

The public API returns `direct_links` containing only provider identity/name, not
raw link or review evidence URLs. New-tab same-origin forms use
`POST /travel-services/{product_id}/hotel-links/{provider}/clickout`, which resolves
the saved ID, checks current eligibility and revalidates the HTTPS destination
before a no-store 303. No caller-supplied destination is used. The endpoint is
anonymous, rate-limited and does not call Travelpayouts, add affiliate click records,
change booking status or mutate a trip. The website check may fail if a booking site
blocks automated verification; keep the hotel selectable and use another reviewed
link. Prices, availability and cancellation rules are confirmed only off-site.

Ordinary links are visibly separated from commission-bearing offers and never show
an affiliate disclosure by themselves. Existing ordinary hotel links remain available
when affiliate credentials are removed; enabling affiliate offers later does not
require rebuilding the hotel catalog or the lodging-selection flow.

### Affiliate offers

1. Verify the current project's subscription status in Travelpayouts, not an older
   screenshot or another project's approval. Record a project evidence URL under
   Brands. Only approved + enabled + verified-within-30-days brands can sell.
2. Import a UTF-8 CSV under Import CSV. Preview performs schema validation, not
   human approval. Commit is idempotent and creates pending products/links. A bad
   preview blocks the whole import. Original creator/product names are retained.
3. Open the source and verify identity, destination and each fact. Hotels require
   official/authorized coordinates, an existing stay area and exact map identity:
   reviewed Naver entry/place ID for Korea; Google Place ID elsewhere. Google or
   Naver pages cannot serve as durable editorial coordinate sources.
4. Approve products individually. Editing important facts returns them to pending.
   Add a separate sales link per verified brand/property mapping. A destination
   search is explicitly a **destination**, never presented as the exact hotel.
5. Run **Verify link & approve**. The server uses the Partner Links API (or a
   verified static link), follows bounded DNS-pinned HTTPS redirects, requires the
   expected brand/product path and original query identity. Static links must
   expose matching marker/project in the Travelpayouts redirect chain; opaque
   unprovable links are not approved. Changing marker/project invalidates static
   verification. Bot protection can prevent automatic verification; do not bypass
   the safety check or claim success.
6. Check coverage and missing facts. Targets: each city has six hotels in at least
   two areas, three tours, two actual airport routes; Japan/Korea/Taiwan each have
   three eSIM plans. Coverage is an editorial count, **not** confirmation of active
   inventory, link usability, bookings or revenue. Review sales links separately.
7. Enable only verified destinations/categories, then public pages, in Release
   controls. Unpriced hotels remain unpriced. A link failure does not substitute
   a different product or silently redirect to a generic home page.

### Destination-level brand offers

Destination-level offers are a separate contract from exact products. They are
stored as a brand, destination, module and original landing page. They may say that
the traveller will continue searching on the named external platform; they must not
claim a particular hotel, transfer, flight, tour, price or availability. Exact
products continue to use `TravelServiceOffer`.

The admin destination-offer checklist only accepts brands and modules from the
code-controlled registry and URLs on that brand's allowlisted domains. Creating or
editing an offer leaves it pending. Approval requires a currently approved and
enabled brand for the configured project, a fresh brand review, a successful Partner
Links conversion (or reviewed static Travelpayouts link), and redirect verification
that preserves the brand and destination identity. Both brand and offer verification
expire after 30 days. A project, marker or account-setting change also invalidates
the saved verification context.

`GET /affiliates/destination-offers?destination_id=...&module=...&placement=...` is
anonymous and returns only offer IDs, brand labels, localized call-to-action text and
same-origin clickout paths. It never returns the original or tracked URL. The associated
POST clickout resolves the stored offer server-side, shares the existing 100 requests per
minute Partner Links budget/cache, records brand/module/destination and the placement
that rendered the button, and returns a no-store 303. Invalid, disabled, stale,
mismatched and unapproved records fail closed.

`placement` is the same closed `BookingPlacement` vocabulary the hotel clickouts use
(`destination`, `hotspot`, `trip`, `stay`, `checklist`, `discovery`, `guide`, `city`, `share`).
`guide` is a travel-intel or how-to article, `city` a destination page and `share` a
read-only shared trip; all three are first-party content surfaces and are **off by
default**. The trip planner uses `trip`. `CatalogConfig.affiliate_placements`
(Release controls → 目的地合作方案) lists the surfaces that may show offers; a surface not
in the list gets an empty options list and a 404 on click, so a page loaded before the
switch was turned off cannot click through. The placement is also the last `sub_id`
segment (`dst_activities_tokyo_zh-TW_guide`) so partner dashboards can split it, and the
admin analytics page reports `affiliate_clicks` by placement, partner, module, destination
and brand (`GET /admin/analytics/affiliates`). Those are redirect counts, not bookings.

`GET /trips/{id}` (full payload) and `GET /shared-trips/{token}` carry
`partner_offers: {destination_id, modules}` — availability only, computed by
`partner_offer_modules` for the `trip` and `share` surfaces respectively — so the planner
and the share page can render a collapsed partner block without a request on first
paint. The offers themselves are fetched only when the block is opened.

Saved-search and trip affiliate options put verified branded destination offers
first. The generic Travelpayouts option is shown only when no branded option is
eligible, and a direct partner with the same brand is not duplicated. Commission is
never used for ranking. Deployment does not seed or approve any brand or destination
offer; the operator must re-check the live Project `570089` state after deployment,
create the intended 33-destination matrix, verify every link, and only then enable
the catalog release controls.

### CSV contract

Required: `source_key,kind,destination_id,title,source_url`.
Optional: `names_json,facts,brand,target_url,scope`. At most 500 rows / 500 KB.
`kind` is `hotel|transfer|tour|esim`; scope is `product|destination`.
`names_json` maps only `en,ja,ko,zh-TW,zh-CN` to reviewed names.
`facts` is JSON (escape quotes using ordinary CSV double-quoting). Use the admin
JSON editor for corrections, or CSV for new entries. Omitted information is unknown.

Facts supported:

- Hotel: `area_code`, `latitude`, `longitude`, `coordinate_source_url`,
  `google_place_id` / `naver_map_url`, `map_verified`, verified `facilities`.
- Transfer: `airport`, `direction` (`arrival|departure|roundtrip`), `passengers`
  (capacity), `luggage`; optional duration and verified availability window.
- Tour: `languages`, `attraction_ids`, `meeting_point`, `duration_minutes`,
  `available_start`/`available_end` (`HH:mm`, both or neither).
- eSIM: ISO `country_codes`, `validity_days`, `data_gb`, `unlimited`, `tethering`,
  `reference_price`, `currency`, timezone-aware `price_checked_at`.

Do not copy full pages, unlicensed images, Google ratings, Google descriptions or
Google-sourced coordinates into this durable catalog. There is no scraping or AI
discovery in this module. Do not append tracking to an already-affiliated URL.

## Recommendations and selections

Hotel cards rank by weighted straight-line distance from existing itinerary
evidence (the existing stay-area engine supplies the stop weights), otherwise the
selected place/city center. The nearby detail entry supports 1/3/5 km. Osaka and
Kyoto have distinct location filters despite sharing a KIX gateway. Commission
is never an input. Amenities, capacity and language filters use only verified facts.
eSIM coverage must include every known trip country and sufficient validity days.
Different currencies/packages are not presented as price comparisons.

`TripServiceSelection` has one row per trip/product and a request hash/idempotency
key. Mutations require ownership + the current itinerary version. Drafts are
flushed first; conflicts remain explicit. Hotel selection updates primary lodging
and eligible daily anchors, protects locked/fixed-time anchors, marks any previous
quote stale, and never creates a zero-price quote. No multi-hotel overnight logic.

Tours and transfers with no explicit times remain to-arrange selections. A later
selection of the same product can schedule it once. Explicit times must be inside
trip dates, one local day, verified availability and capacity, and must not overlap
existing stops. Fixed-time activity rows carry `service_kind` (transfers must not
be hidden in the legacy logistics section). eSIMs never occupy timeline slots.
Scheduling a transfer also requires its airport, direction, flight number and
passenger count. These remain itinerary details, not affiliate tracking parameters.
`booked` is self-reported. Clicking out never marks a booking; cancelling a local
selection neither cancels with the provider nor deletes a scheduled stop.

## Background maintenance

The existing analytics scheduler also submits one daily `travel-services` RQ job
with a deterministic ID and bounded retries; the worker consumes this queue.
An approved Airalo brand and the explicit feed flag are required for feed fetches.
The official XML feed is fixed, HTTPS/DNS-pinned, capped at 15 MB, rejects XML
entities/DTDs and imports at most 500 supported JP/KR/TW products. Unsupported or
unparseable feed data is not replaced with mock data. New facts stay pending.
Price-only refresh preserves reviewed restrictions; identity/package changes require
review. Reference prices disappear after 48 hours without a successful update.
Regional coverage can be entered manually from official sources; it is not guessed
from plan names. Check import history for failed/not-configured feed runs.

Up to 40 approved links are checked daily. Invalid links are disabled without
deleting selections. Unsafe redirects are disabled; transient network failures
advance their check timestamp without disabling the offer or starving later links.
Manual content is flagged for review after 30 days. Brand
and link approvals expire from public eligibility after 30 days.

## Link and analytics contract

`GET /travel-services`, `GET /trips/{id}/travel-services`,
`POST /trips/{id}/travel-services` (Idempotency-Key required),
`PATCH /trips/{id}/travel-services/{selection_id}`,
`PUT|DELETE /saved-items/service/{product_id}`.

`POST /affiliates/offers/{offer_id}/clickout` and
`POST /affiliates/destination-offers/{offer_id}/clickout` accept only a saved offer ID and a
whitelisted placement. The same-origin BFF POST form opens a new tab with a 303;
no arbitrary target URL is accepted. The BFF validates its locale and strips it
before forwarding a controlled header. Destination, not user/trip/product ID, is
used in the network `sub_id`. API credentials stay behind the BFF.

Partner Links requests use one link per call (below the ten-link maximum); a shared
atomic rolling Redis window caps **all brands/legacy flows together** at 100
requests/minute/marker. Cache identity includes project, marker, target, placement,
brand/offer version, locale and token digest. Unsupported brands use only verified
static links. API requests set `shorten=false` to obtain auditable full links;
the full-link cache namespace isolates previously cached branded `tpx.gr` shorteners.
Kiwi.com requires a reviewed static link because the official Partner Links API
excludes it. No Drive keyword injection or automatic link rewriting is introduced.

Production checks on 2026-09-08 confirmed that the configured account can create
full Aviasales, Klook and KKday links. This is conversion evidence, not destination
approval: the checked Klook and KKday pages returned HTTP 403 from the server,
and KKday additionally redirected through an unapproved `invl.me` intermediary.
These candidates remain unpublished until their exact landing pages and complete
redirect chains can be verified. Do not mark anti-bot responses as healthy or relax
the final-brand, destination-identity, or static-tracking requirements.

Click records add nullable actor + brand/type/placement/destination. The admin shows
outbound clicks and self-reported booked selections, and explicitly reports that
confirmed commission is **not connected**. No test order is placed.

## Validation and rollout checklist

- API unit tests cover URL safety, map identity, ranking, coverage, expiration,
  cache isolation and provider failures; integration tests require PostgreSQL.
- Integration: `RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_travel_services_integration.py`.
- Web: i18n parity, typecheck, lint, focused Vitest and production build.
- Browser: `e2e/travel-services.spec.ts` uses clearly labeled fixtures, all five
  locales, 320/390/1280 px, dark appearance, anonymous links and planner back/focus.
- CI additionally runs fresh PostgreSQL migrations, all API/web tests, production
  images and the existing PostgreSQL/Redis/RQ full-stack journey.
- Migration `0063_destination_offers` follows `0062_merchant_platform_links` and
  adds the destination-level offer table with existence guards for current-metadata
  fresh installs. Earlier `0056_travel_services` guards remain in place. Downgrade drops catalog tables; it leaves
  click actors nullable to avoid deleting anonymous accounting history.
- Before production: verify current brand approvals, meet real content targets,
  verify actual landing identity + tracking, inspect empty/error states, and enable
  categories deliberately. CI fixtures are not live provider verification.

## Official references

- [Travelpayouts brands with APIs/feeds](https://support.travelpayouts.com/hc/en-us/articles/20384016664594-Brands-that-provide-access-to-APIs-and-data-feeds-for-Travelpayouts-partners)
- [Partner Links API](https://support.travelpayouts.com/hc/en-us/articles/25289759198226-API-for-Travelpayouts-partner-links)
- [Airalo feeds and affiliate conversion](https://support.travelpayouts.com/hc/en-us/articles/17131439719826-Data-from-Airalo)
