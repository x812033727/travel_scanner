---
id: 2026-10-22-curio-s58-r11-audio-gate
title: Curio S58 R11 audio listening and bounded retakes
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T00:25:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s58
---

# Curio S58 R11 audio listening and bounded retakes

## Current state

- R11 source and written visuals passed independent review; two blind readers each passed 13/13. The frozen creative hashes remain in `docs/videos/curio-s58/review/r11-author-freeze.md`.
- Gemini Sulafat made **146/146** original WAVs and 12:43.67 narration. The first chapter is **50.83 seconds**, and the body is **11:52.83**. See `docs/videos/curio-s58/review/r11-tts-technical.md`.
- The first and one cached repeat `check-audio` both checked **144/146**: **48 ASR/Jev flags** and **2 untranscribed** (`s58047`, `s58143`). The repeat made 0 new transcripts and 0 Jev calls. This is **HOLD**, not an audio PASS. See `docs/videos/curio-s58/review/r11-audio-first-pass-stop-20261022.md`.
- Private `/workspace/.video-work/curio-s58/STOP` is present. No art, music, video, website audio approval, or Studio link is evidenced for this episode.

## To finish

- [ ] Have a reviewer who can actually hear the WAVs use `review/r11-audio-priority-listening.json` to check the 14 semantic-risk IDs and 2 untranscribed IDs; use `r11-audio-triage-a.md` and `r11-audio-triage-b.md` for the other 34 flags. The current model cannot hear local audio.
- [ ] Retake only IDs with confirmed spoken errors, then run the full official `check-audio` against the same R11 script. If the two service-refused IDs still cannot be transcribed, record a supported listening or second-transcriber result explicitly. A transcript spelling difference alone does not warrant a retake.
- [ ] Keep website outline/script/audio card status distinct from technical checks and proceed through native art, brand intro after the 50.83-second opening, 21-second outro, final 16-second Studio targets, QA, Short and private upload link only after their own evidence.

## Verification

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s58 --json` should remain 0 errors and 0 warnings. `npm run check:tasks` validates this task's metadata; neither command hears the voice or approves the audio.
