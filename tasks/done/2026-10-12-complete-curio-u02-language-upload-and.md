---
id: 2026-10-12-complete-curio-u02-language-upload-and
title: Complete Curio U02 language upload and verify Studio delivery
status: done
priority: P2
area: docs
owner: codex-gpt6-curio-u02-upload
claimed_at: 2026-10-12T04:47:16Z
created_at: 2026-10-12T04:47:08Z
completed_at: 2026-10-12T05:11:00Z
branch: codex/curio-u02-language-upload-20261012
depends_on: []
scope:
  - docs/videos/curio-u02/language-upload.md
---

# Complete Curio U02 language upload and verify Studio delivery

## Why

The owner asked to continue the English, Japanese and Korean supplements for the existing private U02 video, YouTube ID `uZ9TlblvrCw`. bb7a already completed the three 704.5-second M4A tracks and current captions. Initial Studio readback showed published CC and metadata but empty audio columns, despite backend text saying the dubs were uploaded. Complete the missing uploads and verify actual delivery using the existing approved media.

## Definition of done

- [x] English, Japanese and Korean audio each finishes processing and is Published in a fresh Studio readback.
- [x] Studio CC readback matches current EN 126 / JA 135 / KO 134 cues, including the corrected Korean `cf9b525f…` version.
- [x] Exact media/caption hashes, backend review and stored attachments, source-bound consumer output and final Studio evidence are recorded with accurate verification boundaries.

## Steps

- [x] Claim the upload-only scope; confirm the existing private video identity, missing Studio audio and current local delivery hashes.
- [x] Upload the three existing M4A tracks and submit the Studio update.
- [x] Wait for audio processing and verify all three final Published states.
- [x] Read back all three CC tracks and resolve any difference against current delivery files.
- [x] Reconcile backend review/attachments and consumer output against current local files.
- [x] Save final Studio publication evidence and record the completed delivery.

## How to verify

Read the three locale rows at `https://studio.youtube.com/video/uZ9TlblvrCw/translations` after a fresh reload; distinguish processing from Published. Compare Studio caption texts against current `upload/captions/*.srt`, recording any limits to timestamp/download verification. Hash exact upload audio/caption files and compare backend stored attachments and native approved-package consumer results. Preserve the original final and Traditional Chinese source. Save evidence under `C:/Users/x8120/mokaair-work/video-language-uZ9TlblvrCw`; do not infer upload from backend declarations alone.

## Completed outcome

All three original M4A tracks are now Published in Studio, alongside the three CC tracks and metadata translations. Fresh reload evidence at `2026-10-12T05:07:59.305Z` is saved in `studio-three-languages-published.json`; JSON SHA `c50d07b26cdc21ec4b596a4b1950f881228fcf080fd0b63c70b57e89904a8af2`. Screenshots are `studio-three-languages-published-names.jpg`, `studio-three-audio-published.jpg` and `studio-en-published-detail.jpg`; the normal narrow viewport is captured in parts without resizing. The 395 caption texts, six metadata fields and approved backend consumer all pass readback. Original media and source files remain unchanged; the video remains private.

## Evidence and boundaries

- Initial Studio audio columns were empty despite existing backend upload declarations. This run uploaded the three existing M4As, waited for processing and verified all nine audio/CC/metadata components Published after a fresh reload. No conversion, replacement, synthesis or new approval was needed; intermediate processing receipts remain historical.
- `studio-text-and-metadata-readback.json/.md` PASS at `04:59:22.564Z`: 69 checks, 16 unchanged input pins, all 395 raw cue strings exact including original LF/spaces, 395 separately flattened DOM labels exact, and all six metadata fields exact. Korean cues 13/122 equal the reviewed current amendments. JSON SHA `c74dc57b99832c3e4bb3d4a5a52831b8c30f21baf18c0f2268ce9c9dac82a10f`. Only 4/5/5 textarea timings were visible; no full Studio timing claim. The single download attempt timed out, so downloaded SRT bytes, playback and synchronization remain unverified.
- Existing native audio checks pass 126/126 lines per language with zero flags and zero unchecked. This task reuses the existing M4A files; no synthesis, paid check or original-video change is authorized by this task's scope.
- Current Korean SRT SHA is `cf9b525f3e349fed2c1f8dbd056d4e4832974a996a0a96a1d544f0af1235e87f`; old publish attachment `68da424d…` predates the two-cue whitespace repair and must not be used as current delivery evidence.
- Original final SHA `d0956ff8dd824375957091f593984914d99d60ccb7ed4e6c03c8fe4937eb79b8`; Traditional Chinese SRT SHA `5bc2d8402229c03ade1173b3fc4554ac247b9260157a80d3dc78feaa1b71d54b`.
- Fresh `u02-approved-readback-2026-10-12T04-55-10-408Z.json/.md` reports PASS, actual SSH exit 0, READ ONLY/repeatable-read transaction and rollback. All 513 accepted QA input hashes match before/after; three original M4As pass exact 704.5-second AAC 48 kHz stereo and full strict decoding. Fourteen original publish roles plus eleven language roles represent 19 distinct stored hashes; all match, and all eleven current language files match local delivery.
- Language review `a0c010cf-0e38-40ed-bd8b-bec37be99cab`, manifest `b1de6a4d43fcf4f777ad67298bd62b0728a6072be30980f1979b3c7e278cdd52`, is approved with its existing decision time `2026-10-11T23:07:10.131196Z`. Native `read_approved_package(verify_files=True)` passes with three dubs/four CC locales and corrected Korean `cf9b525f…`. The old publish `68da424d…` remains historical. This run made no approval action; bb7a's earlier pending/409 snapshot is superseded.
- Validation by root: docs-video tests 199/199, zero failed/skipped, about 32 seconds; task check validated 1,850 files with only unrelated existing stale-claim warnings; both exit 0, diff check PASS. Logs remain in the external audit directory.
- Full file hashes and delivery boundaries are in [language-upload.md](../../docs/videos/curio-u02/language-upload.md). The original video remains private; full player/listening, public visibility and owner playback acceptance are not established.
- Only this task file and `docs/videos/curio-u02/language-upload.md` are edited here. bb7a source scripts, translations, media state, tasks, H01/H02/L08 and foreign-language thumbnails are outside scope. No Git, UI, media stage or tests were run by the documentation subtask.
