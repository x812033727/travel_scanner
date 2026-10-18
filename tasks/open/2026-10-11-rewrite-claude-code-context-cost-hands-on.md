---
id: 2026-10-11-rewrite-claude-code-context-cost-hands-on
title: Rewrite the tutorial claude-code-context-cost-hands-on from real runs
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-context-cost-hands-on
---

# Rewrite the tutorial claude-code-context-cost-hands-on from real runs

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `claude-code-context-cost-hands-on`, 「Claude Code context 用量實測：六種零件讓第一個請求多幾個 token」.
- On the site: on YouTube, not uploaded.
- Read as a tutorial. Verdict: rework. Failed 4 of the 13 questions asked.
- The reader's reason: 量法嚴謹、也有幾個意外的數字，但練習專案的差值太小（五樣合計才 +1,131）又沒說這對觀眾代表什麼，結尾的建議不用量也猜得到，全片沒拿內建的 /context 對照，還花了十幾句交代自己怎麼量、哪裡沒查。
- What it needs (the coordinating session's summary of the reader's sheet): 差值太小又沒說對觀眾代表什麼：用一個差值夠大的真實專案重量，或加上內建 /context 的對照，並刪掉交代自己怎麼量、哪裡沒查的句子。可能需要新的量測。
- Kind of work: new runs, then a rewrite.

What it failed: the example can be followed without an unseen download (E3). Also D1, D3, D4, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/claude-code-context-cost-hands-on/` on main.

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
node tools/video/cli.mjs lint --slug claude-code-context-cost-hands-on
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading.
