---
id: 2026-10-16-install-video-worker-drain-host-anchors
title: Integrate reviewed video worker drain into host deploy anchors
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-16T09:22:49Z
completed_at:
branch:
depends_on: []
scope:
  - ops/release/video_worker_host_patch.py
  - ops/release/test_video_worker_host_patch.py
---

# Integrate reviewed video worker drain into host deploy anchors

## Why

The shell/Node video worker is recreated by both normal and rollback `compose
up`. Its helper cannot protect any deployment until the exact host-only script
calls it at both anchors. #1527's stage installer and #1529's media installer
are still draft dependencies; their output and host bytes must be pinned
before creating a third installer.

## Definition of done

- [ ] A host-only installer pins the exact post-#1527/#1529 script and helper
      hashes, patches both compose anchors, and fails on drift.
- [ ] Normal and rollback paths precheck and warm-drain the video worker before
      recreation, retaining STOP/DEPLOY_DRAIN until exact receipt recovery.
- [ ] Offline tests prove both anchors, changed-script refusal, restore on
      partial write, and no installation during an active deploy lock.

## Steps

- [ ] Wait for independent review and resolution of the warm-drain HOLD:
      general CLI admission, raw manual exec freeze, first legacy-worker
      upgrade, isolated Docker init/PID/exit smoke.
- [ ] Read the reviewed output of `video_media_host_patch.patch_script`, pin
      its exact bytes and two `compose up --no-build -d` anchors, then build
      the narrow installer and tests in these two files.
- [ ] Obtain separately named owner approval before any host installation.

## How to verify

`python3 -m unittest discover -s ops/release -p
test_video_worker_host_patch.py -v`, byte-for-byte synthetic render, `bash -n`
on both rendered scripts, and a fresh read-only production hash comparison.

## Notes

2026-10-16 HOLD / unclaimed: #1527 and #1529 are draft stacked work, and
there is no reviewed target host script after both installers. Do not patch
`ops/release/video_stage_host_patch.py` or
`ops/release/video_media_host_patch.py` in this task; those files belong to
separate active work. The initial legacy worker cannot acknowledge a drain,
and arbitrary raw exec can enter after a point-in-time process snapshot.
No production host script or container has been changed.
