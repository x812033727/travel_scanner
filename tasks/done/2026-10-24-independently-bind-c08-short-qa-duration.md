---
id: 2026-10-24-independently-bind-c08-short-qa-duration
title: Independently bind C08 short QA duration review
status: done
priority: P2
area: tools
owner: codex-root-c08-qa-review
claimed_at: 2026-10-24T05:52:47Z
created_at: 2026-10-24T05:52:43Z
completed_at: 2026-10-24T05:54:37Z
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Independently bind C08 short QA duration review

## Why

PR #1811 fixed the final QA CLI's duplicate eight-minute floor for the exact
owner-approved C08 short-v8. That author change makes two files in the
independent long-form duration receipt stale. Review those bytes and renew only
their SHA256 bindings before the guarded video checks can pass.

## Definition of done

- [x] The report documents the exact C08 QA policy and the ordinary sibling policy.
- [x] The 108-file receipt matches current bytes and the guarded CLI check passes.

## Steps

- [x] Inspect the two-file author diff and run real QA CLI boundary tests.
- [x] Rebind only the two changed file hashes and the report hash.
- [x] Rerun guarded review checks and finish this ticket on PR #1811.

## How to verify

Use the bundled Node runtime for `node --test tools/video/qa/duration.test.mjs
tools/video/core/duration.test.mjs tools/video/core/lint.test.mjs
tools/video/long-form/review.test.mjs`, then `node
tools/video/long-form/cli.mjs check`, `npm run check:tasks`, and `git diff
--check`.

## Notes

At author head `3a16c041963e8ea23714c805ff8c191972d1fdfc`, the two
changed QA files have SHA256 `3f88cb712d7658e0ac2659e79ea67b673f4201b50d04b330265d4b620dcd2c32`
and `0dd86e17c7048f1873d86abf4c07219eed41ca756c0e1bf30288527635ceb3d8`.
Before rebinding, the guarded CLI reports exactly these two stale paths.
Independent focused core/lint/QA run: 75/75 passed. The new QA CLI test uses
the real C08 project and an explicit eight-minute environment setting,
verifies body 7199 fails / 7200 passes, final 9000 passes / 9001 fails,
and verifies the old C08 project does not inherit the short band. Fixtures
contain silent WAVs and fake final bytes; no media acceptance is claimed.

The renewed report SHA256 is `926ee0480dc3a8ef51898fa2cf067af1000a75ebbc31fe0218287dbc2e451dc3`.
The guarded long-form CLI passes all 473 plans; the two shipped receipt tests
pass, and `git diff --check` is clean. No actual C08 narration, final cut,
supplier price, budget approval, production import or upload is claimed.
