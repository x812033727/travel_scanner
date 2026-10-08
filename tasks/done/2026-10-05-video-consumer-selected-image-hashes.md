---
id: 2026-10-05-video-consumer-selected-image-hashes
title: Verify selected image bytes before direct clips and assembly
status: done
priority: P1
area: tools
owner: claude-opus-5-5-image-bytes
claimed_at: 2026-10-07T03:35:41Z
created_at: 2026-10-05T12:57:36Z
completed_at: 2026-10-07T04:08:54Z
branch: claude/sharp-bardeen-ob6fn9
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

### 2026-10-07 implementation (claude-opus-5-5-image-bytes)

- `media/clips.mjs` `changedPictures()`:
  - It runs `core/state.mjs keyframeProblems` on the shots this run uses, and also checks any end frame the manifest records, because a clip is sent with that end frame even when the script no longer asks for one.
  - Direct `clips` runs it after the storyboard approval check and before any status read, upload or submission. `clips import` runs it before money is held or the clip is copied.
  - A mismatch exits 2 and names the file. The manifest, receipts, ledger and media are left as they are.
- `assemble/cli.mjs` `mediaInputs()` checks the bytes before ffmpeg runs and before a segment cached under the manifest's hash is reused:
  - illustrated slides: every selected keyframe;
  - drama: every still shot's picture recorded in `clips/manifest.json`.
  - Clip-cut reuse and unchanged pictures behave as before.
- Tests:
  - `clips.test.mjs`: a changed start, a changed recorded end frame, and import. Each makes zero requests of any kind, leaves the manifest unchanged and holds no money.
  - `assemble.test.mjs`: illustrated and drama-still cases. A valid-byte control reaches ffmpeg; a changed picture does not, and the cached segment is left untouched.
  - Both fail on the old code.
- Code review (2026-10-07) found two blocking issues and fixed them:
  - **A still outside `--shot` could be sent unchecked.** A clip continuing from such a still went out as `previous_frame`.
    `clips.mjs` `uploadApproved()` now hashes every picture right before upload, against the record that names it: the start keyframe, the end frame, and the still that a clip continues from.
  - **Assemble checked the wrong record.** It hashed the clips manifest's still record, but `layoutDrama` uses the keyframes manifest's record first.
    Assemble now checks the record `layoutDrama` uses, and refuses when the two manifests disagree about a still.
- Should-fix: the drama test now uses a real still (`data.visual: "still"`). The cached-segment assertion that proved nothing is gone. The guarantee is that the run is refused before ffmpeg is even looked for.
- Nit: the picture-problem filter matches exact phrases, so a shot ID can no longer trigger it.
- Filed as `2026-10-07-the-thumbnail-is-drawn-from-a`: the thumbnail (`render/plan.mjs`) has the same gap.
- Not changed: a few checks are stricter than the run strictly needs, such as a kept shot's picture or an import's end frame. The reviewer called this defensible. Older manifests always carry sha256 (keyframes.mjs has written it since 5e151982, and clips.mjs for stills since d4e2b6b2), so nothing in production fails on a missing hash.
- Codex review of PR #1364 (2026-10-07, P1) found the gap that was left. A clip continuing from a still outside `--shot` read that still's record in `clips/manifest.json`, written by an earlier run. `uploadApproved()` hashed it against its own old hash. So a still that a later keyframes run had pointed at another file, with the old file left in place, could still be sent as `previous_frame`. The approval no longer covered it. Fixed in `clips.mjs`: the still's clips record must name the file and hash that the keyframes manifest selects, or the clip is refused (exit 2, "run clips --shot <still> first") before it is sent. The new test in `clips.test.mjs` fails on the old code, and it also checks that the remedy works.
