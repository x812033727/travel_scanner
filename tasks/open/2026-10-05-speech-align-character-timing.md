---
id: 2026-10-05-speech-align-character-timing
title: Speech align: character timing from the server for Gemini voices (CPU aligner) and Azure word boundaries
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T16:08:22Z
completed_at:
branch:
depends_on:
  - 2026-10-05-speech-api-tells-a-provider-answer
  - 2026-10-05-reuse-confirmed-speech-results-across-restart
scope:
  - apps/api/app/video_speech/align.py
  - apps/api/app/video_speech/align_api.py
  - apps/api/tests/test_video_speech_align.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/main.py
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - apps/web/app/api/video/speech/align/route.ts
  - apps/web/app/api/video/speech/align/route.test.ts
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/shorts/speech.mjs
  - tools/video/shorts/karaoke.mjs
  - tools/video/shorts/karaoke.test.mjs
  - tools/video/shorts/build.mjs
  - tools/video/shorts/pipeline.test.mjs
  - docs/videos/SHORTS.md
  - .agents/skills/youtube-video/references/shorts.md
---

# Speech align: character timing from the server for Gemini voices (CPU aligner) and Azure word boundaries

## Why

Nothing in the pipeline knows when a character is spoken: the speech server returns WAV
bytes only (`apps/api/app/video_speech`), Gemini TTS has no timestamps and the Azure path is
REST without `WordBoundary`. The karaoke captions of Shorts
(`2026-10-05-shorts-karaoke-captions-estimated-timing`, PR #1292) therefore light their groups
on an estimate inside each phrase and carry a QA warning. Outside tools get this from
ElevenLabs timestamps or a GPL aligner; we want it from our own server, for our own voices.

## Definition of done

- [ ] `POST /video/speech/align` takes `{audio (base64 WAV), text, language}` and returns
      `{source: "aligned" | "azure", chars: [{text, start_ms, end_ms}], model}`; it is
      rate-limited per hour like the judge and answers with a provider answer (not a 500) when
      the aligner is unavailable.
- [ ] A phrase synthesized with an Azure voice carries word boundaries from the Speech SDK's
      `WordBoundary` events without a second call; a Gemini phrase goes through the CPU aligner.
- [ ] Measured on 20 Azure phrases: the aligner's character starts are within 60 ms (median)
      of Azure's own boundaries; the numbers are in this ticket.
- [ ] A Shorts build with a server voice writes `timing.json` with `source: "aligned"`, the
      `captions` QA warning disappears, and the `--captions` default is unchanged.

## Steps

- [ ] Pick the aligner on the API container: Qwen3-ForcedAligner-0.6B (Apache-2.0, character
      level for Chinese), FunASR Paraformer-zh (MIT) or WhisperX's zh wav2vec2 (BSD-2); load
      lazily, one worker thread, measure RSS and seconds per phrase before enabling.
- [ ] `align.py` + `align_api.py` (own router mounted beside `video_speech_router`), schemas,
      tests with a fake aligner; the web proxy route under `apps/web/app/api/video/speech/align/`.
- [ ] Azure: `WordBoundary` through the Speech SDK for standard zh-TW neural voices, returned
      beside the audio or cached by the phrase key.
- [ ] `tts/client.mjs alignClip()`; `shorts/speech.mjs` caches the alignment beside the phrase
      WAV under `.speech-server/`; `karaoke.mjs` takes `chars[]` over the estimate.
- [ ] Docs: `SHORTS.md` §工具端, `references/shorts.md` (the warning goes away).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_align.py -q
node --test tools/video/shorts/karaoke.test.mjs tools/video/shorts/pipeline.test.mjs
node tools/video/shorts/cli.mjs build --file <script> --workdir <VIDEO_WORKDIR> --speech server --captions karaoke
node tools/video/shorts/cli.mjs qa --dir <build> --offline     # captions: ok, no warning
```

## Notes

- Depends on `2026-10-05-shorts-karaoke-captions-estimated-timing` (PR #1292) for the
  `timing.json` contract; add it to `depends_on` once that ticket is in `tasks/done/`.
- Weights' licences are checked at claim time (model cards, not only the code licence); the
  Azure SDK is a binary dependency, not copied code.
- `tts/client.mjs` is also named by `2026-10-05-speech-client-retries-paid-upstream-unavailable`;
  whichever lands second rebases.
- No receipt-bound file in scope.
