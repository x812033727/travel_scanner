---
id: 2026-09-07-mokaair-community-foundation
title: Mokaair community foundation and account safety
status: in-progress
priority: P1
area: api
owner: codex-community
claimed_at: 2026-09-07T09:22:14Z
created_at: 2026-09-07T09:22:13Z
completed_at:
branch: codex/mokaair-community
depends_on: []
scope:
  - apps/api/app/community
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/config.py
  - apps/api/app/auth
  - apps/api/app/i18n.py
  - apps/api/app/worker.py
  - apps/api/app/trips
  - apps/api/app/search/schemas.py
  - docker-compose.yml
  - docker-compose.prod.yml
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - apps/api/migrations
  - apps/api/tests/test_community_foundation.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_ui_text.py
  - .env.example
  - docker-compose.community.yml
  - .github/workflows/ci.yml
  - docs/community.md
  - apps/api/app/ui_text/schemas.py
---

# Mokaair community foundation and account safety

## Why

Members need a public identity and safe publishing without exposing their private
trip plans, account email or unreviewed photos. The accepted community plan also
requires verification, recovery and deletion before public activation.

## Definition of done

- [x] Additive fresh/upgrade migrations and community tables.
- [ ] Default-off, administrator-controlled feature policy and account verification.
- [ ] Private S3 image lifecycle with decoding, metadata removal and short URLs.
- [ ] Durable mail/deletion jobs with retries; existing planning remains available.
- [ ] API tests, Ruff and mypy pass; production activation requirements documented.

## Steps

- [ ] Implement and verify foundations.
- [ ] Verify versioned public posts, moderation, free itinerary forks and collections.
- [ ] Verify mutual-follow messaging, durable notifications and platform-paid translation.
- [ ] Verify reviewed pet conditions, traveller reports and conservative planning filters.

## How to verify

Run API pytest for community and schema, Ruff, mypy, then full CI including a fresh
PostgreSQL database. Test S3 with the companion Compose stack.

## Notes

Implementation starts at main 516713d in an isolated worktree. Community remains off
until all accepted flows pass and the owner supplies public policy/contact details.

Checkpoint: rebased onto main 54009ba; additive community/pet revisions are
0057/0058 after travel services 0056. Draft PR #340 remains private-rollout work.
CI 34130887751 passed the full API suite, Ruff, mypy, fresh PostgreSQL migrations
and private MinIO contracts. An ordered, same-member/same-post conversion funnel
and scoped report-attachment authorization have regression coverage.
Desktop/Pixel 7 real-service journeys reached the blocking checks; correcting
the test contract distinguishes unfollow (403) from hidden blocked peers (404).
CI 34133067407 passed 1,743 API tests with one skipped test, including fresh and
legacy PostgreSQL schema upgrades. Desktop and Pixel 7 publication/message and
SMTP reset/deletion journeys passed. Pet review browser acceptance still fails;
the current run records the secondary administrator trace and bounded actions.
Real reconnect/outage/capacity tests and production launch requirements remain open.
Local Windows has no Docker/PostgreSQL. See docs/community.md for launch gates.

Follow-up: 0060 adds typed post catalog references with legacy pet-ID reads.
Publication filters are rechecked on every read, including source-expired merchants.
Focused contracts cover all three place types, invalid input, duplicate references,
disabled entities and previous-version compatibility. Fresh/legacy migration checks
include the new column; exact-head PostgreSQL CI still must pass before acceptance.

Integration checkpoint: merge main f2c3b2a (hotel booking options). Community
revisions are now 0058 community / 0059 pet friendly / 0060 community places,
following main's 0057 hotel migration. Only unmerged draft migrations were renamed.
