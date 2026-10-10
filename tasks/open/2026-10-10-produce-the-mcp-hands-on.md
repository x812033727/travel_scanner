---
id: 2026-10-10-produce-the-mcp-hands-on
title: Produce the MCP hands-on tutorial under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-10T03:09:14Z
created_at: 2026-10-10T03:08:54Z
completed_at:
branch: claude/mcp-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-mcp-hands-on
  - docs/videos/lexicon.json
---

# Produce the MCP hands-on tutorial under the content-value rules

## Why

The owner asked to keep going with AI tutorials and chose outline A. Earlier tutorials kept
showing MCP tools riding along in every session; this one answers what a viewer then asks: how
to add one tool of their own, how to know Claude used it rather than guessed, and what a
connected tool costs when it is not used. Same order as the last five: plan, run, write. It goes
as far as the publish gate on `/admin/videos`; uploading stays the owner's.

## Definition of done

- [x] A brief by a planner with the rules and no run evidence; outline A, chosen by the owner.
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
node tools/video/cli.mjs lint --slug claude-code-mcp-hands-on
node tools/video/cli.mjs status --slug claude-code-mcp-hands-on
```

`docs/videos/claude-code-mcp-hands-on/runlog.txt` holds every run a card quotes, each with the
server's own request record, and `demo/` the server, its data, each configuration and the
scripts.

## Notes

- Produced on 2026-10-10 with Claude Code 2.1.295 on Windows, Git Bash; twelve sessions on
  sonnet, none repeated. Every session ran with the strict MCP flag and the connector switch off;
  the init line, hook records and debug records show no other MCP server or tool in any of them.
- The demo server is 95 lines of plain Node, JSON-RPC over stdio, written for the handshake-era
  protocol. Claude Code probed it for the 2026-07 revision first, got "method not found", and
  fell back to the handshake in the same process. The server's own request record shows it, and
  the video opens on that record rather than on anything Claude says.
- What only the runs showed: without the server the model neither admitted ignorance nor invented
  an answer; it wrote tool calls for tools it did not have as plain text and stopped. With it,
  each run was three requests: a tool search selecting both tools, both tools in one request,
  the answer. Connecting two deferred tools added about 1,089 tokens to the first request; ten
  more deferred tools added 189; loading them up front added 534 more, and that session's total
  was still smaller, with one request fewer. One run each, so the video draws no conclusion on
  which is cheaper.
- Three ways a set-up server gives no answer, one run each, labelled by how far the call got: no
  allow rule (called, not delivered); the server cannot start (never connected, and the reply
  did not say so; the error is only in the debug record); a tool error (delivered, answered with
  an error, and no shelf was made up).
- The first fact check caught two things worth keeping: "connected but cannot be called" blurred
  connected, called and delivered, and a sentence blamed the strict flag for account connectors
  that the command's own switch turns off.
- Never observed, and not told as seen: a project `.mcp.json` connecting by itself without the
  strict flag (cited), whether a server starts when no tool is called, tool-description wording,
  remote servers, OAuth, the interactive screen, other models.
- In `demo/`, the MCP configuration and hook settings keep neutral file names and `session.sh`
  places them in the throwaway project, so this repository gains no live `.mcp.json`; nothing
  ends in `.log`.
- Narration: 14 of 119 lines flagged on the first audio check, none on the second
  (`narration-rewrites-1.json`). New mishearings: 呼叫進來 as 胡椒進來, 九行 as 就行, 唯讀 as 微調,
  session as 篩選, 四項 as 事項. Longest card state measured from `timeline.json`: 12.8 s.
