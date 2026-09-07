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

- [ ] Additive fresh/upgrade migrations and community tables.
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

Checkpoint: community/schema tests passed locally (30 passed, one real-S3 test
skipped); Ruff and mypy passed. CI now provisions private MinIO and exercises
the same API contracts against PostgreSQL as well as SQLite. Local Windows has
no Docker/PostgreSQL; real service validation is not yet complete. Existing main
now uses migration 0056 for travel services, so community revisions must be
rebased and renumbered before PR delivery. See docs/community.md for launch gates.
