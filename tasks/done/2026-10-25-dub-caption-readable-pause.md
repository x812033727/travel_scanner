---
id: 2026-10-25-dub-caption-readable-pause
title: Use available dub pauses to keep captions within reading speed limits
status: done
priority: P2
area: tools
owner: codex-caption-readable-pause
claimed_at: 2026-10-25T23:49:18Z
created_at: 2026-10-25T23:49:12Z
completed_at: 2026-10-26T00:18:09Z
branch: codex/ai-editable-animation-20261025
depends_on: []
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
---

# Use available dub pauses to keep captions within reading speed limits

## Why

The actual editable-animation film has 18 Spanish, 32 Vietnamese and one Portuguese cue
reading-speed warning, even though those lines have enough unused silence inside their
allocated visual windows. `captionTimelineOf` offers the pause up to the next line, but
`buildCues` stops after speech plus 400 ms. This makes the existing 17-character-per-second
check fail while leaving legal display time unused.

## Definition of done

- [x] Unmeasured, explicitly bound dub captions can use their existing quiet tail to meet the unchanged reading limit.
- [x] Text, cue cuts, first starts, audio samples, measured timing and legacy/passing caption bytes are preserved.
- [x] Display ends respect the line, visual window, next line, content, presentation and intro bounds; insufficient time keeps the warning.
- [x] The original controller regenerates the actual nine-locale captions and verifies the real files before delivery.
- [x] Full relevant video checks pass after the final code review.

## Steps

- [x] Diagnose the 51 actual warnings using read-only timeline/caption evidence.
- [x] Add a conservative fixed-cut reading-time allocation for explicitly windowed, unmeasured dubs only.
- [x] Add regression tests for readable pause use, unchanged cuts/defaults/measured onsets, all time fences and unresolved invalid/insufficient spans.
- [x] Run the targeted caption suite and independent actual in-memory reconstruction.
- [x] Complete original-controller real caption regeneration and broader validation.

## How to verify

`node --test tools/video/core/captions.test.mjs` passes 50 tests. The actual independent
in-memory reconstruction reports Spanish 18→0, Portuguese 1→0 and Vietnamese 32→0 native
cue problems, with unchanged cue cuts and text. SRT serialization/parsing is checked again.
Run `npm run test:docs-videos` and regenerate with the existing caption-only command under
the original project's exclusive lease; inspect every warning and actual output byte binding.

## Notes

- Scope is only `tools/video/core/captions.mjs` and its tests. No media, source translation,
  audio, retry, threshold, provider, approval or publication operation was performed here.
- The existing original film/controller owns `/workspace/work/ai-animation-01`; do not start
  a competing producer. Its generated caption files still contain the old warnings until its
  controller explicitly regenerates them at a safe lease boundary.
- Read-only diagnosis: `/workspace/work/ai-animation-01/caption-window-readability-diagnosis.json`.
- Independent current-code memory verification:
  `/workspace/work/ai-animation-01/caption-pause-independent-inmemory-review.json`.
  ES 117 cues/17 changed lines, at most 498 ms extra; PT 104 cues/one line, 229 ms;
  VI 119 cues/27 lines, at most 749 ms. Primary SRT/VTT bytes remain unchanged in memory.
- Targeted test log: `/workspace/work/ai-animation-01/caption-pause-targeted-tests.log`.
- Final independent review after finite-span/hash and separate content/presentation-bound
  hardening: `/workspace/work/ai-animation-01/caption-pause-independent-final-review.json`.
  The reviewer reran all 50 targeted tests and the actual in-memory ES/PT/VI and primary
  byte checks against core SHA `545b7228201c4043d48d2d2dfc6bca1762dfe5ee7e300c359ce872a07cb978b1`.
  No remaining concrete defect was found. This is not an actual-media regeneration result.
- The policy gives only deficient cues their missing reading milliseconds and shifts later
  pieces inside the same bounded window. It preserves every existing cue cut and does not
  claim the globally most compact possible allocation; an unresolved line stays flagged.
- Subsequent actual root regeneration was independently checked against all 18 immutable
  before files. Report `/workspace/work/ai-animation-01/caption-pause-production-verification.json`
  (SHA `77a071d0f75beb0cabeefa782d502f07a9c422c385a76af512348d35d82f1466`)
  verifies nine actual native SRT/VTT pairs, 51→0 reading warnings, 45 changed lines/59 retimed
  cues, unchanged text/cuts/per-line first starts, unchanged primary bytes and unchanged
  JA/ES/VI checked audio fingerprints. Every changed line stays inside every strict fence.
  Two pre-existing, unchanged visual holds are disclosed separately: EN291f73 367 ms and
  JA47c7d2 333 ms, both carrying native `absorbed: next-slack` metadata. No new crossing was
  introduced. This does not approve audio or a complete language package; TH remains deferred.
  Root owns the final broader-check result and task closeout.

- Root ACTUAL production regeneration/verification completed2026-10-26T00:02Z: all9SRT/VTT nativebytes/width/speed/overlap/duration checks pass, stable snapshot. Physical warnings ES18/PT1/VI32→0, not an exit0-only claim. 45lines/59cues retimed, alltext/cuts/line-firststarts andprimarySRT/VTT unchanged; no new crossings. Existing unchanged native EN/JA absorbed-slack caption holds are separately disclosed by the actual production report, not mislabeled newly introduced or globally zero.
- Independent ACTUALafter report /workspace/work/ai-animation-01/caption-pause-production-verification.json SHA77a071d0f75beb0cabeefa782d502f07a9c422c385a76af512348d35d82f1466; JA/ES/VI trackhashes/sizes/ffprobe589.6 remain matched to genuine earlier media proofs. No voice/retry/approval/provider/Studio operation occurred.
- Root broader checks after final545policy: test:tools2732total/2727passed/0failed/5unrelateddefault-platform-browser-optinskips; test:docs-videos236passed/0failed; targetedcaption50passed. Logs and actual artifact QA are referenced in docs/videos/ai-editable-explainer-animation/research/media-checkpoints/caption-pause-root-verification.json. This closes the caption-timing defect only; the film's ENunknownpayment/failedKO/PT/ID/THservicedeferremainseparateunfinishedwork.
