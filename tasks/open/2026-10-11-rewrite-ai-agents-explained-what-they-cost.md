---
id: 2026-10-11-rewrite-ai-agents-explained-what-they-cost
title: Rewrite the explainer ai-agents-explained-what-they-cost with the facts it lacks
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
  - docs/videos/ai-agents-explained-what-they-cost
---

# Rewrite the explainer ai-agents-explained-what-they-cost with the facts it lacks

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-agents-explained-what-they-cost`, 「AI 代理是什麼、跑一次多少錢，以及控制預算前該確認的設定」.
- On the site: final video approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 6 of the 12 questions asked.
- The reader's reason: 片名答應的「跑一次多少錢」只有一張沒列單價、自稱示意的五輪表，硬上限也沒講設定名稱和位置，另有十七句旁白是放到任何題目都成立的提醒。
- What it needs, in the reader's words: 把單價和算式放上卡片（最好換成一次實際跑出的用量或有出處的價目），寫出硬上限的設定名稱和所在頁面，並刪掉「完成要有證據」「先從安全的工作開始」這類通用提醒。這需要補新事實（實際價目或實跑、設定路徑），不是只改寫就夠。
- Kind of work: new facts or runs, then a rewrite.

What it failed: more than ten narration sentences that hold without the subject (D2); key facts in the source's own words on cards that name it (X3). Also D3, D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-agents-explained-what-they-cost/` on main.

## Definition of done

- [ ] Whoever takes it first decides whether the example or the angle can carry a film at all.
      If it cannot, the brief opens with 「含金量不足：…」 and the task ends there.
- [ ] The script meets `VALUE_RULES` and `TEACHING_RULES` as they stand since 2026-10-11
      (`tools/video/automation/register.mjs`; the guide is `script-writing.md` §含金量).
- [ ] A reader who did not write it answers the same questions and it passes what it failed here.
- [ ] Nothing is synthesized, rendered or uploaded until the owner has agreed to the cost of
      producing it.

## Steps

- [ ] Read the film as it is and the reader's reason above.
- [ ] Find the missing facts at their sources, or make the missing run, and record where each came from.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-agents-explained-what-they-cost
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
