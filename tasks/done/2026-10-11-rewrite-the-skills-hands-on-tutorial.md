---
id: 2026-10-11-rewrite-the-skills-hands-on-tutorial
title: Rewrite the Skills hands-on tutorial against the CLAUDE.md arm
status: done
priority: P2
area: docs
owner: claude-opus-skills-rewrite
claimed_at: 2026-10-11T11:19:53Z
created_at: 2026-10-11T11:19:47Z
completed_at: 2026-10-11T12:13:44Z
branch: claude/skills-hands-on-rewrite
depends_on: []
scope:
  - docs/videos/claude-code-skills-vs-claude-md
---

# Rewrite the Skills hands-on tutorial against the CLAUDE.md arm

## Why

`docs/videos/claude-code-skills-vs-claude-md` is a finished ten-minute tutorial on Claude Code
Skills (2026-10-09). On 2026-10-11 the owner refused another tutorial for too little substance,
the content-value rules were tightened (`tools/video/automation/register.mjs`, `VALUE_RULES`),
and a blind reading judged this film "rework":

1. Its headline, "with the Skill 3 of 3, without 0 of 3", compares a Skill with Claude told
   nothing. The viewer's real alternative is the same five steps left in CLAUDE.md, which had
   one session and did all five steps.
2. Its choosing rules were quoted from official pages and tied to no observed result.
3. Eleven narration sentences talked about the film's own making.
4. The full `claude -p` command was on no card, and the logging hook was shown in part.

## Definition of done

- [x] The brief names the simple way (不用這個方法：the same procedure in CLAUDE.md) and lists,
      before any session, the runs and what would count as a difference.
- [x] Both arms are run on the same request, three sessions an arm, and every session is in
      `runlog.txt` with its command, tool version, output and score.
- [x] The brief records what the runs showed and says plainly whether the example carries the film.
- [x] `video.json` shows the two arms side by side in the runs' own words, ties each choosing
      rule to a measured result, has no sentence about the film's own making, and carries the
      command a viewer types on a card as typed.
- [x] `claims.md` points every claim at its evidence.
- [x] `node tools/video/cli.mjs lint --slug claude-code-skills-vs-claude-md` ends with 0 errors.

Not part of this task, filed as `2026-10-11-decide-and-fact-check-the-rewritten`: the
owner's choice of the outline (option D, or "the example does not carry a film") and an
independent fact-check of the rewritten script (the two verify files are for the old one).

## Steps

- [x] Plan the CLAUDE.md arm in `brief.md` and commit it before the first session.
- [x] 23 headless sessions on 2026-10-11 (Claude Code 2.1.295, `--model sonnet`): skill against
      CLAUDE.md on the release request, the same with five procedures, a request that only asks
      for a look, one base session, three slash calls, one session typed exactly as the card shows.
- [x] Results into `runlog.txt`, `demo/results/` and `brief.md`.
- [x] Rewrite `video.json` (option D) and `claims.md`.
- [x] Lint, the hygiene test and the docs-videos test.

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-skills-vs-claude-md     # 0 errors
node --test tools/repo-hygiene.test.mjs tools/docs-videos-tests.test.mjs
# the model-free checks of the new seed files (needs Claude Code and Git Bash):
WORK=/tmp/skills-work bash docs/videos/claude-code-skills-vs-claude-md/demo/m-checks-2.sh
```

The numbers on the cards are in `docs/videos/claude-code-skills-vs-claude-md/demo/results/2026-10-11.summary.txt`;
how each was produced is in `runlog.txt` from the line `2026-10-11   THE CLAUDE.md ARM`.

## Notes

- What the runs showed. Every scored step came out the same in both arms: 3 of 3 against 3 of 3
  with one procedure, with five procedures in a 59-line CLAUDE.md against five skills, and on a
  request that mentions the release but only asks for a look (neither arm changed a file).
  What differs is size. First request above "no procedure": skill +61 tokens, CLAUDE.md +486;
  five skills +288, five-procedure CLAUDE.md +1,155. A session in which Claude picks the skill
  up by itself sends one request more (39,565 input tokens against 30,296); called as
  `/release-prep 0.3.1` it does not (30,407). On the look request the skill was still called
  3 of 3 and no step was carried out.
- So the film's old headline measured "told" against "not told", not Skill against CLAUDE.md.
  The rewrite opens on the equality and builds the choosing rule on the two costs.
- Open judgement, written into `brief.md` for the owner: the example stands on a measured cost
  of a few hundred tokens a request and on the slash entry point, not on the Skill doing
  something CLAUDE.md cannot do to the result. If that is not enough for a tutorial, the
  example has to change, not the script: nothing cheaper to run was found in which a Skill
  beats CLAUDE.md on the outcome.
- The lint needs `pinyin-pro`; this worktree had no `node_modules`. It was run with a resolve
  hook that borrows the package from another checkout on the machine; nothing was installed.
- `*.log` is ignored by git, so a session log kept under `demo/results/` has to be named `.txt`.
- The shell that starts the sessions carried `CLAUDE_EFFORT=xhigh` on 2026-10-11 and `high` on
  2026-10-09; the runner set it to `high`. Whether it changes a headless session is not measured.
- A request's size depends on the project folder's path, so sizes are only compared between
  sessions made in the same folder on the same day.
- The script that built `video.json` is outside the repository; `claims.md` says what it
  checked. Whoever edits a code, terminal or quote card by hand should check it against the
  source file again.
