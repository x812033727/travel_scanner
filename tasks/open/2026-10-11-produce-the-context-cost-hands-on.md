---
id: 2026-10-11-produce-the-context-cost-hands-on
title: Produce the context-cost hands-on tutorial under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-11T05:03:29Z
created_at: 2026-10-11T05:03:16Z
completed_at:
branch: claude/context-cost-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-context-cost-hands-on
---

# Produce the context-cost hands-on tutorial under the content-value rules

## Why

The owner asked to keep making AI tutorials. Nine earlier ones each built one part of a Claude
Code setup and measured, in passing, what it added to the first request. This one puts the parts
side by side in one small project and measures them the same way: CLAUDE.md, a Skill, a
subagent, an MCP server, a hook and a plugin, each as a difference from a bare baseline, then one
working session. Same order as the last nine: plan, run, write. It goes as far as the publish
gate on `/admin/videos`; uploading stays the owner's.

## Definition of done

- [x] A brief by a planner with the rules and no run evidence, reviewed by two independent
  reviewers before any session ran; outline A, the plan's recommendation.
- [x] The listed runs made and logged: thirteen headless sessions and the model-free checks.
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
node tools/video/cli.mjs lint --slug claude-code-context-cost-hands-on
node tools/video/cli.mjs status --slug claude-code-context-cost-hands-on
```

`docs/videos/claude-code-context-cost-hands-on/runlog.txt` holds every run a card quotes, and
`demo/` the practice project, each part under a neutral file name, the scripts that assemble
and run them, the measuring script a viewer can use on their own streams, and each run's
figures.

## Notes

- Produced on 2026-10-11 with Claude Code 2.1.295 on Windows, Git Bash; thirteen sessions on
  sonnet, each once, none with `--force`, every one with `--permission-mode default` and no
  Bash. The logging hook blocks any file-tool call aimed outside the project and the
  after-session check fails on one; none happened. In all thirteen the init lists held nothing
  that was neither the seed's nor Claude Code's own.
- The plan was reviewed before the paid runs, which was new for this series. The reviewers
  found that the MCP arm would have measured two things at once (the server, and deferred tool
  loading being switched on by the first deferred tool), that the "cannot tell" yardstick could
  be zero, that the measuring script counted a foreground subagent's report twice, and that the
  file tools were pre-approved for any path. All four were fixed before the first session.
- The run stopped itself after ten sessions: the two baselines differed by 80 tokens against a
  limit of 20. The first session of the day in the folder lists one more of Claude Code's own
  skills than every later one. The coordinator wrote an amended rule into the run log before the
  third baseline existed (the base is the mean of the baselines whose init counts match; the
  first is its own row), the third baseline came out 4 from the second, and three more sessions
  ran. The video tells viewers the rule was changed and why; the original-rule tables are kept.
- What the runs showed, as differences in the first request: the first deferred MCP server in a
  project with eight built-in tools +713, of which 463 came with deferred loading and not with
  the server's two tools (+250 when loaded at once); a seven-line CLAUDE.md +305; the plugin
  +127; a SessionStart hook printing 65 characters +78; one Skill +63; one subagent +54; a
  registered hook that never fires, indistinguishable from nothing. The parts add up (1,133
  against 1,131 together). `input_tokens` was 2 every time: only input plus cache write plus
  cache read can be compared.
- The first fact check found that "the ToolSearch result is one character" was the measuring
  script's own newline between two empty strings; the result is two tool references and no
  text. The second found that the bar's floor of 11 was justified with a range that spanned two
  different arms of an earlier video; the largest same-setup difference there is 10. The bar
  stayed 11, fixed before the runs; the sentence about it changed. Both are corrected by
  coordinator notes at the end of `runlog.txt`.
- Narration: 21 of 107 lines flagged on the first audio check, then 3, then none
  (`narration-rewrites-1.json`, `-2.json`). A bare 尺 was heard as 直, 十 and 此; 請求 as 氣球;
  量到的 as 聊到的; 這些數字 as 這些樹枝; 那一列 as 內斂. Narration 10:23; longest card state
  measured from `timeline.json`: 12.4 s; the second chapter starts at 31.8 s.
- One speech request ended in a 504 with no answer and the tool refused to send it again by
  itself; the entry was cleared with `tools/video/tts/speech-journal.mjs forget` and the line
  synthesized once more, so at worst one line's characters were counted twice.
