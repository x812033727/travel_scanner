---
id: 2026-10-09-fix-what-the-first-use-of
title: Fix what the first use of the content-value rules found unclear or impossible
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-09T03:51:26Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/templates
  - tools/video/core/lint.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Fix what the first use of the content-value rules found unclear or impossible

## Why

`VALUE_RULES` (PR 1392, deployed 2026-10-09) were written from a comparison of two videos and
had never been used. Their first use was a re-plan and re-write of the rejected Mods video
(`docs/videos/claude-code-mods-hands-on`), by a planner and a writer that were each asked to
report where a rule was unclear, contradicted another rule, or could not be met with the slide
templates. The rules did change the result: the planner refused the old angle, wrote four
outcomes with their proof, and marked what had not been observed. But both agents had to guess
in the places below, and a model on the host will guess differently each time.

## What they found

Evidence

1. Evidence between none and all is undefined. 「要先實作」 is only required when a tutorial has
   no run evidence at all. A mod that is validated and tested but never loaded, or run in a
   headless session but never seen in an interactive one, sits in between, and "the result
   first, on screen" then has only test output to show.
2. For something a model wrote on request, the rules do not say what the proof is: the request,
   the artefact, or both from the same run. The same sentence does not reproduce the same code.
3. A step outside the outcomes (how to keep a mod, how to turn it off) may have only an official
   example. The rules speak of outcomes in one place and of steps in another and do not say
   whether such a chapter stands.
4. "A risk, limit or warning is said once" collides with the teaching route's "label what is
   untested, compare expected and observed": statements of evidence status have to recur.

Templates against "the exact thing, in full"

5. `code` takes 64 characters a line and 16 lines (about 10 to 12 fit with a title and a
   caption); `chat` takes 44 characters; `terminal` takes 78 columns of command, 8 lines, and no
   home directory. Real source had a 143-character line and real output a 367-column line. The
   rule should say what to do: re-wrap the source and run it again, or show an excerpt and put
   the whole file in the description; never change a character.
6. No template holds an excerpt of real output with its date and tool version, or a command
   longer than 78 columns. The writer fell back to `quote`, `compare` and `table`, with the date
   in `compare.verdict`, which the template neither documents nor checks.
7. A tool result read out of a session (a digest of `claude -p --output-format stream-json`) is
   not what a terminal printed, so it cannot go on a `terminal` card. Nothing says how to show it.
8. "The card's source field" exists on `quote` and `stats` only. `table`, `steps`, `bullets` and
   `compare` have nowhere to name a source.
9. `code` has no per-line reveal, so one block repeats across scenes with a different highlight
   (27 scenes in this script) and the narration points at it (「亮起來的這一行」). The rules do
   not say whether pointing at a card counts toward "at most two sentences describe a picture".
10. `steps` always draws STEP n and arrows and cannot show alternatives; the brief asked for it.
11. `planner.md` says to use only the templates in `TEMPLATE_SPECS` and also to use `screencast`,
    which is not in it.

Structure

12. The teaching route says ONE recurring example; the value rules say to reach the length with
    a second worked example. Whether the second is the route's "contrast" is not said.
13. The cap on risk collides with "a common failure and how to find it" and with the fourth
    move, "the exception". Both agents read the cap as covering warnings about the subject only.
14. The teaching route wants trust settled before access is granted; the fixed chapter order
    puts loading under "how do I do it", before "how do I know it worked".
15. "Something one line answers" has no edge: running one command and reading four kinds of line
    in its output was counted as an outcome; another reader would not.
16. "Never the hook unless the subject is an incident": may a tool tutorial open on the owner's
    own incident, or on another tool's limit? Both agents assumed yes.
17. "Every sentence carries a fact, a step, a reason, a result or a choice" against the required
    comment question, subscribe invitation and `cta` card.
18. Chapter one may not pass 30 seconds (lint) while the result comes first, so the mechanism
    had to move to chapter two; and the outro's three sentences share one state under the
    15-second cap with a 1.5-second tail.

Other contradictions in the prompt files

19. `planner.md`: every number comes from an official page opened today, otherwise write
    「以官網為準」. A run record, a limit in one's own code and the owner's own incident have no
    category, and that phrase is the hedge lint counts and the value rules forbid.
20. Opinions may only come from the channel's stance, but the manual route does not carry the
    stance text; the planner reused the numbers of an older brief.
21. `writer-video.md`: its "WRITE HERE ONLY" line omits `shorts.json` while its Shorts section
    says to write one and assumes `shot` scenes.

## Definition of done

- [ ] Each item above is answered in `VALUE_RULES`, the teaching route, the prompt docs or a
  template, or is written down as deliberately left to the writer.
- [ ] Evidence has named levels (tested, run in a session, seen in the interface) and the rules
  say what each may be used to show.
- [ ] A long real line has one sanctioned treatment, and a template can carry an excerpt of real
  output with its date and version.
- [ ] The source of a fact can be named on every card that states one.
- [ ] Prompt tests cover the changed wording; the duration receipt is rebound by a reviewer.

## Steps

- [ ] Decide items 5 to 8 with the template code open (`tools/video/templates/templates.mjs`,
  `theme.css`): which are rule wording and which need a template field.
- [ ] Rewrite the rule text; keep it shorter than it is now where two rules become one.
- [ ] Re-run the planner on one past brief to see the guesses are gone.

## How to verify

`node --test tools/video/automation/prompts.test.mjs tools/video/core/lint.test.mjs`,
`node tools/video/long-form/cli.mjs check`, and a planner run on the Mods topic that reports no
item from this list again.

## Notes

- Source of the list: the planner's and the writer's reports for `claude-code-mods-hands-on`,
  2026-10-09. The brief and `claims.md` in that folder show each guess in place.
- Related gates that are not rule wording: `2026-10-09-send-a-final-cut-back-to`,
  `2026-10-09-give-the-automated-route-a-way`, `2026-10-09-judge-a-brief-s-viewer-outcomes`.
