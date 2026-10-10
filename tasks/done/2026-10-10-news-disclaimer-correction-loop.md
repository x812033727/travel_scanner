---
id: 2026-10-10-news-disclaimer-correction-loop
title: Investigate recurring news disclaimer corrections after locale review
status: done
priority: P1
area: api
owner: codex-news-recovery-6f71
claimed_at: 2026-10-10T00:52:37Z
created_at: 2026-10-10T00:43:43Z
completed_at: 2026-10-10T01:16:13Z
branch: codex/news-recovery-20261010
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_policy.py
  - apps/api/tests/test_news_pipeline.py
---

# Investigate recurring news disclaimer corrections after locale review

## Why

The 2026-10-10 08:36 Taipei production snapshot has 75 candidates currently held
for locale review; 74 of their latest locale-review reasons concern investment
disclaimers. All 75 retain a discarded second-round correction with verdict
`revise`. The 90-candidate redraft queue has already been returned by the judge,
including 42 candidates at the lifetime two-rewrite cap. Retrying the full story
can spend calls without resolving the translation problem.

The earlier disclaimer fix (#1371, `af596412c`) and correction-history fix
(#988, `1765b223d`) are both ancestors of live SHA
`35f99a16d7e4bcd5807845cdeded929894bf21ac`. This is not an undeployed-fix report.
The former `_canonical_disclaimer_text` appends a canonical sentence when only
the callout title contains the marker, and `_locale_review` reapplies it after
the reviewer returns a correction. This permits a possible delete/reappend
cycle within one callout. The snapshot alone does not establish the cause in
each candidate because it lacks the original and raw corrected document text.

## Definition of done

- [x] A minimal hash-bound regression reproduces the deletion/reappend cycle;
      individual production candidates still require fresh independent review.
- [x] A correction that preserves the required warning can pass both locale-review
      rounds without reintroducing a sentence the reviewer repeatedly removes.
- [x] Regression checks exercise the complete correction/helper/second-review
      sequence and preserve legitimate warnings and original-document verdicts.
- [x] Existing held drafts and judge rewrite limits remain intact; any production
      recovery is a separately authorized, bounded operation with readback.

## Steps

- [x] Reproduce from hash-bound original/corrected documents or a minimal fixture;
      distinguish helper reappending from a model failing to return its correction.
- [x] Align the warning helper and hard checks with the documented
      disclaimer requirement without blindly deleting the warning.
- [x] Run targeted policy/pipeline tests and the applicable API checks.
- [x] Hand the verified repair and a precise recovery cohort to the current
      news-backlog operations task.

## How to verify

Run `pytest tests/test_news_policy.py tests/test_news_pipeline.py` from `apps/api`
with the worktree virtual environment, then applicable ruff and mypy checks.
The regression must compare original, raw corrected and post-helper hashes and
simulate the second reviewer, not merely assert helper idempotence or callout count.
Do not call production providers or reopen candidates as part of reproduction.

## Notes

- Read-only inspection evidence: `<home>/.codex/news-review/20261010-6f71/`;
  `snapshot.json`, `readback.json`, `inspection-items.json` and
  `inspection-summary.json`. Snapshot SHA-256:
  `8545e0f27902e0765a8a73eb21eaabf24cc5241adddf9a7217e38c2fe8aab84f5`.
- Four current candidates have five related assessments on 2026-10-10 Taipei:
  CFTC `60bb93bf-13c4-4402-ad2a-49dc7076360f`, DWF/BitGo
  `0f5b3fda-7270-4cfb-b978-f6b2c0a1be0b`, Starknet `a823405c` prefix,
  Ledger `efc90b90-7f0d-41f9-b4a3-2b4f7d59b4b0`. Four of those assessments
  have identical original and discarded-correction fingerprints. Starknet also
  has a punctuation correction, so its hashes differ.
- Related open tasks: `2026-10-07-resolve-current-news-review-and-redraft`
  (production cohort), `2026-10-06-news-judge-translations-only-rerun`
  (translations-only recovery). This ticket investigates the warning-correction
  cycle rather than introducing that broader recovery route.
- No candidate was retried, rejected, rewritten or published during this inspection.
- Repair: recognize the existing explicit title/body callout without appending a
  sentence to it. Only the news-specific crypto finance-no-disclaimer error is
  excluded when that callout exists; shared lint and every other hard check remain.
- Key regressions failed before the repair (4 failures, exit 1) and passed after
  it (4 passes, exit 0). Policy, pipeline, automation and saved-bundle suites:
  267 passed, exit 0. Full API Ruff, git diff --check and task validation passed.
  Mypy app: 470 files, no issues, exit 0. Mypy tests: 380 files, no issues, exit 0.
- Independent code/operator review found no blocking issue. The implementation
  changes only policy.py and its policy/pipeline tests; no production data or
  judge history is changed by this patch.
- Draft PR #1411 contains the repair. The repository CI and owner-controlled
  merge/deploy remain separate gates from completion of the authored repair.
