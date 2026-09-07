# Mokaair community: private rollout and operations

This is a default-off addition to the existing Next.js BFF / FastAPI /
PostgreSQL / Redis / RQ application. It is not a separate social network service.
The owner must explicitly authorize public activation after acceptance. A merged
branch or green build alone is not evidence that mail, moderation or policies are
ready. The existing travel tools, accounts, locale-aware links, usage ledger and
read-only `/share/[token]` links remain independent.

## Routes and authorization

The five-locale Web routes include `/community` (recommended/latest/following),
`/community/search`, `/community/new`, `/community/drafts`, `/community/posts/:id`,
`/community/profiles/:handle`, `/community/collections`, `/community/settings`,
`/community/messages`, `/pet-friendly`, `/pet-friendly/:id`, `/explore` and `/my`.
The account area includes email verification, password recovery and confirmed
account deletion. Public identity is opt-in: account email is not a display name.

The public status API is `GET /api/v1/community/status`; it exposes only six
boolean switches with `Cache-Control: no-store`. Failed status reads hide the
community entry points. The effective `community` row in `provider_configs`
overrides `COMMUNITY_ENABLED`; the initial default is false. Existing effective
environment and database administrators share `/api/v1/admin/community/*` and
`/api/v1/admin/pet-friendly/*` authorization. No new client-inferred admin role is
introduced. The six switches cover community, publishing, comments, messages,
translation and pet reports. Unlike the older layout-only switches, these are
enforced by the APIs. Disabling a switch does not delete stored data.

Publication, comments, images and messages require a verified account. Existing
unverified members retain ordinary travel-tool access. The first three distinct
posts require manual approval; republishing one post does not advance that count.
Subsequent risky edits require review and leave the previous approved revision
visible. Moderation and restrictions require a reason and an admin audit record.
Report review shows the reported version/selected message context, not a general
administrator inbox. Members can read their own review results without access to
other reporters, moderator identities or unrelated accounting logs.

## Private images

Provide an S3-compatible private bucket through these server-side settings:

| Setting | Purpose |
| --- | --- |
| `COMMUNITY_S3_ENDPOINT` | API/worker endpoint; HTTPS in production |
| `COMMUNITY_S3_PUBLIC_ENDPOINT` | Browser-reachable signed-upload/image endpoint |
| `COMMUNITY_S3_REGION`, `COMMUNITY_S3_BUCKET` | Signing region and private bucket |
| `COMMUNITY_S3_ACCESS_KEY`, `COMMUNITY_S3_SECRET_KEY` | Restricted server credentials |
| `COMMUNITY_MEDIA_ORIGIN` | Exact image endpoint origin allowed by Web CSP; no secrets |

Never grant anonymous bucket reads or place the bucket behind a public caching
proxy. Configure CORS for the exact Web origin, POST and GET as required by the
S3 service; allow signed form uploads. Use a bucket lifecycle rule to expire
abandoned `quarantine/` uploads after one day. This rule must not expire completed
draft/post media. Scope the service identity to the designated bucket, with only
the object operations the image processor and account erasure require. Set any
object-version retention/backups in accordance with the published deletion policy.

Uploads accept only JPEG, PNG and WebP, at most 10 MB and 25 million decoded
pixels. Decoding rejects malformed and animated images, removes metadata
(including EXIF location), and creates WebP display/thumbnail variants. A post
allows ten images, a pet report five and an avatar one. No arbitrary remote image
fetching is supported. Raw objects are quarantined until processing completes.
Draft and pending images are owner-only; moderators use scoped review access.
Published media receives short authorizations of at most 60 seconds. Withdrawal
stops new authorizations; already downloaded bytes cannot be recalled.

## Mail and background jobs

Configure `COMMUNITY_SMTP_HOST`, `COMMUNITY_SMTP_PORT`,
`COMMUNITY_SMTP_STARTTLS`, optional username/password, and `COMMUNITY_MAIL_FROM`.
Production requires STARTTLS and a correct HTTPS `NEXT_PUBLIC_SITE_URL`.
Mail links carry a single-use 30-minute token in the fragment, not a query string;
the confirmation page removes that fragment before subsequent navigation.
Password reset does not disclose whether an address exists. Successful reset
increments the authentication version. Account deletion requires a separate
email confirmation plus `DELETE`, immediately revokes access and hides content.
Administrator self-deletion is blocked, preserving existing self-disable rules.

The existing RQ worker consumes `community`; the `community-sweeper` service
requeues durable database jobs once a minute. The encrypted mail job payload is
cleared when finished. Mail retries are bounded; account cleanup remains retryable.
Monitor job status in the community overview and worker logs. Account cleanup
removes private media/profile/travel details and de-identifies retained foreign
key identities. Historical accounting and already-delivered messages remain;
delivered messages display a deleted-member identity. Apple token revocation uses
the existing auth-revocation workflow. Do not manually delete database identities
with retained ledger foreign keys. Backup retention and legal retention require
an explicit operator policy; a background cleanup pass does not purge backups.

## Travel copies, translation and messages

Public itineraries are immutable, allowlisted snapshots: relative day, location
order and duration, without private notes, real lodging/flight details, bookings,
passengers or original quotations. Authors preview and authorize copying. A copy
uses the reader's departure date, stores provenance and starts without valid
prices/routes; it costs no member uses. Recalculation continues to use the existing
operation-cost catalog. Idempotency prevents duplicate trips on retry. Withdrawal
stops new reads/copies but preserves existing private copies and their replay.

Messages require current mutual following for every send. Unfollow, blocking and
restrictions stop new messages immediately. PostgreSQL is the durable source;
Redis wakes SSE listeners. Cursor replay and message idempotency handle reconnects.
Block filtering applies to both logged-in members, not anonymous public visitors;
the interface discloses this limitation. Analytics do not collect message bodies.

Translation uses the configured Gemini guide provider and a separate platform
character allowance, not the member ledger. Failures preserve original text.
Source edits change the cache fingerprint. Capacity is reserved before provider
calls, including failed calls, because provider usage may already have occurred.
The community overview reports distinct users by activity and return visits,
active authors, moderation age, translation reservations and durable jobs. These
activity totals are not an ordered attribution funnel or provider invoice totals.

## Pet-friendly data

A canonical place links reviewed hotspot/merchant/restaurant/hotel identities;
traveller reports never overwrite official rules. Each animal species has its own
status, weight/count rules, indoor/outdoor access, equipment, reservation, fee and
lodging conditions. Null means unknown. Freshness defaults to 180 days and is
configurable. Conflicts set a disputed state until an administrator checks a
source; the history retains evidence and before/after rules.

Filtering requires fresh verified rules that satisfy all requested conditions.
Unknown and incompatible places appear only when explicitly requested. Manual
trip insertion warns about conflicts; pet-aware AI candidates are limited to
verified compatible identities and report an insufficient-candidate gap instead
of relaxing conditions. No dataset is claimed to cover all destinations.

## Local and CI acceptance

The companion is development-only and uses published, non-production credentials:

```bash
docker compose -f docker-compose.yml -f docker-compose.community.yml up --build
```

Mailpit is loopback-only on port 8025, SMTP on 1025 and MinIO on 9000. If running
Web outside Compose, set its `COMMUNITY_MEDIA_ORIGIN` to the public S3 origin and
keep API/worker S3 settings consistent. Create a test administrator with the
existing `app.cli create-admin --password-stdin`; there is no auth bypass or
automatically created public member. Enable only the isolated test database's
community settings through the administrator API/UI.

```bash
cd apps/api
uv run ruff check .
uv run mypy app
uv run pytest tests/test_schema.py tests/test_community_foundation.py
uv run pytest --cov=app
# With PostgreSQL and private S3 test services:
# RUN_INTEGRATION_TESTS=1 COMMUNITY_TEST_S3=1 uv run pytest tests/test_community_foundation.py
cd ../..
npm run check:tasks
npm run check:i18n
npm run typecheck:web
npm run lint:web
npm run test:web
npm run build:web
cd apps/web
# Real app stack + Mailpit + private S3, test administrator seeded:
# COMMUNITY_E2E=1 PLAYWRIGHT_REUSE_EXISTING=true npx playwright test e2e/community.spec.ts
```

CI runs SQLite contracts plus PostgreSQL parameterizations and a real S3 signed
upload/processing test. The full-stack job runs existing travel journeys first
with community still off, then the community journeys on desktop and Pixel 7.
It stores browser artifacts separately. Windows without Docker cannot substitute
SQLite results for PostgreSQL, SMTP, Redis or real object-storage acceptance.

## Public-launch gates (not completed by adding this document)

- Complete fresh and existing PostgreSQL migrations, concurrency, private-media
  authorization, three-post moderation, copy/replay, reconnect and outage tests.
- Verify five locales, desktop/Pixel 7, keyboard controls, light/dark appearance,
  upload failures, rate limits, load/capacity and operational recovery.
- Complete privacy/terms/contact pages with the actual operator, retention rules,
  complaint process and contact details. Do not invent these values.
- Confirm production S3/CORS/lifecycle/private access, SMTP delivery, translation
  capacity, moderation staffing and escalation ownership using real services.
- Finish the ordered conversion funnel and comprehensive acceptance matrix;
  aggregate activity counts are not a substitute for full conversion tracking.
- Only then authorize and enable the community in the production admin console.
