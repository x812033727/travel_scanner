---
id: 2026-10-04-plan-frontend-monetization-placements-and-refresh
title: Plan frontend monetization placements and refresh readiness
status: done
priority: P2
area: docs
owner: codex-monetization
claimed_at: 2026-10-04T05:53:57Z
created_at: 2026-10-04T05:53:56Z
completed_at: 2026-10-04T06:14:43Z
branch: codex/frontend-monetization-20261004
depends_on: []
scope:
  - docs/frontend-monetization-plan.md
  - docs/monetization-alternatives.md
---

# Plan frontend monetization placements and refresh readiness

## Why

The owner asked for frontend advertising and affiliate placement planning and
optimization. The September revenue plan contains stale ad-enable and article
measurement assumptions, and no current page-by-page placement/rollout matrix.

## Definition of done

- [x] A page-by-page plan separates ads, affiliate entries and direct sponsorship.
- [x] Read-only live settings, source capabilities and unverified revenue are distinguished.
- [x] The old plan no longer says individual article views are impossible or implies current advertising is off.
- [x] Metrics, rollout order and existing owner-dependent tickets are documented.

## Steps

- [x] Audit existing frontend, analytics and official partner/ad policies.
- [x] Verify public ad config and Tokyo affiliate inventory without submitting clickouts.
- [x] Write placement plan and correct old measurement statements.
- [x] Run task/diff checks and independent review of recommendations.

## How to verify

Review docs/frontend-monetization-plan.md against current components and the
linked official sources. Run npm run check:tasks and git diff --check.

## Notes

- 2026-10-04 public config: enabled=true, cmp_enabled=true. This is not account
  approval, active CMP message, ad delivery or revenue evidence.
- The Tokyo activities/guide query returned a Klook option; the live city page
  displayed activities/transport partner buttons and disclosure. No partner POST,
  order, conversion, sponsor sale or production write was performed.
- The 2026-09-29 owner choice to retain the destination activation task and avoid
  production data changes remains intact. Real partner attribution acceptance,
  hosting programme links and signed-in ad strategy remain in their existing tickets.
- Independent source/policy review corrected the income formula to use AdSense
  account page views and page RPM from the same reporting period, and removed the
  stale claim that one hosting sale necessarily beats display ad income.
- Task check validated 1,391 files; diff whitespace check passed. This planning
  document does not turn a historical owner estimate into current measured traffic.
