---
id: 2026-10-05-speech-align-character-timing
title: Speech align: character timing from the server for Gemini voices (CPU aligner) and Azure word boundaries
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1-align
claimed_at: 2026-10-05T17:03:51Z
created_at: 2026-10-05T16:08:22Z
completed_at:
branch: claude/speech-align-timing
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

- [x] `POST /video/speech/align` takes `{audio (base64 WAV), text, language}` and returns
      `{source: "aligned" | "azure", chars: [{text, start_ms, end_ms}], model}`; it is
      rate-limited per hour like the judge and answers with a provider answer (not a 500) when
      the aligner is unavailable.
- [ ] A phrase synthesized with an Azure voice carries word boundaries from the Speech SDK's
      `WordBoundary` events without a second call; a Gemini phrase goes through the CPU aligner.
      (Azure: done, through `speech` in the same request. Gemini: no aligner ships, see Notes;
      follow-up `2026-10-05-speech-align-gemini-cpu-aligner`.)
- [ ] Measured on 20 Azure phrases: the aligner's character starts are within 60 ms (median)
      of Azure's own boundaries; the numbers are in this ticket. (Needs live Azure, which the
      session that built this could not reach; the command is in Notes.)
- [x] A Shorts build with a server voice writes `timing.json` with `source: "aligned"`, the
      `captions` QA warning disappears, and the `--captions` default is unchanged. (With an Azure
      voice; a Gemini voice stays `estimated` until the follow-up.)

## Steps

- [x] Pick the aligner on the API container: Qwen3-ForcedAligner-0.6B (Apache-2.0, character
      level for Chinese), FunASR Paraformer-zh (MIT) or WhisperX's zh wav2vec2 (BSD-2); load
      lazily, one worker thread, measure RSS and seconds per phrase before enabling. (Measured;
      none enabled. Notes.)
- [x] `align.py` + `align_api.py` (own router mounted beside `video_speech_router`), schemas,
      tests with a fake aligner; the web proxy route under `apps/web/app/api/video/speech/align/`.
- [x] Azure: `WordBoundary` through the Speech SDK for standard zh-TW neural voices, returned
      beside the audio or cached by the phrase key. (Beside the audio: the align route takes the
      synthesis request and answers audio + boundaries; the tool caches both under the phrase key.)
- [x] `tts/client.mjs alignClip()`; `shorts/speech.mjs` caches the alignment beside the phrase
      WAV under `.speech-server/`; `karaoke.mjs` takes `chars[]` over the estimate.
- [x] Docs: `SHORTS.md` §工具端, `references/shorts.md` (the warning goes away).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_align.py -q
node --test tools/video/tts/client.test.mjs tools/video/shorts/karaoke.test.mjs tools/video/shorts/pipeline.test.mjs
node tools/video/shorts/cli.mjs build --file <script> --workdir <VIDEO_WORKDIR> --speech server --captions karaoke
node tools/video/shorts/cli.mjs qa --dir <build> --offline     # captions: ok, no warning (Azure voice)
```

## Notes

- Claimed with `--force` over its two open, unowned dependencies: neither is a precondition.
  `2026-10-05-speech-api-tells-a-provider-answer` reclassifies the existing routes' lost answers
  (shares `tools/video/tts/client.mjs`); `2026-10-05-reuse-confirmed-speech-results-across-restart`
  journals paid requests (shares `tools/video/shorts/speech.mjs`). This ticket adds a new route
  and new functions beside theirs; whichever lands second rebases.
- **Scope decided the shape of the Azure path.** `admin_api.py` and `azure.py` are not in this
  ticket's scope (they are in the first dependency's), so the speech route still synthesizes
  over REST and cannot cache boundaries by phrase key. Instead the align route accepts the same
  synthesis request as `speech` and does that one synthesis itself through the SDK, answering
  the WAV (base64) beside the boundaries, with the same budget reservation, allowlist and error
  codes. `shorts/speech.mjs` uses it for Azure voices (`synthesizeAligned`), so a phrase is still
  paid for once; a site from before the route answers 404 and the tool synthesizes as before.
- **Azure SDK measured** (`azure-cognitiveservices-speech` 1.52.0): 2.7 MB wheel, 9 MB installed,
  import 0.19 s, 36 MB RSS. `ldd` of the core library: libstdc++, libuuid, libm, libc only; the
  device-audio extension is the one that links `libasound.so.2`, and in-memory synthesis
  (`audio_config=None`) never loads it, so `python:3.13-slim` needs no apt package. The SDK is
  imported lazily inside `align.py`; a host that cannot load it answers 503, not a crashed API.
  `uv.lock` was re-locked with uv 0.12.22, the version the Dockerfile pins (the lock moved from
  revision 3 to 5; two packages added, the SDK and `azure-core`).
- **CPU aligner: measured, not shipped** (4-core machine, Python 3.13, 2026-10-05).
  Qwen3-ForcedAligner-0.6B and WhisperX's wav2vec2 need torch: out for a 3 GB container.
  `sherpa-onnx` 1.13.8: 4.4 MB wheel, 38 MB installed (+5 MB libs), 27 MB RSS on import.
  `sherpa-onnx-streaming-zipformer-zh-14M-2023-02-23`: 74 MB tarball, 25 MB of int8 files,
  load 0.6 s, 126 MB RSS, 50–60 ms per 3 s clip on one thread. `sherpa-onnx-paraformer-zh-small-2024-03-09`:
  78 MB tarball. `sherpa-onnx-paraformer-zh-2023-03-28`: 1.03 GB tarball (int8 about 230 MB).
  `onnxruntime` 1.30: 23.6 MB wheel (sherpa bundles its own). `vosk` 0.3.45: 7.2 MB wheel plus a
  42 MB Chinese model (word level, mainland lexicon). Not enabled because (1) accuracy could not
  be measured here: no speech audio to align and no Azure to compare against, and a transducer's
  token times are emission times that trail the onset, so the 60 ms median is unproven; (2) the
  Dockerfile is outside this scope, so the weights would be a runtime download into a container
  layer lost on every deploy; (3) the weights' model cards were not checked for licence here.
  The hook is `align.load_aligner()` (returns None) with `run_aligner` on a worker thread and
  `video_align_failed` for a model that throws; the route, the client and `karaoke.mjs` already
  handle `source: "aligned"`, so the follow-up adds a backend only.
- **Accuracy check the owner runs** (DoD 3, live Azure): synthesize 20 zh-TW phrases through
  `POST /video/speech/align` with `speech` (the tool: a karaoke build with an Azure voice fills
  `.speech-server/<key>.timing.json` with `source: "azure"`); those boundaries are the reference.
  Once an aligner ships, send each cached WAV with its text as `audio` + `text` and compare each
  unit's `start_ms` with the azure file's: `python - <<EOF` over the two JSON lists, median of
  `abs(aligned.start_ms - azure.start_ms)` per unit, must be ≤ 60 ms. Until then the Azure path
  is the reference itself and the box stays open.
- Azure times a Chinese word of several characters as one `WordBoundary`; `chars_from_boundaries`
  shares the span evenly between its characters (one syllable each). A `<sub alias>` term keeps
  the union of its alias words' boundaries, whether the service echoes the alias or the written
  term; boundaries are matched by text, in order, inside the units' spoken forms, so a boundary
  the text does not contain is skipped and never shifts the rest. Punctuation the service does
  not time takes the gap between its neighbours.
- `tests/test_error_localization.py` exempts operator surfaces by file name (`admin`); the ticket
  names this file `align_api.py`, so its refusals are `AlignRefused` from `align.py`, turned into
  the route's `AppError` there (as `admin_api` does with `CheckUnavailable`). Rename the file to
  carry `admin` if literal codes are ever wanted there.
- Tool side: only a `--captions karaoke` build asks the server to time clips it has not timed yet
  (`narrate({ align })`); a plain build takes what the cache holds. `timing.json` is `aligned`
  only when every phrase was measured; a timing whose units do not spell the phrase keeps that
  phrase's estimate; with nothing measured the file and `checks.json.captions` are byte for byte
  what they were.
- No receipt-bound file in scope; `node tools/video/long-form/cli.mjs check` passes.
