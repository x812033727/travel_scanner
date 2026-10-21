---
id: 2026-10-20-produce-skill-is-an-instruction-booklet
title: Produce Skill is an instruction booklet: write one for the event folder, for non-technical users
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-10-20T19:05:00Z
created_at: 2026-10-20T19:04:30Z
completed_at:
branch: claude/ai-video-production-520ea2
depends_on: []
scope:
  - docs/videos/claude-skill-manual-event-folder
---

# Produce Skill is an instruction booklet: write one for the event folder, for non-technical users

## Why

The owner (2026-10-21) set 俗說 AI's 「Skill 出來滿一年了」 (58,000 views in six days on a
3,570-subscriber channel) as the second model: one mapping (a Skill is an instruction booklet)
carried through the whole video, the booklet's cover sentence and steps read out in full, exact
menu names, an admitted uncertainty, one safety paragraph. This is the pair's second video: the
first (`claude-code-beginner-event-folder`) uses a ready `/signup-check` Skill on the same invented
event folder; this one teaches writing it, with progressive loading measured in tokens.
Slug `claude-skill-manual-event-folder`.

## Definition of done

- [x] Brief (outline A), four outcomes with 成立條件, mechanical 要先實作 list.
- [x] 29 headless sessions in `runlog.txt` and `demo/` (27 planned + 2 added to test the appendix
      location fix). Outcomes 1, 2, 4 hold; 3 downgraded (the vague cover was opened 3/3 too).
- [x] Script, two fact-check rounds (4, 2 corrections), listener pass, two revisions after the
      blind panel plus two small fixes; lint clean; `category: "tutorial"`.
- [x] Narration synthesized; audio check rounds: 37, 7, 1 flagged lines reworded.
- [ ] final.mp4, captions, QA, review-push final (chained after the fourth audio check).
- [ ] Owner approvals on /admin/videos (outline, narration, final), then package and publish gate.
- [ ] On YouTube (the owner uploads).

## Steps

- [x] Plan, run, write, verify, listen, panel, voice, render.
- [ ] Assemble, captions, QA, review-push final, package, publish gate.

## How to verify

```bash
node tools/video/cli.mjs status --slug claude-skill-manual-event-folder
node tools/video/cli.mjs qa --slug claude-skill-manual-event-folder
```

## Notes

- The main example equals the simple ways on batch two (pasting the seven steps, CLAUDE.md, and
  even no instructions all pass 6/6); the brief's pre-agreed handling is told honestly: the booklet
  buys not pasting (309 vs 33 characters), not carrying (+462 tokens on every request) and
  portability (CITED). The measured surprises are the appendix missed in 5 of 8 runs when step 5
  names the file without its location (fixed 2/2 by naming the path), the fat booklet costing the
  same before opening and 2.8× per request after, and the vague cover opened every time.
- Blind panel ended at 10 of 13 after three readers; readers consistently found the token-number
  stretch (02:42–03:38) dense, so the narration now says only 77 and 462 aloud.
- Layout: a six-row request table overflowed and became a code card; the thumbnail headline needed
  two short lines (`Skill\n**是說明書**`) to pass the 24 px rule.
- The web app's upload steps, plans and sync are CITED only (no login here); the zh-TW help page
  names the menu 「自定義 > 技能」.
