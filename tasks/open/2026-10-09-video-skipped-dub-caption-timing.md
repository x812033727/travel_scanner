---
id: 2026-10-09-video-skipped-dub-caption-timing
title: Use narration caption timing when a retained dub is genuinely skipped
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T13:32:11Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/core/stages.mjs
  - tools/video/core/stages.test.mjs
---

# Use narration caption timing when a retained dub is genuinely skipped

## Why

A normal DevDay English dub completed its first audio check, then a retake no
longer fitted its window. The normal worker wrote a genuine skipped.json but
retained the earlier track/timeline and all audio/check evidence. runCaptions
still selected that retained currentDub timeline. The renewal language binder
correctly required the narration presentation for a dub whose status is skipped,
so it rejected the new captions after some file PUTs and before a LANG POST.

## Definition of done

- [ ] A genuinely skipped dub's SRT/VTT and caption manifest follow the approved
      narration presentation, even when a current earlier dub track is retained.
- [ ] Current accepted dubs still use their own timing; stale/missing and
      unselected tracks retain their existing behavior.
- [ ] The normal renewal binder accepts the truthful skipped-dub package, with
      all original audio, flags and skip reason unchanged.

## Steps

- [ ] Reproduce the retained-current-track plus genuine-skip state locally.
- [ ] Align normal caption source selection with actual dub status without
      deleting track evidence or changing its skip/approval status.
- [ ] Verify narration/dub/stale/unselected cases and their actual cue timings.

## How to verify

Run `node --test tools/video/core/stages.test.mjs` and the relevant renewal binder
tests. The regression should prove actual cue boundaries, not merely a manifest
label, and require no live model, speech request or backend submission.

## Notes

- Actual private evidence under `<home>/mokaair-work/handoff/`
  `branding-peak-20261008/continuation`:
  `DevDay-EN-SKIP-caption-diagnosis.actual.json` SHA
  `ceaa47ded3705a3336d4314d7a8714d82ff6e8b6bb138c7d943af711ea30926f`.
- Normal genuine-SKIP candidate used localeCues(presented,texts,en,narration,null)
  and the unchanged toSrt/toVtt/checkCues. Candidate SRT SHA6a97a330; retained-dub
  SRT SHAf9312e1e. Both have186 cues, but their boundaries differ.
- Actual four-CC normal binder fixture passed with zero models/speech/API writes;
  SHA b0ccc6fc77a154f60cc25370e6578a11dbea6953878f61cc1c6ed874c21b0e86.
  It retained the genuine21.0 characters/sec warning. Mock file attachments are
  a local fixture, not a real LANG submission or owner acceptance.
- All182 current English WAVs,153 ASR records,nine flags,retake fit result and
  skip reason remain retained. The original successful/partial provider history
  must not be reset or replayed to fix caption source selection.
- Only this follow-up handoff is authored; canonical production tools remain
  frozen while the private, exact-source recovery is completed.
