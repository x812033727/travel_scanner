---
id: 2026-10-04-news-publish-retired-diagram
title: Fix news publication blocked by the retired diagram requirement
status: done
priority: P1
area: api
owner: codex-gpt-6-news-recovery
claimed_at: 2026-10-04T05:32:49Z
created_at: 2026-10-04T05:30:20Z
completed_at: 2026-10-04T05:40:46Z
branch: codex/news-publish-diagram-regression
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_assets_storage.py
  - docs/news-automation.md
---

# Fix news publication blocked by the retired diagram requirement

## Why

Production scanning and three news workers are healthy, but automated news has not
published since 2026-09-30 20:31 UTC. PR #1042 removed the fixed editorial-process
figure at the owner's request; `ensure_assets` now creates only hero and social
artwork and removes old diagram blocks. `hard_policy_problems` still requires an
SVG diagram, so every otherwise eligible five-locale article fails publication.

## Definition of done

- [x] An article with actual generated news assets passes the diagram-related policy.
- [x] Other news publication checks remain enforced in all five locales.
- [x] A regression test fails on the old policy and passes on the corrected policy.
- [x] Documentation describes hero/social artwork without requiring the retired figure.
- [x] The validated fix and production evidence are ready for review; a separate recovery
      ticket records pending activation.

## Steps

- [x] Read production settings, sources, candidates, runs and RQ state without writes.
- [x] Identify the asset/policy mismatch and the owner's prior decision in #1042.
- [x] Remove the obsolete SVG requirement and test the real assets/policy boundary.
- [x] Run focused news suites, ruff, mypy and task validation.
- [x] Prepare the exact deployment/recovery handoff.

## How to verify

`cd apps/api && uv run pytest tests/test_news_assets_storage.py tests/test_news_automation.py
tests/test_news_pipeline.py tests/test_news_review_actions.py -q`

`uv run ruff check .`; `uv run mypy app`; `uv run mypy tests`;
`npm run check:tasks`.

## Notes

- Live read at 2026-10-04 05:27 UTC: SHA d038b035e; enabled/automatic and all
  three auto-publish flags true; 22 enabled sources; news queue, started and
  scheduled registries empty; three workers idle. Source scans succeeded recently.
- 38 needs_redraft/hard-check candidates plus one saved manual-review hard-check
  candidate; sampled lints all report `news_diagram`. The newest also has CJK
  punctuation errors, which remain a separate editorial hold.
- The 162 zh_draft_ready and 133 duplicate_uncertain candidates retain their
  individual review decisions; this fix does not approve or requeue them.
- Collision preflight: #1041 and #1172 are already merged into origin/main;
  their named branches are absent from local worktrees and remote heads, and
  there are no open news PRs. Their lingering review tickets still claim docs
  and the whole tests directory. A forced claim only bypasses these inactive,
  already merged scope records; their task files are not modified.
- No production settings, candidates, content or services have been changed.
- Regression proof: the old policy fails the real assets/policy test with only
  `news_diagram` in all five locales. Corrected asset storage suite: 9 passed.
  Focused assets/automation/pipeline/review-actions/admin suites: 220 passed.
- `ruff check .` passed; mypy app (460 source files) and mypy tests (362 source
  files) passed; task validation and diff whitespace checks passed. An optional
  formatter check flags three existing, unchanged policy spans; the required
  ruff check is clean and unrelated formatting was left alone.
- Independent review confirmed that source checks, five-locale verification,
  final-editor/Jev decisions and other hard policy rules remain unchanged.
- Operational continuation: `2026-10-04-news-publication-recovery`. That open
  ticket distinguishes the 38 unsaved bundles and one saved article, including
  punctuation holds and final gates that still need to run.
