# Modular Stay22 switch

## Operator contract

Use **Admin → Hotels → Hotel settings**. `stay22.enabled` is the master switch.
Turning it off retains AID, LMA ID, integration mode and native-platform choices,
but restores the existing affiliate/direct-link policy. The UI distinguishes the
confirmed saved mode from an unsaved preview; saving does not execute vendor code.

Two integration modes deliberately do different jobs:

| Mode | Public destination hotel document | Native app/trip buttons |
| --- | --- | --- |
| Off | Existing page and channels | Existing affiliate/direct policy |
| Allez | Existing page | Reviewed exact links use server Allez where eligible |
| Full Script + native Allez | Isolated public hotel document with LMA | Existing audited POST → server Allez where eligible |

Native Allez retains existing-affiliate priority and its three supported OTA
selections. The public LMA document exposes only independently reviewed original
property URLs, not already wrapped Allez URLs. Native POST endpoints are not
invented as LMA DeepStruct patterns, and neither hidden outbound links nor fake
property identifiers are used to make the vendor scanner find a hotel.

## Actual Hub configuration inspected

The user supplied LMA ID `6aa15a455ff1d17f658d1692` for `mokaair.com` and explicitly
accepted the full scope shown in Hub: Agoda, Booking.com, Expedia, GetYourGuide,
Hotels.com, KAYAK and Vrbo, plus Spark and Nova. Hub's editing page says provider
exclusions/default-feature adjustments require contacting Stay22. The application
must not suggest its three native Allez platform checkboxes control that full SDK.

The documented bootstrap sets `window.Stay22.params.lmaID` before loading only
`https://scripts.stay22.com/letmeallez.js`. The Script ID is validated configuration,
not arbitrary JavaScript or a user-controlled script URL. Hub initially showed
Inactive; this is not proof of a defect, and saving our configuration is not proof
of SDK execution, a verified click, booking or commission.

Sources: [user's Script details](https://hub.stay22.com/en/lma-script-builder/6a9fc80810fb99ee3eccdc9b/detail/6aa15a455ff1d17f658d1692),
[official installation and DeepStruct guide](https://community.stay22.com/how-to-set-up-your-letmeallez-script).

## Lifecycle and privacy boundary

LMA lives only in a separate root document for public destination hotel pages.
The ordinary root continues to own admin, authentication and private itinerary
flows. A full document navigation is required when crossing that boundary; removing
a React `<Script>` element cannot undo a third-party observer, timer or handler.
The Script document has no session/Email header, personal collections, private trip
identifiers or private editing widgets. Travelpayouts Drive is not loaded in the
same Script document. Switching off affects new documents; reload already-open
Script pages to discard vendor code that has executed.

Explicit non-hotel views and destinations outside the reviewed city catalogue
retain their original workflow. Destination navigation from that original view
uses full document anchors even within the same route group. The SDK also checks
`document.referrer`: private paths, query/fragment conditions and foreign origins
prevent loading. A clean destination URL alone does not conceal a private referrer.

This is DOM/document separation, **not a separate cookie or security origin**.
Stay22 remains a trusted third-party script running on the site's origin. Do not
claim it is technically unable to make same-origin requests or that these layouts
provide account isolation. No arbitrary SDK loader, private data payload or new
analytics identifier is introduced by this integration.

DNT/GPC, configuration-read failure and non-production origins prevent SDK loading.
Script additionally requires the ordinary hotel direct-link policy to be enabled:
its original anchors must remain permissible when a blocker or network failure
prevents SDK execution. Disabling ordinary links disables the effective Script
configuration and original-link endpoint, but does not disable eligible native Allez.
The public configuration endpoint exposes only effective state, mode and a valid
LMA ID. Original hotel links still require publication, review, age and URL/DNS
safety gates. Enabling the full SDK does not add new hotel platform types, verify
missing hotel URLs or guarantee all seven suppliers appear in this catalog.

The Script catalog is a public browsing surface; it does not silently copy private
itinerary settings or fabricate dates, room types, prices or inventory. Dates and
occupancy must be confirmed at the external platform. Existing native POST Allez
buttons retain their validated optional booking-context handling.

## Validation and rollout status

The earlier first-click fix `d9ef8fcd` is merged and live; its exact official and
Booking discovery POSTs returned 303. The production setting at the start of this
change is Allez enabled for Booking only (`mokaair`, config version 7).

This new Script work is separate. Tests use synthetic vendor responses and block
external traffic; no test orders or real affiliate clicks are used in CI. Review
and merge the feature, deploy its exact green main SHA, then explicitly save the
Script mode/ID in the admin UI. Verify a small genuine visit in Chrome and Hub
before calling the SDK or account attribution verified. Do not relabel the older
Allez verification as LMA verification.

Browser fixtures enforce offline mode with a disconnected-network canary in
addition to request interception. Query stripping is asserted over loopback HTTP
with redirects disabled, followed by a separate clean-document browser check.
An earlier exploratory fixture could let fulfilled redirects escape interception
and may have made unintended production page GETs; that run is not network-isolation
evidence. The affected CI runs were canceled before publishing the corrected
transport. No real affiliate click or booking is claimed by any of these checks.

Local validation: full Ruff and mypy (291 application files), full ESLint,
five-language checks, 27 tooling tests and a production Next build (267 routes)
passed. Backend scope has 326 passing tests and two PostgreSQL-only skips;
the isolated public document has 44 passing focused Vitest tests and admin switch
has 10. The corrected offline-guarded Playwright run passed all 50 cases across
Desktop Chromium and Pixel 7 (28 Script and 22 existing Allez), including production
wire headers, mode switching, public/private document boundaries and modal layout.
The complete
local Vitest run was intentionally stopped under host memory pressure rather than
reported as a pass; CI remains responsible for the complete regression suite.
