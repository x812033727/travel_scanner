# Contextual travel services

## Release boundary

The catalog is off by default. This implementation does not apply brand approvals,
invent inventory, seed fabricated hotels or deploy production configuration. It does
not charge a member's use balance. Partners complete all bookings externally.

Public routes: `/{locale}/destinations/{tokyo|osaka|kyoto|seoul|busan|taipei}/services`.
Administration: `/{locale}/admin/travel-services`. The planner's four service shortcuts
and existing stay-area flow use the same catalog. Hotspot details link to nearby stays.
Public browsing and clickout are anonymous; saving and selecting require sign-in.

The existing encrypted **API & keys → Travelpayouts** configuration is the network
account. Its token, marker, project ID and enabled flag are reused, never sent to
the browser. No Klook or KKday direct affiliate key is required.

## Operator sequence

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
deleting selections. Manual content is flagged for review after 30 days. Brand
and link approvals expire from public eligibility after 30 days.

## Link and analytics contract

`GET /travel-services`, `GET /trips/{id}/travel-services`,
`POST /trips/{id}/travel-services` (Idempotency-Key required),
`PATCH /trips/{id}/travel-services/{selection_id}`,
`PUT|DELETE /saved-items/service/{product_id}`.

`POST /affiliates/offers/{offer_id}/clickout` accepts only a saved offer ID and a
whitelisted placement. The same-origin BFF POST form opens a new tab with a 303;
no arbitrary target URL is accepted. The BFF validates its locale and strips it
before forwarding a controlled header. Destination, not user/trip/product ID, is
used in the network `sub_id`. API credentials stay behind the BFF.

Partner Links requests use one link per call (below the ten-link maximum); a shared
atomic rolling Redis window caps **all brands/legacy flows together** at 100
requests/minute/marker. Cache identity includes project, marker, target, placement,
brand/offer version, locale and token digest. Unsupported brands use only verified
static links. No Drive keyword injection or automatic link rewriting is introduced.

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
- Migration `0056_travel_services` follows `0055_analytics_event_names`; existence guards
  support metadata-based fresh installs. Downgrade drops catalog tables; it leaves
  click actors nullable to avoid deleting anonymous accounting history.
- Before production: verify current brand approvals, meet real content targets,
  verify actual landing identity + tracking, inspect empty/error states, and enable
  categories deliberately. CI fixtures are not live provider verification.

## Official references

- [Travelpayouts brands with APIs/feeds](https://support.travelpayouts.com/hc/en-us/articles/20384016664594-Brands-that-provide-access-to-APIs-and-data-feeds-for-Travelpayouts-partners)
- [Partner Links API](https://support.travelpayouts.com/hc/en-us/articles/25289759198226-API-for-Travelpayouts-partner-links)
- [Airalo feeds and affiliate conversion](https://support.travelpayouts.com/hc/en-us/articles/17131439719826-Data-from-Airalo)
