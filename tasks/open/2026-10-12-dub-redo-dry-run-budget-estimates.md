---
id: 2026-10-12-dub-redo-dry-run-budget-estimates
title: Make dub redo dry-run and budget estimates match targeted retakes
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T03:33:23Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Make dub redo dry-run and budget estimates match targeted retakes

## Why

`dub --redo <flags> --dry-run` reports no work when a flagged line's text and
cached clip are still current, even though the real command will buy that retake.
The outer monthly-budget preflight uses the same incomplete cache-only selection.
This makes the cost shown before an explicitly requested retake misleading.

Observed on H02 (`curio-h02`), Japanese line `cb08d4da`, on 2026-10-12:

- Dry run started at `03:28:08.468Z` with `--locale ja --line-by-line --format mp3
  --redo .../review/check-flags.ja.json --dry-run`. It reported `120 requests,
  0 to synthesize; about 0 billable characters now` and exited 0.
- The equivalent real run started at `03:28:32.217Z`, retook the one unchanged-text
  flagged line, and exited 0 at `03:30:04.527Z`: `1 requests synthesized
  (31 billable characters), 119 reused`.

The retake was intended and authorized; the defect is in its dry-run and
preflight estimate, not in selecting the flagged line for actual synthesis.

## Definition of done

- [ ] With all clips current and one unchanged-text line flagged by `--redo`,
      dry-run reports that pending retake and its billable characters. A mock of
      the observed 31-character case reports 1 pending request / 31 characters,
      rather than 0 / 0.
- [ ] Dry-run, outer monthly `needed`, and real retake dispatch derive the same
      requested line bodies under `--redo`, including a partial retake in a
      multi-line scene and `--line-by-line`. Current unflagged lines remain reused.
- [ ] The monthly preflight includes those retake characters and refuses an
      insufficient remaining allowance before any mocked speech POST. Sufficient
      allowance dispatches only the requested retake bodies.
- [ ] Existing no-redo cache reuse, missing/stale clips and `--force` behavior
      remain consistent with the estimate. No provider call is added to dry-run;
      its existing read-only status lookup, when configured, is unaffected.
- [ ] Regression tests run with fake speech/media dependencies and temporary
      fixture workdirs. They neither consume paid quota nor use live H02 assets.

## Steps

- [ ] Reproduce the fully cached, same-text flagged retake with a failing test
      in `tools/video/dubs/dubs.test.mjs`; capture dry-run output and real mock
      dispatch bodies/billable totals from the same fixture.
- [ ] Align the cost/pending selection used by dry-run and the outer monthly
      guard with `dubLocale`'s redo-aware `current`, `retakes` and `estimateFor`
      logic; avoid three diverging versions of that decision.
- [ ] Add the partial-scene, line-by-line, unchanged unflagged-cache and monthly
      insufficient-budget cases, then run the relevant checks.

## How to verify

```bash
node --test tools/video/dubs/dubs.test.mjs
npm run test:tools
npm run check:tasks
```

Tests must compare the planned billed line bodies/count with actual mocked
dispatch for the same flags, cache and CLI options. A test that only repeats an
estimator's arithmetic is insufficient. Do not replay this incident against the
live media workdir or provider just to verify the fix.

## Notes

- Filed only, intentionally unclaimed. No implementation, media stage, lease,
  cache or provider operation is part of filing this task.
- Confirmed current code: `dubLocale` parses `values.redo` and its `current`
  predicate rejects a request containing a flagged line. `retakes` and
  `estimateFor` use the flagged/stale subset. Outer `dryRun` is not passed
  `values`, and both its pending selection and outer `needed` only inspect cache
  keys plus clip existence; they omit the explicit redo set.
- Local evidence directory:
  `C:/Users/x8120/mokaair-work/video-language-6hswTvAftUA/`.
  `dub-2026-10-12T03-28-08-468Z.log` SHA-256:
  `38a3607435a0e8b09ccbabce94c9ec3f1ace9c556af8a9fbd33175b1ff227dbe`.
  `dub-2026-10-12T03-28-32-217Z.log` SHA-256:
  `3125d3cf6fffbef761b12e39b58fdd0521045b286742a6feb36e5ec518fcc45e`.
  The adjacent `.receipt.json` files retain exact args,
  start/end times and exit codes. These are read-only incident evidence.
- Duplicate check: searched `tasks/open/` and `tasks/done/` for dub dry-run,
  redo/billable and budget-estimate terms, and read the open tools list. The
  completed `2026-09-28-dub-skip-the-whole-scene-request` introduced optional
  line-by-line synthesis to avoid split fallbacks; it does not cover this
  redo-aware estimate mismatch. No duplicate follow-up was found.
