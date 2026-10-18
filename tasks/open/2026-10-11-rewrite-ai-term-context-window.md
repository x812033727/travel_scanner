---
id: 2026-10-11-rewrite-ai-term-context-window
title: Tighten the explainer ai-term-context-window
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T11:44:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-term-context-window
---

# Tighten the explainer ai-term-context-window

## Why

On 2026-10-11 the owner decided that every film the blind reading did not pass goes back to
be rewritten. The method, the questions and the first table are in
`tasks/done/2026-10-11-tutorial-worth-rules.md`. This is one of those films.

- Film: `ai-term-context-window`, 「上下文視窗（Context Window）是什麼？塞得進去，不等於讀得懂｜AI 名詞十分鐘」.
- On the site: storyboard approved, not uploaded.
- Read as an explainer. Verdict: rework. Failed 4 of the 12 questions asked.
- The reader's reason: 定義、Lost in the Middle 原句和「三種忘記」的分法有料，但片子沒有告訴觀眾在任何一個真實工具裡怎麼看出是哪一種，摘要漏掉「尚未核准」的示範也是作者自己寫的兩段字，再加上約三分之一旁白是桌子比喻和通用的文件整理建議。
- What it needs, in the reader's words: 需要新的事實與實跑：點名至少一兩個常用工具在對話過長時的實際做法（截斷、摘要、怎麼看得出來），並把自己寫的「壞摘要」換成真實模型對那三份紀錄產生的摘要。其餘只要改寫：刪掉重複的桌子比喻與通用的整理建議，把「視窗大小除以每份 token 數」的算法連同怎麼算 token 一起放上卡片。
- Kind of work: mostly rewriting, plus the one thing the reader names.

What it failed: more than ten narration sentences that hold without the subject (D2). Also D4, S1, S2, which nearly every film failed and which are not what this rewrite is judged by.

## Where its script is

`docs/videos/ai-term-context-window/` on main.

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
- [ ] Cut what repeats and add the one thing the reader says is missing.
- [ ] Rewrite, lint, and have someone else check it.

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-term-context-window
```

and the questions above, answered from the script alone by a reader who did not write it.

## Notes

- The reader saw the script as text (cards and narration), not the finished video, and the
  verdict is a model's reading. For explainers there was no film the owner had refused to
  measure the questions against, so the line between "publish" and "rework" is soft.
