# Travel search and social discovery

## Product and rollout boundary

Mokaair's discovery entry combines approved travel facts, source-linked articles,
YouTube references, public travel stories and deliberately published itinerary
snapshots. The first audience is Traditional-Chinese independent travelers, with
Japanese, Korean and Taiwanese destinations emphasized while all five locales and
the existing destination directory remain available.

`DISCOVERY_ENABLED=false` is the default. A merge or deployment does not authorize
turning this flag on, enabling community, opening registration, importing content,
granting creator invitations or activating a paid provider. `/discovery/status`
is a public read-only switch. Discovery and `COMMUNITY_ENABLED` are independent:
catalog browsing and private discovery preferences must not open social APIs.

The existing airfare/lodging `/search` and saved-trip editor remain separate.
`/explore` is the content-search route; `/explore/collections` holds the unified
private collection experience. The new mobile navigation keeps Explore,
Collections, My trips and My visible. Publishing and notifications are secondary
actions and respect the community gates. When discovery is unavailable, existing
home and navigation remain usable. No default paid request accompanies page loads.

## Data and privacy contract

- Search/feed aggregate existing catalog references. No public web crawler,
  automatic AI answer, private itinerary search or commission-based ranking.
- Only currently public, reviewed and permitted-source data are eligible.
  Provider expiry, restricted/erased profiles, withdrawals and bidirectional
  blocks are rechecked; a pagination cache is not publication authority.
- Keyword and destination alias matching are explicit. Empty results are empty,
  not synthesized recommendations. Original-language content stays labelled.
- Results are a bounded discovery window, not a complete catalog export: up to
  100 eligible candidates per source, supplemental explicit-interest windows, and
  a five-minute, reader-bound ordering of at most 500 IDs. Each page reauthorizes
  current records; Redis never stores private content or raw search text.
- Preferences use explicit destinations/topics, saves and follows only. Users
  can dismiss results or reset. Personal responses are never shared between users.
- Collections reuse the existing private collection/reference storage. Article
  and video references do not become itinerary stops; only server-confirmed
  eligible place identities can go through the existing trip selection API.
- Creator invitations grant publication eligibility, not admin access or a
  review bypass. Existing verification, first-post review, risky-edit revision
  safety, reporting, blocking and account erasure remain required.
- YouTube URLs normalize to provider and 11-character video ID. Stored user input
  cannot assert embeddability. Fresh permitted provider evidence is needed for an
  embedded player; otherwise show a source link and the unknown/stale status.
- The privacy-enhanced iframe is click-to-load without autoplay, at least 200px
  in each dimension. Preserve source attribution and controls. No download,
  rehosting, transcript scraping or remote HTML injection.

Official player reference: https://developers.google.com/youtube/player_parameters

## Measurement

`GET /admin/discovery/metrics` is admin-only and reports the current environment's
last seven UTC days, excluding bots and honoring the existing analytics opt-out
and enable switches. It exposes aggregate search/no-result counts, saves, place
additions, publication and returning engaged **sessions**, not a claim about people.
Moderator-approved publications count as publications but do not turn moderator
review sessions into engaged travel-planning sessions.
Search terms, private trip text and viewing history are not stored in these events.
No event is sent to a new analytics vendor.

The product's north-star goal is returning members who save, plan or share. The
current consented analytics identity is session-scoped, so cross-day member
retention and attributable save-to-trip conversion are explicitly unavailable,
not fabricated zero percentages. Establish a baseline before promising lift;
any future stable member measurement requires a separate privacy-reviewed design.

## Acceptance and operations

1. Run API Ruff/mypy/full pytest and fresh/legacy PostgreSQL Alembic checks.
2. Run Web lint, typecheck, i18n, Vitest, tools/task checks and production build.
3. Run `e2e/discovery.spec.ts` on desktop Chromium and Pixel 7 for search, filters,
   source/type labels, private actions, keyboard focus, dark mode and click-only
   video loading. These responses are labelled test fixtures, not provider data.
4. Run `e2e/discovery-full-stack.spec.ts` with `DISCOVERY_E2E=1`, isolated
   PostgreSQL/Redis/Mailpit/API/worker and production Web. The separate workflow
   uses ordinary signup, verification, admin invitations/review and private APIs,
   never a production token or test-only authentication bypass.
5. Before any public activation, separately verify mail, media, moderation staffing,
   user-facing rules, actual approved content coverage and owner authorization.

Local browser commands use the existing Playwright configuration. Do not point
full-stack acceptance at production. Existing `ci.yml` regression suites remain
unchanged; `travel-discovery.yml` adds the new enabled-feature acceptance path.
