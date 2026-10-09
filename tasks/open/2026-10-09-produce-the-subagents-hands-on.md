---
id: 2026-10-09-produce-the-subagents-hands-on
title: Produce the subagents hands-on tutorial under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T20:07:40Z
created_at: 2026-10-09T20:07:39Z
completed_at:
branch: claude/subagents-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-subagents-hands-on
  - docs/videos/lexicon.json
---

# Produce the subagents hands-on tutorial under the content-value rules

## Why

The owner asked to keep making AI tutorials. The Skills tutorial ended on a procedure that loads
only when used; this one takes the next question: when should work go to a separate agent with
its own context, and how do you know it did. Same order as the last four: plan, run, write. It
goes as far as the publish gate on `/admin/videos`; uploading stays the owner's.

## Definition of done

- [x] A brief by a planner with the rules and no run evidence; outline A, as the owner delegated.
- [x] The listed runs made and logged: twelve headless sessions and the model-free checks.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings; the layout check run
  before narration.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`), their findings applied.
- [x] Narration synthesized and checked until no line was flagged; the audio gate approved it.
- [x] Its files in the repository.
- [ ] The cut, and the final and publish gates.
- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Plan, run, write, verify twice, narrate.
- [ ] `render`, `assemble`, `captions`, `review-push --gate final`, `package`,
  `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-subagents-hands-on
node tools/video/cli.mjs status --slug claude-code-subagents-hands-on
```

`docs/videos/claude-code-subagents-hands-on/runlog.txt` holds every run a card quotes, and
`demo/` the practice project, each way of writing the agent file, and the scripts.

## Notes

- Produced on 2026-10-09 and 10 with Claude Code 2.1.295 on Windows, Git Bash; twelve sessions,
  none repeated; only claude-sonnet-5-5 appears in any stream. The subagent's model was pinned
  with the environment pair, so the agent file's `model` field was not observed.
- What only the runs showed: with the question handed to the subagent, the tool results left in
  the main conversation were 1,028 to 1,266 characters against 24,792 to 34,419 kept inline, and
  the main conversation's last request was about 15,000 tokens smaller; the answer was 7 of 7 on
  both sides. Whole-session tokens and cost did not separate the arms, so the video does not say
  delegating costs more or less. Under `-p` Claude delegated by itself 3 of 3 when the project
  agent existed, and not at all to a built-in agent in the one run without it. Five of eight
  delegations ran in the background: the tool result is a launch message and the report arrives
  later as a system line. `result.usage` leaves the subagent out; `modelUsage` and the cost
  include it.
- Not to be credited to the subagent: Claude rewrote the task each time and in four of eight
  mentioned crossing files itself; in the write run the main conversation wrote the file and the
  subagent was never asked to. Three subagent reports carry the same wrong side remark, and the
  main conversation repeated it in three final replies; the score does not see it.
- Never observed, and not told as seen: an agent written but not delegated to, any delegation
  rate, the effect of the description, what a subagent does when it lacks a tool, the interactive
  screen, personal or plugin agents, parallel agents, other models.
- A validated file can still fail to load: the description-less variant exits 0 with a warning,
  and the official page says a session skips it. The first fact check caught the script saying
  only the other variant fails to load.
- Every session's debug log says a server-side advisor tool is enabled with claude-opus-5-5; no
  stream, usage or cost shows it used. It is not set by the project. The description says so.
- In `demo/`, agent and CLAUDE.md variants keep neutral file names and `session.sh` places them
  in the throwaway project; it refuses a run folder inside a git repository. The six practice
  logs end in `.log`, which this repository ignores, so they are force-added.
- Narration: 14 of 118 lines flagged on the first audio check, then 3, then 1, then none
  (`narration-rewrites-1.json`, `-2.json`). 主對話 in the middle of a sentence was misheard five
  ways; 交辦 as 交版／膠版; 前景 as 前進; 背景 as 北京. Longest card state measured from
  `timeline.json`: 12.1 s.
