---
id: 2026-10-11-value-rules-in-the-bound-files
title: Carry the 2026-10-11 value rules into the two files the duration receipt binds
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-11T09:50:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Carry the 2026-10-11 value rules into the two files the duration receipt binds

## Why

`2026-10-11-tutorial-worth-rules` added to the content-value rules after the owner refused a
finished tutorial. Two places that state the same rules were left as they were, because the
duration receipt (`docs/videos/long-form/review.json`) binds them and another task held the
receipt that day:

- `tools/video/automation/prompts.mjs`, the planner's brief template: `## 觀眾看完能做到的事 —
  one or two concrete things the viewer can DO afterwards`. `VALUE_RULES`, appended to the
  same prompt, says two to four and now adds that its number holds. The template should say
  the same thing as the rule.
- `.agents/skills/youtube-video/SKILL.md` rule 11 (and its copy under `.claude/skills/`)
  summarises the six content-value rules of 2026-10-09 and not what 2026-10-11 added.

Two smaller things from the same reading belong here because they are rule text:

- Seven of the ten hands-on tutorials do not show on a card the full command the viewer must
  type; their cards say the remaining flags are in the description. The rule that allows it:
  "A command too long for a terminal card goes on a code card when it fits as typed; otherwise
  its parts go in a table and the whole command in the description." Decide whether the
  command for the main example may be split at all, or must be written with the shell's own
  line continuation and run that way.
- `MISHEARD_WORDS` maps 「我沒有跑過」 to 「這支影片沒有跑過」. The narration is no longer
  allowed to say either.

## Definition of done

- [ ] The planner's template and `VALUE_RULES` give one number for the outcomes, and the
      template asks for a list.
- [ ] `SKILL.md` rule 11 names the 2026-10-11 additions, in both copies.
- [ ] The rule for a command too long for a card is decided and written, with one of the
      seven films' commands as the test case.
- [ ] The duration receipt is re-bound by an independent reviewer.

## Steps

- [ ] Check that no in-progress task holds `docs/videos/long-form/review.json`.
- [ ] Edit the template line, `planner.md` already says two to four; edit rule 11 twice.
- [ ] The receipt increment (a reviewer other than the author; `tools/video/long-form`).

## How to verify

```bash
node --test tools/video/automation/prompts.test.mjs tools/video/long-form/review.test.mjs
node tools/video/long-form/cli.mjs check
npm run test:tools
```

## Notes

- `npm run test:tools` keeps the two `SKILL.md` copies byte-identical.
