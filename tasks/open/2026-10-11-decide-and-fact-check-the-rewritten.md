---
id: 2026-10-11-decide-and-fact-check-the-rewritten
title: Decide and fact-check the rewritten Skills hands-on tutorial
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T12:13:06Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-skills-hands-on
---

# Decide and fact-check the rewritten Skills hands-on tutorial

## Why

`docs/videos/claude-code-skills-hands-on` was rewritten on 2026-10-11 (task
`2026-10-11-rewrite-the-skills-hands-on-tutorial`) so that its main example is the same
procedure kept in CLAUDE.md beside the same procedure as a Skill. The runs showed no difference
in any scored step; the measured differences are sizes (CLAUDE.md adds 486 tokens to the first
request against the Skill's 61; a session in which Claude calls the Skill itself sends one or
two requests more; the slash call does not). The rewrite says so on screen. What is still open
before anything downstream starts:

- The owner has not chosen the new outline (option D in `brief.md`). The brief asks the owner
  to judge whether an example that stands on a few hundred tokens a request and on the slash
  entry point is enough for a tutorial, or whether the example has to change.
- An independent fact-check was made the same day (`verify-3.md`: 188 claims, twelve findings,
  pass after fixes) and its fixes were applied. Nobody has read the script again since those
  fixes, which added three scenes and five narration lines.

## Definition of done

- [ ] The owner's decision on option D is recorded (`approve --gate outline`, or the brief's
      first line reads 「含金量不足：…」 and the film is dropped or replanned).
- [x] An independent fact-check of the rewritten script: `verify-3.md`, 2026-10-11.
- [ ] If it goes ahead: a short second reading of what changed after `verify-3.md` (its last
      section lists every change), by someone who did not make the changes.
- [ ] If it goes ahead: the cards the writer doubted fit the frame (`look-call`, a one-line JSON
      quote; `slash-score`, a four-column table; `rule` row 3, a long cell) are judged by the
      render stage, and cut or split if it reports an overflow.

## Steps

- [ ] Ask the owner with options: go ahead with option D; replan the example; drop the film.
- [ ] The second reading, then the listener pass, then speech and render as usual.

## How to verify

`node tools/video/cli.mjs status --slug claude-code-skills-hands-on` shows the outline approved.
The status line "fact-checked" only tests that `verify-1.md` exists, so it has been ticked since
2026-10-09 and says nothing about this script; read `verify-3.md` instead.

## Notes

- The run log's 2026-10-11 section and `demo/results/2026-10-11.summary.txt` hold every number.
- All 125 narration lines need speech again: 47 are new and most of the 78 kept ids were reworded.
- What `verify-3.md` says a reader cannot rely on, and the script now words accordingly: the
  22-request break-even is an estimate on a small project, not a threshold; "give the must-hold
  step to a Hook" is the official recommendation, not something measured here; "one more
  request" held in the three paired runs and was two more in two of ten sessions; "the two
  sides are the same" means no difference was observed in three runs an arm.
- Left because each needs a new run: a measured break-even on a larger project; a control run
  without `--setting-sources`; the CLAUDE.md arm with the `# vX.Y.Z` title line written in
  (`claims.md`, c60).
