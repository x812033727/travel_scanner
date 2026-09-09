---
id: 2026-09-09-hotel-evidence-continuation
title: Hotel evidence continuation after deployment
status: done
priority: P1
area: ops
owner: codex-hotel-evidence-review
claimed_at: 2026-09-09T00:28:09Z
created_at: 2026-09-09T00:28:09Z
completed_at: 2026-09-09T01:14:44Z
branch: codex/hotel-evidence-continuation-20260909
depends_on: []
scope:
  - docs/hotel-review-evidence-20260909
  - ops/hotel_review_evidence_20260909.py
---

# Hotel evidence continuation after deployment

## Why

Continue the user's hotel review with fresh IAB evidence after deployment f752ce43
and schema 0064. Prior batch finished at 40 approved/20 pending hotel products and
300 approved/60 pending options. Do not renew or overwrite prior receipts/evidence.

## Definition of done

- [x] Capture fresh live baseline and check the current normal review contract.
- [x] Research missing exact hotel/map/provider identities with timestamped sources.
- [x] Apply only sufficiently evidenced bounded decisions via normal admin services;
  preserve all prior approvals, out-of-scope full rows, settings, quotes and audits.
- [x] Verify actual effects and remaining evidence gaps without claiming all approved.

## Steps

- [x] Confirm current services/health/ready and identify application source changes.
- [x] Obtain new IAB source evidence; keep research leads separate from actual reads.
- [x] If writing, dry-run, fresh protected backup, normal guarded apply and replay.
- [x] Save independent SQL/public verification, tests and item-specific remaining notes.

## How to verify

Use the current deployed application source for normal guard/schema checks. Verify
all hotel rows before/after/replay, SQL receipts/audits/protected group fingerprints,
and anonymous six-city/five-locale public output. Use scoped Ruff/offline tests and
node tools/tasks.mjs check. No raw SQL moderation, paid calls, quote/booking,
deployment, migration, setting changes or unsupported map/coordinate overrides.

## Notes

Fresh 2026-09-09T00:27Z status: eight app services f752ce43, healthy Postgres/Redis,
/health ok and /ready schema 0064_klook_affiliate_channels. Travel service files
changed with the Klook channel release; inspect current code before reusing operators.
Research and validation delegates worked on bounded, disjoint artifacts within the
new evidence folder. Main agent performed all actual IAB observations and guarded writes.

19/19 normal approvals: Westin Kyoto product, 9 Kyoto Expedia, 7 Osaka global Rakuten,
2 Tokyo Agoda. Final 41 approved/19 pending hotels and 318 approved/42 pending options;
public 41/227. All 420 full rows unchanged on replay; original 340 approvals and 401
out-of-scope rows protected. Prior pending reasons retained, not fabricated fresh reviews.

Qualified acceptance, not full pass: strict provider-config invariant failed on a
concurrent layout.alerts_enabled change at 00:59:41 UTC, before first hotel edit
01:00:29. Backup/current read-only comparison proves only layout config/updated_at
changed, other 14 provider rows unchanged. Matching layout audit uses same admin actor;
do not infer another person. No setting restored or altered by this task. Original
strict failure/evidence/checker retained; 11 other SQL groups, all hotel/public/replay
checks pass. 229 tests, scoped Ruff, task board passed. See REPORT.md and qualified
assessment artifacts. Broad hotel moderation remains unfinished as listed in
remaining-items.json; this narrow new-evidence batch is complete, no PR/push/deploy.
