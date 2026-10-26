---
id: 2026-10-14-make-whisper-second-opinion-work-with
title: Make Whisper second opinion work with PyAV 19 on Windows
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-25T23:03:47Z
created_at: 2026-10-14T13:04:54Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/whisper_second_opinion.py
  - tools/video/tts/whisper_second_opinion.test.py
  - docs/videos/DUBS.md
---

# Make Whisper second opinion work with PyAV 19 on Windows

## Why

During H04 Japanese dub QA on Windows, the documented independent checker
`tools/video/tts/whisper_second_opinion.py` failed before transcribing a WAV.
With faster-whisper 1.2.1 and PyAV 19.0.1, faster-whisper calls
`av.open(..., metadata_errors="ignore")`, but PyAV 19 rejects that keyword:
`TypeError: open() got an unexpected keyword argument 'metadata_errors'`.
After a temporary external wrapper removed that argument, printing Japanese
text failed under the default cp1252 console encoding with
`UnicodeEncodeError`. `PYTHONIOENCODING=utf-8` allowed the checker to run.
The production worker's pinned dependencies should be checked separately;
this task is for the documented local Windows path and a version-safe fix.

## Definition of done

- [ ] The documented checker transcribes Japanese and Korean WAVs on Windows
      with a supported faster-whisper/PyAV pair, including non-ASCII stdout.
- [ ] `check-audio --second-opinion` can parse the returned clip lines and
      clear a real Gemini-only false alarm without a local wrapper.
- [ ] A regression test covers the compatibility and Unicode output path.

## Steps

- [ ] Reproduce with faster-whisper 1.2.1 / PyAV 19.0.1 and inspect compatible
      version pins or a decoder path that does not depend on the removed kwarg.
- [ ] Make the checker emit UTF-8 text on Windows regardless of console code
      page; keep the existing clip-name plus transcript output contract.
- [ ] Update the documented local setup command if a version pin is required.

## How to verify

On Windows with a Japanese and Korean test WAV, run
`python tools/video/tts/whisper_second_opinion.py ja <clip.wav>` and the `ko`
equivalent, then run `check-audio --second-opinion "<python> tools/video/tts/whisper_second_opinion.py"`
against a fully cached dub. Confirm exit 0, UTF-8 transcripts and no new
provider request just to repeat this verification.

## Notes

An external `video-whisper-compat.py` wrapper that strips
`metadata_errors` from `av.open` plus `PYTHONIOENCODING=utf-8` let the H04 JA
check complete; it is not a repository fix. The model used was cached Whisper
medium. Do not treat this as a request to re-record the voice or retry a
speech-journal entry.

## Notes (2026-10-25, claude-opus-5-5)

- Fixed together with `2026-10-10-whisper-pyav19-second-opinion`: the script no longer calls PyAV (it reads the WAV with the standard library), and it writes each line as UTF-8 bytes to `sys.stdout.buffer`, so a cp1252 console prints Japanese, Korean and Thai. The regression is a node test (`tools/video/tts/whisper-second-opinion.test.mjs`) that sets `PYTHONIOENCODING=cp1252`; the Windows run itself was not repeated here (Linux container).
