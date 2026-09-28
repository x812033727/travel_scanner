---
id: 2026-09-28-pr925-shorts-validation-caption-guards
title: PR925: preserve Shorts reports and selected caption tracks
status: done
priority: P1
area: tools
owner: codex-pr-merge-watch-shorts
claimed_at: 2026-09-28T13:13:11Z
created_at: 2026-09-28T13:04:18Z
completed_at: 2026-09-28T13:18:35Z
branch: codex/pr925-shorts-validation
depends_on: []
scope:
  - tools/video/shorts/cli.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/core.test.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/package.mjs
  - tools/video/shorts/push.mjs
  - tools/video/shorts/pipeline.test.mjs
---

# PR925: preserve Shorts reports and selected caption tracks

## Why

PR #925 restores the Shorts tool on current main but does not contain the locally saved
validation/report fix from the superseded #906 review. Malformed scene/evidence input throws
instead of reporting validation errors, and an interrupted report write can truncate the last
complete report. Separately, translated captions can pass QA with arbitrary timestamps and
selected translated caption files disappear between local QA and the server upload package.

## Definition of done

- [x] Both script versions return findings for malformed scene/evidence collections and rows.
- [x] A failed report update preserves the preceding complete JSON through shared atomicWrite.
- [x] Translated text is allowed while its timestamps must match the current timeline.
- [x] Selected caption locales are checked in the package and reach the server as caption roles.
- [x] Focused tests and task validation pass; live pilot and publication acceptance stay separate.
- [x] A settings lookup failure leaves the previous upload package unchanged and returns failure.
- [x] Caption bytes are bound into metadata and changed bytes cannot reuse a prior approved review.

## Steps

- [x] Inspect exact PR head, main, active local worktrees, remote branches, task ownership and PRs.
- [x] Reproduce the defects using immutable source in ignored scratch; validate a six-file proposal.
- [x] Apply only the six source/test files and this new task; preserve unrelated tasks and branches.
- [x] Run focused checks, close this own task, and stop at a tested local commit for root review.

## How to verify

```sh
node --test --test-reporter=tap --test-concurrency=1 tools/video/shorts/core.test.mjs tools/video/shorts/pipeline.test.mjs
node tools/tasks.mjs check
git diff --check
```

## Notes

- Authorized scope: user asked to fix all PR conflicts/CI failures and preserve automatic merge;
  coordinator assigned this narrow repository correctness repair after independent review.
- Reviewed PR #925 head: `725d2d5acc2d6f6ddb56b13985e26f4dc4253f01`; author remote unchanged at
  handoff, no active local author worktree on its replacement branch. T1 author's task is done.
- Reused the idle managed `pr905-schedule-guard` checkout after the #921 reviewer released it
  clean at `5c3eeadde2191789fb5ffb03d712fd19a1b121c3`; previous local branches stay preserved.
- Created `codex/pr925-shorts-validation` from the reviewed PR head and merged main
  `27755064e429605bf6e786cd66acd508c1de3645` cleanly as `a577b38c323c0fc7fac8b15baf5e650b15afb724`.
  The merge brings the already-reviewed story quota and migration-chain repair, with no Shorts drift.
- The code/test portion of `aef6dcfb06949776edd57510f6486c3c7fc17079` is reused; none of the
  superseded #906 task records or previously blocked task mutations are included or retried.
- Server contract verified at exact PR head: `video_youtube/sync.py` loads `captions_*` roles,
  uses `payload.locales` to preserve locale spelling, and uploads every supplied package track.
  No API/schema/migration change is required for the caption repair.
- Private fixture evidence: 41 tests, before 29 passed / 12 failed; proposed fix 41 passed.
  All tests use local fixtures/fake clients, one Node worker; no browser/ffmpeg/service calls.
- Actual integrated checkout: 41/41 focused tests passed in 21.24 seconds. Its first run passed
  core 14/14 but could not import the pipeline because this reused checkout has no node_modules.
  A test-process-only import hook reused the watcher's installed pinyin-pro 3.29.4 after verifying
  identical package-lock hashes and the exact locked package version; no dependency install,
  node_modules mutation, product source substitution or external service was used. The hook and
  both logs are ignored under `test-results/pr925-integration/`.
- Private proof/patch: watcher `test-results/pr925-readonly-review/receipt.json` and
  `complete-code-only.patch`. Selected existing CC files are propagated; this does not generate
  translations or claim the metadata localization workflow, real voice account, pilot,
  deployment or YouTube publication was validated.
- Stop at a local tested commit for coordinator review. No push, CI rerun, automatic merge
  change, deployment, production migration or publication is authorized in this handoff.
- Reopened only this own task after independent review reproduced two further failures.
  Coordinator authorized the seventh code file `cli.mjs` for the swallowed settings failure;
  no other task records or blocked #906 mutations are part of this continuation.
- The additional settings/caption binding regressions failed 4/4 before the follow-up fix;
  all preceding 41 tests still passed. The corrected implementation passed 45/45, then the final
  run with two asynchronous upload-change cases passed 47/47 in 14.33 seconds. Settings503
  leaves metadata, description, manifest and package report unchanged; changed timestamps,
  same-clock translated text and legacy packages cannot reuse an existing approved review.
- Selected caption SHA256s are embedded in metadata, the server's approval identity. Repackaging
  changed bytes creates a different metadata SHA; preflight checks occur before any requests,
  and upload-time hashes are checked again before a publish review is submitted.
- After the first tested repair commit, fresh main `ebde813d6a7fa9cdd8282bfa2400d002c0a6add8`
  was inspected (only two guides, their assets and task/evidence records) and merged cleanly as
  `d2ba2899cd6ba908117625dc98c10fa11cb9e3d6`. It changes no tested tooling/dependency files.
