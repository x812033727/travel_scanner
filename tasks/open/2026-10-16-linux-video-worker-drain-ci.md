---
id: 2026-10-16-linux-video-worker-drain-ci
title: Run video worker drain behavior tests on Linux CI
status: in-progress
priority: P1
area: ops
owner: codex-video-worker-warm-drain
claimed_at: 2026-10-16T09:19:00Z
created_at: 2026-10-16T09:18:50Z
completed_at:
branch: codex/video-worker-warm-drain-20261016
depends_on: []
scope:
  - .github/workflows/ci.yml
---

# Run video worker drain behavior tests on Linux CI

## Why

The worker drain helper and shell use Linux process and signal semantics. On
Windows, `unittest` skips their behavior cases, and this checkout's WSL
`CreateVm` times out. A skipped local run is not evidence that the drain works.

## Definition of done

- [x] The Ubuntu video-tests job checks both shell scripts' syntax and runs
      the process/fake-Docker behavior tests without a skip.
- [ ] The first stacked PR run reports the Linux test result; a green check
      still does not replace an isolated Docker init smoke test.

## Steps

- [x] Add the focused test step to the existing video-tests job.
- [ ] Read back the named CI step and its test count after pushing the PR.

## How to verify

On Ubuntu: `bash -n ops/release/video_worker_drain.sh && sh -n
ops/video/worker.sh && python3 -m unittest discover -s ops/release -p
test_video_worker_drain.py -v`. Check the named CI step on the PR.

## Notes

The local Windows run skips all seven Linux-only tests; WSL `CreateVm` timed out.
No Docker/tini smoke has been performed. This ticket concerns CI wiring only,
not approval to install the helper or touch the production host.
