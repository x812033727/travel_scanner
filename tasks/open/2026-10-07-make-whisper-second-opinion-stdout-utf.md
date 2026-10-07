---
id: 2026-10-07-make-whisper-second-opinion-stdout-utf
title: Make Whisper second-opinion stdout UTF-8 on Windows
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T05:28:38Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/whisper_second_opinion.py
---

# Make Whisper second-opinion stdout UTF-8 on Windows

## Why

The native Whisper Python script prints Unicode transcripts to a Node pipe using
the Windows default stdout encoding. During the LLM selected-language check, a
complete Japanese transcript raised UnicodeEncodeError at the final print under
cp1252/charmap. Native check-audio surfaces only the first line of the child error,
so all 33 doubts remained flagged and the traceback was hidden.

An offline single-clip reproduction used the existing small model, same raw clip
and hints: default encoding exited 1 in 22.68 seconds; PYTHONIOENCODING=utf-8 and
PYTHONUTF8=1 exited 0 in 21.07 seconds with a complete Japanese transcript and empty
stderr. No provider request was made. The exact diagnostics are under
`C:\Users\x8120\mokaair-work\llm-language-completion-20261007\evidence\whisper-diagnostics`.

## Definition of done

- [ ] Native second-opinion stdout carries complete Japanese, Korean and Chinese
  transcripts as UTF-8 on Windows without requiring undocumented shell variables.
- [ ] A focused offline encoding check covers an initially non-UTF-8 stdout,
  without loading/downloading a model or calling a provider.

## Steps

- [ ] Check current ownership before touching the shared Python script.
- [ ] Set an explicit UTF-8 output contract while preserving the native clip-name
  and transcript protocol, then verify the encoding regression.

## How to verify

Reproduce with a non-UTF-8 stdout and a stubbed transcriber containing Japanese and
Korean characters. Verify raw stdout is UTF-8 and native parsing retains both
transcript lines. Existing native second-opinion Node tests should still pass.

## Notes

This is a deferred native-tool fix. The active video operation uses explicit UTF-8
environment variables and a private wrapper that archives actual stderr/progress
and exit status. The wrapper does not alter source scripts, scores, flags or audio
approval. The stdout encoding failure is distinct from Windows journal promotion
EPERM, tracked in `2026-10-07-preserve-full-speech-answers-when-windows`.
