---
id: 2026-10-08-animatic-title-gap-subtitle-boundary
title: Animatic skips title spans and crashes subtitle lookup before next shot
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-08T14:57:11Z
completed_at:
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on: []
scope:
  - .agents/skills/animation-preproduction/scripts/animatic.mjs
  - .claude/skills/animation-preproduction/scripts/animatic.mjs
  - tools/animation-preproduction.test.mjs
---

# Animatic skips title spans and crashes subtitle lookup before next shot

## Why

`animaticShots()` currently exports only `plan.shots`, omitting non-shot title scenes while keeping their timeline gaps. In the e001 text animatic, a01-s008 ends at 15.7 s but a01-s010 starts after the omitted a01-s009 title. `show()` selects the future shot during the gap; `lineAt()` computes a negative line index and dereferences `undefined.speaker`. Real browser playback stops at 15.7 s with the button still showing pause. At the exact last frame, `findIndex()` also returns -1 and the current code selects the first shot instead of the last.

## Definition of done

- [ ] Preserve and display title/non-shot scene spans in the HTML preview, with their actual text and subtitle timing.
- [ ] Subtitle lookup safely handles empty lines, times before the span, exact boundaries and the final frame.
- [ ] A full e001 23:23.533 estimated animatic plays beyond all four title boundaries and stops on the last scene without a console error.
- [ ] `.agents` and `.claude` copies stay byte-identical and regression tests cover the real gap and final-frame cases.

## Steps

- [ ] Claim narrow scope; compare the scoped workaround linked below with upstream generator behavior.
- [ ] Repair generator and tests, then browser-check normal playback and final seek; do not equate generated HTML with completed viewing.

## How to verify

Run `node --test tools/animation-preproduction.test.mjs`, then `npm run test:tools`. Generate e001 HTML with `animatic.mjs`, start from 0, watch through the first title around 15.7 s, all other title boundaries, and seek to the exact end. Assert no undefined speaker and that final scene remains a05-s091.

## Notes

2026-10-08 independent reviewer observed `TypeError: Cannot read properties of undefined (reading 'speaker')` at `lineAt`, then `show`, then `tick`; error time 14:51:05.266Z, first playback started 14:50:49.419Z. This is an actual player defect, not hidden-tab timer throttling.

The e001 task uses an isolated [render-proposal.mjs](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/render-proposal.mjs) to include all 459 scenes, clamp subtitle indexing and preserve the last frame. Its 2,295 boundary probes pass; this does not fix the shared skill. Original generator files and their tests were not changed in this task filing. Ticket released for the shared fix.
