# Combined long-form duration validation

Date: 2026-10-02 (Asia/Taipei). This records the implementation integrated into draft PR #1098. No media was generated, re-rendered, imported, deployed or published.

This is the tested snapshot at `84f2775e`. The subsequent main merge, migration ordering repair and genuine review refresh are recorded in [main-sync-validation.md](main-sync-validation.md); the earlier migration numbers and PR draft status below describe that historical snapshot.

## Combined behavior

All 473 effective planning entries retain their source hashes and decisions: seasons one and three have 100 entries each, season two has 92 adopted packages, brand stories have 100 entries and AI terms have 81 entries including one already covered term. Seasons one through three and AI terms target 600 seconds; brand stories retain 780 seconds and the AI range remains 540–660 seconds. The eight duplicate exclusions and the covered term are not remade.

Flat explainers accept integer minutes 8–20 with a ten-minute default. Legacy flat worker state below eight minutes is normalized to ten before new drafts, resumed writes, script fixes and replanning; invalid values fail before a model request. Ordinary drama and compilation limits retain their own formats. Generic long-video settings, prompts and lint also receive the peer implementation's eight-minute lower bound.

QA retains both rules. The five requested catalogs require current, hash-bound body and final-cut evidence of at least 14,400 frames at 30 fps. Bookends cannot fill a short body. The generic long-video final-cut rule also rejects invalid, fractional or string frame counts and a different FPS. Test-fixture exemptions require the actual repository test/smoke entry point; ordinary workers and CLIs cannot disable the floor through an inherited fixture marker. The actual-body floor is always fixed.

## Provenance and independent review

- Base: `a1b3cbada94a46bc2d3d83fc44988b49ab6b71b7`. Landed batch-nine source files from #1083 are reused without changing their historical bytes.
- Peer branch `claude/video-min-8-minutes` at `6523a44f0c89a82baaa844941d62afa4b7a61788`, now submitted as PR #1103, is incorporated on this draft. Another owner's branch and PR state are untouched; their completed ticket is imported exactly as Git provenance.
- The genuine independent [DURATION_ONLY report](review.md) and [receipt](review.json) bind all 70 registered files. The reviewer independently checks the installed report and every current file hash. Its final report SHA is `9d01f55e57f1469e43d17a3f25b305641cc28e0d296d3373379e3e7ef463df62`, including the separately reproduced, single-line review-form label correction. The CLI rejects missing, incomplete or stale review bindings.
- Independent comparisons preserve 307 historical source files, all 184 Shorts and the original localized titles. All 92 effective season-two chapter budgets total 600 seconds.
- All ten original package validators pass using their explicit `--batch=batch01` through `batch09` and `--batch=completion` arguments. Earlier negative-case validation is recorded in the original [validation history](validation.md).

## Local checks

| Check | Result | Scope |
| --- | --- | --- |
| Full tools suite | 1,113 passed, 2 skipped, 0 failed; exit 0 | Combined implementation and 70-file review guard |
| Worker/core regression | 67 passed; exit 0 | New drafts, old persisted worker state, script fixes and replanning |
| Planning/review/runtime integration regression | 19 passed; exit 0 | After the genuine 70-file receipt was installed |
| API affected regression | 149 passed, 5 skipped; exit 0 | Duration schemas, series, requests, settings and database-dependent cases |
| UI affected regression | 31 passed; exit 0 | Series/explainer duration behavior |
| Review-form regression | 30 passed; exit 0 | Deterministic reproduction of the obsolete 8–12 accessible-name expectation failed; only that expectation was corrected to the current 8–20 label |
| API schema and migration regression | 10 passed, 1 PostgreSQL skip; exit 0 | Constraint and migration behavior; live database verification belongs to CI |
| Full API pytest | 5,485 passed, 427 skipped, 2 warnings; exit 0 | Combined implementation; database/service integration runs in CI |
| Full API ruff and both mypy checks | Exit 0 | 447 app source files and 342 test source files |
| Web lint, i18n and typecheck | Exit 0 | Five locales and 25 namespaces |

The original full web run was started before the review-form expectation was corrected: 3,743 passed and one failed in 340 files, exit 1. Its sole failure was the stale label mismatch. A targeted reproduction established that exact cause, and all 30 tests in that file pass after its single-line correction, independently repeated by the reviewer. This is a full-run failure followed by a focused correction and validation, not a claimed second full local run. CI runs the complete web suite on the final pushed combined SHA. Local skips are not database acceptance.

## Migration order and delivery gate

The adopted `0117_video_min_8_minutes` follows `0116_video_project_category` and raises both generic settings bounds in one update before replacing the constraint with 8–30 minutes. A downgrade widens the constraint while retaining raised values. The local migration graph has a single head.

Unmerged Shorts PR #1097 also currently adds an 0117 revision after 0116. Before either later merge, the second implementation must rebase its own migration onto the actual landed head. If Shorts lands first, this duration migration and its regression test must be renumbered to 0118 with the Shorts revision as parent, then independently reviewed again. If this implementation lands first, the Shorts owner must rebase that revision onto this one. Never introduce a dependency on an unlanded migration or leave two unplanned heads; CI checks the graph and runs real PostgreSQL upgrades.

PR #1098 remains draft with `no-auto-merge`. Required checks `api`, `web`, `containers` and `full-stack-smoke` must pass on the final combined SHA before any separately authorized merge. These records establish planning and code delivery, not actual narration, images, cuts, listening approval or publication.
