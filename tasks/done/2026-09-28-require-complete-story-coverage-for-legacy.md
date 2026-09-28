---
id: 2026-09-28-require-complete-story-coverage-for-legacy
title: Require complete story coverage for legacy news evidence hashes
status: done
priority: P1
area: api
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T05:17:00Z
created_at: 2026-09-28T05:16:42Z
completed_at: 2026-09-28T06:51:38Z
branch: codex/pr892-evidence-guard
depends_on: []
scope:
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/feeds.py
  - apps/api/tests/test_news_legacy_evidence.py
---

# Require complete story coverage for legacy news evidence hashes

## Why

PR #892 accepts an old extractor hash when the modern extractor differs. With a
self-closing image after navigation or the opening paragraph, the old extractor
never recorded the rest of the story. Editing that story leaves the legacy hash
unchanged, so the compatibility fallback currently approves changed evidence.
The merge watch reproduced this on exact head a82d08d7 with synthetic HTML.

## Definition of done

- [x] Legacy compatibility only accepts a complete current story covered by the
      authenticated legacy text; newly uncovered body text requires fresh evidence.
- [x] Existing complete legacy text plus removed chrome remains compatible.
- [x] Changed-body, truncated-body and partial-line cases fail closed in regression tests.
- [x] Focused tests, lint and typing pass.
- [x] Current-head CI passes after the fix is pushed.

## Steps

- [x] Reproduce unchanged legacy text despite an edited body after a self-closing tag.
- [x] Verify the regression fails before the guard change (three failures: returned True).
- [x] Add the exact coverage guard and verify compatibility and rejection cases.

## How to verify

From apps/api: `uv run --locked pytest tests/test_news_legacy_evidence.py tests/test_news_automation.py -q`.
Run ruff on changed Python files and mypy on news automation and its test module.

## Notes

- PR #892 is temporarily draft pending this fix. No production or publication action.
- The existing broader body-hash migration ticket is unowned and remains open;
  this narrow fix does not claim to finish that separate migration/release work.
- Dedicated branch codex/pr892-evidence-guard preserves the original PR commits.
  Synthetic reproduction is retained in test-results/pr892-legacy-probe.json.
- The original author added policy/backfill work while the guard was being investigated.
  Preserved commits through 8221e13a and moved our cases to a separate test file so they do
  not overlap that active task's test module. The guard does not change those policy decisions.
- Before the fix, all three new cases returned `(True, [])` for the edited story and failed.
  After the fix, the new module and existing news-automation module pass all 30 tests.
  Ruff and mypy pass for both edited modules and the new regression module.
  Receipts: test-results/pr892-before-guard.log and pr892-after-guard.log.
- Rebased only this fix onto the author's rewritten head 812004c0, preserving the additional
  trusted-source configuration. The same 30 tests pass again on that base
  (test-results/pr892-rebased-guard.log). Waited for the author's CI and rechecked their
  subsequent heads before pushing, preserving all intervening author commits.
- The author's 18bfc9bd run passed, then their branch was rebased again onto main9081d0a2
  as 8b3640ac. The news source/test files are identical across these bases; only main's CI
  evidence fix and season review package changed. Rebased only our guard onto 8b3640ac.
  Pushed the guard safely as da9bd6bbc151b65a99e04faf652468469a4f62e5. All nine relevant checks
  on that head passed, including CI run 36386153434 (full API, web, containers and smoke).
  Its exact API tree d232030dfa030740e1ee771c8c08e174252df844 matches the locally tested tree.
- Main subsequently advanced to 79e26fcd. The completed guard still needs the normal base
  update and latest-head CI before PR merge; this task closes only the implemented and
  validated evidence-coverage bug, not production backfill or the broader hash migration.
