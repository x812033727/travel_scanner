---
id: 2026-10-22-review-everyday-curio-lint-duration-binding
title: Review everyday Curio lint duration binding
status: review
priority: P1
area: docs
owner: codex-gpt6-duration-independent-review
claimed_at: 2026-10-22T02:40:33Z
created_at: 2026-10-22T02:39:53Z
completed_at:
branch: codex/everyday-curio-guard
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Review everyday Curio lint duration binding

## Why

PR #1667 adds a Curio visual gate to everyday brand stories. Its two changed core lint files are bound by the independently reviewed long-form duration receipt, so CI's smoke test fails until a separate reviewer checks the duration effect and rebinds those exact bytes.

## Definition of done

- [x] An independent duration-only review covers the two changed files and the other 106 bindings remain current.
- [x] The report and receipt bind the exact code bytes and explain why the visual gate cannot lower the duration floor.
- [ ] The plan check, receipt test and PR smoke check pass on the reviewed head.

## Steps

- [x] Compare the prior receipt, report hash, source diff and all 108 registered file hashes.
- [x] Inspect the visual predicate and run focused lint, duration and plan tests.
- [x] Record the independent review and update only the two changed file bindings.
- [ ] Verify and push the reviewed PR head.

## How to verify

`node tools/video/long-form/cli.mjs check`; `node --test tools/video/long-form/review.test.mjs tools/video/core/duration.test.mjs tools/video/long-form/plans.test.mjs tools/video/core/lint.test.mjs`; PR #1667 smoke CI.

## Notes

Claimed with `--force` only after confirming that the three overlapping receipt claims belong to already merged PRs #1387 (2026-10-18), #1593 (2026-10-19) and #1614 (2026-10-20). Their board files remain stale, but no open PR owns this receipt scope. The author of the source change is `codex-gpt6-everyday-curio-guard`; this receipt reviewer is a different agent. Before rebinding, `check` failed only on `tools/video/core/lint.mjs` and `tools/video/core/lint.test.mjs`; the prior report hash matched its receipt. Focused lint, duration and plan tests passed 68/68 on Node v24.13.0. After rebinding, the plan check passed all 473 plans and the receipt-inclusive suite passed 70/70. Local `npm run check:tasks` remains blocked by the guard ticket's preexisting untracked `tasks/done/` duplicate; CI sees only the tracked open file. The exact deletion had already been rejected by automatic approval review as `blocked by policy`, so no alternate deletion was attempted. No paid media or upload was called.
