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
request against the Skill's 61; a session in which Claude calls the Skill itself sends one
request more; the slash call does not). The rewrite says so on screen. Two things were outside
that task and nothing downstream should start before them:

- The owner has not chosen the new outline (option D in `brief.md`). The brief asks the owner
  to judge whether an example that stands on a few hundred tokens a request and on the slash
  entry point is enough for a tutorial, or whether the example has to change.
- `verify-1.md` and `verify-2.md` checked the 2026-10-09 script. Nobody independent has checked
  the rewritten `video.json` and `claims.md` against `runlog.txt`.

## Definition of done

- [ ] The owner's decision on option D is recorded (`approve --gate outline`, or the brief's
      first line reads 「含金量不足：…」 and the film is dropped or replanned).
- [ ] If it goes ahead: a `verify-3.md` from an agent that did not write the script, with every
      card that claims a run found in `runlog.txt` and every cited page reopened.
- [ ] If it goes ahead: the two cards the writer doubted fit the frame (`look-call`, a one-line
      JSON quote; `slash-score`, a four-column table) are judged by the render stage, and cut or
      split if it reports an overflow.

## Steps

- [ ] Ask the owner with options: go ahead with option D; replan the example; drop the film.
- [ ] Fact-check, then the listener pass, then speech and render as usual.

## How to verify

`node tools/video/cli.mjs status --slug claude-code-skills-hands-on` shows the outline approved
and the script fact-checked against its current hash.

## Notes

- The run log's 2026-10-11 section and `demo/results/2026-10-11.summary.txt` hold every number.
- All 120 narration lines need speech again: 42 are new and most of the 78 kept ids were reworded.
- If the owner wants the two arms' instructions to be exactly equivalent, CLAUDE.md has to carry
  the `# vX.Y.Z` title line the template has, and that arm has to be run again (`claims.md`, c60).
