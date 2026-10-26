---
id: 2026-10-26-whisper-worker-pyav-decode-smoke
title: Pin worker PyAV compatibility and exercise real decoding
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-26T14:13:11Z
completed_at:
branch: codex/whisper-pyav-compat-20261026
depends_on: []
scope:
  - ops/video/Dockerfile
---

# Pin worker PyAV compatibility and exercise real decoding

## Why

The worker image pins `faster-whisper==1.2.1` but leaves its PyAV dependency
unbounded. A fresh installation selected PyAV 19.0.2. Imports and a cached
Whisper medium model load both succeeded, but the first actual audio operation
failed before producing a transcript:

```text
faster_whisper/audio.py:46
av.open(input_file, mode="r", metadata_errors="ignore")
TypeError: open() got an unexpected keyword argument 'metadata_errors'
```

The native checker correctly retains the original audio flags after this
exception. Its independent check therefore cannot help distinguish a real
misread from a first-transcriber false alarm. The current Docker `smoke` target
checks import and runner usage only; neither exercises this removed API.

This ticket covers the **worker image dependency and decode smoke**, not a
checker shim or a change to audio judgments. The earlier
[production checker report](2026-10-10-whisper-pyav19-second-opinion.md) scopes
the Python runner, while the [Windows/local setup follow-up](2026-10-14-make-whisper-second-opinion-work-with.md)
also covers Unicode console output. Neither currently scopes the Dockerfile.

## Definition of done

- [ ] A fresh worker image installs a dependency pair that supports the native
      `faster_whisper.audio.decode_audio` path. `av==18.0.0` with
      `faster-whisper==1.2.1` is the combination actually verified below.
- [ ] The existing Docker `smoke` target decodes and resamples a generated,
      nonzero PCM WAV. It checks the sample count, float32 dtype, finite values
      and nonzero output without loading a model or making an ASR/network call.
- [ ] The normal image and smoke builds pass in CI or a suitable build
      environment. Any production deployment/readback stays with its owning
      release workflow; this ticket does not authorize a deployment.
- [ ] Existing locale/clip/hints interfaces, models, QA thresholds, retry caps,
      uncertain billing holds and owner approvals remain unchanged.

## Steps

- [x] Reproduce the real PyAV 19 decode API failure and identify why import/model
      loading alone misses it.
- [x] Verify the public PyAV 18.0.0 API/wheel and a real generated-PCM decode
      with the existing faster-whisper version, outside the repository.
- [x] Check fresh main, worktrees, remote branches and open PRs; attempt the
      normal narrow claim without forcing another holder.
- [ ] After the overlapping scope is legitimately released or narrowed, claim
      this ticket and apply the minimal Dockerfile change below.
- [ ] Run the actual worker/smoke builds, record the results, and submit the
      code change for review. Do not treat this handoff as an implemented fix.

## How to verify

Proposed minimum dependency change in `ops/video/Dockerfile`:

```diff
- && /opt/whisper/bin/pip install --no-cache-dir "faster-whisper==1.2.1" \
+ && /opt/whisper/bin/pip install --no-cache-dir "faster-whisper==1.2.1" "av==18.0.0" \
```

Add a real decode invocation beside the existing Whisper import/usage checks in
`FROM worker AS smoke`. This exact Python command was run successfully with
the compatible external runtime on 2026-10-26; only the Python executable path
changes inside the image:

```sh
/opt/whisper/bin/python -c 'import io, math, wave, struct, numpy as np; from faster_whisper.audio import decode_audio; source=io.BytesIO(); writer=wave.open(source,"wb"); writer.setparams((1,2,48000,0,"NONE","not compressed")); writer.writeframes(struct.pack("<6000h",*(round(3276.8*math.sin(2*math.pi*440*i/48000)) for i in range(6000)))); writer.close(); source.seek(0); decoded=decode_audio(source,sampling_rate=16000); assert decoded.dtype==np.dtype("float32"); assert decoded.shape==(2000,); assert np.isfinite(decoded).all(); assert np.abs(decoded).max()>0'
```

This creates a 0.125-second 48 kHz mono PCM16 tone in memory and calls the same
decoder/resampler as the real runner. It does not instantiate `WhisperModel`,
load a checkpoint, transcribe speech, open a video clip or require credentials.
Do not replace it with another import-only check.

After implementing the change and checking current build policy/resources:

```sh
DOCKER_BUILDKIT=1 docker build -f ops/video/Dockerfile -t video-worker:pyav-compat .
DOCKER_BUILDKIT=1 docker build -f ops/video/Dockerfile --target smoke --progress plain .
npm run check:tasks
git diff --check
```

## Notes

### Scope-blocked handoff, 2026-10-26

- Worktree: `/workspace/travel_scanner_asr_compat`; branch
  `codex/whisper-pyav-compat-20261026`; checked base
  `origin/main` at `80cb444e2d87b7b53639bd203dfa19c6edd0ef90`.
- `who-is-on-it --scope ops/video/Dockerfile` found no open PR touching the
  file. Remote branch/PR searches found no Whisper/PyAV fix. The Dockerfile on
  fresh main still contains the unbounded dependency and import/usage checks.
- The normal claim was actually refused:

  ```text
  2026-10-26-whisper-worker-pyav-decode-smoke covers files already being changed by 2026-10-24-bug-1-4 (claude-opus-5-5-xitong-120min); run 'next' for a task that is free, or pass --force
  ```

- [The holder](2026-10-24-bug-1-4.md) remains `in-progress`, with scope
  `ops/video`. Its claim is stale by age, but scope collision checks still
  refuse the new claim. No `--force`, release, takeover or edit of the holder
  was attempted. This ticket stays open and unclaimed; **the Dockerfile was
  not modified**.
- The checker itself is also covered by the held
  [five-language worker task](2026-10-19-worker-video-languages-five.md).
  Keeping the proposed fix inside the Dockerfile avoids that separate scope.

### Actual failure and compatible-runtime evidence

- Full native one-clip failure trace, outside git:
  `/workspace/work/video-asr-runtime/diagnostics/one-native-TH.stderr.log`,
  SHA-256 `a7afc9372d68ab9cecd6bd18677be03d2f16f4489acfa80dbb00c1bfc5400272`.
  The exception occurred at `av.open` argument validation, before decoded
  samples or a transcript existed. This is not evidence of a bad voice take.
- Diagnosis receipt:
  `/workspace/work/video-asr-runtime/diagnostics/native-audio-dependency-failure-diagnosis.json`,
  SHA-256 `de4b2b6711dbab3fa25fe73f3be5060e9ba96de11c8f79f48da1aab01dc4daa4`.
- The runtime owner actually changed only `av==19.0.2` to `av==18.0.0` in an
  independent venv. Its `faster-whisper==1.2.1`, other distributions, medium
  checkpoint, runner and QA configuration stayed unchanged. Compatible receipt:
  `/workspace/work/video-asr-runtime/runtime-ready-compatible.json`, SHA-256
  `57b652d570e87fad17fde911678b7a00d3aff5d86736310bf0d8032af5e62f53`.
- Public API confirmation:
  `https://raw.githubusercontent.com/PyAV-Org/PyAV/v18.0.0/av/container/core.py`,
  retrieved source SHA-256
  `adde3cbf3bd601a86eb5d8eb7ad5969663275d71afaf2a6a3b0aaf87482e0dd2`;
  the `metadata_errors` argument remains in the v18 `open` signature.
- Verified public wheel: `av-18.0.0-cp311-abi3-manylinux_2_28_x86_64.whl`,
  35,536,910 bytes, SHA-256
  `ae56b40b6f8b067a8ad2dac664fbfbabac7f7a55b9a7bb031eb99289252bc017`.
- The compatible receipt records a real 6,000-sample 48 kHz generated PCM
  fixture decoding to 2,000 float32 samples at 16 kHz, finite/nonzero, with zero
  video audio files, model inferences, ASR calls or paid calls.
- This handoff's proposed inline command was also actually run using
  `/workspace/work/video-asr-runtime/venv/bin/python`: exit 0, PyAV 18.0.0,
  2,000 float32 samples, finite/nonzero, peak `0.100006103515625`. Its generated
  fixture SHA-256 was
  `f04e8467e4cda99f8e223c47c1fb3fbe313bfa4149e1fb3bece81659e316418f`.
  No model was instantiated, downloaded or transcribed by this check.
- No Docker build, production-image install, deployment, film-ASR clearance,
  approval, threshold change or billing reconciliation is claimed here.
- Ticket-only checks: `npm run check:tasks` exited 0 and validated 2,190 task
  files, with existing overlapping-scope warnings preserved in
  `/workspace/work/asr-compat-audit/check-tasks.log`; `git diff --cached --check`
  passed. Only this new open ticket is staged; the Dockerfile remains identical
  to the checked main revision.

Next: wait for the `ops/video` holder to release/narrow its scope, recheck fresh
main and competing PRs, claim normally, then implement and build the worker
image and smoke target. The external runtime fix already unblocks the current
film operator independently of this packaging ticket.
