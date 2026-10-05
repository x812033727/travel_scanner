---
id: 2026-10-05-video-consumer-selected-image-hashes
title: Verify selected image bytes before direct clips and assembly
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-05T12:57:36Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
---

# Verify selected image bytes before direct clips and assembly

## Why

Working keyframe filenames are reused by later takes/providers. Historical cache
entries fail closed on a changed image SHA, and the media store retains the
original object by slug/SHA. However, the direct clips and assembly commands can
consume a selected working file without comparing its actual bytes to the
approved manifest. A manifest-only approval can therefore appear current after
the selected JPG/PNG has changed. The automatic flow and review upload/download
paths have additional byte checks; this is a separate direct-command gap.

## Definition of done

- [ ] Direct clips rejects a changed selected start or required end image before
      status/upload/paid submission, preserving all existing receipts and media.
- [ ] Direct assembly rejects the changed selected image before ffmpeg or reuse
      of a segment cached under the unchanged manifest hash.
- [ ] Unchanged approved images and clip-cut reuse keep their current behavior;
      no provider settings, owner decisions, original objects or cache entries
      are rewritten to make a mismatch pass.

## Steps

- [ ] Check current scopes/PRs and claim before editing the four consumer paths.
- [ ] Add the missing actual-byte gate at both direct consumer boundaries.
- [ ] Exercise source-bound failure and valid-input cases with no real model calls.

## How to verify

Use an approved, unchanged manifest and approval record, then change only the
selected start/end file bytes. Assert direct clips makes zero status, upload and
submit calls. Seed an old assembled segment cache under the same manifest and
assert assembly neither invokes ffmpeg nor reuses it. Keep a valid-byte control
and the existing clip-cut tests. Run focused clips/assembly tests, task checks,
and the required tools checks before a PR.

## Notes

- Filed from read-only diagnosis on 2026-10-05. Sources at reviewed fd85dfc54 and
  deployed d7ae39a2b are identical for all cited consumer/guard files.
- Argon's 49 original Gemini objects were verified present, stable and matching
  their original ready-job SHA in the actual media store. Fifteen current target
  paths now match new MiniMax jobs; thirty-three differ from older entries because
  of prior Gemini versions. This does not establish original asset loss or an
  incorrectly adopted storyboard in the automatic flow.
- Private diagnosis: C:/Users/x8120/mokaair-work/diagnostics/news-video-20261005/pr1275-direct-picture-consumer-gap-readonly.md.
- Existing automatic/review/download guards passed five targeted offline checks.
  No direct-consumer fix, production restore, paid generation or deployment is
  included in this task filing. Claim remains open for a separate bounded fix.
