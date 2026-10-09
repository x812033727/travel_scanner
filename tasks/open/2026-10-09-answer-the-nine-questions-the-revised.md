---
id: 2026-10-09-answer-the-nine-questions-the-revised
title: Answer the nine questions the revised content-value rules raised on their second use
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T07:54:00Z
created_at: 2026-10-09T07:53:31Z
completed_at:
branch: claude/content-value-rules-fixes-2
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
---

# Answer the nine questions the revised content-value rules raised on their second use

## Why

The rules revised in PR 1396 were used a second time the same day, on a tutorial about settings
hooks (`docs/videos/claude-code-hooks-hands-on`), this time in the order plan, run, write. The
planner was again asked what it had to guess. It listed nine places, most of them about that
order, which the rules had not foreseen: a planner who works before any run has no evidence to
name.

## What the planner found, and the answer

1. Planning before the runs: an outcome has no level yet. Answer: it names the level its listed
   run will give and stands until the runs; they are made and recorded before the outline is
   chosen, and an outcome whose run failed is dropped then.
2. Who records a run: the planner's own model-free checks sat outside the repository. Answer: a
   run counts once it is in the video's run log, whoever made it.
3. No higher level exists for a command and its output. Answer: list a higher level only where
   there is something to see.
4. A session's events on a `steps` card. Answer: allowed, with its `source`.
5. The limits of the video's own example ("this guard does not see shell edits") against the
   cap on risk. Answer: said plainly, outside the cap.
6. Mixed evidence on one card with one `source`. Answer: one card, one level; split it or name
   the odd row's level in that row.
7. Real output, not source, that breaks a card (an absolute path in a test runner's output).
   Answer: excerpt whole lines in order, or run again from a folder whose path fits; never edit.
8. A fixed order of questions against "do not repeat the earlier video". Answer: tutorials share
   the order; the example, the opening and the sequence of cards must differ.
9. A `code` card with a caption and no title. Answer: 9 lines beside a title and a caption, 12
   beside a caption alone.

## Definition of done

- [x] Each of the nine is answered in `VALUE_RULES`, with the same in `planner.md`,
  `writer-video.md` and the Chinese of `script-writing.md` §含金量.
- [x] The prompt test holds the new wording.
- [ ] What the same video's writer reports is folded in before the PR is opened.

## Steps

- [x] Rule text, prompt docs, test.
- [ ] Add the writer's findings; open the PR.

## How to verify

`node --test tools/video/automation/prompts.test.mjs tools/video/automation/register.test.mjs`
and `node tools/video/long-form/cli.mjs check` (no bound file changes in this task).

## Notes

- The 12 lines for a caption-only code card come from the Mods tutorial's writer, who rendered a
  12-line card with a caption; the template itself refuses only past 16 lines, and the renderer
  refuses what its panel cannot show.
- No model was run against this text either.
