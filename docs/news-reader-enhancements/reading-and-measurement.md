# Article continuation and first-party click reporting

The existing related-reading cards now offer a clear next step, and article topic links
point directly to their canonical hubs. The API still selects only readable, published
references in the requested language, in its existing editorial order. A related article
is not automatically described as a tutorial: both news and tutorials can have kind `life`.

## What is measured

`content_link_click` records a click on one of the marked related-reading or topic links.
The existing first-party event path identifies the source article. A closed `content_link`
object contains only `placement` (`related` or `topic`) and `target_path`. Source and target
must match the public article/topic route vocabulary and fit the existing 128-character
storage bound. Locale prefixes are removed from targets; queries, fragments, private
routes, external URLs, unknown fields and mismatched placements are rejected. No free-text
properties, body-inline tracking or new personal identifiers are introduced.

The browser waits for `GET /analytics/config` to return
`content_link_click_enabled: true`. An older API that omits the capability receives only
the event types it already understands. First-party disablement, DNT and GPC continue to
prevent collection; these new events also require a public source article. The event is
sent with keepalive and does not cancel or wait for navigation. Keyboard activation and
middle-click retain the ordinary link behavior. New content events are not sent to GA4;
its existing denied-consent defaults and third-party audience restrictions are unchanged.

## Reading the report

`GET /admin/analytics/content?range=30d&include_bots=false` requires `analytics.read` and
returns `Cache-Control: no-store`. The existing admin analytics page loads it separately,
so an unavailable or older endpoint cannot erase the traffic dashboard or affiliate report.
The section uses dedicated five-language catalogs rather than the shared admin catalog.

The report shows actual browser continuation-click counts and the top 20 source/target,
placement and language combinations. It separates environments and excludes bots by
default. These are client-reported interactions, not independently verified consumption.
The total includes all recorded clicks in the window; the list shows the top 20 pairs only.

The 24-hour, 7-day, 30-day and 90-day windows read retained raw events. A shorter configured
retention clips the window and is disclosed. The earliest retained continuation event is
shown explicitly; it is not claimed to be the original installation or tracking date.
The 12-month selection reports unavailable because the long-term rollup does not retain
these link dimensions. Empty data is not evidence that nobody continued reading: collection
may be disabled, blocked or declined.

No exposure event is collected. These numbers must not be labelled CTR, completed reads,
search impressions, rankings, purchases or income. Existing affiliate redirect counts
remain separate. Historical page views cannot be backfilled into continuation clicks.

## Compatibility and verification

No database migration, model or analytics scheduler changes are required. The event
vocabulary is already application-validated, and the existing JSON field stores the closed
payload. The typed browser schema does not widen the generic server-event property filter.
Old web clients continue working with the new API; new web clients remain functional with
the old API and simply omit the new event.

Focused tests cover route/payload rejection, capability negotiation, DNT/GPC, first-party
disablement, private pages, navigation without a measurement response, duplicate event IDs,
raw-window limits, exact source/target grouping, stale admin responses and separate failure
states. The PostgreSQL integration case exercises real JSON extraction/grouping and removes
only its own event IDs. Browser regressions live in the existing CI-listed
`guides-adsense.spec.ts` and `admin-analytics.spec.ts`.

This implementation and its tests do not authorize merging, deploying, enabling analytics,
publishing content or claiming a live traffic/revenue improvement.
