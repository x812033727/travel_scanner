---
id: 2026-09-07-mokaair-community-foundation
title: Mokaair community foundation and account safety
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-07T09:22:13Z
completed_at:
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/tests/test_community_foundation.py
  - docs/community.md
---

# Mokaair community foundation and account safety

## Why

Members need a public identity and safe publishing without exposing their private
trip plans, account email or unreviewed photos. The accepted community plan also
requires verification, recovery and deletion before public activation.

## Definition of done

- [x] Additive fresh/upgrade migrations and community tables.
- [x] Default-off, administrator-controlled feature policy and account verification.
- [x] Private S3 image lifecycle with decoding, metadata removal and short URLs.
- [x] Durable mail/deletion jobs with retries; existing planning remains available.
- [x] API tests, Ruff and mypy pass; production activation requirements documented.

## Steps

- [x] Implement and verify foundations.
- [x] Verify versioned public posts, moderation, free itinerary forks and collections.
- [x] Verify mutual-follow messaging and reviewed pet/traveller/planning contracts;
      historical real-service browser acceptance is recorded below, with fresh
      local API contract checks on 2026-09-29.
- [ ] Complete real-service translation failure/revision, worker restart/outage and
      capacity recovery acceptance; local contracts alone do not complete it.

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

CI 34137517824 / 43d0481 passed 1,776 API tests (one skipped), Ruff, mypy,
fresh/upgrade PostgreSQL and private S3. Publication/message and real SMTP
browser journeys passed on both devices; the pet draft-hydration race was then
fixed in e096aeb. That commit also adds a real offline/reconnect message check.
Do not mark social/pet acceptance complete until the full browser run passes.

e096aeb passed full CI 34138592625, including all six community browser journeys
and real offline catch-up. A repeat at 06b3b94 exposed PostgreSQL FK deadlocks
between the comment Post lock and fork User lock. The fix uses NO KEY UPDATE
for immutable-ID serialization and adds a PostgreSQL barrier test that forces
both locks to overlap, with concurrent idempotent forks. Verify this test in CI.

CI 34139969746 / e071cc7 passed Web, containers and all real-service browser
journeys. The new PostgreSQL regression failed during fixture setup because the
moderation response contains state/version, not the post ID. Preserve the published
post response separately before approval; rerun the barrier test on PostgreSQL.

34c4a84 passed complete CI 34140678769 and 34140675466, including the PostgreSQL
deadlock regression. Main fd160ff was integrated; 5282df2 passed full CI before
the owner-authorized squash merge of PR #340 as 7f21d7e. Main CI 34144356856
also passed (1,781 API tests, two skipped). The existing SSH path deployed that
exact SHA after a verified backup; migrations 0058–0060, ten running services,
three readiness checks and the authenticated admin page passed. Community stays
off, registration stays closed, and production SMTP is not configured. Details
and the backup location are in docs/community.md.

Follow-up on codex/community-account-safety: three added SQLite regressions first
failed against main: stale deleted-account mail issuance, cached consumed-token
reuse and retained typed post-place references. Fix by taking User before Token
locks, refreshing both snapshots and clearing place_refs during erasure. Add real
PostgreSQL overlap/replay/issuance tests; those must pass CI before this follow-up
is accepted. The wider background-worker/deletion, outage/capacity and multi-locale
browser acceptance work remains open.

### 2026-09-29 local P1 reconciliation (codex-p1-product)

Claimed for the owner-authorized P1 review. The matching implementation PRs are
merged and no matching open PR or active same-feature implementation was found.
The former broad scopes have been narrowed to this local acceptance work. Forced
claims only bypass historical/shared scope metadata; no other agent application
changes are taken over. No production or cloud-account access is included.

The local run of `tests/test_hotspot_discovery.py` and
`tests/test_community_foundation.py` passed: **52 passed, 8 skipped** in 213.84s.
The skipped cases require PostgreSQL or private S3; this machine has no Docker
command and no listening PostgreSQL/Redis/MinIO/Mailpit companion services.
The always-on contracts cover mutual messaging, token erasure/replay, translation
cache invalidation/budget, conservative pet filters and durable-job erasure.
This is API contract evidence, not a worker restart/load or real SMTP/S3 result.
PR #343 already merged the account-safety fixes; do not reimplement the stale
follow-up paragraph above. See `docs/community-local-acceptance-2026-09-29.md`
for the separately identified browser UI evidence and remaining real-service work.
