# Long-form duration revision validation

Date: 2026-10-02 (Asia/Taipei). This records local planning and code checks; no actual video was rendered, measured, imported, deployed or published.

## Planning and independent review

- All 473 effective plans passed `node tools/video/long-form/cli.mjs check`: 100 first-season, 92 adopted second-season, 100 third-season candidates, 100 brand stories and 81 AI terms, including the one covered term.
- All ten original second-season package validators passed. The original negative harness rejected all 22 malformed cases and restored a passing baseline.
- Independent [DURATION_ONLY review](review.md) found no remaining required fixes. Its [receipt](review.json) binds 21 implementation, plan, document and test files. The first rebase onto `abbc276d409e9ac5e1e5c765792b569b14f99588` preserved all bindings. A second rebase onto `eda3b60fa9fb0d98e3c72ef31bcee67a7325d506` added upstream character-look validation in `series.py`; a genuine independent incremental review confirmed the minute-patch blocks remain byte-identical and the other 20 bindings remain unchanged. The updated report SHA is `9bc82b69faa54f895b215f2ade407a4f9d5d5905f80917c5c775843ba321fb51`. The installed report, refreshed receipt, full CLI check and 14 new tests passed again.
- Independent byte comparisons preserve 307 historical planning-source files and all 184 second-season Shorts. All 92 revised chapter budgets total 600 seconds; eight duplicate rejections remain excluded. Brand/AI targets and the covered AI term remain intact.
- The four new Node duration/planning/review test files passed 14 tests, including the real QA CLI fixture, the exact frame boundary, excluded bookends, stale evidence, catalog completeness and independent-review drift.

## Local checks

| Check | Result | Scope |
| --- | --- | --- |
| Full tools suite | 1,099 passed, 2 skipped, 0 failed; exit 0 | Repeated after rebase, including the final review guard |
| Full API pytest | 5,460 passed, 426 skipped; exit 0 | Before rebase; database/service integration needs CI |
| Full web Vitest | 3,740 passed in 340 files; exit 0 | Before rebase |
| API affected regression suites | 105 passed, 3 database skips; exit 0 | Final rebase onto eda3b60f, including 21 upstream character-look cases; urllib3 2.8.0 |
| UI affected regression suites | 30 passed; exit 0 | Repeated after rebase |
| API ruff, mypy app, mypy tests | Exit 0 | Full checks before rebase; affected ruff and four-file mypy repeated after the final rebase |
| Web lint, i18n, typecheck | Exit 0 | Full checks before rebase; i18n and full typecheck repeated afterward |

The skipped integration tests require the CI database/service environment. CI results belong to the pushed PR head and must be checked separately; local passes do not establish CI, browser, owner or production acceptance.

## Delivery boundary

These changes revise production plans and reject insufficient actual body/final durations when QA runs. A ten-minute chapter budget remains an estimate. Full manuscripts, new facts, narration, imagery, actual cuts and listening approval still follow the existing production gates.

PR #1098 stays draft with `no-auto-merge`. The separately submitted `claude/video-min-8-minutes` branch also edits duration API/UI/QA paths; its integration must preserve the ten-minute catalog targets and the actual-body floor before either implementation is merged together. This revision does not change another owner's branch or task.
