---
id: 2026-10-05-speech-align-gemini-cpu-aligner
title: Speech align: a CPU aligner for Gemini clips behind load_aligner
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T17:27:01Z
completed_at:
branch:
depends_on:
  - 2026-10-05-speech-align-character-timing
scope:
  - apps/api/app/video_speech/align.py
  - apps/api/tests/test_video_speech_align.py
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - apps/api/Dockerfile
  - docs/videos/SHORTS.md
---

# Speech align: a CPU aligner for Gemini clips behind load_aligner

## Why

`POST /video/speech/align` (ticket `2026-10-05-speech-align-character-timing`) times an Azure
phrase from the service's own word boundaries, but the Shorts channel voice is a Gemini voice
(`tools/video/shorts/site.mjs` `CHANNEL_VOICE`), and Gemini has no timing at all. For a clip sent
as `audio` + `text` the endpoint answers 503 `video_align_unavailable` because
`app/video_speech/align.py` `load_aligner()` returns `None`: no model ships. The karaoke captions
of a Gemini Short therefore still light on the estimate and the quality check still warns.
Everything else is in place: the contract (`chars: [{text, start_ms, end_ms}]`, `source:
"aligned"`, `model`), the thread hook (`run_aligner`), the route's refusals, the tool's cache
(`.speech-server/<key>.timing.json`, asked again every build until the server answers) and
`karaoke.mjs`; this ticket only has to put a model behind the hook.

## Definition of done

- [ ] `load_aligner()` returns an aligner on the production API container; a Gemini phrase sent
      as `audio` + `text` answers `source: "aligned"` with one entry per written unit
      (`align.units_of_text`), and the Shorts QA `captions` warning disappears for a Gemini Short.
- [ ] Measured on 20 Azure phrases against Azure's own boundaries (the parent ticket's check, now
      with the aligner timing the same WAV): the aligner's unit starts are within 60 ms (median)
      of the boundaries; the numbers are in this ticket.
- [ ] The container stays under its memory: RSS of the API process with the model loaded and one
      phrase aligned is in this ticket, the model loads lazily on the first request, one worker
      thread, and a failing model answers 502 `video_align_failed`, never a 500.
- [ ] The weights' licence is written here from the model card (not only the code's licence), and
      no code is copied from a GPL/AGPL/non-commercial project.

## Steps

- [ ] Pick the model from what was measured on 2026-10-05 (4-core machine, Python 3.13):
      `sherpa-onnx` 1.13.8 is a 4.4 MB wheel, 38 MB installed, 27 MB RSS on import;
      `sherpa-onnx-streaming-zipformer-zh-14M-2023-02-23` (74 MB tarball, 25 MB of int8 files)
      loads in 0.6 s, sits at 126 MB RSS and decodes a 3 s clip in 55 ms on one thread;
      `sherpa-onnx-paraformer-zh-small-2024-03-09` is a 78 MB tarball;
      `sherpa-onnx-paraformer-zh-2023-03-28` is 1.03 GB (its int8 model about 230 MB).
      Qwen3-ForcedAligner-0.6B and WhisperX's zh wav2vec2 need torch and do not fit the image.
      `vosk` 0.3.45 is a 7.2 MB wheel plus a 42 MB Chinese model, word level, mainland lexicon.
      A transducer's token times are emission times, late against the onset: measure the offset
      on the Azure phrases first (DoD 2) and correct it, or prefer Paraformer's CIF timestamps.
- [ ] Decide where the weights live: baked into `apps/api/Dockerfile` (pinned URL and sha256), or
      fetched on first use into a directory the api container can write and keep across deploys
      (today it has no such volume; `/tmp` is lost on every redeploy).
- [ ] Alignment from recognition: the model's tokens with timestamps, matched to the written text
      by edit distance so matched characters become anchors and the rest take the gap between
      their anchors (the same fill as `align._fill_gaps`), so a misread character never shifts the
      whole phrase; or a true CTC forced alignment over the reference tokens if the chosen model
      exposes its log-probabilities.
- [ ] `tests/test_video_speech_align.py` already runs the route with a fake aligner; add the real
      model's unit test behind a marker that skips without the weights.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_align.py -q
node tools/video/shorts/cli.mjs build --file <script> --workdir <VIDEO_WORKDIR> --speech server --captions karaoke
node tools/video/shorts/cli.mjs qa --dir <build> --offline     # captions: ok, no warning, with a Gemini voice
```

## Notes

- Filed by the parent ticket on 2026-10-05 with its measurements; see
  `docs/videos/SHORTS.md` §工具端 (`speech/align`) and the docstring of
  `apps/api/app/video_speech/align.py` for the decision not to ship one blind: no speech audio to
  align here, no Azure to compare against, and the Dockerfile outside that ticket's scope.
- `numpy` is already a runtime dependency (through ortools), so an ONNX model needs only
  `sherpa-onnx` (which bundles onnxruntime) or `onnxruntime` (a 23.6 MB wheel) itself.
