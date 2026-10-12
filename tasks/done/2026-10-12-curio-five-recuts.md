---
id: 2026-10-12-curio-five-recuts
title: Remaster five published Curio videos with narrated openings and musical end screens
status: done
priority: P1
area: docs
owner: codex-curio-recuts-8bc3
claimed_at: 2026-10-12T12:36:46Z
created_at: 2026-10-12T12:36:29Z
completed_at: 2026-10-12T14:00:31Z
branch: codex/curio-five-recuts-20261012
depends_on: []
scope:
  - docs/videos/curio-five-recuts-20261012
---

# Remaster five published Curio videos with narrated openings and musical end screens

## Why

The owner requests complete new versions of five already uploaded Curio episodes:
Roanoke (h02), Area 51 (u02), Tunguska (h03), crop circles (l08), and Mary Celeste
(h01). Each needs a narrated 30–60 second condensation before the channel bumper,
the approved musical end-screen outro, and synchronized English, Japanese, Korean
and Traditional Chinese openings, captions and audio tracks. The owner explicitly
selected new complete files for later reupload; existing uploads remain preserved.

## Definition of done

- [x] Five complete 1080p films with new narrated openings, channel bumper, retained
      chapter 2 onward, and the approved 21-second musical outro.
- [x] All four language openings and CC follow the new common timeline; three
      supplemental audio tracks retain the existing reviewed body audio.
- [x] Every package has updated localized metadata/chapters and exact Studio
      end-screen timing, with final/source hashes and media verification.
- [x] Deliver reviewable files; report owner playback and later reupload separately.

## Steps

- [x] Inventory source files, ownership, current branding and existing delivery.
- [x] Confirm reupload and four-language scope directly with the owner.
- [x] Write and independently review source-bound condensation scripts.
- [x] Synthesize only new lines with durable request receipts, then verify speech.
- [x] Assemble isolated output and verify frames, audio, captions and source retention.
- [x] Prepare upload packages and record outstanding owner actions.

## How to verify

Runners and verification instructions live in docs/videos/curio-five-recuts-20261012.
Validate exact retained picture packets, source hashes before/after, complete AV
decoding, 30fps frame totals, 48kHz audio length, integrated loudness/peak, all CC
cue ranges and localized chapters. Check intro/body and body/outro joins visually.
Native audio checks for only the new narration remain distinct from owner listening.

## Notes

- External output: C:/Users/x8120/mokaair-work/curio-five-recuts-20261012.
- Source-map.json identifies the authoritative original paths. Four use
  mokaair-work/videos/<slug>; H01 uses videos/_h01-native-delivery/curio-h01.
  The older H01 canonical final no longer matches its upload metadata, so do not use it.
- All five frozen source scripts match the original timeline speech hashes.
- The H01 Japanese body contains 117/118 native-clear lines plus one exact
  owner-accepted mtua line; preserve that provenance instead of claiming native full PASS.
- Current v4 outro was read back from video-worker: hash
  00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396.
  Golden Hour–Telecasted, existing owner-selected YouTube Audio Library asset.
- Clickable elements require Studio setup after new upload. Existing template
  oxEtlA8GWas: best for viewer, subscribe, latest upload; begin at duration minus 16s.
  Actual frame review found the old minus-17 guidance still overlaps a 1s CTA fade.
- Isolated editorial remasters do not bypass canonical uploaded/approved protection
  or claim to implement the unrelated global bumper-position task.
- No new image generation or whole-body speech synthesis is needed.
- New four-language scripts contain 144 lines. Independent editorial review and
  five speech cache/alignment safety tests passed. A real FFmpeg synthetic
  integration fixture passed; this is not completion evidence for the five films.
- All 20 new opening tracks are checked, with exact-waveform offline evidence
  resolving ASR false positives. Primary flags remain preserved. Five first
  retakes, two H03 pronunciation repairs, and one L08 wording repair are recorded.
- H03 uses h03-pronunciation-specs.json; L08 uses l08-wording-specs.json. The
  original shared intro-specs.json was not changed during active rendering.
- All five final films passed complete technical QA and limited still-image review.
  U02 additionally uses u02-visual-specs.json to select frame 316 of the comparison
  card, after the first extraction caught its second column before reveal.
  This visual-only repair reused the same verified speech and captions.
- Fresh delivery-index verification reports 5/5 with no errors: five complete
  MP4 files, 20 CC files, 15 supplemental WAV files, four localized descriptions
  per film, thumbnails, chapters, checksums and last-16-second Studio settings.
  Full evidence and hashes are in DELIVERY-REPORT.md and the external index.
- Source pictures and all retained body PCM were unchanged. Automated QA and
  sampled stills do not claim full owner playback, listening, upload or publication.
  The owner-selected scope is complete files for later reupload; Studio clickable
  elements remain a post-upload action. No new YouTube uploads were performed.
- Speech/retake/revision tests passed; docs-video suite passed 209/209 under
  bundled Node 24.19. System Node 24.13 reproduced a known native child-process
  crash (3221226505); the original failure log is preserved with the successful
  bundled-runtime rerun. The newer revision tests passed separately.
