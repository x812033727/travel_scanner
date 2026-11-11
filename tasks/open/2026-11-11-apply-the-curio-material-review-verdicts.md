---
id: 2026-11-11-apply-the-curio-material-review-verdicts
title: Apply the curio material review: verdicts in themes.json, closing chapters 30-60 s, reserve themes off the producible list
status: in-progress
priority: P1
area: tools
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T01:45:07Z
created_at: 2026-11-11T01:44:55Z
completed_at:
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - tools/video/curio/pool
---


# Apply the curio material review: verdicts in themes.json, closing chapters 30-60 s, reserve themes off the producible list

## Why

On 2026-11-11 the owner approved the material review (`docs/videos/history-curiosity/pool/reviews/material-20261111.md`):
83 ready, 14 merge, 9 reserve. Closing chapters run 30-60 s, and the eight-minute floor stays.

## Definition of done

- [x] Every theme in `themes.json` carries `material` (verdict, reviewed_on, review; missing, plus merge_with for merge themes).
- [x] Closing chapters (title 「結檔…」) over 60 s are cut to 60 s on ready and reserve themes, and the saved seconds are not refilled, so target_minutes drops with them (26 themes). Merge themes keep theirs until they are rewritten.
- [x] `PRODUCIBLE.html` lists only ready themes (83). `THEMES.md` shows each verdict and what is missing.
- [x] `validateThemes` checks the field, with a test.
- [ ] The 14 merges are written as merged themes (follow-up; editorial work).

## Notes

- The rebuild also refreshed three input hashes in pool.json (curio-h24, curio-s42 video.json), which other work had changed. The build does that as a matter of course.
- The owner's 「同意」 is read as covering T96, T104 and T107 too (single-episode cores compressed into one chapter each), as the review proposed.
