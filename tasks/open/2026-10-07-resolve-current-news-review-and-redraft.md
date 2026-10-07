---
id: 2026-10-07-resolve-current-news-review-and-redraft
title: Resolve current news review and redraft backlog with audited outcomes
status: in-progress
priority: P1
area: ops
owner: codex-news-backlog-review
claimed_at: 2026-10-07T13:04:35Z
created_at: 2026-10-07T13:04:11Z
completed_at:
branch: codex/news-backlog-review-20261007
depends_on: []
scope:
  - docs/news-backlog-review-2026-10-07.md
---

# Resolve current news review and redraft backlog with audited outcomes

## Why

The owner requested decisions for the current news review queue and rewrites for the
redraft queue. They explicitly chose existing AI review after rewriting, with publication
when qualified. The 2026-10-07 13:04 UTC baseline contains 411 manual-review, 105
needs-redraft and four failed candidates. Existing automation is enabled in automatic
mode, all verticals allow publication and Claude Opus 5.5 review is enabled.

## Definition of done

- [ ] Every baseline candidate has a verified publication, documented rejection or
      duplicate outcome, or a documented unresolved blocker with a follow-up task.
- [x] Saved five-locale bundles are preserved and repaired without unnecessary redrafting.
- [ ] Rewrites run through independent verification and existing AI review.
- [ ] Durable before/after snapshots and audited actions support all outcome counts.

## Steps

- [x] Check the shared board, active branches and open PRs; capture baseline.
- [x] Confirm the owner's choice for review and publication after rewriting.
- [x] Release a small review/redraft pilot and inspect its actual decisions.
- [ ] Resolve excluded technical holds and failed candidates.
- [ ] Process the remaining baseline in bounded batches and verify final outcomes.
- [x] Start a bounded one-shot driver for the original eligible manual-review IDs.

## How to verify

Read persisted news candidate, assessment, run and audit rows, then verify published
article locales on the public site. Queue submission is not completion.

## Notes

- Persistent workspace: `<home>/.codex/news-review/20261007-fe41/`.
- `baseline.json` preserves all 520 candidates, documents, evidence, assessments and
  runs. `technical-holds.json` isolates holds the judge cannot resolve directly.
- No global provider, feature or publication settings have been changed.
- At 13:27 UTC, three baseline candidates were published, four rejected, two duplicate;
  the remaining 511 were still held or processing. This is not final completion.
- The original manual-review driver started at 13:29 UTC, PID 154702. Durable host
  receipts are in `/root/news-review-20261007-fe41/queue-driver/run`.
- The tested disclaimer code fix is tracked by
  `2026-10-07-recognize-translated-news-disclaimer-notices-and`; production rollout and
  redrafts blocked by that defect remain outstanding.
