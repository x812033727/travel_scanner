---
id: 2026-10-11-rewrite-claude-code-mcp-hands-on
title: Rewrite the tutorial claude-code-mcp-hands-on from real runs
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-mcp-hands-on
---

# Rewrite the tutorial claude-code-mcp-hands-on from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `claude-code-mcp-hands-on`, 「Claude Code MCP 教學：自己寫 95 行的 MCP 伺服器，接三次、不接三次」.
- On the site: on YouTube, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 6 of the 13 questions asked.
- The reader's reason: 伺服器的程式只秀出片段（say()、hand.jsonl 的四則訊息、完整的 claude 指令都沒上畫面），觀眾不下載示範資料夾就寫不出自己的伺服器，而且範例的資料就在專案裡，片子自己的 r1 也證明不接 MCP 一樣查得到。
- What it needs (the coordinating session's summary of the reader's sheet): 換一個資料不在專案裡、不接 MCP 就拿不到的例子（片中自己的對照組證明現在這個例子不接也查得到），並把伺服器程式完整放上卡片。需要新的實跑。
- Kind of work: new runs, then a rewrite.

What it failed: the main result can be had the simple way with nothing lost (W2); the viewer could make or change one from what is shown (W4); every step to repeat is on a card in full (E2); the example can be followed without an unseen download (E3). Also D1, D3, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/claude-code-mcp-hands-on/` on main.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
      For a tutorial that means real runs in the run log, the simple way run beside the
      subject on the same input, and no narration about the making.
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Make the missing runs on the owner's machine (the host worker runs nothing) and record them.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-mcp-hands-on
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
