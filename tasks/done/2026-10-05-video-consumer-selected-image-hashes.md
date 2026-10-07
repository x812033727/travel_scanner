---
id: 2026-10-05-video-consumer-selected-image-hashes
title: Verify selected image bytes before direct clips and assembly
status: done
priority: P1
area: tools
owner: claude-opus-5-5-image-bytes
claimed_at: 2026-10-07T02:32:18Z
created_at: 2026-10-05T12:57:36Z
completed_at: 2026-10-07T02:38:03Z
branch: claude/happy-carson-c1hy91
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

- [x] Direct clips rejects a changed selected start or required end image before
      status/upload/paid submission, preserving all existing receipts and media.
- [x] Direct assembly rejects the changed selected image before ffmpeg or reuse
      of a segment cached under the unchanged manifest hash.
- [x] Unchanged approved images and clip-cut reuse keep their current behavior;
      no provider settings, owner decisions, original objects or cache entries
      are rewritten to make a mismatch pass.

## Steps

- [x] Check current scopes/PRs and claim before editing the four consumer paths.
- [x] Add the missing actual-byte gate at both direct consumer boundaries.
- [x] Exercise source-bound failure and valid-input cases with no real model calls.

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
- Private diagnosis (kept off the repository, in the owner's local diagnostics folder): news-video-20261005/pr1275-direct-picture-consumer-gap-readonly.md.
- Existing automatic/review/download guards passed five targeted offline checks.
  No direct-consumer fix, production restore, paid generation or deployment is
  included in this task filing. Claim remains open for a separate bounded fix.

## 2026-10-07 implementation (claude-opus-5-5-image-bytes)

- `clips` (media/clips.mjs, `changedKeyframes`): after the storyboard approval check and before the
  dry run, the status call, any upload or submission, every selected clip shot's and still's start
  picture and required end picture is hashed and compared with the sha256 its keyframes manifest
  entry names. A missing file or other bytes is a `MediaError` for the owner (exit 3) naming the
  shot, which picture and the file. Kept clips of selected shots are checked too (fail closed): an
  approved storyboard whose picture changed is a mismatch whatever the clip.
- `assemble` (assemble/cli.mjs): after the layout and before any ffprobe/ffmpeg, every motion
  scene whose keyframe carries a sha256 (a still shot, from the keyframes or clips manifest) is
  hashed; a mismatch exits 2 (usage) before a segment is encoded or a cached one, keyed on the
  manifest's unchanged hash, is reused. Cards (sha256 null) and clips are not affected.
- Nothing is rewritten to make a mismatch pass: the manifests, the cached segment and the clips
  manifest are left as they were (asserted).
- Tests: `clips.test.mjs` changes the selected start and the end picture, run and dry run, and
  counts zero requests of any kind; `assemble.test.mjs` changes a still's keyframe with a seeded
  segment cache and asserts no tool call, the cache untouched and no build, plus the unchanged
  control reaching the tools. Both fail with the gate removed (checked).
- Verified: `node --test tools/video/media/clips.test.mjs tools/video/assemble/assemble.test.mjs`;
  `npm run test:tools` green but for the duration receipt, rebound by an independent reviewer in
  the next commit (assemble/cli.mjs, assemble.test.mjs and clips.test.mjs are bound).
