---
id: 2026-10-08-integrate-external-look-import-duration-review
title: Integrate external look import duration review after PR 1387 receipt reconciliation
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-08T15:16:48Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Integrate external look import duration review after PR 1387 receipt reconciliation

## Why

The external-look import implementation changes three SHA-bound test/review files. Its independent duration-only delta review passes, but refreshing the shared report here would overlap active PR #1387. The shared receipt still rejects this branch until both increments are reconciled.

## Definition of done

- [ ] Reconcile the current landed/shared report with the independently reviewed external-look increment; retain prior review provenance and bind the actual integrated bytes.
- [ ] Long-form review gate and relevant duration regressions pass on the integrated head without weakening the guard.

## Steps

- [ ] Recheck #1387 and #1388 ownership, heads and exact deltas before claiming this shared scope.
- [ ] Inspect the increment and any intervening source changes, update report/receipt only after independent review, then run checks.

## How to verify

Run `node --test tools/video/long-form/review.test.mjs tools/video/core/duration.test.mjs tools/video/qa/duration.test.mjs tools/video/long-form/integration.test.mjs` and `node tools/video/long-form/cli.mjs check` on the integrated head.

## Notes

Evidence: `docs/videos/series-plans/ou-de-jianghu/visual-development/import-contract/duration-increment-review.md` and its JSON contain the independent read, exact three hashes and 20 passing targeted tests. Author codex-ou-import; reviewer codex-ou-root-review. On 2026-10-08, who-is-on-it found #1387 touching review.md; neither shared receipt file was modified by #1388 in this turn. This is integration follow-up, not paid production authority.
