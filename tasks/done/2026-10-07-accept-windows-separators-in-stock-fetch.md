---
id: 2026-10-07-accept-windows-separators-in-stock-fetch
title: Accept Windows separators in stock fetch output regression
status: done
priority: P3
area: tools
owner: codex-windows-video-validation
claimed_at: 2026-10-08T17:10:17Z
created_at: 2026-10-07T04:08:54Z
completed_at: 2026-10-08T17:26:32Z
branch: codex/windows-video-validation-20261009
depends_on: []
scope:
  - tools/video/media/media.test.mjs
---

# Accept Windows separators in stock fetch output regression

## Why

The stock-fetch regression at media.test.mjs:483 expects the diagnostic source
path to contain forward slashes. On Windows the actual successful output uses
the native separator in `docs\\videos\\fixture-minimal\\video.json`; the
picture and credit were stored correctly, but the assertion fails.

## Definition of done

- [x] The regression verifies the same source asset/credit on Windows and Linux
      while accepting the platform's diagnostic path separator.

## Steps

- [x] Narrow the assertion to preserve the asset-count/credit behavior check.
- [x] Run the focused case on Windows and Linux.

## How to verify

`node --test --test-name-pattern="stock fetch stores the photo"
tools/video/media/media.test.mjs`.

## Notes

Observed in the 2026-10-07 complete Windows tools run, actual exit 1. Raw evidence
is retained outside Git in
`<home>/mokaair-work/handoff/renewed-finals-20261007/native-unit-full-tools-check-20261007.log`.
No provider or production operations are needed for this mocked regression.

### 2026-10-09 Windows repair and validation

- Adopted this existing task for the stock assertion only. The CLI's source path is now checked as an exact output line built with `path.join("docs", "videos", "fixture-minimal", "video.json")`; the picture hash, stored bytes, credit, asset count and repeat-download assertions are unchanged. No production code changed.
- The earlier complete Windows run reproduced the forward-slash mismatch at `media.test.mjs:540`; evidence is in `<home>/mokaair-work/windows-video-validation-20261009/remaining-tools-failures-observed.txt`.
- Bundled Node v24.19.0 ran the complete `media/media.test.mjs`, `review/sync.test.mjs` and `shorts/from-drama.test.mjs` files with `--test-concurrency=3`: actual exit 0, 131 passed, 0 failed, 0 skipped, duration 140141 ms. Full log: `<home>/mokaair-work/windows-video-validation-20261009/path-assertions-after.log`.
- `git diff --check` passed for the three changed test files. Linux verification remains for CI; no local Linux pass is claimed.
### Cross-platform closeout

PR #1391 at `ea02610af9742b3893261564ab7433cf7ae67648` passed Ubuntu video-tests and web-checks. The media-equipped tools job completed 2,202 tests: 2,201 passed, zero failed/cancelled, one existing API-runtime skip; docs-video passed 199/199. Web-checks completed 2,178 passes with 13 environment skips and no failures. This validates the same committed test changes as the Windows focused runs above. The independent sync-test duration increment is `3acd739f4`; all 473 plans and both receipt tests pass. Remaining intermittent journal rename contention is handled separately and does not change this fixture/assertion fix. This implementation closure does not authorize merge or deployment.
