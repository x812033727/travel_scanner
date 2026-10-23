# Preschool artifact integrity

`audio.py` records an `artifact_integrity` receipt when it assembles an episode.
The receipt binds the complete resolved lesson (text and measured timeline) to
the size and SHA-256 of all five M4A tracks and eight SRT/VTT files. `mux()` copies
that receipt into `checks.json`, so the audio assembly and the completed final
remain separately identifiable. Resume, build, verification and packaging all
validate these receipts. A changed byte or source causes rejection/reassembly;
a present but invalid receipt never falls back to legacy handling.

Rendering writes `picture.checks.json` with the resolved-source fingerprint,
renderer fingerprint, frame rate, size and SHA-256. `--mux-only` requires this
receipt to match the actual picture and requested lesson. Missing receipts,
different text even at the same duration, or changed artwork require a render.
Mux records the picture's proven renderer metadata, not the current renderer's
identity. Completed final checks also retain `picture_integrity` to prevent a
new standalone picture from being packaged alongside an older final.

## Existing 48 episodes

The original delivery predates sidecar hashes. This is missing provenance
metadata, not evidence that those videos are damaged. Read-only compatibility
verification anchors the old files to their existing source-bound, hashed,
fully decoded `final.mp4`:

- Each audio sidecar's encoded packet content and timestamps must match its
  corresponding final audio stream.
- SRT/VTT bytes must match subtitles regenerated from the resolved lesson.
- A picture without a final-bound picture receipt must match the final video's
  encoded packet content and timestamps, even if a newer standalone render
  receipt exists.

Verification and packaging do not write upgraded metadata into original media.
An audio resume can persist a new receipt only after the legacy checks succeed.
If the checked final is unavailable, rebuild the audio from the source/cache;
do not create a receipt merely by hashing unknown files. A historical pilot
without `picture.checks.json` remains verifiable/packageable, but `--mux-only`
requires rerendering it before making a new final.

To inspect the original delivery without rewriting its report, media or ZIPs:

```sh
python tools/video/preschool/verify_series.py \
  --source docs/videos/english-preschool-series/lessons.json \
  --output /workspace/preschool-series-output \
  --report /tmp/preschool-integrity-verification.json
python tools/video/preschool/package_series.py \
  --resolved /workspace/preschool-series-output/lessons.resolved.json \
  --output /workspace/preschool-series-output --check-only
```

## Regression checks

```sh
node --test tools/video/preschool/integrity.test.mjs
```

The existing `npm run test:tools` glob includes this wrapper. It runs Python with
`-S`, so the ten temporary-fixture tests require neither Pillow, ffmpeg, speech
dependencies nor network access. They cover same-size sidecar byte changes,
audio reassembly preceding mux, mixed old/new receipts, missing or changed
picture receipts, and same-duration English text changes before mux.
