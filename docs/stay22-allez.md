# Stay22 exact hotel clickouts

## What this adds

Reviewed catalog hotels can open their exact Booking.com, Agoda or Expedia
property page through Allez without loading a map. This is a clickout integration,
not an availability API, booking engine, or confirmed commission report. Dynamic
hotel-provider quotes and their existing clickouts remain separate.

The booking panel appears in destination catalogs, near-hotspot catalogs, and the
trip accommodation catalog. The trip stay-area flow puts reviewed hotels first;
the map is a collapsed, consent-gated secondary option. Original trip dates and
saved travelers are projected as `booking_context`, independently of a live
provider's shorter search window or the Tokyo/Taipei map pilot.

## Configuration and rollout

`/admin/hotels` → configuration includes an independently saved Stay22 section:

```json
{
  "version": 12,
  "stay22": {
    "enabled": false,
    "aid": "mokaair",
    "enabled_providers": []
  }
}
```

Send this to `PATCH /api/v1/admin/hotels/config`. The catalog's existing JSON and
optimistic version lock are reused; no migration is needed. An older full config
PUT that omits `stay22` preserves it. Modifying Stay22 requires the backend
`settings.manage` capability; content-only users cannot alter affiliate settings.
The existing hotel-workspace read gate still applies to its UI. A settings-only
operator can PATCH only Stay22 fields, not unrelated hotel content configuration.

Each platform exposes counts and real record filters for existing affiliate,
Stay22-capable, missing URL, expired review and blocked records. “Capable” means a
reviewed exact link can be used if enabled, not that tracking is verified. Maps
settings remain independent. Disabling Allez restores the ordinary channel
selection without rewriting any hotel/offer record.

Initial release stays **disabled**. After separately authorized deployment, a
human with the Stay22 account should check a small number of reviewed property
links, same-hotel landing, retained dates/occupancy and Hub attribution. Enable
only individually verified platforms. Do not make test orders or infer commission
from click counts. Merge, deploy and live activation are separate approvals.

## Routing and safety contract

1. A valid existing exact-hotel affiliate offer wins.
2. Without that offer, an enabled Stay22 platform may use Allez.
3. Otherwise, the existing ordinary-link setting decides direct versus unavailable.

An error while executing the existing affiliate channel does **not** switch it to
Stay22. Its existing direct fallback policy is unchanged. DNT/GPC exclude the new
Stay22 channel, also respecting the ordinary-link setting. Eligibility is checked
again on click, so old browser cards cannot bypass changed config or expired review.

`POST /api/v1/travel-services/{product_id}/booking-options/{option_id}/clickout`
returns 303. It accepts an empty body for legacy callers or an optional JSON /
URL-encoded form with only:

```json
{"check_in":"2030-11-01","check_out":"2030-11-30","adults":2,"children":1}
```

Dates must be complete, real calendar dates, not past in the destination timezone,
and checkout must follow check-in. No dates or guest counts are invented. Users
can explicitly choose to set dates on the OTA. Only whole-number adults 1–9 and
children 0–9 are accepted; total party policy follows the existing traveler schema.
Rooms and ages appear in the saved preference summary but are not sent to Allez.
The OTA must confirm them. Inputs are capped at 4 KiB and reject duplicate fields,
caller URLs, AID, channels, arbitrary tracking data and undocumented parameters.

Allez URLs are built exclusively on the server:
`https://www.stay22.com/allez/{booking|agoda|expedia}` with `aid`, once-encoded exact
`link`, `campaign`, `lang`, `currency=TWD`, optional `checkin`, `checkout`, `adults`
and `children`. Campaigns contain only public destination, platform, locale and
placement labels. No account/trip ID, contact data or private itinerary is sent.
No Stay22 request is made during catalog loading, map expansion, hover or prefetch.

Exact property URL paths are deliberately conservative. Query strings, fragments,
embedded redirects, tracking, encoded traversal and non-property paths are not
wrapped. Editors must review clean canonical links rather than the system silently
stripping parameters. Existing HTTPS/OTA host/DNS/identity/review gates remain in
effect. There is no Roam, LinkSwap, LMA, fuzzy matching or whole-site rewriting.

The BFF enforces same-origin POST, never follows affiliate redirects, forwards
DNT/GPC, and applies no-store/no-referrer. Browser-form failures return a localized
HTML retry/return page; JSON clients retain Problem Details. A bounded first-party
`return_to` hint is consumed only by the BFF error page and stripped before the
upstream API call. Retry retains the four non-secret preference fields. It cannot
turn into an arbitrary redirect. The original tab and itinerary remain untouched.

## Observability and verification

`AffiliateClick` stores partner `stay22`, original OTA, public placement/destination
and `redirected` status. `HotelBookingClick` stores actual mode and fallback state.
Neither record means a booking or earned commission. No new database table is used.

Focused backend tests cover URL encoding, exact identity safety, channel precedence,
privacy, dates/party parsing, real first-party HTTP click persistence, stale reviews,
unknown options, JSON config preservation, capability checks and optimistic locking.
Browser fixtures cover destination, nearby and trip lodging panels on desktop and
Pixel 7, with no real affiliate clicks. The BFF has separate safe-error HTML and
proxy tests; five-locale keys/placeholders are checked alongside normal i18n checks.
General CI also runs the existing PostgreSQL/Redis/full-stack/migration and Compose
checks; external OTA/Stay22 tracking health is not a CI claim.

## Official protocol references

- [Allez quick start](https://dev.stay22.com/docs/allez/quick-start)
- [Allez parameters](https://dev.stay22.com/docs/allez/parameters)

Documentation supports the link format, not a guarantee that a particular account,
platform, date, room or tracking attribution will survive its final redirect.
