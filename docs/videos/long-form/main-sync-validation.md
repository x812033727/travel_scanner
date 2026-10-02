# Long-form validation after the current main merge

Date: 2026-10-02 (Asia/Taipei). This continuation repairs PR #1098 after a later author synchronized main. It changes no production settings, submits no media jobs and publishes no videos.

## Observed state and cause

The previous `84f2775e` revision passed all eleven CI jobs. Remote `7c7a917b` merges that revision with main `14970711`, retaining both sides of the production-profile and duration changes. Main now includes character looks (#1095), slides PSNR (#1096), drama production profiles (#1094), Shorts automation (#1097) and source-language prompts (#1099). The continuation fast-forwards to preserve that submitted merge rather than overwriting it.

Shorts #1097 has actually landed `0117_video_shorts_topics` after 0116. The unmerged duration revision still used a separate 0117 after the same parent, producing two heads. Its API schema check failed with three failures and its full-stack upgrade failed with `Multiple head revisions`; neither failure was an infrastructure flake. Web unit checks passed, but web/tools and video smoke correctly rejected fifteen changed SHA bindings in the old independent duration receipt. They did not measure or approve a video.

## Repair and review

- Rename only the unmerged duration revision and its test to `0118_video_min_8_minutes`; parent is the already-landed `0117_video_shorts_topics`. Update revision/docstrings, the test's migration constant and the exact two review-registry paths.
- Add an explicit revision/parent assertion to the existing migration regression. Retain its setting backfill, idempotent upgrade, eight-minute constraint and widening downgrade behavior.
- Retain all 70 review requirements. A genuine independent incremental report must inspect the fifteen current-main changes plus the renamed migration/test and registry. Only then may its report and matching receipt replace the stale installed version. No removed bindings or relaxed drift checks are used to turn CI green.
- Keep all 473 plans, ten-minute explainer defaults, legacy-worker repair and fixed measured body/final floor. Main's Shorts, production profiles, character looks and PSNR behavior remain present. A subsequent merge also reuses #1100's localized-thumbnail implementation at main `a8f0833e`; its QA CLI change receives a genuine additional binding review.

## Local verification

| Check | Result |
| --- | --- |
| Alembic graph | Sole head `0118_video_min_8_minutes`, after Shorts 0117 |
| Schema, SQL dialect and renamed migration tests | 10 passed, 1 PostgreSQL skip; exit 0 |
| Full API ruff and mypy app/tests | Exit 0; 452 app and 344 test files |
| Worker, duration, QA, prompt, drama, assembly and production regressions | 192 passed; exit 0 |
| Ten original season-two package validators | All passed using explicit batch arguments |
| Thumbnail, i18n, packaging, rendering and duration integration | 59 passed; exit 0 after the latest main merge |

The first genuine continuation review binds 18 changes and 52 unchanged files, report SHA `97a79eb4299ba2f27a8ea7f0beff41420b8dad12ed814436b760c036b3a84768`. Its original complete tools suite passed 1,142 tests with two skips. The additional thumbnail review changes only the QA CLI binding, retains the duration context and both duration rules, and passes 17 QA/integration tests plus 15 independent thumbnail/i18n tests. The final genuine report is `dc6492c76d66fe9d9067703dc211d1aa96488772f4c16c87a5a7601b60a69cc4`: 19 changed bindings and 51 unchanged bindings relative to the old snapshot, with all 70 current files required. After mechanical installation, the reviewer independently confirms the exact report/receipt/file bytes, 19 catalog/review/runtime tests and CLI 473; all pass with exit 0.

The complete final tools suite passes **1,149 tests, zero failures and two skips**, exit 0. Task validation accepts **1,277 files**, and `git diff --check` passes. The later peer report commit `56815409` is preserved through a normal merge; the installed report covers the additional thumbnail merge and the explicit migration-parent regression, so no old or partial receipt replaces it. [Remaining stages and original tickets](remaining-stages.md) provide the next production entry points without treating plans as completed media.

At the final local delivery commit, fresh CI on the pushed revision is pending; its final SHA and actual outcomes belong in PR #1098. PostgreSQL/service integration still requires CI; a local skip is not a successful upgrade. The old green SHA cannot establish the later main-merged revision's acceptance.

## Delivery boundary

PR #1098 became non-draft outside this continuation; its existing `no-auto-merge` label remains. Required `api`, `web`, `containers` and `full-stack-smoke` must pass on the repaired final SHA before any separately authorized merge. This work does not change another author's branch, completed ticket or the landed Shorts migration.

The 473 entries remain duration planning records. First-season launch buffers and pilots, third-season production packages, brand-story pilots and AI-term narration/media continue in their existing tasks and production gates. This repair does not assert those full manuscripts, paid media jobs, listening approval, final cuts or owner publication are complete.
