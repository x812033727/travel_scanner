---
id: 2026-10-25-keep-whisper-second-opinion-decoding-compatible
title: Keep Whisper second-opinion decoding compatible with PyAV
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-25T11:59:14Z
completed_at:
branch:
depends_on: []
scope:
  - ops/video/Dockerfile
  - tools/video/tts/whisper_second_opinion.py
  - tools/video/tts/second-opinion.test.mjs
---

# Keep Whisper second-opinion decoding compatible with PyAV

## Why

An eight-language video run installed faster-whisper 1.2.1 with PyAV 19.0.2.
The model loads, but the first real clip fails because decode_audio passes
metadata_errors to av.open, and this PyAV version no longer accepts that keyword.
Native check-audio correctly retained all flags instead of treating the failed
secondary transcription as evidence. A private task venv pinned to PyAV 16.1.0
decoded the same clip successfully; the shared worker runtime is unchanged.

## Definition of done

- [ ] The worker's second-opinion runtime can decode a real WAV and transcribe it with its configured model.
- [ ] Dependency compatibility is maintained by an appropriate constraint or decoder update, with a meaningful check.

## Steps

- [ ] Reproduce metadata_errors TypeError using faster-whisper 1.2.1 and PyAV 19.0.2.
- [ ] Choose a compatible dependency range or safe upstream decoder update; preserve script-blind transcription.
- [ ] Validate an actual clip and the existing second-opinion integration tests.

## How to verify

In the worker image, run tools/video/tts/whisper_second_opinion.py with a real
locale and WAV, then check-audio with its configured second-opinion command.
Loading WhisperModel alone is insufficient: decoding happens in transcribe.

## Notes

- Observed 2026-10-25 during openai-dns-containment eight-language production.
- Actual exception: TypeError: open() got an unexpected keyword argument 'metadata_errors', faster_whisper/audio.py:46.
- Private workaround only: faster-whisper 1.2.1, av 16.1.0, CPU int8 medium. The same uncu.wav returned a real Vietnamese transcript after pinning.
- No shared Dockerfile, transcriber or verification thresholds were changed by the video task.
