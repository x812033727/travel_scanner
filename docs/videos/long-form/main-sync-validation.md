# Long-form validation after the current main merge

Date: 2026-10-02 (Asia/Taipei). This continuation repairs PR #1098 after a later author synchronized main. It changes no production settings, submits no media jobs and publishes no videos.

## Observed state and cause

The previous `84f2775e` revision passed all eleven CI jobs. Remote `7c7a917b` merges that revision with main `14970711`, retaining both sides of the production-profile and duration changes. Main now includes character looks (#1095), slides PSNR (#1096), drama production profiles (#1094), Shorts automation (#1097) and source-language prompts (#1099). The continuation fast-forwards to preserve that submitted merge rather than overwriting it.

Shorts #1097 has actually landed `0117_video_shorts_topics` after 0116. The unmerged duration revision still used a separate 0117 after the same parent, producing two heads. Its API schema check failed with three failures and its full-stack upgrade failed with `Multiple head revisions`; neither failure was an infrastructure flake. Web unit checks passed, but web/tools and video smoke correctly rejected fifteen changed SHA bindings in the old independent duration receipt. They did not measure or approve a video.

## Repair and review

- Rename only the unmerged duration revision and its test to `0118_video_min_8_minutes`; parent is the already-landed `0117_video_shorts_topics`. Update revision/docstrings, the test's migration constant and the exact two review-registry paths.
- Add an explicit revision/parent assertion to the existing migration regression. Retain its setting backfill, idempotent upgrade, eight-minute constraint and widening downgrade behavior.
- Retain all 70 review requirements. A genuine independent incremental report must inspect the fifteen current-main changes plus the renamed migration/test and registry. Only then may its report and matching receipt replace the stale installed version. No removed bindings or relaxed drift checks are used to turn CI green.
- Keep all 473 plans, ten-minute explainer defaults, legacy-worker repair and fixed measured body/final floor. Main's Shorts, production profiles, character looks and PSNR behavior remain present.

## Local verification

| Check | Result |
| --- | --- |
| Alembic graph | Sole head `0118_video_min_8_minutes`, after Shorts 0117 |
| Schema, SQL dialect and renamed migration tests | 10 passed, 1 PostgreSQL skip; exit 0 |
| Full API ruff and mypy app/tests | Exit 0; 452 app and 344 test files |
| Worker, duration, QA, prompt, drama, assembly and production regressions | 192 passed; exit 0 |
| Ten original season-two package validators | All passed using explicit batch arguments |

Final genuine-review checks, the complete tools suite and the pushed revision's CI are recorded when available. PostgreSQL/service integration still requires CI; a local skip is not a successful upgrade. The old green SHA cannot establish the later main-merged revision's acceptance.

## Delivery boundary

PR #1098 became non-draft outside this continuation; its existing `no-auto-merge` label remains. Required `api`, `web`, `containers` and `full-stack-smoke` must pass on the repaired final SHA before any separately authorized merge. This work does not change another author's branch, completed ticket or the landed Shorts migration.

The 473 entries remain duration planning records. First-season launch buffers and pilots, third-season production packages, brand-story pilots and AI-term narration/media continue in their existing tasks and production gates. This repair does not assert those full manuscripts, paid media jobs, listening approval, final cuts or owner publication are complete.
