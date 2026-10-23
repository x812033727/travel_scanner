---
id: 2026-10-07-preschool-english-five-pilots
title: Produce five preschool English pilot lessons with embedded English and four language tracks
status: done
priority: P2
area: docs
owner: codex-preschool-pilot
claimed_at: 2026-10-07T16:00:21Z
created_at: 2026-10-07T15:59:54Z
completed_at: 2026-10-07T19:09:25Z
branch: work
depends_on: []
scope:
  - docs/videos/english-preschool-pilot
  - tools/video/preschool
---

# Produce five preschool English pilot lessons with embedded English and four language tracks

## Why

The owner requested the first five preschool English videos from the agreed preschool-to-university course. Each pilot should be about three minutes, embed English into the picture, preserve shared English demonstrations, and offer English plus zh-TW/zh-CN/ja/ko teaching audio with only the latter four CC languages.

## Definition of done

- [x] Five playable preschool MP4s with measured 3–5 minute durations, five audio tracks, four CC tracks, and no English CC.
- [x] An offline preview player independently selects teaching audio and CC; a downloadable package includes all media.
- [x] Source, localization, timing and verification records are retained without checking media into the public repository.

## Steps

- [x] Inspect existing video tools and credentials; confirm the existing long-form route does not meet this brief.
- [x] Write five lessons, 50 scenes and four-language localization, including 12 listening tasks with six-second response intervals.
- [x] Build the original Sunny/Pip visuals and short-course preview pipeline without changing global long-form rules.
- [x] Synthesize all tracks, render each MP4, and validate the measured media.
- [x] Check media decoding and player control logic; package deliverables. A real browser playback check was interrupted at the permission request, so browser playback is not claimed as tested.

## How to verify

Run Python compilation for tools/video/preschool/*.py and npm run check:tasks. Build audio.py against the merged lesson source, then build.py against its measured lessons.resolved.json. Each episode's checks.json verifies ffprobe dimensions, duration, five audio streams and four non-English subtitle streams. Inspect actual scene frames, and use Playwright against the local index.html to test playback, seeking and language selection.

## Notes

- Media workspace: /workspace/preschool-pilot-output (outside git). The authored data and reproducible tools are in the scopes above.
- The managed environment is not paired to the production video speech service and has no configured outbound credentials. The delivered trial uses Microsoft Edge read-aloud voices, explicitly labeled as preview voices. It does not claim to use the backend's configured Gemini/Azure voice.
- Backend integration is not performed: the current long-form CLI has an eight-minute floor, forces original-language CC, and does not preserve shared English demonstrations across translated dubs. The trial uses a separate explicit preschool profile, not drama/smoke overrides. No backend settings or publication state are changed.
- English demonstrations are content-addressed and reused in every teaching language. Scene timing uses actual decoded PCM lengths. Quiz translations appear only at reveal; response intervals remain clear. The English teacher instruction is also embedded in the picture before the target phrase.
- Completed media durations: 180, 180, 180, 184.733333 and 180 seconds. All five MP4s fully decode with ffmpeg without errors; each has one 720p video, five AAC tracks and four non-English CC tracks. All 40 SRT/VTT files follow measured timing, and all 12 quiz response intervals are six seconds with no answer translation.
- Voice synthesis: 251 cached clips, five complete episodes, no skipped languages. Visual review corrected cookies/trays, triangular counting layout, fallen blocks, and stand/sit transitions before final rendering.
- The offline player's nine control checks pass with jsdom and mocked media decoding. Real Chromium playback remains untested because its network permission request was interrupted; no permission bypass or repeat escalation was used.
- Delivery: /workspace/preschool-pilot-output/Sunny_Pip_5_Episodes.zip (44.3 MiB, 79 entries, zip integrity checked), plus five clearly named standalone MP4s. Backend production adoption is recorded in 2026-10-07-preschool-video-backend-profile.
