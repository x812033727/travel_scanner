---
id: 2026-10-12-complete-curio-l08-and-h01-language
title: Complete Curio L08 and H01 language upload
status: done
priority: P2
area: docs
owner: codex-gpt6-l08-h01-upload
claimed_at: 2026-10-12T08:29:59Z
created_at: 2026-10-12T08:27:44Z
completed_at: 2026-10-12T13:02:19Z
branch: codex/curio-l08-h01-language-upload-20261012
depends_on: []
scope:
  - docs/videos/curio-l08/i18n
  - docs/videos/curio-l08/video.json
  - docs/videos/curio-h01/i18n
  - docs/videos/curio-h01/video.json
  - docs/videos/curio-l08-h01-language-upload.md
---

# Complete Curio L08 and H01 language upload

## Why

The owner requested English, Japanese and Korean metadata, CC and dubbed audio for the existing crop-circle (L08) and Mary Celeste (H01) episodes after H03 delivery. Continue from the bb7a production handoff and existing reviewed translations/media rather than restarting production.

## Definition of done

- [x] Both episodes use their current approved cut; all selected foreign tracks pass native fit and configured checks except the exact H01 JA mtua clip explicitly heard and accepted by the owner. Preserve its original 117/118 + 1 flag with the separate hash-bound acceptance.
- [x] Source-bound captions, metadata, language manifests and backend attachments pass exact consumer verification.
- [x] Both episodes are uploaded as new private videos under the owner's authorization, with all six language tracks, CC and metadata directly verified.
- [x] Delivery evidence distinguishes local checks, backend approvals, Studio status and playback/listening limits; draft PR and task handoff are complete.

## Steps

- [x] Inventory existing source, reviews, media, uncertainty journals and producer ownership.
- [x] Create and claim an isolated worktree at current origin/main; preserve bb7a uncommitted files.
- [x] Adopt the already-approved H01 native 081b final through guarded activation, preserving current translations and original media.
- [x] Complete L08 JA second transcription and resolve only remaining current audio flags.
- [x] Finish H01 JA under the exact recorded owner acceptance and preserve L08 KO full pass, then regenerate captions/package and verify backend approval pins.
- [x] Check existing video identities and obtain explicit owner direction for first private uploads when no matching videos exist.
- [x] Upload the completed episodes and selected components as private videos, then verify all Published rows and exact texts.
- [x] Save delivery record, open draft PR and close this task.

## How to verify

Use official video CLI stages, full current audio/source/clip bindings, strict decode and native fit replay, caption/source coverage and exact packaged SRT checks. Read back approved attachments with the native consumer. Studio must directly show Published; saved exact cue/title/description captures and screenshots establish online text delivery. Never treat a status or automated check as human listening.

## Notes

- Completed 2026-10-12: L08 `mLxCEB_wSLk` and H01 `efSy-Jxq-s8` are private. All six foreign audio tracks, six foreign CC tracks and six metadata sets show Published. Backend private sync completed for both. Native approved-package consumers each pass 59 checks, re-hash every attachment, and confirm exact bound IDs in read-only transactions that were rolled back.
- H01 JA remains native 117/118 plus one exact owner-accepted `mtua` clip. After Studio rejected WAV, fresh owner authority allowed deleting only that failed track and uploading a verified MP3 transcode. No new synthesis; backend WAV and original flags/acceptance remain intact.
- Official downloads contain 1,051 exact cues across eight CC tracks. YouTube adds one terminal LF; the original strict byte-check failures remain alongside the exact-content diagnosis. All four metadata pairs per video were read back; H01 then completed sync using the same approved package.
- Native lint: zero errors. Docs-video tests: 199/199 passed. Full player playback and full-video human listening were not performed. No public release, merge or deployment is authorized.
- Final evidence index: `<home>/mokaair-work/video-language-l08-h01/L08-H01-DELIVERY-FINAL.json`, SHA256 `f8a04848cdc468a2d71e48186927beb6b257caa82a8e8f56b83d8107f06abb5d`. Full history remains in that audit directory, including `task-before-final-close.md`. [Delivery record](../../docs/videos/curio-l08-h01-language-upload.md).
- Collision refresh before PR: current origin/main `a933427269e55365c3f3eed4769ca70ce9a8e692`; local branches, remote heads and open PRs show no competing L08/H01 delivery. Existing bb7a/3a3c and all other worktrees were preserved.
