---
id: 2026-10-11-produce-the-mcp-tool-loading-hands
title: Produce the MCP tool-loading hands-on tutorial under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-11T13:17:44Z
created_at: 2026-10-11T13:17:39Z
completed_at:
branch: claude/mcp-tool-loading-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-mcp-tool-loading-hands-on
  - docs/videos/lexicon.json
---

# Produce the MCP tool-loading hands-on tutorial under the content-value rules

## Why

The owner asked to keep making AI tutorials. The one before this measured that the first MCP
server attached to a small project added 713 tokens to the first request, 463 of which came with
deferred tool loading being switched on and not with the server's two tools, and could not say
what that part was, how either figure grows with the number of tools, or where deferred loading
starts to pay. This tutorial measures exactly that: one local server with 2, 10 and 40 tools,
deferred against loaded up front. Same order as the last ten: plan, run, write. It goes as far
as the publish gate on `/admin/videos`; uploading stays the owner's.

## Definition of done

- [x] A brief by a planner with the rules and no run evidence, reviewed by an independent
  reviewer before any session ran; outline A, the plan's recommendation.
- [x] The listed runs made and logged: fourteen headless sessions and the model-free checks.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings; the layout check run
  before narration.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`), their findings applied.
- [x] Narration synthesized and checked until no line was flagged; the audio gate approved it.
- [x] Its files in the repository.
- [ ] The cut, and the final and publish gates.
- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Plan, review the plan, run, write, verify twice, narrate.
- [ ] `render`, `assemble`, `captions`, `review-push --gate final`, `package`,
  `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-mcp-tool-loading-hands-on
node tools/video/cli.mjs status --slug claude-code-mcp-tool-loading-hands-on
```

`docs/videos/claude-code-mcp-tool-loading-hands-on/runlog.txt` holds every run a card quotes,
and `demo/` the practice project, the server under a neutral layout, the scripts that assemble
and run it, the two reading scripts a viewer can use on their own streams, and each run's
figures.

## Notes

- Produced on 2026-10-11 with Claude Code 2.1.295 on Windows, Git Bash; fourteen sessions on
  sonnet, every one with `--permission-mode default` and no Bash; the only allow rule is the one
  MCP tool the last two sessions call. The server is the seed's stdio script: read-only lookups
  over a small data file, no network. In all fourteen the init lists held nothing that was
  neither the seed's nor Claude Code's own.
- No reading rule was changed during the runs, which the previous tutorial could not say. What
  made that possible: the review before the runs (a straight-line check that would have judged
  a perfectly proportional result "off the line", a card command that subtracted the wrong
  baseline, a reading script that changed its own rule once a zero-tool run existed), a warm-up
  session excluded by rule, and a separate baseline for the up-front arms so that every figure
  differs from its base by one thing.
- What the runs showed, as differences in the first request: deferred +710, +811 and +1,214 at
  2, 10 and 40 tools; loaded up front +246, +941 and +3,586. Up front is smaller at two tools by
  467 and deferred is smaller at ten by 127 and at forty by 2,369; the two cross between two and
  ten (about eight on a straight line, a calculation). Each further tool costs about 13 deferred
  (its name) and about 87 up front (its definition). The server alone, with no tools, costs 69;
  about 618 arrives with the first deferred tool and not when the server is attached. What that
  part consists of could not be split.
- The cap went from 12 to 14: the reviewer recommended the zero-tool run, and one arm had to be
  rerun because its init list carried one more of Claude Code's own skills (three of fourteen
  runs did; it moved the first request by 0 to 2 tokens here, against about 80 in the previous
  tutorial). The last pair, a session that uses one tool in each mode, could not be subtracted
  for the same reason; the video shows the two side by side and draws no difference.
- The first fact check found the built-in tool count said to be eight in every run (seven with
  tool search off), viewer commands that fail under zsh, and thirteen spoken uses of a phrase
  already on the misheard list. The second, run as two checkers with different lenses and a
  third who merged them, found two wrong sentences in the description (what the scripts refuse,
  and which table lacks a value) and private words (臂, a bare 尺) left where a viewer meets
  them.
- A reviewer reported "written" for a findings file that did not exist, and the planner waited
  35 minutes for it. Hand-offs by file are now checked for the file before the next step starts.
- Narration: 18 of 117 lines flagged on the first audio check, then 3, then none
  (`narration-rewrites-1.json`, `-2.json`). A clause-initial 延後 was heard as 然後; 只 before a
  verb as 解, 至, 職 and 直 (只多 as 至多, which reverses the meaning); 沒接 as 媒介; 工具數 as
  公倍數; 推回 as 退回. Narration 10:42; longest card state measured from `timeline.json`:
  12.5 s; the second chapter starts at 27.0 s.
- One transcription request ended in a 502 with no answer and the tool refused to send it again
  by itself; the entry was cleared with `tools/video/tts/speech-journal.mjs forget` and the
  check run again, so at worst one clip was transcribed twice.
