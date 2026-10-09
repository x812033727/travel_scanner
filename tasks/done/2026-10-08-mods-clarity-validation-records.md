---
id: 2026-10-08-mods-clarity-validation-records
title: Repair Mods clarity draft validation records
status: done
priority: P1
area: docs
owner: codex-mods-validation
claimed_at: 2026-10-08T16:51:27Z
created_at: 2026-10-08T16:51:24Z
completed_at: 2026-10-08T17:13:26Z
branch: codex/mods-clarity-20261009
depends_on: []
scope:
  - docs/videos/claude-code-mods-no-sandbox-before-install/revision-review.md
  - tasks/done/2026-10-08-mods-tutorial-clarity.md
  - tasks/open/2026-10-08-mods-tutorial-revision-production.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Repair Mods clarity draft validation records

## Why

PR #1390 CI found host-specific paths in new documentation and stale duration-review bindings for the changed teaching prompts and automated-route reference. These are omissions in the source handoff, separate from the two Windows runtime failures.

## Definition of done

- [x] Repository documentation uses portable path placeholders without weakening the hygiene guard.
- [x] An independent reviewer verifies and binds both changed duration-covered files.
- [x] Relevant local checks pass.
- [x] Linux CI for the repaired source head is successful and recorded.

## Steps

- [x] Read failed CI logs and reproduce the two recorded causes.
- [x] Replace five host-specific path references with `<home>`.
- [x] Obtain independent incremental duration review for both changed bindings.
- [x] Verify local hygiene, prompts, receipt tests and all long-form plans.
- [x] Record Linux CI results for the pushed source head before closing this task.

## How to verify

Run `node --test tools/repo-hygiene.test.mjs tools/video/long-form/review.test.mjs`, `node tools/video/long-form/cli.mjs check`, and `npm run check:tasks`. Check the new PR head's CI runs after pushing.

## Notes

CI at 6895b1f5b reported only the hygiene guard and stale duration bindings in web-checks. The shared review files also receive an independent one-file Windows-test increment in a separate managed worktree; the same reviewer will handle these sequentially against each branch's verified baseline. No other PR branch is modified. Keep both increments if they later meet on main. No production deployment or media publication is part of this task.

Local verification completed on Windows ARM64 with bundled Node v24.19.0:

- Portable-path repair: `aabb920dbf11c230a4736c5c3d53bf32ea634ca7`; repository hygiene tests passed 3/3 without changing the guard.
- Independent duration receipt: `81184d531f970bd394a39f2bde39df4dd37a2d87`; the reviewer verified all 108 baseline bindings against `c6454463d0eb53e4c8166be0b93a587598c03208`, rebound only the automated-route reference and prompts, and preserved the other 106 bindings and prior increments.
- `tools/video/automation/prompts.test.mjs`: 23/23 passed.
- `tools/video/long-form/review.test.mjs`: 2/2 passed.
- `tools/video/long-form/cli.mjs check`: PASS for all 473 plans, preserving 600/780-second targets, 480-second measured floors, source hashes and covered status.

Linux CI was independently read back on source head `1bc0a95bcc873ef71dd9dbd002aafa339939c9d1`:

- [video-tests job 113436598386](https://github.com/x812033727/travel_scanner/actions/runs/37813649077/job/113436598386): completed successfully on `ubuntu-latest`. Documentation-video tests passed 199/199 with no skips; the media-enabled tools run passed 2,195, skipped 1, failed 0 (2,196 total).
- [web-checks job 113436598378](https://github.com/x812033727/travel_scanner/actions/runs/37813649077/job/113436598378): completed successfully on `ubuntu-latest`. Tools tests passed 2,175, skipped 12, failed 0 (2,187 total); 1,684 task files validated. This job does not install the media dependencies exercised by video-tests.
- Complete logs and a source-bound receipt are preserved outside Git at `<home>/mokaair-work/mods-clarity-20261009/ci/validation-1bc0a95bc-0U4OeQ/`. SHA-256: video-tests log `732c400cd661210e8df905fc30d81a9183569401a651502e139be5cf9c6725f7`; web-checks log `a8b262fec6a9c1ec68587aefda888846e9c2bdb40fc91f8ea28209b1e4e05ab1`.

The scoped hygiene and duration-binding repair is verified locally and in these Linux jobs. The task-only closure commit is newer than the tested source SHA and its CI is pending; this record does not claim that all PR checks or that newer commit are green. PR #1390 remains a draft. The independent Windows runtime fixes belong to their separate branch and task.
