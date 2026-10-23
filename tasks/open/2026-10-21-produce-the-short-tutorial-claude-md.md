---
id: 2026-10-21-produce-the-short-tutorial-claude-md
title: Produce the short tutorial 'CLAUDE.md is the house rules' (paper look, one concept, 7 minutes)
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-10-21T13:50:26Z
created_at: 2026-10-21T13:49:27Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-md-house-rules
---

# Produce the short tutorial 'CLAUDE.md is the house rules' (paper look, one concept, 7 minutes)

## Why

The owner (2026-10-21) watched the two 13-minute tutorials of PR #1643 and found them dull, hard
to follow and visually weak; the target is the view counts of the two reference videos. The second
round of the reference study (`docs/videos/reference-study-20261021/README.md` §第二輪) found
three causes: the overview topic is taken by 400k+ presenter videos with full desktop recording;
every chapter narrated run-log detail; all 102/104 states were text cards. The owner decided: both
kinds of tutorial, the short "one concept" kind first; the two #1643 videos stay as material; demo
pictures are synthesized terminals plus official-page captures; the first short one is
「CLAUDE.md 就是員工守則」. Rules: `teaching-flow.md` §十–§十二.

## Definition of done

- [ ] A video `claude-md-house-rules` (`category: "tutorial"`, 8:00–8:30, zh-TW only) reaches the
      publish gate on the site with the owner approving outline, audio, final and publish by hand.
- [ ] It is the short kind: one concept, the house-rules comparison carried through, the title
      sentence spoken within 15 seconds, chapters named as the viewer's questions, no run code or
      source stamp in card text or narration, at least half of the states non-text.
- [ ] Blind panel (tutorial wording) at least 11 of 13 with no reader calling it a report; listener
      ten questions all "no"; check-audio clean.

## Steps

- [x] Brief with three outline options (reusing the event-folder runs as RUN evidence); Jev picked A (0.89 / 0.96).
- [x] 「要先實作」 runs N0–N2 made and logged (runlog.txt, demo/N1, demo/N2) before the outline was chosen.
- [x] Script under §十–§十二 with `keys`, `icon`, `numeral`, `typing`, `theme: "paper"` (sidecar paper.json folded in once #1651's schema landed locally).
- [x] Fact check round 1 (58 claims, 0 fact changes; round 2 not required), listener pass (44 items applied), blind panel six readers 8→11→12→11→12→12.
- [x] tts 8:04, check-audio 0 flagged after two rewording rounds, render 61 states (paper look), assemble, captions zh-TW, qa.
- [x] review-push: outline (A), audio and final approved by the owner on 2026-10-22 (the first two rounds of clicks landed on other videos); package 4/4; publish gate submitted and pending the owner; languages.json written with empty locales.

## How to verify

`node tools/video/cli.mjs lint --slug claude-md-house-rules` and `qa --slug claude-md-house-rules`
all green; the contact sheet shows one thing per state and a key sentence band; the owner's four
approvals on /admin/videos.

## Notes

- The renderer fields (`theme`, `keys`, `icon`, `numeral`, `typing`) come from a parallel PR;
  script work can go ahead, render waits for it.
- Material: `docs/videos/claude-code-beginner-event-folder/` (runlog, demo/g1 self-written
  CLAUDE.md with the wrong rule 3, n1/v1/s1 comparison, extras).
