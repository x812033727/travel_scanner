---
id: 2026-10-11-restore-tidy-capped-list-retention-guard
title: Keep video media when the capped site list omits its current metadata
status: done
priority: P2
area: tools
owner: codex-tidy-capped-list-guard
claimed_at: 2026-10-11T15:21:18Z
created_at: 2026-10-11T14:18:55Z
completed_at: 2026-10-11T15:55:14Z
branch: codex/tidy-capped-list-retention-20261011
depends_on: []
scope:
  - tasks/open/2026-10-11-restore-tidy-capped-list-retention-guard.md
  - tasks/done/2026-10-11-restore-tidy-capped-list-retention-guard.md
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
---

# Keep video media when the capped site list omits its current metadata

## Why

The site returns only its newest 200 videos. Tidy currently falls back to local upload approvals when a finished video is missing from that list. An old local date cannot prove that the current language gates, dub requests or scheduled publication no longer need its source media.

## Definition of done

- [x] A done video omitted from a successfully read site list is held without changing any media or record bytes, including dry-run.
- [x] An unread site list remains held; current listed videos still respect publication dates, pending review, language work, dub requests, localization and compilation retention.
- [x] Empty and capped-200 regression fixtures fail against the old code and pass after the guard; positive current-metadata cases still work.
- [x] Focused tests, docs-video and task checks pass; run the tools suite and disclose any independently reproduced baseline failure tracked by an existing task, then provide a local commit for integration into draft PR #1450.

## Steps

- [x] Check fresh main, active claims, local/remote branches and open PRs: no active implementation overlaps tidy.mjs.
- [x] Add only the missing-entry guard on current main.
- [x] Add byte-preserving offline regression and positive retention-date cases.
- [x] Run checks and repeat collision checks before delivering the local commit.

## How to verify

Use only temporary fixtures in tools/video/automation/tidy.test.mjs. Run node --test tools/video/automation/tidy.test.mjs, npm run test:tools, npm run test:docs-videos and npm run check:tasks. No production tidy, media deletion, provider, deployment or paid action is authorized by this source fix.

## Notes

- Same restored ID from PR #1450 at 3cd660d42776d8e588e3198c57d1b35b8bbe3132; created_at is unchanged. The original metadata-only scope is now expanded in this isolated implementation branch after the collision check.
- Tests ran from base main 657d34790d1446d4f4b2784b4cf5261a22f2c5f6. Before local delivery this isolated branch rebased to 6b5370b6fd661a8733392b79c2458bea9c70a7fb; no tools/ or shared-skill file changed between those main commits.
- Historical source refs: codex/pr921-tidy-metadata-current@a89cfa65ef518198b4b6f641148519431df4f6ae and codex/pr921-tidy-metadata-guard@1c3c08a80ca3e7ba7015d2d0da9510c4adbf913e. The original pr-merge-watch dirty checkout is untouched.
- Preserve current four-language, dub-retry, pending-review and compilation rules; do not transplant the old branch wholesale.
- Root owns final review and merge. The user's final direction is to consolidate the fix into existing draft PR #1450; do not create a new PR or push this implementation branch.
- Root's 2026-10-11 line-by-line review of tidy.mjs and tidy.test.mjs: PASS. The patch keeps missing site rows fail-closed and applies the current site publication date after a row reappears; the scope remains narrow.

- Regression proof: before-guard.log exit 1, all 5 new cases failed on the original implementation. After the guard, tidy.test.mjs exit 0: 40 passed, 1 existing Windows file-symlink skip. The fixture checks retain all media, records, approvals and auto.json bytes.
- Runtime: bundled Node 24.19.0; this worktree npm ci exit 0 (547 packages). tidy.mjs and tidy.test.mjs are outside long-form REVIEW_FILES; no duration-rule files changed.
- Related checks: docs-video tests pass 199/199; the duration validator passes all 473 plans; check:tasks validates all 1848 tasks with only existing stale-claim warnings.
- The Windows tools-suite reference-analysis comparison failure is already tracked by 2026-10-07-windows-reference-comparison-ffmpeg and 2026-10-06-reference-analysis-compare-range-4-6. The unchanged reference-analysis test fails again alone on synthetic seconds 4-6 with ffmpeg N-125875-g5d4d3bdc61-20260731, wrapped_avframe Invalid argument, exit 4294967274 and no output packets. This guard changes no file the comparison imports, and no duplicate task or out-of-scope FFmpeg fix is needed.
- The attempted tools suite also reproduces existing Windows baselines in 2026-10-07-windows-video-test-imports, 2026-10-07-make-project-lease-test-children-use and 2026-10-09-windows-video-test-path-assertions. After more than 185 seconds without progress at the automation test's c: ESM error, root authorized stopping only the verified self-owned hanging child; fresh parent, start-time, command and actual CWD checks matched this isolated checkout, and the remaining suite continued. No complete-suite PASS is claimed.
- An independently rerun outline-lost assertion confirms the known Windows separator mismatch. A suite-only en-to-ko dub-alias failure passes in its isolated rerun; do not infer a production defect or create a duplicate task without its final assertion evidence.
- Final tools-runner result: exit 1, 2246 tests, 2224 passed, 9 failed and 13 skipped. Its nine failure entries are the FFmpeg comparison, the stopped automation test file, two project-lease child imports, three path assertions (stock, outline-lost and brightness), and two EPERM speech-journal renames (dub aliases and Shorts lab). The latter are covered by existing 2026-10-09-windows-speech-journal-rename-failures; their stacks reach the same unchanged atomicWrite/durableWrite/sendOnce paths. The tools suite is not green, and the hung automation file was not completed.
- Repeated pre-delivery collision check: only this implementation task owns tidy.mjs, and no open PR touches tidy.mjs or tidy.test.mjs. Root has reviewed the complete source/test patch; all remaining baseline issues already have open task files, so no duplicate follow-up is added.
