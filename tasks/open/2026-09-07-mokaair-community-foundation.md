---
id: 2026-09-07-mokaair-community-foundation
title: Mokaair community foundation and account safety
status: review
priority: P1
area: api
owner: codex-community-recovery-20261003
claimed_at: 2026-10-03T12:37:39Z
created_at: 2026-09-07T09:22:13Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/api/tests/test_community_service_recovery.py
  - apps/api/tests/support/community_service_runtime.py
  - apps/api/tests/support/community_translation_upstream.py
  - docs/community.md
  - docs/community-service-recovery-acceptance-2026-10-03.md
  - .github/workflows/ci.yml
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

### 2026-10-03 isolated service recovery preparation

Force-claimed only this foundation ticket after the fresh seven-path gate proved
that the sole normal-claim refusal was PR #1172's already-merged `apps/api/tests`
ancestor metadata. Its original task, owner and remaining media/production gates
are preserved. The gate checked 495 refs, 976 committed task blobs, 28 registered
worktrees and the complete open-PR paths (only our #1175). Exact scoped Git/tree
comparison at main `a9c8e2b7e2b0a44cea5c9766e1699785c259c96f` found no new work.
Two 2026-08-31 OneDrive CI copies and stale done article-image review copies were
classified from landed history and left untouched. Private gate receipt:
`community-foundation-recovery-20261003/seven-path-gate-final.json`, SHA-256
`69c53e1b0e890c7e8e514f52d34ad00946098cf4dfe22f42bc5569f82430dd16`.

Prepared six real-service scenarios in a new opt-in suite; the existing mocked
foundation harness is unchanged. Scope is the three new test/support files, the
community documentation and a single CI step. After the concurrent tools run
finished, the exact 15-line CI step was inserted after stack readiness and before
the browser journeys, with a 15-minute bound; the rest of the workflow is unchanged.

Local preparation passed AST parsing, Ruff, Ruff format checks and scoped mypy
for all three new Python files. Final guarded collection found the exact six
node IDs, exit 0, without fixtures, test bodies, network requests or services.
The actual interpreter was the current API venv's Python 3.13.15; environment
variables were allowlisted, Settings environment-file loading was disabled and
both real-service opt-ins were absent. Its private collection receipt is
`community-foundation-recovery-20261003/collect-20261003T131353Z/receipt.json`,
SHA-256 `92b578f9c2ecf0a303a6f603b68560d69a824c1ccca4b51542127545bb519170`.
Scoped mypy passed after explicit Windows-visible attribute/type declarations
and an explicit existing default status value; its receipt is
`mypy-20261003T131047Z/receipt.json`, SHA-256
`6c4e927fdc244c6f30d76a39b9ad17ad75f4e13cd3bfd2f5912b755653c26f1d`.
Independent source-only review passed, including a byte-exact reversal check of
those type-only changes; final increment receipt SHA-256 is
`dfc34af30f528652019e8ff9575f04d9341cb2925438f9f4413ed5098705f6ba`.

Exact-head real-service CI is still pending. See
`docs/community-service-recovery-acceptance-2026-10-03.md` for observable contracts
and a capacity proposal requiring owner review. No capacity threshold is accepted,
no real-service pass is claimed, and this ticket must not be marked done yet.

Before committing, the upstream fixture's 76 CRLF endings were normalized to LF
so its physical bytes equal the Git-staged candidate. Independent reversal
reconstructs the original `6c10edec...` hash exactly; the AST is unchanged and the
other two files retain their original hashes. Final upstream SHA-256 is
`26540f05ffca4496545147c1dda6e2bb1a184294c1dafb453090ce9511ace606`.
The original preparation receipts remain intact; independent sidecar SHA-256 is
`8e2e37b5c526bc218d4497cdddda3bf81cb3569aef7ba12b53ffd19ee17ba32d`.
Read-only CI dependency/isolation review passed without service execution or
limit changes; receipt SHA-256
`6a6b7c1416c0931c13f5a782e7e07b1fa0f83ffb42f2219ad2e5a3be892f3c92`.

First exact-head CI `641e2576a2212550db384cfe5b9d3a3dc98b0b8f` exposed one
Linux-only mypy error: the inline conditional references Windows-only
`subprocess.CREATE_NO_WINDOW`. The equivalent statement-level platform branch
retains Windows hidden-process flags and Linux zero flags, with session/cleanup
behavior unchanged. Independent mechanical reversal recovers the exact original
runtime bytes; incremental review SHA-256
`ccfe963fefda7da1fe8692ed781ffccee64fa1c9a063d1155bf7cdd7bdd75392`.
Ruff/format and explicit `mypy --platform linux` pass all three fixture files;
Linux-target mypy receipt SHA-256
`81fecc7da9f58af0169be60de75660e07a125abb1012866bec13a06b24e9c17d`.
New runtime SHA-256 is
`625c01c131a9b54265fc7c8141f4236ddaafdda72f4d07f89bdcea7eb08d093e`;
the first CI's old runtime hash and failures remain preserved. New-head complete
CI and actual service acceptance remain required.

The first full-stack job has now completed. At PR head `641e2576...`, actual
checkout/GITHUB_SHA `61d41868ff88f88f3e86e76578939b0ec84c8382` ran all six
recovery cases: 6 passed, zero failures/skips, 391.00 seconds. Its sanitized
receipt confirms owned processes stopped, shared services were not stopped and
capacity acceptance was false. It binds the old runtime `5969aa1a...`, so the new
`625c01c1...` candidate still requires its own CI. The wider job failed because
the separate community browser matrix had 12 passed / 18 failed; those failures
are being repaired and this foundation ticket remains review.
Private canonical receipt SHA-256
`2f6b3b589cadaebf0dab9a1d388197f7b0a8ae4289fb77739ae062545daa8a81`.
Immutable [first full-stack job](https://github.com/x812033727/travel_scanner/actions/runs/37126555983/job/111212893808).
