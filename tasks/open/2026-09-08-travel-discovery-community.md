---
id: 2026-09-08-travel-discovery-community
title: Community curated video invitations and collection references
status: in-progress
priority: P1
area: api
owner: codex-discovery-community
claimed_at: 2026-09-08T23:24:28Z
created_at: 2026-09-08T23:24:09Z
completed_at:
branch: codex/travel-discovery-community
depends_on: []
scope:
  - apps/api/app/community
  - apps/api/app/saved
  - apps/api/migrations/versions/0066_discovery_community.py
  - apps/api/tests/test_discovery_community.py
  - apps/api/tests/test_community_foundation.py
---

# Community curated video invitations and collection references

## Why

Discovery needs safe video references, reviewed creator publishing, and private saved
article/video/hotel references without creating a second collection architecture or
requiring ordinary readers to enroll in the social publishing profile.

## Definition of done

- [x] Post snapshots accept only bounded canonical YouTube IDs; public playback is
      allowed only with fresh explicit provider embeddability evidence, otherwise link-only.
- [x] Discovery rollout requires a versioned administrator invitation to publish;
      invitations never bypass verification, restriction, first-post review, or erasure.
- [x] Existing private collections support reviewed guides/hotels, with account-only
      discovery service wrappers and current authorization checks on every read.
- [x] Account erasure clears invitations, discovery preferences, video/place references,
      and hotel favorites; consent-aware analytics records successful new actions only.

## Steps

- [x] Add 0066 with fresh-metadata and legacy-upgrade existence guards.
- [x] Preserve reviewed snapshots and reauthorize cached post candidates, blocks,
      withdrawals, locale/following filters before bounded feed limits.
- [x] Exercise migration idempotence, API policy, source freshness, private ownership,
      mixed legacy collections, replay analytics, and deletion in focused regressions.
- [ ] Parent integration: run PostgreSQL CI (including bounded concurrent first invite),
      full-stack E2E, complete API/web checks, and archive task after delivery.

## How to verify

From apps/api, using the sibling mokaair-admin-domains Python runtime with this
worktree on PYTHONPATH and DATABASE_URL=sqlite+aiosqlite://, RUN_INTEGRATION_TESTS=0:

- `python -m pytest tests/test_discovery_community.py tests/test_community_foundation.py -q`
  — 67 passed, 3 skipped in 53.51s. Skips are PostgreSQL-only/concurrency/integration
  checks; no production database or provider calls were used.
- `python -m ruff check app/community migrations/versions/0066_discovery_community.py tests/test_discovery_community.py tests/test_community_foundation.py` — passed.
- `python -m mypy app/community` — passed, 21 source files after final compatibility
  fixes; parent full mypy is the final integrated gate.
- `python -m alembic heads` — 0066_discovery_community (head).
- `git diff --check` — passed.

## Notes

- Discovery wrappers own the discovery flag; community endpoints retain OpenSession.
  Shared collection services require active authenticated accounts and private ownership,
  not Profile enrollment. Existing pet/restaurant references remain usable in their
  original community view; unsupported discovery references are removable unavailable
  entries and do not fail an entire collection.
- Invitation lock order is User FOR NO KEY UPDATE, invitation, then existing
  Profile/Post locks. The existing User row protects first-ever version=0 creation.
  This also allows FK KEY SHARE checks and serializes concurrent erasure/revocation.
- Revoking an invitation prevents new publication/approval/restoration; it does not
  silently remove previously reviewed public content. Existing moderation does takedowns.
- Public videos never fetch provider content. Current YouTube imports do not persist
  explicit embeddability status, so existing videos honestly remain link-only. Future
  trusted metadata can populate youtube_status; editorial approval alone is not proof.
- Existing test_community_foundation.py scope was explicitly added by parent solely
  to include 0066 in its legacy migration chain; current-column assertions remain intact.
- Final compatibility review added destination-alias search, SQL/JSON-null-aware
  post/itinerary filtering before the candidate limit, and canonical UUID replay
  matching that preserves existing collection row identities and avoids double analytics.
- Independent discovery review found cached User erasure races and stale-video
  starvation before the source limit; discovery owner fixed both with regressions.
- Final rich-card integration extracts `public_media_refs(session, revision)` from
  the existing post serializer. It returns ordered ID/alt/dimensions only, omits
  missing/deleted images, preserves the reviewed revision, and performs no storage
  access. Discovery reuses these refs; the existing media endpoint remains the
  authorization boundary for every short-lived signed URL.
- Publication analytics now identify the real request actor and mark the coarse
  `publication_source` as `author` or `moderator`; moderation does not attribute an
  administrator session to the content author. Replays still produce no new event.
- Latest focused addon check: `pytest tests/test_discovery_community.py -q` reports
  39 passed, 1 PostgreSQL-only skipped in 15.98s. Owned Ruff checks and mypy across
  21 community source files both pass after the image/helper and actor refinements.
- No commits, merges, paid calls, or production changes were performed by this task.
