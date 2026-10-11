---
id: 2026-10-11-tutorial-worth-rules
title: Hold a tutorial to what its viewer gains: the example beats the simple way, the subject is opened, the narration does not talk about the making
status: done
priority: P1
area: tools
owner: claude-opus-5-5-worth-rules
claimed_at: 2026-10-11T09:43:13Z
created_at: 2026-10-11T09:41:09Z
completed_at: 2026-10-11T09:51:39Z
branch: claude/tutorial-worth-rules
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/value-rules.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
---

# Hold a tutorial to what its viewer gains: the example beats the simple way, the subject is opened, the narration does not talk about the making

## Why

On 2026-10-11 the owner watched a finished, unpublished tutorial,
`claude-code-mods-delivery-check-tutorial`, and said its substance is so low that publishing
it is pointless. The film met every rule written when it was made, and it passes today's
lint with 0 errors and 0 warnings. What it teaches: load a supplied mod, and a panel reports
whether three file names are in a folder the viewer already has open.

Three independent readings of the film (two of the script alone, one against the channel's
other Mods film) found:

- 12 to 15 of 127 narration lines explain how a mod works; 96 lines stand word for word if
  "Mod" is replaced by "a shell script" or "a prompt".
- The mod is 274 lines of JavaScript in `materials/delivery-check/hooks/`. None of the film's
  26 code cards shows a line of it. There is no terminal output and no picture of the panel.
- "A file that exists is not a file that is finished" is restated in 18 of 63 scenes.
- Three sections (content review, a date edit, a course variant: 20 scenes, 31% of the
  narration) do not use the mod, or use one that was never built.
- The same check is a one-line `Test-Path` loop or a look at the folder, and the film says a
  single prompt is enough for a one-off.

Then thirteen tutorials were read by blind judges against thirteen yes-or-no questions
(eighteen answer sheets; the five films read twice agreed on 63 of 65 answers):

| Film | Verdict | Failed of 13 |
| --- | --- | --- |
| claude-code-mods-delivery-check-tutorial (refused by the owner 2026-10-11) | drop / drop | 12 / 12 |
| claude-code-mods-no-sandbox-before-install (refused by the owner 2026-10-09) | rework / rework | 11 / 11 |
| codex-practical-01-cli (branch `codex/codex-practical-series-20261011`) | rework / rework | 7 / 9 |
| claude-code-mcp-hands-on | rework | 6 |
| claude-code-plugins-hands-on | rework | 6 |
| claude-code-skills-hands-on | rework | 5 |
| claude-code-permissions-hands-on | publish | 5 |
| claude-code-context-cost-hands-on | rework | 4 |
| claude-code-mods-hands-on | publish / rework | 4 / 4 |
| claude-code-subagents-hands-on | publish | 4 |
| claude-code-claude-md-hands-on | publish | 3 |
| claude-code-hooks-hands-on | publish / publish | 3 / 3 |
| claude-code-headless-hands-on | publish | 2 |

The two films the owner refused failed these and every other film passed them: the content
of the thing taught is on screen; the film has an observed result the viewer would not have
predicted; the main result is the output of a real run. Both refused films and the Codex
lesson had 28 to 50 narration sentences that hold with no mention of the subject; the ten
hands-on films had 2 to 9. All ten hands-on films had 4 to 16 narration sentences about the
film's own making (what was not run or not seen), which the rule on evidence labels allowed.
Three hands-on films compared their subject with nothing at all instead of with the simple
way a viewer would use (Skills, Plugins, MCP).

The rule text itself pushed the refused film where it went. The teaching route asked for
"one main worked example, a purposeful contrast and a transfer exercise" that "may be
variations of the main case": four chapters, 41% of the narration, are variations of one
small check. "A useful workflow, not an internal-code tour" was read as leave to keep the mod
shut. "Label the result as expected and the walkthrough as untested" kept unrun parts in the
film under a label.

## Definition of done

- [x] The rules sent to the planner, the writer and the listener of a slides video say: a
      result the viewer can already reach in a minute is not an outcome; a tutorial's main
      example has to beat the simple way, shown side by side; the subject is opened on the
      cards and the viewer changes it; a tutorial opens on a result nobody would guess; the
      narration does not talk about the making; a contrast or an exercise uses the subject
      and adds a result.
- [x] The teaching route's three sentences that led the refused film are amended.
- [x] The same rules are in the hand-driven guide (`script-writing.md`, the planner and
      writer prompt references).
- [x] Tests pin the new sentences.

## Steps

- [x] `VALUE_RULES` and `TEACHING_RULES` in `tools/video/automation/register.mjs`.
- [x] `tools/video/automation/value-rules.test.mjs` (a new file: `prompts.test.mjs` is in the
      scope of `2026-10-11-explainer-family-cute-presets`).
- [x] `script-writing.md`, `prompts/planner.md`, `prompts/writer-video.md`.

## How to verify

```bash
node --test tools/video/automation/value-rules.test.mjs tools/video/automation/prompts.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- This is prompt text. It reaches the automated worker after a deploy, and an agent driving
  the tools by hand only through the skill. Nothing checks it: the gate is
  `2026-10-11-judge-a-tutorial-s-worth-before`.
- Not changed, because the duration receipt binds them and
  `2026-10-11-explainer-family-cute-presets` holds the receipt: the planner's template line in
  `tools/video/automation/prompts.mjs` (it still says "one or two concrete things"; the value
  rules now say theirs holds) and rule 11 of `SKILL.md`. Filed as
  `2026-10-11-value-rules-in-the-bound-files`.
- The judges read each film as text (cards and narration), not the finished video. "publish"
  and "rework" are a model's reading; only the first two rows have the owner's own verdict.
- One of the thirteen questions did not discriminate: "is any single point made in three or
  more scenes" failed on 17 of 18 sheets. A gate should not use it as written.
- The answer sheets, the film texts the judges read and the scripts that built the table were
  kept outside the repository, in the session that made them. The questions are in the gate
  task.
- `MISHEARD_WORDS` still maps 「我沒有跑過」 to 「這支影片沒有跑過」. The new rule keeps that
  sentence out of the narration altogether; the entry is left as it is.
- `node --test tools/*.test.mjs` on this Windows machine: 296 of 298 pass, one skipped, and
  `reference-analysis.test.mjs` (--compare) fails. It imports none of the files changed here.
