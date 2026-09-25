---
id: 2026-09-25-video-captions-cues-that-wrap-into
title: Video captions: cues that wrap into three lines and words glued together
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T06:10:41Z
created_at: 2026-09-25T06:10:34Z
completed_at: 2026-09-25T06:14:18Z
branch: claude/video-caption-wrap
depends_on: []
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
---

# Video captions: cues that wrap into three lines and words glued together

## Why

On 2026-09-25 `captions` built the pilot video's (`ai-model-choice`) five tracks. `checkCues` flagged 3 English and 13 Korean cues that wrapped onto three lines. Some also had words glued together: "September2026", "보장은없습니다", "둘째,저는".

There were three causes in `tools/video/core/captions.mjs`:
- **Fit was judged by character count.** `splitText` only asked whether a cue was under `maxChars × maxLines`. Korean has long words and breaks only at spaces, so a 35-character line can be under 36 and still need three lines.
- **Greedy cutting left scraps.** An 88-character English line became an 84-character cue plus "2026.".
- **Merging scraps broke the fit and dropped spaces.** `timePieces` merged a scrap shorter than 0.9 s into its neighbour with no space, even when the result could no longer fit.

## Definition of done

- [x] No cue is cut or merged into something that needs more than two lines.
- [x] Words in English and Korean cues keep their spaces.
- [x] A line just over one cue is cut into even halves, not a full cue plus a scrap.

## Steps

- [x] Add `fits()`: lay the text out greedily into `maxChars`-wide lines, keeping Latin words and numbers whole. Greedy layout uses the fewest lines, so when `fits()` is true `wrapCue` can always find a break.
- [x] Replace clause-greedy `splitText` with a DP: fewest cues first, then the most even ones. A cut mid-clause costs as much as one cue being a quarter as long as the others. A cue never starts with punctuation.
- [x] `timePieces(pieces, start, end, rules)`: merge only when the merged cue still fits, and join with `joinPieces` (a space in word-based locales). A scrap that fits with neither neighbour stays short.
- [x] Remove the unused `clauses()`. `hardSplit` now uses the same tokens and is the last resort.

## How to verify

- `node --test tools/video/core/captions.test.mjs`: 14 pass. The new tests use the pilot's own examples.
- Pilot `captions` before → after:
  - en: 163 cues → 164; 3 three-line cues → 0.
  - ko: 172 cues → 185; 13 three-line cues → 0.
  - No cue anywhere is under 0.9 s, and no words are glued together.
  - The remaining warnings are English and Japanese reading-speed notes. The caption reviewer had already decided to leave those alone.

## Notes

- zh-TW, zh-CN and ja cut at any character, so their cue counts did not change (157/157/167).
- Japanese reading speed is checked against 8 characters a second. The pilot has 31 cues over it (8.2–11). That is a trade-off to settle in translation, not a layout bug, so it is not in this ticket.
